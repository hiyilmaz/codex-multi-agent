import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_HOME = REPO_ROOT / "variants/claude/home"
LAUNCHER = REPO_ROOT / "variants/claude/bin/claude"
INSTALLER = REPO_ROOT / "bin/codex-user-install"
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
ROLES = ("planner", "tdd-guide", "code-reviewer", "security-reviewer")


class ClaudeRuntimeTests(unittest.TestCase):
    def test_claude_source_layout_is_portable(self) -> None:
        self.assertTrue((CLAUDE_HOME / "CLAUDE.md").is_file())
        self.assertTrue((CLAUDE_HOME / "settings.json").is_file())
        self.assertTrue((CLAUDE_HOME / "README.md").is_file())
        self.assertTrue(LAUNCHER.is_file())
        for role in ROLES:
            self.assertTrue((CLAUDE_HOME / "agents" / f"{role}.md").is_file())
        for skill in ("orchestration-gate", "tdd-workflow", "hypothesis-workflow", "record-archive"):
            self.assertTrue((CLAUDE_HOME / "skills" / skill / "SKILL.md").is_file())

    def test_installed_claude_matches_source_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for source in CLAUDE_HOME.rglob("*"):
                if source.is_file():
                    target = runtime / source.relative_to(CLAUDE_HOME)
                    self.assertTrue(target.is_file(), target)
                    self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertTrue((runtime / "bin/llm-claude").stat().st_mode & stat.S_IXUSR)

    def test_claude_policy_preserves_truthful_success_and_exact_chain(self) -> None:
        policy = (CLAUDE_HOME / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn(CHAIN, policy)
        self.assertIn("Do not skip", policy)
        for marker in ("Truthful Success Reporting", "success=true", "success=false", "No evidence means no success"):
            self.assertIn(marker, policy)

    def test_claude_agents_are_markdown_frontmatter_and_distinct(self) -> None:
        bodies = []
        for role in ROLES:
            text = (CLAUDE_HOME / "agents" / f"{role}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {role}", text)
            self.assertIn("tools:", text)
            self.assertNotIn("model_reasoning_effort", text)
            bodies.append(text)
        self.assertEqual(len(set(bodies)), len(ROLES))

    def test_settings_json_is_minimal_and_safe(self) -> None:
        settings = json.loads((CLAUDE_HOME / "settings.json").read_text(encoding="utf-8"))
        serialized = json.dumps(settings).lower()
        self.assertNotIn("bypasspermissions", serialized)
        self.assertNotIn("apikey", serialized)
        self.assertNotIn("hook", serialized)
        self.assertEqual(settings, {"permissions": {"defaultMode": "default"}})

    def test_source_excludes_runtime_and_secret_artifacts(self) -> None:
        forbidden = {"credentials.json", ".credentials.json", "history.jsonl", "stats-cache.json", "session-env"}
        present = {path.name for path in (REPO_ROOT / "variants/claude").rglob("*")}
        self.assertTrue(forbidden.isdisjoint(present))

    def test_launcher_forwards_args_sets_home_and_propagates_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            binary_dir = root / "bin"
            runtime_bin = runtime / "bin"
            binary_dir.mkdir()
            runtime_bin.mkdir(parents=True)
            installed = runtime_bin / "llm-claude"
            installed.write_bytes(LAUNCHER.read_bytes())
            installed.chmod(0o755)
            native = binary_dir / "claude"
            native.write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' \"$CLAUDE_CONFIG_DIR\"\nprintf '<%s>\\n' \"$@\"\nexit 7\n",
                encoding="utf-8",
            )
            native.chmod(0o755)
            environment = {
                **os.environ,
                "PATH": f"{binary_dir}:/usr/bin:/bin",
                "CLAUDE_CONFIG_DIR": "/hostile/inherited/path",
            }
            result = subprocess.run(
                (str(installed), "--model", "test model"),
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.stdout.splitlines()[0], str(runtime))
            self.assertIn("<--model>", result.stdout)
            self.assertIn("<test model>", result.stdout)
            self.assertNotIn("hostile", result.stdout + result.stderr)

    def test_launcher_missing_native_binary_fails_clearly(self) -> None:
        result = subprocess.run(
            ("/bin/bash", str(LAUNCHER)),
            env={"PATH": "/usr/bin:/bin"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("native claude", result.stderr.lower())

    def test_launcher_has_valid_bash_syntax_and_executable_mode(self) -> None:
        result = subprocess.run(("/bin/bash", "-n", str(LAUNCHER)), capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(LAUNCHER.stat().st_mode & stat.S_IXUSR)


if __name__ == "__main__":
    unittest.main()
