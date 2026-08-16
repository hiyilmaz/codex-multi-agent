import unittest

from codex_tool_installer.execution import LifecycleExecutor
from codex_tool_installer.models import Status, ToolDefinition, ToolHealth


class LifecycleTests(unittest.TestCase):
    def test_middle_tool_failure_does_not_stop_later_tool(self):
        calls = []

        def install(tool):
            calls.append(tool.name)
            if tool.name == "middle":
                raise RuntimeError("simulated package failure")

        tools = [
            ToolDefinition(name=name, kind="cli", executable=name, platforms=("macos",), verify=((name, "--version"),))
            for name in ("first", "middle", "last")
        ]
        initial = {tool.name: ToolHealth(tool.name, Status.MISSING) for tool in tools}
        results = LifecycleExecutor(install=install, verify=lambda tool: tool.name != "middle").execute(tools, initial)
        self.assertEqual(["first", "middle", "last"], calls)
        self.assertEqual(Status.HEALTHY, results["first"].status)
        self.assertEqual(Status.FAILED, results["middle"].status)
        self.assertEqual(Status.HEALTHY, results["last"].status)

    def test_missing_cli_mcp_installs_and_healthy_mcp_reverifies(self):
        installed, verified = [], []
        tool = ToolDefinition("serena", "cli_mcp", "serena", ("macos",), (("serena", "--version"),))
        result = LifecycleExecutor(lambda item: installed.append(item.name), lambda item: verified.append(item.name) or True).execute([tool], {"serena": ToolHealth("serena", Status.MISSING)})
        self.assertEqual(["serena"], installed)
        self.assertEqual(["serena"], verified)
        self.assertEqual(Status.HEALTHY, result["serena"].status)

    def test_check_reverifies_configured_mcp_without_mutation(self):
        calls = []
        tool = ToolDefinition("github", "mcp", None, ("macos",), (("codex", "mcp", "get", "github"),))
        result = LifecycleExecutor(lambda _: self.fail("must not install"), lambda item: calls.append(item.name) or False, lambda _: self.fail("must not configure")).execute([tool], {"github": ToolHealth("github", Status.BROKEN)}, mode="check")
        self.assertEqual(["github"], calls)
        self.assertEqual(Status.BROKEN, result["github"].status)

    def test_repair_reinstalls_broken_cli(self):
        calls = []
        tool = ToolDefinition("rg", "cli", "rg", ("macos",), (("rg", "--version"),))
        result = LifecycleExecutor(lambda item: calls.append(item.name), lambda _: True).execute([tool], {"rg": ToolHealth("rg", Status.BROKEN)}, mode="repair")
        self.assertEqual(["rg"], calls)
        self.assertEqual(Status.HEALTHY, result["rg"].status)


if __name__ == "__main__":
    unittest.main()
