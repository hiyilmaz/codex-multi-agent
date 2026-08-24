import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK = REPO_ROOT / "bin" / "cma-tool-check"
TOOLS = ("node", "npm", "npx", "codex", "bwrap", "agent-browser", "gh", "img-process", "serena")


class CmaToolCheckTests(unittest.TestCase):
    def write_tool(self, directory: Path, name: str, version: str, *, version_exit: int = 0, mcp_exit: int = 0):
        command = directory / name
        command.write_text(
            "#!/bin/bash\n"
            "if [[ \"${1:-}\" == \"--version\" ]]; then\n"
            f"  printf '%s\\n' '{version}'\n"
            f"  exit {version_exit}\n"
            "fi\n"
            "if [[ \"$0\" == *'/codex' && \"${1:-}\" == \"mcp\" && \"${2:-}\" == \"list\" ]]; then\n"
            "  printf '%s\\n' 'context7 enabled'\n"
            f"  exit {mcp_exit}\n"
            "fi\n"
            "exit 64\n",
            encoding="utf-8",
        )
        command.chmod(0o755)

    def environment(self, root: Path):
        fake_bin = root / "bin"
        fake_bin.mkdir()
        home = root / "home"
        home.mkdir()
        return fake_bin, {
            **os.environ,
            "HOME": str(home),
            "PATH": str(fake_bin),
        }

    def run_check(self, environment, *args):
        root_args = ("--allow-root",) if os.geteuid() == 0 else ()
        return subprocess.run(
            ("/bin/bash", str(CHECK), *root_args, *args),
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_help_and_unknown_option_do_not_probe_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_bin, environment = self.environment(Path(directory))
            self.write_tool(fake_bin, "node", "v22.0.0")

            help_result = self.run_check(environment, "--help")
            bad_result = self.run_check(environment, "--unknown")

            self.assertEqual(0, help_result.returncode)
            self.assertIn("Usage: cma-tool-check", help_result.stdout)
            self.assertEqual(2, bad_result.returncode)
            self.assertIn("unknown option", bad_result.stderr)

    def test_inventory_reports_real_paths_versions_and_optional_missing_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_bin, environment = self.environment(Path(directory))
            for name in ("node", "npm", "npx", "codex"):
                self.write_tool(fake_bin, name, "v22.3.0" if name == "node" else f"{name}-version")

            result = self.run_check(environment, "--show-mcp-output")

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(f"node | PASS | {fake_bin / 'node'} | v22.3.0", result.stdout)
            self.assertIn(f"npm | FOUND | {fake_bin / 'npm'} | npm-version", result.stdout)
            self.assertIn(f"codex | FOUND | {fake_bin / 'codex'} | codex-version", result.stdout)
            self.assertIn("bwrap | MISSING | - | -", result.stdout)
            self.assertIn("agent-browser | MISSING | - | -", result.stdout)
            self.assertIn("MCP | PASS | codex mcp list | -", result.stdout)
            self.assertIn("context7 enabled", result.stdout)
            self.assertIn("SUMMARY", result.stdout)

    def test_node_requires_v22_or_newer_and_valid_version_output(self):
        for version in ("v21.9.0", "22.0.0", "v22", "garbage"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                fake_bin, environment = self.environment(Path(directory))
                self.write_tool(fake_bin, "node", version)
                self.write_tool(fake_bin, "codex", "codex-version")

                result = self.run_check(environment)

                self.assertNotEqual(0, result.returncode)
                self.assertIn("NODE_22_PLUS=FAIL", result.stdout)
                self.assertIn(version, result.stdout)

    def test_version_and_mcp_failures_are_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_bin, environment = self.environment(Path(directory))
            self.write_tool(fake_bin, "node", "v22.0.0")
            self.write_tool(fake_bin, "npm", "npm-version", version_exit=9)
            self.write_tool(fake_bin, "codex", "codex-version", mcp_exit=7)

            result = self.run_check(environment)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("npm | VERSION_FAILED", result.stdout)
            self.assertIn("MCP | FAIL | codex mcp list | exit 7", result.stdout)

    def test_untrusted_terminal_control_output_and_mcp_output_are_hidden_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_bin, environment = self.environment(Path(directory))
            self.write_tool(fake_bin, "node", "v22.0.0")
            self.write_tool(fake_bin, "codex", "codex-version")
            self.write_tool(fake_bin, "npm", "npm\x1b[2Jversion")

            result = self.run_check(environment)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("[unsafe terminal output suppressed]", result.stdout)
            self.assertNotIn("context7 enabled", result.stdout)

    @unittest.skipUnless(os.geteuid() == 0, "requires a real root process")
    def test_root_requires_explicit_allow_root_before_probing_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            fake_bin, environment = self.environment(Path(directory))
            self.write_tool(fake_bin, "node", "v22.0.0")
            self.write_tool(fake_bin, "codex", "codex-version")

            blocked = subprocess.run(
                ("/bin/bash", str(CHECK)), env=environment, text=True, capture_output=True, check=False
            )
            allowed = subprocess.run(
                ("/bin/bash", str(CHECK), "--allow-root"),
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(2, blocked.returncode)
            self.assertIn("running as root requires --allow-root", blocked.stderr)
            self.assertEqual(0, allowed.returncode, allowed.stderr)

    def test_execution_does_not_write_to_home_or_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_bin, environment = self.environment(root)
            working_directory = root / "work"
            working_directory.mkdir()
            (working_directory / "unchanged.txt").write_text("before\n", encoding="utf-8")
            for name in ("node", "npm", "npx", "codex"):
                self.write_tool(fake_bin, name, "v22.0.0" if name == "node" else f"{name}-version")

            before = self.tree_hash(root / "home", working_directory)
            result = subprocess.run(
                ("/bin/bash", str(CHECK), *(("--allow-root",) if os.geteuid() == 0 else ())),
                cwd=working_directory,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(before, self.tree_hash(root / "home", working_directory))

    def test_documentation_describes_portable_read_only_usage(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "docs" / "CHANGELOG.md").read_text(encoding="utf-8")

        self.assertIn("bin/cma-tool-check", readme)
        self.assertIn("--allow-root", readme)
        self.assertIn("--show-mcp-output", readme)
        self.assertIn("running as root requires --allow-root", CHECK.read_text(encoding="utf-8"))
        self.assertIn("Node.js 22", readme)
        self.assertIn("read-only", readme.lower())
        self.assertIn("cma-tool-check", changelog)

    def tree_hash(self, *roots: Path):
        digest = hashlib.sha256()
        for root in roots:
            for path in sorted(root.rglob("*")):
                digest.update(str(path.relative_to(root)).encode())
                digest.update(str(path.stat().st_mode).encode())
                if path.is_file():
                    digest.update(path.read_bytes())
        return digest.hexdigest()


if __name__ == "__main__":
    unittest.main()
