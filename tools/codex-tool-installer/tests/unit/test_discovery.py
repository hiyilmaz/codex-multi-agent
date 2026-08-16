import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.discovery import discover, preflight
from codex_tool_installer.models import Status
from codex_tool_installer.process import CommandResult


class Runner:
    def __init__(self, code=0): self.code, self.calls = code, []
    def run(self, command, **kwargs): self.calls.append(tuple(command)); return CommandResult(self.code, "v1\n", "")


class DiscoveryTests(unittest.TestCase):
    def test_corrupt_config_stops_preflight_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text("[broken", encoding="utf-8")
            before = config.read_bytes()
            result = discover({"HOME": directory, "PATH": "", "GITHUB_PAT_TOKEN": "present"}, Runner(), {"system": "Darwin", "machine": "arm64"})
            okay, issues = preflight(result)
            self.assertFalse(okay)
            self.assertFalse(result.config_valid)
            self.assertTrue(issues)
            self.assertEqual(before, config.read_bytes())
            self.assertTrue(all(state.status in {Status.MISSING, Status.INVALID_CONFIG} for state in result.tools.values()))

    def test_preflight_disk_and_platform_boundaries(self):
        result = discover({"HOME": "/nonexistent", "PATH": ""}, Runner(), {"system": "Linux", "distribution": "Ubuntu", "version": "24.10"})
        okay, issues = preflight(result, free_bytes=1)
        self.assertFalse(okay)
        self.assertTrue(any("Ubuntu" in issue for issue in issues))
        self.assertTrue(any("disk" in issue for issue in issues))


if __name__ == "__main__": unittest.main()
