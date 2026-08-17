import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from codex_tool_installer.cli import _codex_validate, main
from codex_tool_installer.process import CommandResult


class MissingRunner:
    def run(self, command, **kwargs):
        return CommandResult(1, "", "not available in fake environment")


class ConfiguredRunner:
    def run(self, command, **kwargs):
        if tuple(command[:3]) == ("codex", "mcp", "get"):
            return CommandResult(0, '{"name":"' + command[3] + '"}')
        if tuple(command[:3]) == ("codex", "mcp", "list"):
            return CommandResult(0, "", "")
        return CommandResult(1, "", "missing")


class BrokenTransport:
    def request(self, name, method, params, environ):
        return {"tools": []} if method == "tools/list" else {"isError": True}


class ConcurrentConfigEditTransport:
    def __init__(self, config):
        self.config = config

    def request(self, name, method, params, environ):
        if method == "tools/list":
            self.config.write_text('model = "user-concurrent-edit"\n', encoding="utf-8")
            return {"tools": []}
        return {"isError": True}


class HealthyDeepwikiTransport:
    def request(self, name, method, params, environ):
        if method == "tools/list":
            return {"tools": [{"name": item} for item in ("ask_question", "read_wiki_contents", "read_wiki_structure")]}
        return {"content": [{"type": "text", "text": "ok"}]}


class SelectiveMcpTransport:
    def __init__(self, broken=()):
        self.broken = set(broken)

    def request(self, name, method, params, environ):
        if name in self.broken:
            return {"tools": []} if method == "tools/list" else {"isError": True}
        tools = {
            "deepwiki": ("ask_question", "read_wiki_contents", "read_wiki_structure"),
            "github": ("search_repositories",),
            "context7": ("resolve-library-id", "query-docs"),
        }
        if method == "tools/list":
            return {"tools": [{"name": item} for item in tools[name]]}
        return {"content": [{"type": "text", "text": "ok"}]}


class Prompt:
    def __init__(self, value): self.value = value
    def secret(self, message): return self.value


class CliJourneyTests(unittest.TestCase):
    def test_default_manage_changes_config_and_reports_not_preserved_then_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text('model = "safe"\n', encoding="utf-8")
            runner = ConfiguredRunner()
            payloads = []
            for _ in range(2):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "deepwiki"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=runner,
                        connectivity_probe=lambda: True,
                        mcp_transport=HealthyDeepwikiTransport(),
                    )
                self.assertEqual(0, code)
                payloads.append(json.loads(output.getvalue()))
            self.assertFalse(payloads[0]["summary"]["config_preserved"])
            self.assertTrue(payloads[1]["summary"]["config_preserved"])
            self.assertEqual(1, config.read_text(encoding="utf-8").count("[mcp_servers.deepwiki]"))

    def test_failed_prompted_mcp_rolls_back_config_and_does_not_store_secret(self):
        secret = "unique-secret-never-print"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            original = b'model = "safe"\n'
            config.write_bytes(original)
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt(secret)):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "github"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(),
                        connectivity_probe=lambda: True,
                        mcp_transport=BrokenTransport(),
                    )
            payload = json.loads(output.getvalue())
            github = next(tool for tool in payload["tools"] if tool["name"] == "github")
            self.assertEqual(1, code)
            self.assertIn(github["status"], {"BROKEN", "FAILED"})
            self.assertEqual(original, config.read_bytes())
            self.assertFalse((root / ".codex" / "credentials").exists())
            self.assertNotIn(secret, output.getvalue())
            self.assertTrue(payload["summary"]["config_preserved"])

    def test_successful_prompted_mcp_persists_credential_after_verification(self):
        secret = "successful-secret-never-print"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".codex").mkdir()
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt(secret)):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "github"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(), connectivity_probe=lambda: True,
                        mcp_transport=SelectiveMcpTransport(),
                    )
            credential_path = root / ".codex" / "credentials"
            self.assertEqual(0, code)
            self.assertTrue(credential_path.exists())
            self.assertEqual(0o600, credential_path.stat().st_mode & 0o777)
            self.assertNotIn(secret, output.getvalue())

    def test_credential_store_failure_rolls_back_config_without_printing_secret(self):
        secret = "store-failure-secret-never-print"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            original = b'model = "safe"\n'
            config.write_bytes(original)
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt(secret)), patch(
                "codex_tool_installer.cli.ProtectedFileStore.set", side_effect=OSError("simulated store failure")
            ):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "github"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(), connectivity_probe=lambda: True,
                        mcp_transport=SelectiveMcpTransport(),
                    )
            payload = json.loads(output.getvalue())
            github = next(tool for tool in payload["tools"] if tool["name"] == "github")
            self.assertEqual(1, code)
            self.assertEqual("FAILED", github["status"])
            self.assertEqual(original, config.read_bytes())
            self.assertFalse((root / ".codex" / "credentials").exists())
            self.assertNotIn(secret, output.getvalue())

    def test_later_mcp_failure_preserves_earlier_successful_mcp(self):
        secret = "later-failure-secret-never-print"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text('model = "safe"\n', encoding="utf-8")
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt(secret)):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "deepwiki", "github"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(), connectivity_probe=lambda: True,
                        mcp_transport=SelectiveMcpTransport(broken={"github"}),
                    )
            current = config.read_text(encoding="utf-8")
            self.assertEqual(1, code)
            self.assertIn("[mcp_servers.deepwiki]", current)
            self.assertNotIn("[mcp_servers.github]", current)
            self.assertNotIn(secret, output.getvalue())

    def test_failed_mcp_does_not_overwrite_concurrent_user_config_edit(self):
        secret = "concurrent-edit-secret-never-print"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            config.write_text('model = "safe"\n', encoding="utf-8")
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt(secret)):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "github"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(), connectivity_probe=lambda: True,
                        mcp_transport=ConcurrentConfigEditTransport(config),
                    )
            payload = json.loads(output.getvalue())
            github = next(tool for tool in payload["tools"] if tool["name"] == "github")
            self.assertEqual(1, code)
            self.assertEqual("FAILED", github["status"])
            self.assertEqual('model = "user-concurrent-edit"\n', config.read_text(encoding="utf-8"))
            self.assertFalse(payload["credentials"]["GITHUB_PAT_TOKEN"]["available"])
            self.assertNotIn(secret, output.getvalue())

    def test_empty_prompt_is_auth_required_and_does_not_change_config(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.parent.mkdir()
            original = b'model = "safe"\n'
            config.write_bytes(original)
            output = io.StringIO()
            with patch("codex_tool_installer.cli.MaskedPrompt", return_value=Prompt("")):
                with redirect_stdout(output):
                    code = main(
                        ["--json", "install", "context7"],
                        environ={"HOME": str(root), "PATH": ""},
                        platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                        runner=ConfiguredRunner(), connectivity_probe=lambda: True,
                    )
            payload = json.loads(output.getvalue())
            context7 = next(tool for tool in payload["tools"] if tool["name"] == "context7")
            self.assertEqual(1, code)
            self.assertEqual("AUTH_REQUIRED", context7["status"])
            self.assertEqual(1, payload["summary"]["auth_required"])
            self.assertEqual(0, payload["summary"]["failed"])
            self.assertEqual(original, config.read_bytes())

    def test_go_install_is_rediscovered_from_scoped_path_in_same_run(self):
        class InstallingGoRunner:
            def __init__(self, go_workspace):
                self.go_workspace = go_workspace

            def run(self, command, **kwargs):
                if len(command) >= 3 and tuple(command[1:3]) == ("env", "GOBIN"):
                    return CommandResult(0, f"\n{self.go_workspace}\n", "")
                if tuple(command[:2]) == ("go", "install"):
                    target = self.go_workspace / "bin" / "osv-scanner"
                    target.write_text("binary", encoding="utf-8")
                    target.chmod(0o700)
                    return CommandResult(0, "", "")
                if Path(command[0]).name == "osv-scanner":
                    return CommandResult(0, "osv-scanner 2.5.0\n", "")
                return CommandResult(1, "", "missing")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool_bin = root / "tool-bin"
            go_path = root / "go-workspace" / "bin"
            tool_bin.mkdir()
            go_path.mkdir(parents=True)
            fake_go = tool_bin / "go"
            fake_go.write_text("go", encoding="utf-8")
            fake_go.chmod(0o700)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    ["--json", "install", "osv-scanner"],
                    environ={"HOME": str(root), "PATH": str(tool_bin)},
                    platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                    runner=InstallingGoRunner(go_path.parent), connectivity_probe=lambda: True,
                )
            payload = json.loads(output.getvalue())
            osv = next(tool for tool in payload["tools"] if tool["name"] == "osv-scanner")
            self.assertEqual(0, code)
            self.assertEqual("HEALTHY", osv["status"])

    def test_newly_installed_go_refreshes_scoped_path_before_tool_install(self):
        class DependencyInstallingRunner:
            def __init__(self, go_executable, go_workspace):
                self.go_executable = go_executable
                self.go_workspace = go_workspace

            def run(self, command, **kwargs):
                if tuple(command[:3]) == ("sudo", "apt-get", "install"):
                    self.go_executable.write_text("go", encoding="utf-8")
                    self.go_executable.chmod(0o700)
                    return CommandResult(0, "", "")
                if len(command) >= 3 and tuple(command[1:3]) == ("env", "GOBIN"):
                    return CommandResult(0, f"\n{self.go_workspace}\n", "")
                if tuple(command[:2]) == ("go", "install"):
                    target = self.go_workspace / "bin" / "osv-scanner"
                    target.write_text("binary", encoding="utf-8")
                    target.chmod(0o700)
                    return CommandResult(0, "", "")
                if Path(command[0]).name == "osv-scanner":
                    return CommandResult(0, "osv-scanner 2.5.0\n", "")
                return CommandResult(1, "", "missing")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool_bin = root / "tool-bin"
            go_workspace = root / "go-workspace"
            tool_bin.mkdir()
            (go_workspace / "bin").mkdir(parents=True)
            runner = DependencyInstallingRunner(tool_bin / "go", go_workspace)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    ["--json", "install", "osv-scanner"],
                    environ={"HOME": str(root), "PATH": str(tool_bin)},
                    platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                    runner=runner, connectivity_probe=lambda: True,
                )
            payload = json.loads(output.getvalue())
            osv = next(tool for tool in payload["tools"] if tool["name"] == "osv-scanner")
            self.assertEqual(0, code)
            self.assertEqual("HEALTHY", osv["status"])

    def test_non_regular_config_returns_structured_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / ".codex" / "config.toml"
            config.mkdir(parents=True)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    ["check", "--json"],
                    environ={"HOME": str(root), "PATH": ""},
                    platform_facts={"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "x86_64"},
                    runner=MissingRunner(), connectivity_probe=lambda: True,
                )
            payload = json.loads(output.getvalue())
            self.assertEqual(1, code)
            self.assertFalse(payload["codex"]["config_valid"])
            self.assertTrue(payload["issues"])
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
