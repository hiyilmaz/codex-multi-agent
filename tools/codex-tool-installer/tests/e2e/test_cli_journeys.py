import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from codex_tool_installer.cli import _codex_validate, main
from codex_tool_installer.process import CommandResult


class MissingRunner:
    def run(self, command, **kwargs):
        return CommandResult(1, "", "not available in fake environment")


class ConfiguredRunner:
    def run(self, command, **kwargs):
        if tuple(command[:3]) == ("codex", "mcp", "get"):
            return CommandResult(0, '{"name":"' + command[3] + '"}')
        return CommandResult(1, "", "missing")


class BrokenTransport:
    def request(self, name, method, params, environ):
        return {"tools": []} if method == "tools/list" else {"isError": True}


class CliJourneyTests(unittest.TestCase):
    def test_codex_validation_targets_the_requested_config(self):
        class CapturingRunner:
            def __init__(self):
                self.calls = []

            def run(self, command, **kwargs):
                self.calls.append((tuple(command), kwargs))
                return CommandResult(0)

        runner = CapturingRunner()
        config = Path("/isolated/.codex/config.toml")
        self.assertTrue(_codex_validate(config, runner, {"HOME": "/user", "CODEX_HOME": "/isolated/.codex"}))
        self.assertEqual(str(config), runner.calls[0][1]["env"]["CODEX_CONFIG"])
        self.assertEqual("/isolated/.codex", runner.calls[0][1]["env"]["CODEX_HOME"])

    def test_global_options_have_identical_position_semantics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".codex").mkdir()
            environment = {"HOME": str(root), "PATH": ""}
            outputs = []
            for args in (["--json", "--mcp-mode", "verify-only", "check"], ["check", "--json", "--mcp-mode", "verify-only"]):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(
                        args,
                        environ=environment,
                        platform_facts={"system": "Darwin", "machine": "arm64"},
                        runner=MissingRunner(),
                        connectivity_probe=lambda: True,
                    )
                outputs.append((code, json.loads(output.getvalue())))
            self.assertEqual(outputs[0], outputs[1])

    def test_codex_home_selects_config_without_changing_home(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex_home = root / "isolated-codex"
            codex_home.mkdir()
            output = io.StringIO()
            with redirect_stdout(output):
                main(
                    ["--codex-home", str(codex_home), "--json", "check"],
                    environ={"HOME": str(root / "user-home"), "PATH": ""},
                    platform_facts={"system": "Darwin", "machine": "arm64"},
                    runner=MissingRunner(),
                    connectivity_probe=lambda: True,
                )
            self.assertEqual(str(codex_home / "config.toml"), json.loads(output.getvalue())["codex"]["config"])

    def test_dry_run_and_check_are_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text('model = "preserved"\n', encoding="utf-8")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            for args in (["--dry-run", "--json"], ["check", "--json"]):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(
                        args,
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Darwin", "machine": "arm64"},
                        runner=MissingRunner(),
                        connectivity_probe=lambda: True,
                    )
                payload = json.loads(output.getvalue())
                self.assertIn("tools", payload)
                self.assertEqual(11, len(payload["tools"]))
                self.assertIn(code, (0, 1))
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_check_reports_functional_mcp_failure_not_cached_visibility(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text('[mcp_servers.deepwiki]\nurl = "https://mcp.deepwiki.com/mcp"\n', encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    ["check", "--json"], environ={"HOME": str(root), "PATH": ""},
                    platform_facts={"system": "Darwin", "machine": "arm64"}, runner=ConfiguredRunner(),
                    connectivity_probe=lambda: True, mcp_transport=BrokenTransport(),
                )
            deepwiki = next(tool for tool in json.loads(output.getvalue())["tools"] if tool["name"] == "deepwiki")
            self.assertEqual(1, code)
            self.assertEqual("BROKEN", deepwiki["status"])


if __name__ == "__main__":
    unittest.main()
