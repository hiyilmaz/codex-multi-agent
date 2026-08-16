import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.config import update_config_transactionally


class IdempotencyTests(unittest.TestCase):
    def test_second_run_has_zero_installs_writes_backups_or_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text('model = "preserve"\n', encoding="utf-8")
            block = {"url": "https://example.invalid/mcp", "enabled": True}
            first = update_config_transactionally(path, "deepwiki", block, lambda _: True, "one")
            snapshot = path.read_bytes()
            backups = list((path.parent / "backups").glob("*"))
            second = update_config_transactionally(path, "deepwiki", block, lambda _: True, "two")
            self.assertTrue(first.changed)
            self.assertFalse(second.changed)
            self.assertEqual(snapshot, path.read_bytes())
            self.assertEqual(backups, list((path.parent / "backups").glob("*")))
            self.assertEqual(1, path.read_text().count("[mcp_servers.deepwiki]"))


if __name__ == "__main__":
    unittest.main()
