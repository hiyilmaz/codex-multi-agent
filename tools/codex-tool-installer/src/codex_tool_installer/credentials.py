from __future__ import annotations

import getpass
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Protocol


class SecureStore(Protocol):
    def get(self, name: str) -> str | None: ...
    def set(self, name: str, value: str) -> None: ...


class CredentialPrompt(Protocol):
    def secret(self, message: str) -> str: ...


class MaskedPrompt:
    def secret(self, message: str) -> str:
        return getpass.getpass(message)


@dataclass(frozen=True)
class CredentialResult:
    available: bool
    value: str | None = None
    source: str | None = None


def resolve_credential(name: str, environ: Mapping[str, str], store: SecureStore | None, prompt: CredentialPrompt | None, non_interactive: bool) -> CredentialResult:
    if environ.get(name):
        return CredentialResult(True, environ[name], "environment")
    if store:
        value = store.get(name)
        if value:
            return CredentialResult(True, value, "secure-store")
    if non_interactive or prompt is None:
        return CredentialResult(False)
    value = prompt.secret(f"{name} required (leave empty to skip): ")
    if not value:
        return CredentialResult(False)
    return CredentialResult(True, value, "prompt")


class ProtectedFileStore:
    """Fallback store for Ubuntu; callers should prefer a system keyring."""

    def __init__(self, path: Path):
        self.path = path

    def get(self, name: str) -> str | None:
        if not self.path.exists():
            return None
        if self.path.is_symlink():
            raise PermissionError("Credential helper must not be a symlink")
        if self.path.stat().st_mode & 0o077:
            raise PermissionError("Credential helper permissions must be 0600")
        for line in self.path.read_text(encoding="utf-8").splitlines():
            key, _, value = line.partition("=")
            if key == name:
                return value
        return None

    def set(self, name: str, value: str) -> None:
        existing = {}
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                key, _, current = line.partition("=")
                if key:
                    existing[key] = current
        existing[name] = value
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.path.is_symlink():
            raise PermissionError("Credential helper must not be a symlink")
        descriptor, temp_name = tempfile.mkstemp(prefix=".credentials.", dir=self.path.parent)
        temp = Path(temp_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write("".join(f"{key}={val}\n" for key, val in sorted(existing.items())))
                handle.flush()
                os.fsync(handle.fileno())
            if self.path.exists() and self.path.is_symlink():
                raise PermissionError("Credential helper became a symlink")
            os.replace(temp, self.path)
        finally:
            temp.unlink(missing_ok=True)


class MacOSKeychainStore:
    def __init__(self, runner, service: str = "codex-tool-installer"):
        self.runner, self.service = runner, service

    def get(self, name: str) -> str | None:
        result = self.runner.run(("security", "find-generic-password", "-s", self.service, "-a", name, "-w"))
        return result.stdout.rstrip("\n") if result.returncode == 0 else None

    def set(self, name: str, value: str) -> None:
        # Secret travels through stdin-capable adapter state, never a shell.
        if not hasattr(self.runner, "run_with_input"):
            raise RuntimeError("Runner does not support secret stdin")
        result = self.runner.run_with_input(("security", "add-generic-password", "-U", "-s", self.service, "-a", name, "-w"), value)
        if result.returncode:
            raise RuntimeError("Keychain write failed")


class LibsecretStore:
    def __init__(self, runner): self.runner = runner

    def get(self, name: str) -> str | None:
        result = self.runner.run(("secret-tool", "lookup", "application", "codex-tool-installer", "key", name))
        return result.stdout.rstrip("\n") if result.returncode == 0 else None

    def set(self, name: str, value: str) -> None:
        if not hasattr(self.runner, "run_with_input"):
            raise RuntimeError("Runner does not support secret stdin")
        result = self.runner.run_with_input(("secret-tool", "store", "--label", "Codex Tool Installer", "application", "codex-tool-installer", "key", name), value)
        if result.returncode:
            raise RuntimeError("Secret store write failed")


_SECRET_PATTERNS = (
    re.compile(r"(?i)(authorization\s*:\s*(?:bearer\s+)?)[^\s,;]+"),
    re.compile(r"(?i)((?:token|api[_-]?key|pat)[\w-]*\s*[=:]\s*)[^\s,;]+"),
)


def redact(text: str, secrets=()) -> str:
    redacted = text
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "[REDACTED]")
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub(r"\1[REDACTED]", redacted)
    return redacted
