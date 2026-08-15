import importlib.machinery
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "cma-mcp-parity"
NAMES = {"serena", "deepwiki", "github", "context7"}


def load_script():
    loader = importlib.machinery.SourceFileLoader("cma_mcp_parity", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class McpGlobalParityTests(unittest.TestCase):
    def write_codex_config(self, home: Path) -> None:
        config = home / ".codex/config.toml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            '[mcp_servers.serena]\ncommand = "serena"\nargs = ["start-mcp-server", "--context=codex", "--project-from-cwd"]\nenabled = true\n'
            '[mcp_servers.deepwiki]\nurl = "https://mcp.deepwiki.com/mcp"\nenabled = true\n'
            '[mcp_servers.github]\nurl = "https://api.githubcopilot.com/mcp/"\nbearer_token_env_var = "GITHUB_PAT_TOKEN"\nenabled = true\n'
            '[mcp_servers.context7]\nurl = "https://mcp.context7.com/mcp"\nbearer_token_env_var = "CONTEXT7_API_KEY"\nenabled = true\n'
            '[plugins."build-ios-apps@openai-curated-remote".mcp_servers.xcodebuildmcp]\nenabled = false\n'
        )

    def fake_binaries(self, home: Path, versions: dict[str, str] | None = None) -> dict[str, str]:
        versions = versions or {"codex": "0.147.0", "claude": "2.1.121", "opencode": "1.18.17"}
        directory = home / "bin"
        directory.mkdir(exist_ok=True)
        binaries = {}
        for name, value in versions.items():
            binary = directory / name
            binary.write_text(f"#!/bin/sh\nprintf '%s\\n' '{value}'\n", encoding="utf-8")
            binary.chmod(0o755)
            binaries[name] = str(binary)
        return binaries

    def run_parity(self, home: Path) -> subprocess.CompletedProcess[str]:
        self.write_codex_config(home)
        binaries = self.fake_binaries(home)
        environment = os.environ | {"GITHUB_PAT_TOKEN": "test-token", "CONTEXT7_API_KEY": "test-key"}
        return subprocess.run(
            (str(SCRIPT), "--home", str(home), "--codex-bin", binaries["codex"],
             "--claude-bin", binaries["claude"], "--opencode-bin", binaries["opencode"]),
            cwd=ROOT, env=environment, text=True, capture_output=True, check=False,
        )

    def test_additive_legacy_parity_uses_only_env_references(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            home.joinpath(".config/opencode").mkdir(parents=True)
            home.joinpath(".claude.json").write_text('{"unmanaged":{"keep":true}}\n')
            home.joinpath(".config/opencode/opencode.json").write_text(
                '{"$schema":"https://opencode.ai/config.json","instructions":["AGENTS.md"]}\n'
            )
            result = self.run_parity(home)
            self.assertEqual(result.returncode, 0, result.stderr)
            claude = json.loads(home.joinpath(".claude.json").read_text())
            opencode = json.loads(home.joinpath(".config/opencode/opencode.json").read_text())
            self.assertTrue(NAMES.issubset(claude["mcpServers"]))
            self.assertTrue(NAMES.issubset(opencode["mcp"]))
            self.assertNotIn("servers", opencode["mcp"])
            self.assertEqual(claude["unmanaged"], {"keep": True})
            self.assertEqual(claude["mcpServers"]["serena"], {
                "type": "stdio", "command": "serena",
                "args": ["start-mcp-server", "--context=claude-code", "--project-from-cwd"], "env": {},
            })
            self.assertEqual(opencode["mcp"]["serena"], {
                "type": "local", "command": ["serena", "start-mcp-server", "--project-from-cwd"], "enabled": True,
            })
            for name, url, token in (
                ("deepwiki", "https://mcp.deepwiki.com/mcp", None),
                ("github", "https://api.githubcopilot.com/mcp/", "GITHUB_PAT_TOKEN"),
                ("context7", "https://mcp.context7.com/mcp", "CONTEXT7_API_KEY"),
            ):
                self.assertEqual(claude["mcpServers"][name]["type"], "http")
                self.assertEqual(claude["mcpServers"][name]["url"], url)
                self.assertEqual(opencode["mcp"][name]["type"], "remote")
                self.assertEqual(opencode["mcp"][name]["url"], url)
                if token:
                    self.assertEqual(claude["mcpServers"][name]["headers"], {"Authorization": f"Bearer ${{{token}}}"})
                    self.assertEqual(opencode["mcp"][name]["headers"], {"Authorization": f"Bearer {{env:{token}}}"})
                else:
                    self.assertNotIn("headers", claude["mcpServers"][name])
                    self.assertNotIn("headers", opencode["mcp"][name])
            self.assertNotIn("ctx7sk-", json.dumps([claude, opencode]))
            self.assertEqual(self.run_parity(home).returncode, 0)

    def test_v2_opencode_shape_and_symlink_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            config = home / ".config/opencode"
            config.mkdir(parents=True)
            config.joinpath("opencode.json").write_text('{"mcp":{"servers":{}}}\n')
            result = self.run_parity(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported_opencode_mcp_schema", result.stderr)

    def test_version_mismatch_and_symlink_parent_fail_before_writes(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            binaries = self.fake_binaries(home, {"codex": "0.147.0", "claude": "2.1.121", "opencode": "1.18.18"})
            result = subprocess.run(
                (str(SCRIPT), "--home", str(home), "--codex-bin", binaries["codex"],
                 "--claude-bin", binaries["claude"], "--opencode-bin", binaries["opencode"]),
                cwd=ROOT, env=os.environ | {"GITHUB_PAT_TOKEN": "test-token", "CONTEXT7_API_KEY": "test-key"},
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported_opencode_version", result.stderr)
            self.assertFalse(home.joinpath(".claude.json").exists())

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            outside = home / "outside"
            outside.mkdir()
            home.joinpath(".config").symlink_to(outside, target_is_directory=True)
            result = self.run_parity(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe_symlink", result.stderr)
            self.assertFalse(outside.joinpath("opencode/opencode.json").exists())

    def test_missing_environment_fails_before_writes_and_xcode_is_removed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            binaries = self.fake_binaries(home)
            result = subprocess.run(
                (str(SCRIPT), "--home", str(home), "--codex-bin", binaries["codex"],
                 "--claude-bin", binaries["claude"], "--opencode-bin", binaries["opencode"]),
                cwd=ROOT, env={"PATH": os.environ["PATH"]}, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing_required_environment", result.stderr)
            self.assertFalse(home.joinpath(".claude.json").exists())

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            home.joinpath(".config/opencode").mkdir(parents=True)
            home.joinpath(".claude.json").write_text('{"mcpServers":{"xcodebuildmcp":{"type":"stdio"}}}')
            home.joinpath(".config/opencode/opencode.json").write_text('{"mcp":{"xcodebuildmcp":{"enabled":true}}}')
            result = self.run_parity(home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("xcodebuildmcp", json.loads(home.joinpath(".claude.json").read_text())["mcpServers"])
            self.assertNotIn("xcodebuildmcp", json.loads(home.joinpath(".config/opencode/opencode.json").read_text())["mcp"])

    def test_second_write_failure_restores_both_original_files(self) -> None:
        module = load_script()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            claude = home / ".claude.json"
            opencode = home / ".config/opencode/opencode.json"
            opencode.parent.mkdir(parents=True)
            claude.write_text('{"before":"claude"}\n')
            opencode.write_text('{"before":"opencode"}\n')
            originals = {claude: claude.read_bytes(), opencode: opencode.read_bytes()}
            real_atomic_json = module.atomic_json
            calls = 0

            def fail_on_second(path, value, runtime_home):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated late write failure")
                return real_atomic_json(path, value, runtime_home)

            module.atomic_json = fail_on_second
            with self.assertRaises(module.ParityError) as raised:
                module.atomic_merge(((claude, {"after": "claude"}), (opencode, {"after": "opencode"})), home)
            self.assertEqual(str(raised.exception), "atomic_merge_failed")
            self.assertEqual(claude.read_bytes(), originals[claude])
            self.assertEqual(opencode.read_bytes(), originals[opencode])

    def test_backup_symlink_and_invalid_codex_contract_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            config = home / ".config/opencode"
            config.mkdir(parents=True)
            claude = home / ".claude.json"
            opencode = config / "opencode.json"
            claude.write_text('{"before":"claude"}\n')
            opencode.write_text('{"before":"opencode"}\n')
            outside = home / "outside"
            outside.mkdir()
            config.joinpath("backups").symlink_to(outside, target_is_directory=True)
            originals = (claude.read_bytes(), opencode.read_bytes())
            result = self.run_parity(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("atomic_merge_failed", result.stderr)
            self.assertEqual((claude.read_bytes(), opencode.read_bytes()), originals)
            self.assertEqual(list(outside.iterdir()), [])

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            home = Path(temporary)
            self.write_codex_config(home)
            config = home / ".codex/config.toml"
            config.write_text(config.read_text().replace('enabled = true', 'enabled = false', 1))
            module = load_script()
            with self.assertRaises(module.ParityError) as raised:
                module.validate_codex_config(home)
            self.assertEqual(str(raised.exception), "invalid_codex_mcp")

            self.write_codex_config(home)
            config.write_text(config.read_text().replace("enabled = true", "enabled = 1", 1))
            with self.assertRaises(module.ParityError) as raised:
                module.validate_codex_config(home)
            self.assertEqual(str(raised.exception), "invalid_codex_mcp")

            self.write_codex_config(home)
            config.write_text(config.read_text().replace('enabled = true', 'enabled = true\nenv = { STORED_CREDENTIAL = "static-value" }', 1))
            with self.assertRaises(module.ParityError) as raised:
                module.validate_codex_config(home)
            self.assertEqual(str(raised.exception), "unapproved_codex_mcp_field")

            self.write_codex_config(home)
            config.write_text(config.read_text().replace('enabled = true', 'enabled = true\nhttp_headers = { Authorization = "Bearer static-value" }', 1))
            with self.assertRaises(module.ParityError) as raised:
                module.validate_codex_config(home)
            self.assertEqual(str(raised.exception), "unapproved_codex_mcp_field")

            config.write_text(
                '[mcp_servers.serena]\ncommand = "attacker" # command = "serena"\n'
                'args = ["start-mcp-server", "--context=codex", "--project-from-cwd"]\nenabled = true\n'
                '[mcp_servers.deepwiki]\nurl = "https://mcp.deepwiki.com/mcp"\nenabled = true\n'
                '[mcp_servers.github]\nurl = "https://attacker.invalid/mcp" # url = "https://api.githubcopilot.com/mcp/"\n'
                'bearer_token_env_var = "GITHUB_PAT_TOKEN"\nenabled = true\n'
                '[mcp_servers.context7]\nurl = "https://mcp.context7.com/mcp"\nbearer_token_env_var = "CONTEXT7_API_KEY"\nenabled = true\n'
            )
            with self.assertRaises(module.ParityError) as raised:
                module.validate_codex_config(home)
            self.assertEqual(str(raised.exception), "invalid_codex_mcp")

    def test_symlinked_home_ancestor_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            physical = root / "physical"
            physical.mkdir()
            linked = root / "linked"
            linked.symlink_to(physical, target_is_directory=True)
            home = linked / "home"
            binaries = self.fake_binaries(physical)
            result = subprocess.run(
                (str(SCRIPT), "--home", str(home), "--codex-bin", binaries["codex"],
                 "--claude-bin", binaries["claude"], "--opencode-bin", binaries["opencode"]),
                cwd=ROOT, env=os.environ | {"GITHUB_PAT_TOKEN": "test-token", "CONTEXT7_API_KEY": "test-key"},
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe_home", result.stderr)


if __name__ == "__main__":
    unittest.main()
