import unittest

from codex_tool_installer.execution import LifecycleExecutor, default_selection, interactive_selection, parse_selection
from codex_tool_installer.manifest import TOOL_MANIFEST
from codex_tool_installer.models import DiscoveryResult, PlatformInfo, Status, ToolDefinition, ToolHealth
from codex_tool_installer.reporting import render_json, render_summary, summarize


class ExecutionReportingTests(unittest.TestCase):
    def test_summary_separates_auth_required_and_uses_exact_preservation_input(self):
        platform = PlatformInfo("Linux", "24.04", "x86_64", "bash", "", True, "ubuntu-24.04")
        before = DiscoveryResult(
            platform,
            {"github": ToolHealth("github", Status.AUTH_REQUIRED)},
            True, "/tmp/config.toml", True, {}, {"GITHUB_PAT_TOKEN": False}, (),
        )
        final = DiscoveryResult(
            platform,
            {"github": ToolHealth("github", Status.AUTH_REQUIRED)},
            True, "/tmp/config.toml", True, {}, {"GITHUB_PAT_TOKEN": False}, (),
        )
        summary = summarize(final, before, config_preserved=False)
        self.assertEqual(0, summary.failed)
        self.assertEqual(1, summary.auth_required)
        self.assertFalse(summary.config_preserved)

    def test_selection_and_dependency_blocking(self):
        self.assertEqual(set(TOOL_MANIFEST), default_selection(TOOL_MANIFEST))
        self.assertEqual({"rg"}, parse_selection(["rg"], TOOL_MANIFEST))
        with self.assertRaises(ValueError): parse_selection(["unknown"], TOOL_MANIFEST)
        dependency = ToolDefinition("dep", "cli", "dep", ("macos",), (("dep", "--version"),))
        consumer = ToolDefinition("consumer", "cli", "consumer", ("macos",), (("consumer", "--version"),), dependencies=("dep",))
        health = {"dep": ToolHealth("dep", Status.MISSING), "consumer": ToolHealth("consumer", Status.MISSING)}
        def fail_dependency(tool):
            if tool.name == "dep":
                raise RuntimeError("dependency install failed")
        result = LifecycleExecutor(fail_dependency, lambda _: True).execute([dependency, consumer], health)
        self.assertEqual(Status.FAILED, result["dep"].status)
        self.assertEqual(Status.BLOCKED, result["consumer"].status)

    def test_repair_and_skip_modes(self):
        tool = ToolDefinition("tool", "cli", "tool", ("macos",), (("tool", "--version"),))
        executor = LifecycleExecutor(lambda _: None, lambda _: True)
        state = executor.execute([tool], {"tool": ToolHealth("tool", Status.MISSING)}, mode="repair")
        self.assertEqual(Status.SKIPPED, state["tool"].status)
        state = executor.execute([tool], {"tool": ToolHealth("tool", Status.BROKEN)}, selected=set())
        self.assertEqual(Status.SKIPPED, state["tool"].status)

    def test_renderers_do_not_require_secret_values(self):
        payload = {"platform": {"system": "Darwin", "architecture": "arm64"}, "tools": [{"name": "rg", "selected": True, "status": "HEALTHY"}], "selected_count": 1}
        self.assertIn("rg", render_summary(payload))
        self.assertIn('"selected_count": 1', render_json(payload))

    def test_interactive_customize_and_cancel(self):
        answers = iter(("u", "rg,github"))
        self.assertEqual({"rg", "github"}, interactive_selection(("rg", "github", "serena"), lambda _: next(answers), lambda _: None))
        self.assertIsNone(interactive_selection(("rg",), lambda _: "cancel", lambda _: None))


if __name__ == "__main__": unittest.main()
