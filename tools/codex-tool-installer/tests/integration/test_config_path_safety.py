import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.config import ConfigTransactionError, update_config_transactionally


class ConfigPathSafetyTests(unittest.TestCase):
    def test_config_symlink_fails_closed_without_target_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "outside.toml"
            target.write_text('owner = "user"\n', encoding="utf-8")
            config = root / "config.toml"
            config.symlink_to(target)

            with self.assertRaises(ConfigTransactionError):
                update_config_transactionally(
                    config,
                    "deepwiki",
                    {"url": "https://mcp.deepwiki.com/mcp"},
                    lambda _: True,
                    "20260817-000000",
                )

            self.assertEqual('owner = "user"\n', target.read_text(encoding="utf-8"))

    def test_non_regular_config_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.toml"
            config.mkdir()
            with self.assertRaises(ConfigTransactionError):
                update_config_transactionally(config, "deepwiki", {"url": "https://example.invalid"}, lambda _: True, "stamp")

    def test_symlinked_ancestor_fails_closed_without_outside_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside"
            nested = outside / "nested"
            nested.mkdir(parents=True)
            config = nested / "config.toml"
            config.write_text('owner = "user"\n', encoding="utf-8")
            alias = root / "alias"
            alias.symlink_to(outside, target_is_directory=True)

            with self.assertRaises(ConfigTransactionError):
                update_config_transactionally(
                    alias / "nested" / "config.toml",
                    "deepwiki",
                    {"url": "https://mcp.deepwiki.com/mcp"},
                    lambda _: True,
                    "stamp",
                )

            self.assertEqual('owner = "user"\n', config.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
