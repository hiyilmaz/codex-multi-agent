import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER = REPO_ROOT / "bin/cma-tools"
SETUP = REPO_ROOT / "bin/codex-setup"


class CmaToolsIntegrationTests(unittest.TestCase):
    def fake_environment(self, root: Path):
        fake_bin = root / "bin"
        fake_bin.mkdir()
        ambient_log = root / "ambient-codex-tools.log"
        command = fake_bin / "codex-tools"
        command.write_text(
            "#!/usr/bin/env bash\n"
            "printf '%s\\n' \"$*\" >> \"$AMBIENT_CODEX_TOOLS_TEST_LOG\"\n"
            "exit 91\n",
            encoding="utf-8",
        )
        command.chmod(0o755)
        python_log = root / "python.log"
        python_probe_log = root / "python-probe.log"
        python_script = (
            "#!/usr/bin/env bash\n"
            "if [[ \"${1:-}\" == '-I' && \"${2:-}\" == '-S' && $# -eq 4 ]]; then\n"
            "  printf '%s\\n' \"$*\" >> \"$PYTHON_PROBE_TEST_LOG\"\n"
            "  [[ \"${PYTHON_TEST_VERSION_OK:-1}\" == '1' ]]; exit\n"
            "fi\n"
            "if [[ \"$*\" != *codex_tool_installer* ]]; then exit 0; fi\n"
            "printf 'ARGS=%s\\n' \"$*\" >> \"$PYTHON_TEST_LOG\"\n"
            "printf '%s' \"${PYTHON_TEST_STDERR:-}\" >&2\n"
            "exit \"${PYTHON_TEST_EXIT:-0}\"\n"
        )
        for name in ("python3.13", "python3.12", "python3.11", "python3"):
            python = fake_bin / name
            python.write_text(python_script, encoding="utf-8")
            python.chmod(0o755)
        uv_log = root / "uv.log"
        installed_log = root / "installed-codex-tools.log"
        uv_tool_bin = root / "uv-tool-bin"
        uv_tool_bin.mkdir()
        uv_codex_tools = uv_tool_bin / "codex-tools"
        uv_codex_tools.write_text(
            "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> \"$INSTALLED_CODEX_TOOLS_TEST_LOG\"\n",
            encoding="utf-8",
        )
        uv_codex_tools.chmod(0o755)
        uv = fake_bin / "uv"
        uv.write_text(
            "#!/usr/bin/env bash\n"
            "if [[ \"$*\" == 'tool dir --bin' ]]; then printf '%s\\n' \"$UV_TEST_BIN_DIR\"; exit 0; fi\n"
            "printf '%s\\n' \"$*\" >> \"$UV_TEST_LOG\"\n",
            encoding="utf-8",
        )
        uv.chmod(0o755)
        npx = fake_bin / "npx"
        npx.write_text(
            '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$NPX_TEST_LOG"\n', encoding="utf-8",
        )
        npx.chmod(0o755)
        return {
            **os.environ,
            "HOME": str(root / "home"),
            "PATH": f"{fake_bin}:{os.environ['PATH']}",
            "AMBIENT_CODEX_TOOLS_TEST_LOG": str(ambient_log),
            "PYTHON_TEST_LOG": str(python_log),
            "PYTHON_PROBE_TEST_LOG": str(python_probe_log),
            "INSTALLED_CODEX_TOOLS_TEST_LOG": str(installed_log),
            "UV_TEST_LOG": str(uv_log),
            "UV_TEST_BIN_DIR": str(uv_tool_bin),
            "NPX_TEST_LOG": str(root / "npx.log"),
        }, ambient_log, python_log, python_probe_log, installed_log, uv_log

    def test_adapter_always_forces_verify_only_for_read_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, python_log, python_probe_log, _installed_log, _uv_log = self.fake_environment(root)
            for mode in ("check", "dry-run"):
                result = subprocess.run((str(ADAPTER), mode), env=environment, text=True, capture_output=True, check=False)
                self.assertEqual(0, result.returncode, result.stderr)
            lines = python_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(lines))
            self.assertTrue(all("--mcp-mode verify-only" in line for line in lines))
            self.assertTrue(all("-B -I -S -c" in line for line in lines))
            self.assertTrue(all("run_module(\"codex_tool_installer\"" in line for line in lines))
            self.assertTrue(all(str(REPO_ROOT / "tools/codex-tool-installer/src") in line for line in lines))
            self.assertIn("check", lines[0])
            self.assertIn("--dry-run", lines[1])
            probes = python_probe_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(probes))
            self.assertTrue(all(line.startswith("-I -S -c") for line in probes))
            self.assertFalse(ambient_log.exists())

    def test_adapter_forwards_json_for_check(self):
        with tempfile.TemporaryDirectory() as directory:
            environment, _, python_log, _, _, _ = self.fake_environment(Path(directory))
            result = subprocess.run(
                (str(ADAPTER), "check", "--json"), env=environment, text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("check --json", python_log.read_text(encoding="utf-8"))

    def test_read_paths_propagate_bundled_python_failures_without_path_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, python_log, _python_probe_log, _installed_log, _uv_log = self.fake_environment(root)
            environment["PYTHON_TEST_EXIT"] = "37"
            environment["PYTHON_TEST_STDERR"] = "bundled failure\n"

            result = subprocess.run(
                (str(ADAPTER), "check"), env=environment, text=True, capture_output=True, check=False
            )

            self.assertEqual(37, result.returncode)
            self.assertIn("bundled failure", result.stderr)
            self.assertTrue(python_log.exists())
            self.assertFalse(ambient_log.exists())

    def test_read_paths_fail_closed_without_supported_python(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, python_log, python_probe_log, _installed_log, _uv_log = self.fake_environment(root)
            environment["PYTHON_TEST_VERSION_OK"] = "0"

            result = subprocess.run(
                (str(ADAPTER), "check"), env=environment, text=True, capture_output=True, check=False
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Python 3.11 or newer is required", result.stderr)
            self.assertFalse(python_log.exists())
            self.assertEqual(4, len(python_probe_log.read_text(encoding="utf-8").splitlines()))
            self.assertFalse(ambient_log.exists())

    def test_install_executes_the_just_installed_uv_entrypoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, _python_log, _python_probe_log, installed_log, uv_log = self.fake_environment(root)

            result = subprocess.run(
                (str(ADAPTER), "install", "--yes"),
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("--mcp-mode verify-only", installed_log.read_text(encoding="utf-8"))
            self.assertIn("tool install --force --python 3.11", uv_log.read_text(encoding="utf-8"))
            self.assertFalse(ambient_log.exists())

    def test_setup_defaults_to_check_and_preserves_explicit_modes(self):
        setup_input = "\nn\nn\n\n\n\n\nn\n\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, python_log, _python_probe_log, installed_log, uv_log = self.fake_environment(root)
            default = subprocess.run(
                (str(SETUP), "--variant", "codex"),
                cwd=REPO_ROOT,
                env=environment,
                input=setup_input,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, default.returncode, default.stderr)
            self.assertEqual(1, len(python_log.read_text(encoding="utf-8").splitlines()))
            self.assertIn("--mcp-mode verify-only", python_log.read_text(encoding="utf-8"))
            self.assertFalse(installed_log.exists())
            self.assertFalse(uv_log.exists())
            self.assertFalse((root / "npx.log").exists())

            skipped = subprocess.run(
                (str(SETUP), "--variant", "codex", "--tools-mode", "skip"),
                cwd=REPO_ROOT, env=environment, input=setup_input, text=True, capture_output=True,
            )
            self.assertEqual(0, skipped.returncode, skipped.stderr)
            self.assertEqual(1, len(python_log.read_text(encoding="utf-8").splitlines()))

            checked = subprocess.run(
                (str(SETUP), "--variant", "codex", "--tools-mode", "check"),
                cwd=REPO_ROOT,
                env=environment,
                input=setup_input,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, checked.returncode, checked.stderr)
            self.assertEqual(2, len(python_log.read_text(encoding="utf-8").splitlines()))

            installed = subprocess.run(
                (str(SETUP), "--variant", "codex", "--tools-mode", "install"),
                cwd=REPO_ROOT,
                env=environment,
                input=setup_input,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, installed.returncode, installed.stderr)
            self.assertEqual(1, len(installed_log.read_text(encoding="utf-8").splitlines()))
            self.assertIn("--mcp-mode verify-only", installed_log.read_text(encoding="utf-8"))
            self.assertIn("tool install --force --python 3.11", uv_log.read_text(encoding="utf-8"))
            self.assertFalse(ambient_log.exists())

    def test_setup_default_health_failure_is_reported_and_explicit_exit_is_preserved(self):
        setup_input = "\nn\nn\n\n\n\n\nn\n\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, _, python_log, _, installed_log, uv_log = self.fake_environment(root)
            environment.update(PYTHON_TEST_EXIT="37", PYTHON_TEST_STDERR="probe failed\n")
            config = root / "home/.codex/config.toml"
            config.parent.mkdir(parents=True)
            config.write_bytes(b'model = "preserved"\n')
            for extra, expected in (((), 0), (("--tools-mode", "check"), 37)):
                with self.subTest(extra=extra):
                    result = subprocess.run(
                        (str(SETUP), "--variant", "codex", *extra), cwd=REPO_ROOT, env=environment,
                        input=setup_input, text=True, capture_output=True,
                    )
                    self.assertEqual(expected, result.returncode, result.stderr)
                    self.assertIn("probe failed", result.stderr)
                    self.assertIn("STATUS_MESSAGES.md", result.stdout)
                    if not extra:
                        self.assertIn("exit 37", result.stderr)
                        self.assertIn("Kurulum tamamlandı.", result.stdout)
            self.assertEqual(2, len(python_log.read_text(encoding="utf-8").splitlines()))
            self.assertEqual(b'model = "preserved"\n', config.read_bytes())
            self.assertFalse(installed_log.exists())
            self.assertFalse(uv_log.exists())
            self.assertFalse((root / "npx.log").exists())

    def test_setup_default_check_skips_other_variants_and_custom_homes(self):
        setup_input = "\nn\nn\n\n\n\n\nn\n\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, _, python_log, _, _, _ = self.fake_environment(root)
            for args in (("--variant", "claude"), ("--variant", "codex", "--runtime-home", str(root / "custom"))):
                with self.subTest(args=args):
                    result = subprocess.run(
                        (str(SETUP), *args), cwd=REPO_ROOT, env=environment,
                        input=setup_input, text=True, capture_output=True,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertFalse(python_log.exists())

    def test_setup_rejects_tools_for_non_codex_variant_before_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, ambient_log, python_log, _python_probe_log, installed_log, _uv_log = self.fake_environment(root)
            result = subprocess.run(
                (str(SETUP), "--variant", "claude", "--tools-mode", "check"),
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Codex", result.stderr)
            self.assertFalse(ambient_log.exists())
            self.assertFalse(python_log.exists())
            self.assertFalse(installed_log.exists())
            self.assertFalse((root / "home").exists())

    def test_standalone_guide_documents_bundled_and_installed_execution_paths(self):
        guide = REPO_ROOT / "docs/CMA_TOOLS_GUIDE.md"
        content = guide.read_text(encoding="utf-8")
        self.assertIn("bin/cma-tools check", content)
        self.assertIn("bin/cma-tools dry-run", content)
        self.assertIn("Python 3.11", content)
        self.assertIn("bundled", content.lower())
        self.assertIn("uv tool install", content)
        self.assertIn("verify-only", content)


if __name__ == "__main__":
    unittest.main()
