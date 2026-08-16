import tempfile
import unittest
from pathlib import Path

from codex_tool_installer.config import ConfigTransactionError, update_config_transactionally
from codex_tool_installer.execution import LifecycleExecutor
from codex_tool_installer.manifest import TOOL_MANIFEST
from codex_tool_installer.mcp import verify_mcp
from codex_tool_installer.models import Status, ToolHealth


class TimeoutClient:
    def visible(self, name): raise TimeoutError()
    def tools(self, name): return ()
    def call_read_only(self, name, tool): return False


class FailureTests(unittest.TestCase):
    def test_network_apt_and_brew_failures_are_isolated(self):
        tools = (TOOL_MANIFEST["rg"], TOOL_MANIFEST["opengrep"])
        health = {tool.name: ToolHealth(tool.name, Status.MISSING) for tool in tools}
        result = LifecycleExecutor(lambda tool: (_ for _ in ()).throw(RuntimeError("network/package failure")) if tool.name == "rg" else None, lambda _: True).execute(tools, health)
        self.assertEqual(Status.FAILED, result["rg"].status)
        self.assertEqual(Status.HEALTHY, result["opengrep"].status)

    def test_invalid_tokens_and_mcp_timeout_fail_closed_without_secret(self):
        secret = "never-print-this-token"
        github = verify_mcp(TOOL_MANIFEST["github"], TimeoutClient(), credential_available=False)
        context = verify_mcp(TOOL_MANIFEST["context7"], TimeoutClient(), credential_available=True)
        self.assertEqual(Status.AUTH_REQUIRED, github.status)
        self.assertEqual(Status.BROKEN, context.status)
        self.assertNotIn(secret, github.detail + context.detail)

    def test_permission_denied_before_replace_preserves_original(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            original = b'model = "safe"\n'
            path.write_bytes(original)
            import codex_tool_installer.config as config_module
            real_replace = config_module.os.replace
            config_module.os.replace = lambda *_: (_ for _ in ()).throw(PermissionError("denied"))
            try:
                with self.assertRaises(ConfigTransactionError):
                    update_config_transactionally(path, "deepwiki", {"url": "https://example.invalid"}, lambda _: True, "stamp")
            finally:
                config_module.os.replace = real_replace
            self.assertEqual(original, path.read_bytes())


if __name__ == "__main__": unittest.main()
