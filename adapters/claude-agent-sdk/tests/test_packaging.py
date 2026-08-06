import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_python_and_sdk_are_exactly_pinned(self):
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('requires-python = ">=3.10,<4"', text)
        self.assertIn('"claude-agent-sdk==0.2.130"', text)
        self.assertNotRegex(text, r"claude-agent-sdk\s*[~^*<>]")

    def test_lock_contains_exact_sdk_version(self):
        text = (ROOT / "uv.lock").read_text(encoding="utf-8")
        block = re.search(r'(?ms)^\[\[package\]\]\nname = "claude-agent-sdk"\n.*?(?=^\[\[package\]\]|\Z)', text)
        self.assertIsNotNone(block)
        self.assertIn('version = "0.2.130"', block.group(0))


if __name__ == "__main__":
    unittest.main()
