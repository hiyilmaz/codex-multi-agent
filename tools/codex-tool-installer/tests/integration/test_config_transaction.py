import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.config import ConfigTransactionError, update_config_transactionally


class ConfigTransactionTests(unittest.TestCase):
    def test_post_replace_validation_failure_rolls_back_exact_original(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            original = b'model = "mine"\n'
            path.write_bytes(original)
            events = []
            with self.assertRaises(ConfigTransactionError):
                update_config_transactionally(
                    path,
                    "deepwiki",
                    {"url": "https://example.invalid/mcp"},
                    validate_codex=lambda _: False,
                    timestamp="20260813-010203",
                    events=events,
                )
            self.assertEqual(original, path.read_bytes())
            self.assertEqual(["candidate-validated", "backup", "replace", "rollback"], events)
            backup = path.parent / "backups" / "config.toml.20260813-010203"
            self.assertEqual(original, backup.read_bytes())
            self.assertEqual([], list(path.parent.glob(".config.toml.*.tmp")))

    def test_same_timestamp_never_overwrites_prior_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            original = b'model = "mine"\n'
            path.write_bytes(original)
            first = update_config_transactionally(path, "deepwiki", {"url": "one"}, lambda _: True, "same")
            intermediate = path.read_bytes()
            second = update_config_transactionally(path, "deepwiki", {"url": "two"}, lambda _: True, "same")
            self.assertNotEqual(first.backup_path, second.backup_path)
            self.assertEqual(original, Path(first.backup_path).read_bytes())
            self.assertEqual(intermediate, Path(second.backup_path).read_bytes())


if __name__ == "__main__":
    unittest.main()
