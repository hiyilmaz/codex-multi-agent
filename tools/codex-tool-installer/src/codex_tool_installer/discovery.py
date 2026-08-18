from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Mapping

from .config import ConfigError, parse_toml
from .credentials import credential_value_is_usable
from .manifest import TOOL_MANIFEST
from .models import DiscoveryResult, Status, ToolHealth
from .platforms import detect_platform
from .process import ProcessRunner


def managed_bin_environment(
    environ: Mapping[str, str], runner: ProcessRunner
) -> dict[str, str]:
    """Return a scoped PATH that includes supported user-managed bin roots."""
    effective = dict(environ)
    home = Path(effective.get("HOME", str(Path.home())))
    candidates = [home / ".local" / "bin"]
    go = shutil.which("go", path=effective.get("PATH"))
    if go:
        result = runner.run((go, "env", "GOBIN", "GOPATH"), env=effective)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            gobin = Path(lines[0]) if lines and lines[0] else None
            if gobin and gobin.is_absolute():
                candidates.append(gobin)
            elif len(lines) > 1:
                first_gopath = lines[1].split(os.pathsep, 1)[0]
                gopath = Path(first_gopath) if first_gopath else None
                if gopath and gopath.is_absolute():
                    candidates.append(gopath / "bin")
    current = effective.get("PATH", "").split(os.pathsep)
    ordered = []
    for candidate in (*(Path(item) for item in current if item), *candidates):
        value = str(candidate)
        if value and value not in ordered:
            ordered.append(value)
    effective["PATH"] = os.pathsep.join(ordered)
    return effective


def discover(
    environ: Mapping[str, str] | None = None,
    runner: ProcessRunner | None = None,
    platform_facts: Mapping[str, str] | None = None,
    manifest=TOOL_MANIFEST,
) -> DiscoveryResult:
    """Perform discovery without writes, prompts, installs, or store mutation."""
    environ = dict(os.environ if environ is None else environ)
    runner = runner or ProcessRunner()
    platform_info = detect_platform(environ, platform_facts)
    home = Path(environ.get("HOME", str(Path.home())))
    codex_home = Path(environ.get("CODEX_HOME", str(home / ".codex")))
    config_path = Path(environ.get("CODEX_CONFIG", str(codex_home / "config.toml")))
    config_valid = True
    parsed = {}
    issues = []
    if config_path.exists():
        try:
            parsed = parse_toml(config_path.read_text(encoding="utf-8"))
        except (OSError, ConfigError) as exc:
            config_valid = False
            issues.append(str(exc))
    mcp_config = parsed.get("mcp_servers", {}) if isinstance(parsed, dict) else {}
    tools = {}
    credentials = {}
    for name, definition in manifest.items():
        if definition.credential_env:
            credentials[definition.credential_env] = credential_value_is_usable(
                environ.get(definition.credential_env)
            )
        if definition.kind in {"cli", "cli_mcp"}:
            executable = shutil.which(definition.executable, path=environ.get("PATH")) if definition.executable else None
            if not executable:
                tools[name] = ToolHealth(name, Status.MISSING, "Executable not found")
                continue
            command = list(definition.verify[0])
            command[0] = executable
            result = runner.run(command)
            tools[name] = ToolHealth(name, Status.HEALTHY if result.returncode == 0 else Status.BROKEN, result.stderr.strip(), result.stdout.strip().splitlines()[0] if result.stdout.strip() else None)
        else:
            configured = name in mcp_config
            if not config_valid:
                tools[name] = ToolHealth(name, Status.INVALID_CONFIG, "Codex config is invalid")
            elif definition.credential_env and not credentials.get(definition.credential_env):
                tools[name] = ToolHealth(name, Status.AUTH_REQUIRED, f"{definition.credential_env} unavailable")
            elif not configured:
                tools[name] = ToolHealth(name, Status.MISSING, "MCP config missing")
            else:
                result = runner.run(("codex", "mcp", "get", name))
                tools[name] = ToolHealth(name, Status.HEALTHY if result.returncode == 0 else Status.BROKEN, result.stderr.strip())
    capabilities = {
        key: shutil.which(key, path=environ.get("PATH")) is not None
        for key in ("brew", "apt-get", "python3", "pip", "pipx", "uv", "node", "npm", "go", "codex", "security", "secret-tool", "git", "curl")
    }
    return DiscoveryResult(platform_info, tools, capabilities["codex"], str(config_path), config_valid, capabilities, credentials, tuple(issues))


def preflight(result: DiscoveryResult, *, free_bytes: int | None = None, connectivity: bool | None = None, writable: bool | None = None) -> tuple[bool, tuple[str, ...]]:
    issues = list(result.issues)
    if not result.platform.supported:
        issues.append(result.platform.reason)
    if not result.config_valid:
        issues.append("Codex config must be repaired manually before mutation")
    if free_bytes is not None and free_bytes < 100 * 1024 * 1024:
        issues.append("Insufficient free disk space")
    if connectivity is False:
        issues.append("Internet connectivity unavailable")
    if writable is False:
        issues.append("Required user directories are not writable")
    return not issues, tuple(dict.fromkeys(issues))
