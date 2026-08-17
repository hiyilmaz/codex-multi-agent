import unittest

import codex_tool_installer.execution as execution_module
from codex_tool_installer.execution import LifecycleExecutor
from codex_tool_installer.models import Status, ToolDefinition, ToolHealth


class LifecycleTests(unittest.TestCase):
    def test_typed_auth_required_continues_and_plain_runtime_error_stays_failed(self):
        self.assertTrue(hasattr(execution_module, "LifecycleStatusError"))
        LifecycleStatusError = execution_module.LifecycleStatusError
        calls = []
        tools = [
            ToolDefinition(name=name, kind="mcp", executable=None, platforms=("macos",), verify=(("codex", "mcp", "get", name),))
            for name in ("auth", "literal", "last")
        ]

        def configure(tool):
            calls.append(tool.name)
            if tool.name == "auth":
                raise LifecycleStatusError(Status.AUTH_REQUIRED, "TOKEN unavailable")
            if tool.name == "literal":
                raise RuntimeError("AUTH_REQUIRED: must not be parsed")

        results = LifecycleExecutor(lambda _: None, lambda _: True, configure).execute(
            tools, {tool.name: ToolHealth(tool.name, Status.MISSING) for tool in tools}
        )
        self.assertEqual(["auth", "literal", "last"], calls)
        self.assertEqual(Status.AUTH_REQUIRED, results["auth"].status)
        self.assertEqual(Status.FAILED, results["literal"].status)
        self.assertEqual(Status.HEALTHY, results["last"].status)

    def test_pending_transaction_commits_after_verify_and_rolls_back_on_failure(self):
        self.assertTrue(hasattr(execution_module, "PendingTransaction"))
        PendingTransaction = execution_module.PendingTransaction
        events = []
        success = ToolDefinition("success", "mcp", None, ("macos",), (("x",),))
        failure = ToolDefinition("failure", "mcp", None, ("macos",), (("x",),))

        def configure(tool):
            events.append((tool.name, "configure"))
            return PendingTransaction(
                commit=lambda: events.append((tool.name, "commit")),
                rollback=lambda: events.append((tool.name, "rollback")),
            )

        results = LifecycleExecutor(
            lambda _: None,
            lambda tool: events.append((tool.name, "verify")) or tool.name == "success",
            configure,
        ).execute(
            (success, failure),
            {"success": ToolHealth("success", Status.MISSING), "failure": ToolHealth("failure", Status.MISSING)},
        )
        self.assertEqual(
            [
                ("success", "configure"), ("success", "verify"), ("success", "commit"),
                ("failure", "configure"), ("failure", "verify"), ("failure", "rollback"),
            ],
            events,
        )
        self.assertEqual(Status.HEALTHY, results["success"].status)
        self.assertEqual(Status.FAILED, results["failure"].status)

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
