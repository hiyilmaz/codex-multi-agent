import unittest

from codex_tool_installer.execution import LifecycleExecutor
from codex_tool_installer.models import Status, ToolDefinition, ToolHealth


class McpOwnershipModeTests(unittest.TestCase):
    def setUp(self):
        self.tool = ToolDefinition(
            "deepwiki",
            "mcp",
            None,
            ("macos", "linux"),
            (("codex", "mcp", "get", "deepwiki"),),
            mcp={"url": "https://mcp.deepwiki.com/mcp"},
        )

    def test_healthy_mcp_is_verified_without_configuration(self):
        calls = []
        result = LifecycleExecutor(
            lambda _: self.fail("must not install"),
            lambda item: calls.append(("verify", item.name)) or True,
            lambda _: self.fail("must not configure"),
        ).execute(
            [self.tool],
            {self.tool.name: ToolHealth(self.tool.name, Status.HEALTHY)},
            mode="install",
            mcp_mode="manage",
        )
        self.assertEqual([("verify", "deepwiki")], calls)
        self.assertEqual(Status.HEALTHY, result["deepwiki"].status)

    def test_verify_only_never_configures_any_mcp_state(self):
        for status in (
            Status.HEALTHY,
            Status.MISSING,
            Status.BROKEN,
            Status.AUTH_REQUIRED,
            Status.INVALID_CONFIG,
        ):
            with self.subTest(status=status):
                calls = []
                result = LifecycleExecutor(
                    lambda _: self.fail("must not install"),
                    lambda item: calls.append(("verify", item.name)) or True,
                    lambda _: self.fail("must not configure"),
                ).execute(
                    [self.tool],
                    {self.tool.name: ToolHealth(self.tool.name, status)},
                    mode="install",
                    mcp_mode="verify-only",
                )
                if status in {Status.HEALTHY, Status.BROKEN}:
                    self.assertEqual([("verify", "deepwiki")], calls)
                    self.assertEqual(Status.HEALTHY, result["deepwiki"].status)
                else:
                    self.assertEqual([], calls)
                    self.assertEqual(status, result["deepwiki"].status)

    def test_verify_only_cli_mcp_can_install_without_configuration(self):
        tool = ToolDefinition(
            "serena",
            "cli_mcp",
            "serena",
            ("macos", "linux"),
            (("serena", "--version"),),
            mcp={"optional": True},
        )
        calls = []
        result = LifecycleExecutor(
            lambda item: calls.append(("install", item.name)),
            lambda item: calls.append(("verify", item.name)) or True,
            lambda _: self.fail("must not configure"),
        ).execute(
            [tool],
            {tool.name: ToolHealth(tool.name, Status.MISSING)},
            mode="install",
            mcp_mode="verify-only",
        )
        self.assertEqual([("install", "serena"), ("verify", "serena")], calls)
        self.assertEqual(Status.HEALTHY, result["serena"].status)


if __name__ == "__main__":
    unittest.main()
