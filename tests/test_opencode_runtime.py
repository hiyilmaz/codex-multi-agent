import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME = REPO_ROOT / "variants/opencode/home"
LAUNCHER = REPO_ROOT / "variants/opencode/bin/opencode"
INSTALLER = REPO_ROOT / "bin/codex-user-install"


class OpenCodeRuntimeTests(unittest.TestCase):
    def test_config_uses_only_stable_provider_neutral_fields(self) -> None:
        config = json.loads((HOME / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(
            config,
            {
                "$schema": "https://opencode.ai/config.json",
                "instructions": ["AGENTS.md"],
            },
        )
        serialized = json.dumps(config).lower()
        for forbidden in ("provider", "model", "plugin", "/v2"):
            self.assertNotIn(forbidden, serialized)

    def test_agents_are_provider_neutral_markdown_subagents(self) -> None:
        expected = {
            "planner.md",
            "tdd-guide.md",
            "code-reviewer.md",
            "security-reviewer.md",
            "explorer.md",
            "docs-researcher.md",
            "reviewer.md",
            "skill-agent-governor.md",
        }
        agents = HOME / "agents"
        paths = list(agents.glob("*.md"))
        self.assertEqual({path.name for path in paths}, expected)
        self.assertEqual(len({path.read_bytes() for path in paths}), len(expected))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(agent=path.name):
                self.assertIn("mode: subagent", text)
                self.assertNotIn("model:", text)
                self.assertNotIn("permissionMode:", text)
                self.assertNotIn("-sol", text)
                self.assertNotIn("gpt-", text)
                self.assertNotIn("claude-", text.lower())

    def test_policy_preserves_chain_and_truthful_success_contract(self) -> None:
        policy = (HOME / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(
            "planner -> tdd-guide -> code-reviewer -> security-reviewer", policy
        )
        self.assertIn("success=true", policy)
        self.assertIn("No evidence means no success", policy)

    def test_launcher_overrides_hostile_environment_and_propagates_exit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            fake_bin = root / "bin"
            runtime.joinpath("bin").mkdir(parents=True)
            runtime.joinpath("opencode.json").write_text("{}\n", encoding="utf-8")
            fake_bin.mkdir()
            installed_launcher = runtime / "bin/llm-opencode"
            installed_launcher.write_bytes(LAUNCHER.read_bytes())
            installed_launcher.chmod(0o755)
            capture = root / "capture"
            fake = fake_bin / "opencode"
            fake.write_text(
                "#!/usr/bin/env bash\n"
                "printf '%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n' \"$OPENCODE_CONFIG\" \"$OPENCODE_CONFIG_DIR\" \"$XDG_CONFIG_HOME\" \"$XDG_DATA_HOME\" \"$XDG_CACHE_HOME\" \"$XDG_STATE_HOME\" > \"$CAPTURE\"\n"
                "printf '%s\\n' \"$@\" >> \"$CAPTURE\"\n"
                "exit 7\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            result = subprocess.run(
                (str(installed_launcher), "debug", "config"),
                env={
                    **os.environ,
                    "PATH": f"{fake_bin}:{os.environ['PATH']}",
                    "CAPTURE": str(capture),
                    "OPENCODE_CONFIG": "/hostile/config",
                    "OPENCODE_CONFIG_DIR": "/hostile/dir",
                    "XDG_CONFIG_HOME": "/hostile/xdg",
                    "XDG_DATA_HOME": "/hostile/data",
                    "XDG_CACHE_HOME": "/hostile/cache",
                    "XDG_STATE_HOME": "/hostile/state",
                },
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 7)
            self.assertEqual(
                capture.read_text(encoding="utf-8").splitlines(),
                [
                    str(runtime / "opencode.json"),
                    str(runtime),
                    str(runtime / "runtime-state/config"),
                    str(runtime / "runtime-state/data"),
                    str(runtime / "runtime-state/cache"),
                    str(runtime / "runtime-state/state"),
                    "debug",
                    "config",
                ],
            )

    def test_launcher_rejects_symlinked_isolated_state_directories(self) -> None:
        for relative in ("runtime-state", "config", "data", "cache", "state"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                runtime = root / "runtime"
                outside = root / "outside"
                fake_bin = root / "bin"
                runtime.joinpath("bin").mkdir(parents=True)
                outside.mkdir()
                fake_bin.mkdir()
                state_root = runtime / "runtime-state"
                if relative == "runtime-state":
                    state_root.symlink_to(outside, target_is_directory=True)
                else:
                    state_root.mkdir()
                    state_root.joinpath(relative).symlink_to(
                        outside, target_is_directory=True
                    )
                installed_launcher = runtime / "bin/llm-opencode"
                installed_launcher.write_bytes(LAUNCHER.read_bytes())
                installed_launcher.chmod(0o755)
                fake = fake_bin / "opencode"
                fake.write_text(
                    "#!/usr/bin/env bash\n"
                    "printf leaked > \"$OUTSIDE/write-proof\"\n",
                    encoding="utf-8",
                )
                fake.chmod(0o755)

                result = subprocess.run(
                    (str(installed_launcher), "debug", "paths"),
                    env={
                        **os.environ,
                        "PATH": f"{fake_bin}:{os.environ['PATH']}",
                        "OUTSIDE": str(outside),
                    },
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("symbolic link", result.stderr)
                self.assertEqual(list(outside.iterdir()), [])

    def test_skill_agent_governor_requires_approval_for_writes(self) -> None:
        text = (HOME / "agents/skill-agent-governor.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("edit: allow", text)
        self.assertIn("edit: ask", text)
        self.assertNotIn("bash: allow", text)
        self.assertIn("bash: ask", text)

    def test_launcher_fails_clearly_without_native_binary(self) -> None:
        result = subprocess.run(
            (str(LAUNCHER), "--version"),
            env={**os.environ, "PATH": "/usr/bin:/bin"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("native opencode", result.stderr.lower())

    def test_launcher_is_executable_and_has_valid_bash_syntax(self) -> None:
        self.assertTrue(LAUNCHER.stat().st_mode & stat.S_IXUSR)
        result = subprocess.run(
            ("bash", "-n", str(LAUNCHER)), text=True, capture_output=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_install_does_not_touch_native_global_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            native = root / "home/.config/opencode/opencode.json"
            native.parent.mkdir(parents=True)
            native.write_text("native\n", encoding="utf-8")
            result = subprocess.run(
                (str(INSTALLER), "--variant", "opencode"),
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(root / "home")},
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(native.read_text(encoding="utf-8"), "native\n")
            self.assertTrue((root / "home/.llm-runtimes/opencode/AGENTS.md").is_file())

    def test_installed_runtime_manifest_matches_packaged_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            result = subprocess.run(
                (
                    str(INSTALLER),
                    "--variant",
                    "opencode",
                    "--runtime-home",
                    str(runtime),
                ),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            source_files = {
                path.relative_to(HOME)
                for path in HOME.rglob("*")
                if path.is_file()
            }
            installed_files = {
                path.relative_to(runtime)
                for path in runtime.rglob("*")
                if path.is_file()
            }
            self.assertEqual(
                installed_files,
                source_files | {Path("bin/llm-opencode")},
            )

    def test_custom_runtime_rewrites_default_paths_in_installed_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "custom-opencode"
            result = subprocess.run(
                (
                    str(INSTALLER),
                    "--variant",
                    "opencode",
                    "--runtime-home",
                    str(runtime),
                ),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            checked = (
                runtime / "AGENTS.md",
                runtime / "registry/AGENTS_INDEX.md",
                runtime / "registry/SKILLS_INDEX.md",
                runtime / "registry/ORCHESTRATION.md",
            )
            for path in checked:
                text = path.read_text(encoding="utf-8")
                with self.subTest(path=path):
                    self.assertNotIn("~/.llm-runtimes/opencode", text)
                    self.assertIn(str(runtime), text)

    def test_runtime_docs_describe_isolation_and_debug_validation(self) -> None:
        for relative in (
            "README.md",
            "USAGE_GUIDE.md",
            "COMMAND_REFERENCE.md",
            "TURKCE_KURULUM_REHBERI.md",
        ):
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("llm-opencode", text)
                self.assertIn("OPENCODE_CONFIG", text)
                self.assertIn("~/.llm-runtimes/opencode", text)
                self.assertIn("~/.config/opencode", text)


if __name__ == "__main__":
    unittest.main()
