import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "bin/codex-setup"
INSTALLER = ROOT / "bin/codex-user-install"
SYSTEM_PATH = "/usr/bin:/bin"


class CodexSetupContext7Tests(unittest.TestCase):
    def make_environment(
        self,
        root: Path,
        *,
        node_version: str | None = "v22.0.0",
        node_exit: int = 0,
        include_npx: bool = True,
        npx_exit: int = 0,
    ) -> tuple[dict[str, str], Path, Path]:
        fake_bin = root / "fake-bin"
        fake_bin.mkdir()
        if node_version is not None:
            node = fake_bin / "node"
            node.write_text(
                "#!/bin/sh\n"
                "if [ \"${1:-}\" = '--version' ]; then\n"
                "  printf '%s\\n' \"$FAKE_NODE_VERSION\"\n"
                "  exit \"$FAKE_NODE_EXIT\"\n"
                "fi\n"
                "exit 64\n",
                encoding="utf-8",
            )
            node.chmod(0o755)

        npx_log = root / "npx-args.log"
        npx_home_log = root / "npx-home.log"
        if include_npx:
            npx = fake_bin / "npx"
            npx.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" >> \"$FAKE_NPX_LOG\"\n"
                "printf '%s\\n' \"$HOME\" >> \"$FAKE_NPX_HOME_LOG\"\n"
                "exit \"$FAKE_NPX_EXIT\"\n",
                encoding="utf-8",
            )
            npx.chmod(0o755)

        environment = {
            **os.environ,
            "HOME": str(root / "home"),
            "PATH": f"{fake_bin}:{SYSTEM_PATH}",
            "FAKE_NODE_VERSION": node_version or "",
            "FAKE_NODE_EXIT": str(node_exit),
            "FAKE_NPX_LOG": str(npx_log),
            "FAKE_NPX_HOME_LOG": str(npx_home_log),
            "FAKE_NPX_EXIT": str(npx_exit),
            "CONTEXT7_API_KEY": "ctx7-secret-sentinel",
        }
        environment.pop("CODEX_HOME", None)
        return environment, npx_log, npx_home_log

    @staticmethod
    def setup_input(context7_answer: str = "n") -> str:
        return "\ny\ny\nn\n\n\n\n\nn\n" + context7_answer + "\n"

    def run_setup(
        self,
        root: Path,
        environment: dict[str, str],
        *,
        context7_answer: str = "n",
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        runtime = root / "custom-codex"
        result = subprocess.run(
            (str(SETUP), "--variant", "codex", "--runtime-home", str(runtime)),
            cwd=ROOT,
            env=environment,
            input=self.setup_input(context7_answer),
            text=True,
            capture_output=True,
            check=False,
        )
        return result, runtime

    def test_read_only_commands_bypass_node_and_npx_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment = {
                **os.environ,
                "HOME": str(root / "home"),
                "PATH": SYSTEM_PATH,
            }
            commands = (
                (str(SETUP), "--help"),
                (str(SETUP), "--list-variants"),
                (str(INSTALLER), "--help"),
                (str(INSTALLER), "--list-variants"),
            )
            outputs = []
            for command in commands:
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                outputs.append(result.stdout)
            self.assertEqual(outputs[1], outputs[3])
            self.assertFalse((root / "home").exists())

    def test_mutating_entrypoints_accept_node_22_boundary(self) -> None:
        for version in ("v22.0.0", "v23.1.2"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                environment, npx_log, _ = self.make_environment(root, node_version=version)
                setup, runtime = self.run_setup(root, environment)
                self.assertEqual(setup.returncode, 0, setup.stderr)
                self.assertTrue((runtime / "AGENTS.md").is_file())
                self.assertFalse(npx_log.exists())

                install_runtime = root / "installer-runtime"
                installer = subprocess.run(
                    (str(INSTALLER), "--variant", "codex", "--runtime-home", str(install_runtime)),
                    cwd=ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(installer.returncode, 0, installer.stderr)
                self.assertTrue((install_runtime / "AGENTS.md").is_file())

    def test_mutating_entrypoints_reject_unsupported_or_invalid_node_before_writes(self) -> None:
        for version in (None, "v21.99.0", "not-a-node-version", "v22"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                environment, npx_log, _ = self.make_environment(root, node_version=version)
                setup, runtime = self.run_setup(root, environment)
                self.assertNotEqual(setup.returncode, 0)
                self.assertIn("Node.js 22 or newer is required", setup.stderr)
                self.assertFalse(runtime.exists())
                self.assertFalse(npx_log.exists())

                install_runtime = root / "installer-runtime"
                installer = subprocess.run(
                    (str(INSTALLER), "--variant", "codex", "--runtime-home", str(install_runtime)),
                    cwd=ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertNotEqual(installer.returncode, 0)
                self.assertIn("Node.js 22 or newer is required", installer.stderr)
                self.assertFalse(install_runtime.exists())
                self.assertFalse(npx_log.exists())

    def test_mutating_entrypoints_require_npx_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, npx_log, _ = self.make_environment(root, include_npx=False)
            setup, runtime = self.run_setup(root, environment)
            self.assertNotEqual(setup.returncode, 0)
            self.assertIn("npx is required", setup.stderr)
            self.assertFalse(runtime.exists())
            self.assertFalse(npx_log.exists())

            install_runtime = root / "installer-runtime"
            installer = subprocess.run(
                (str(INSTALLER), "--variant", "codex", "--runtime-home", str(install_runtime)),
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(installer.returncode, 0)
            self.assertIn("npx is required", installer.stderr)
            self.assertFalse(install_runtime.exists())

    def test_node_version_command_failure_is_terminal_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, npx_log, _ = self.make_environment(
                root,
                node_version="v22.0.0",
                node_exit=42,
            )
            setup, runtime = self.run_setup(root, environment)
            self.assertNotEqual(setup.returncode, 0)
            self.assertIn("Node.js 22 or newer is required", setup.stderr)
            self.assertFalse(runtime.exists())
            self.assertFalse(npx_log.exists())

            install_runtime = root / "installer-runtime"
            installer = subprocess.run(
                (str(INSTALLER), "--variant", "codex", "--runtime-home", str(install_runtime)),
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(installer.returncode, 0)
            self.assertIn("Node.js 22 or newer is required", installer.stderr)
            self.assertFalse(install_runtime.exists())
            self.assertFalse(npx_log.exists())

    def test_context7_default_yes_runs_exact_unpinned_command_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, npx_log, npx_home_log = self.make_environment(root)
            result, runtime = self.run_setup(root, environment, context7_answer="")
            combined = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((runtime / "AGENTS.md").is_file())
            self.assertEqual(npx_log.read_text(encoding="utf-8").splitlines(), ["ctx7 setup"])
            self.assertEqual(npx_home_log.read_text(encoding="utf-8").splitlines(), [environment["HOME"]])
            self.assertNotIn("ctx7@", npx_log.read_text(encoding="utf-8"))
            self.assertNotIn("--yes", npx_log.read_text(encoding="utf-8"))
            self.assertNotIn(environment["CONTEXT7_API_KEY"], combined)
            self.assertNotIn(environment["CONTEXT7_API_KEY"], npx_log.read_text(encoding="utf-8"))

    def test_context7_explicit_no_does_not_invoke_npx(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, npx_log, _ = self.make_environment(root)
            result, _ = self.run_setup(root, environment, context7_answer="n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(npx_log.exists())

    def test_context7_failure_propagates_exact_exit_without_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment, npx_log, _ = self.make_environment(root, npx_exit=37)
            result, _ = self.run_setup(root, environment, context7_answer="y")
            self.assertEqual(result.returncode, 37, result.stderr)
            self.assertEqual(npx_log.read_text(encoding="utf-8").splitlines(), ["ctx7 setup"])
            self.assertNotIn("Kurulum tamamlandı.", result.stdout)

    def test_custom_runtime_global_context7_target_is_documented(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        command_reference = (ROOT / "COMMAND_REFERENCE.md").read_text(encoding="utf-8")
        turkish_guide = (ROOT / "TURKCE_KURULUM_REHBERI.md").read_text(encoding="utf-8")
        for document in (readme, command_reference, turkish_guide):
            self.assertIn("npx ctx7 setup", document)
            self.assertIn("Node.js 22", document)
            self.assertIn("HOME", document)


if __name__ == "__main__":
    unittest.main()
