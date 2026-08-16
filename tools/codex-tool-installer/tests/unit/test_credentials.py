import os
import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.credentials import LibsecretStore, MacOSKeychainStore, ProtectedFileStore, redact, resolve_credential
from codex_tool_installer.process import CommandResult


class Store:
    def __init__(self, value=None): self.value, self.saved = value, []
    def get(self, name): return self.value
    def set(self, name, value): self.saved.append((name, value))


class Prompt:
    def __init__(self, value): self.value, self.calls = value, []
    def secret(self, message): self.calls.append(message); return self.value


class CredentialTests(unittest.TestCase):
    def test_precedence_and_non_interactive_failure(self):
        store, prompt = Store("stored"), Prompt("prompted")
        result = resolve_credential("TOKEN", {"TOKEN": "environment"}, store, prompt, False)
        self.assertEqual((True, "environment", "environment"), (result.available, result.value, result.source))
        self.assertEqual([], prompt.calls)
        result = resolve_credential("TOKEN", {}, store, prompt, False)
        self.assertEqual("secure-store", result.source)
        self.assertFalse(resolve_credential("TOKEN", {}, None, prompt, True).available)
        self.assertEqual([], prompt.calls)

    def test_masked_prompt_store_and_redaction(self):
        secret = "random-super-secret-9381"
        store, prompt = Store(), Prompt(secret)
        result = resolve_credential("TOKEN", {}, store, prompt, False)
        self.assertTrue(result.available)
        self.assertEqual([("TOKEN", secret)], store.saved)
        output = redact(f"Authorization: Bearer {secret} token={secret}", (secret,))
        self.assertNotIn(secret, output)

    def test_protected_file_store_enforces_0600(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials"
            store = ProtectedFileStore(path)
            store.set("TOKEN", "value")
            self.assertEqual("value", store.get("TOKEN"))
            self.assertEqual(0, path.stat().st_mode & 0o077)
            path.chmod(0o644)
            with self.assertRaises(PermissionError):
                store.get("TOKEN")

    def test_os_secure_stores_use_stdin_for_writes(self):
        class Runner:
            def __init__(self): self.inputs = []
            def run(self, command): return CommandResult(0, "stored\n", "")
            def run_with_input(self, command, value): self.inputs.append((tuple(command), value)); return CommandResult(0)
        for store_type in (MacOSKeychainStore, LibsecretStore):
            runner = Runner()
            store = store_type(runner)
            self.assertEqual("stored", store.get("TOKEN"))
            store.set("TOKEN", "secret")
            self.assertEqual("secret", runner.inputs[0][1])
            self.assertNotIn("secret", runner.inputs[0][0])

    def test_protected_store_refuses_symlink_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.write_text("user-owned", encoding="utf-8")
            target.chmod(0o600)
            link = Path(directory) / "credentials"
            link.symlink_to(target)
            with self.assertRaises(PermissionError):
                ProtectedFileStore(link).set("TOKEN", "secret")
            with self.assertRaises(PermissionError):
                ProtectedFileStore(link).get("TOKEN")
            self.assertEqual("user-owned", target.read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()
