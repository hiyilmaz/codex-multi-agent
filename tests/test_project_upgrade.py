import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_INIT = REPO_ROOT / "bin/codex-project-init"
PROJECT_UPGRADE = REPO_ROOT / "bin/codex-project-upgrade"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ProjectUpgradeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.environment = {**os.environ, "HOME": str(self.home)}

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_command(
        self, *command: str | Path, input_text: str | None = None, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(part) for part in command],
            cwd=REPO_ROOT,
            env=self.environment,
            input=input_text,
            text=True,
            capture_output=True,
            check=check,
        )

    def initialize(self, name: str, variant: str = "codex") -> Path:
        project = self.root / name
        project.mkdir()
        self.run_command(
            PROJECT_INIT, "--variant", variant, project, input_text="y\n"
        )
        return project

    def assert_evidence_mode_prompt_contract(self, text: str) -> None:
        required = (
            "`EVIDENCE_MODE` must be exactly `enable` or `disable`.",
            "Use `disable` when the field is missing or no explicit choice is provided.",
            "If an explicit value is invalid, report it and do not treat evidence automation as enabled.",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_fresh_project_defaults_evidence_mode_and_installs_validation_guidance(
        self,
    ) -> None:
        project = self.initialize("evidence-mode")
        agents = (project / "AGENTS.md").read_text(encoding="utf-8")
        prompt = (
            project / ".codex/prompts/fill-project-configuration.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(agents.count("EVIDENCE_MODE: disable"), 1)
        self.assert_evidence_mode_prompt_contract(prompt)

    def test_evidence_mode_prompt_rejects_allowed_values_only_policy(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_evidence_mode_prompt_contract(
                "`EVIDENCE_MODE` must be exactly `enable` or `disable`."
            )

    def test_fresh_project_records_state_and_is_idempotent(self) -> None:
        project = self.initialize("fresh", "dolphin")
        state = json.loads((project / ".codex/template-state.json").read_text())

        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(state["variant"], "dolphin")
        self.assertEqual(state["files"]["AGENTS.md"]["mode"], "merge")
        self.assertEqual(
            state["files"][".codex/config.toml"]["mode"], "managed"
        )

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("AGENTS.md: UNCHANGED", result.stdout)
        self.assertIn(".codex/template-state.json: UNCHANGED", result.stdout)

    def test_claude_init_creates_minimal_bridge_and_state(self) -> None:
        project = self.initialize("claude-project", "claude")
        bridge = (project / "CLAUDE.md").read_text(encoding="utf-8")
        settings = json.loads((project / ".claude/settings.json").read_text())
        state = json.loads((project / ".codex/template-state.json").read_text())

        self.assertEqual(bridge.strip(), "@AGENTS.md")
        self.assertEqual(settings, {"permissions": {"defaultMode": "default"}})
        self.assertEqual(state["variant"], "claude")
        self.assertEqual(state["files"]["CLAUDE.md"]["mode"], "managed")
        self.assertEqual(state["files"][".claude/settings.json"]["mode"], "managed")

    def test_customized_claude_bridge_is_preserved_by_upgrade(self) -> None:
        project = self.initialize("custom-claude", "claude")
        bridge = project / "CLAUDE.md"
        bridge.write_text("@AGENTS.md\n\n# Local Claude guidance\n", encoding="utf-8")
        before = sha256(bridge)

        preview = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("CLAUDE.md: PRESERVE_CUSTOMIZED", preview.stdout)
        self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)
        self.assertEqual(sha256(bridge), before)

    def test_claude_upgrade_dry_run_is_non_mutating(self) -> None:
        project = self.initialize("claude-dry-run", "claude")
        sentinel = project / ".claude/agents/local.md"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text("local agent\n", encoding="utf-8")
        before = {
            path.relative_to(project).as_posix(): sha256(path)
            for path in project.rglob("*")
            if path.is_file()
        }

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        after = {
            path.relative_to(project).as_posix(): sha256(path)
            for path in project.rglob("*")
            if path.is_file()
        }
        self.assertIn("Dry run only. No files changed.", result.stdout)
        self.assertEqual(after, before)

    def test_claude_init_archives_existing_claude_files_after_confirmation(self) -> None:
        project = self.root / "existing-claude"
        settings = project / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        (project / "CLAUDE.md").write_text("local bridge\n", encoding="utf-8")
        settings.write_text('{"local": true}\n', encoding="utf-8")

        result = self.run_command(
            PROJECT_INIT, "--variant", "claude", project, input_text="y\n"
        )
        self.assertIn("CLAUDE.md", result.stdout)
        archives = list((project / ".codex/archive").glob("init-*/CLAUDE.md"))
        archived_settings = list(
            (project / ".codex/archive").glob("init-*/.claude/settings.json")
        )
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_text(), "local bridge\n")
        self.assertEqual(len(archived_settings), 1)
        self.assertEqual(archived_settings[0].read_text(), '{"local": true}\n')

    def test_claude_init_rejects_symlinked_claude_directory(self) -> None:
        project = self.root / "symlink-init"
        project.mkdir()
        outside = self.root / "outside-init"
        outside.mkdir()
        settings = outside / "settings.json"
        settings.write_text('{"outside": true}\n', encoding="utf-8")
        (project / ".claude").symlink_to(outside, target_is_directory=True)

        result = self.run_command(
            PROJECT_INIT, "--variant", "claude", project, input_text="y\n", check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(settings.read_text(), '{"outside": true}\n')

    def test_init_rejects_symlinked_codex_directory_before_mutation(self) -> None:
        project = self.root / "symlink-codex-init"
        project.mkdir()
        outside = self.root / "outside-codex-init"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_text("outside\n", encoding="utf-8")
        (project / ".codex").symlink_to(outside, target_is_directory=True)

        result = self.run_command(
            PROJECT_INIT, project, input_text="y\n", check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertNotIn("Continue?", result.stdout)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside\n")
        self.assertEqual(list(outside.iterdir()), [sentinel])

    def test_claude_init_rejects_file_directory_before_mutation(self) -> None:
        project = self.root / "file-claude-init"
        project.mkdir()
        claude_path = project / ".claude"
        claude_path.write_text("local file\n", encoding="utf-8")

        result = self.run_command(
            PROJECT_INIT, "--variant", "claude", project,
            input_text="y\n", check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory", result.stderr)
        self.assertNotIn("Continue?", result.stdout)
        self.assertEqual(claude_path.read_text(encoding="utf-8"), "local file\n")
        self.assertFalse((project / "AGENTS.md").exists())
        self.assertFalse((project / ".codex").exists())

    def test_claude_upgrade_rejects_symlinked_claude_directory(self) -> None:
        project = self.initialize("symlink-upgrade", "claude")
        shutil.rmtree(project / ".claude")
        outside = self.root / "outside-upgrade"
        outside.mkdir()
        settings = outside / "settings.json"
        settings.write_text('{"outside": true}\n', encoding="utf-8")
        (project / ".claude").symlink_to(outside, target_is_directory=True)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(settings.read_text(), '{"outside": true}\n')

    def test_upgrade_rejects_symlinked_codex_directory(self) -> None:
        project = self.initialize("symlink-codex-upgrade")
        outside = self.root / "outside-codex-upgrade"
        (project / ".codex").rename(outside)
        (project / ".codex").symlink_to(outside, target_is_directory=True)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)

    def test_upgrade_rejects_symlinked_archive_before_mutation(self) -> None:
        project = self.initialize("symlink-archive-upgrade")
        archive = project / ".codex/archive"
        shutil.rmtree(archive)
        outside = self.root / "outside-archive-upgrade"
        outside.mkdir()
        archive.symlink_to(outside, target_is_directory=True)
        agents = project / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "ORCHESTRATION_MODE: ask-approval\n", ""
            ),
            encoding="utf-8",
        )
        before = agents.read_bytes()

        result = self.run_command(
            PROJECT_UPGRADE, "--apply", "--force", project, check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(agents.read_bytes(), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_claude_upgrade_rejects_file_directory(self) -> None:
        project = self.initialize("file-claude-upgrade", "claude")
        shutil.rmtree(project / ".claude")
        (project / ".claude").write_text("local file\n", encoding="utf-8")

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory", result.stderr)

    def test_legacy_project_preserves_local_files(self) -> None:
        project = self.root / "legacy"
        prompt = project / ".codex/prompts/fill-project-configuration.md"
        config = project / ".codex/config.toml"
        prompt.parent.mkdir(parents=True)
        shutil.copy2(REPO_ROOT / "PROJECT_AGENTS_TEMPLATE.md", project / "AGENTS.md")
        shutil.copy2(REPO_ROOT / "PROJECT_CONFIG_PROMPT.md", prompt)
        shutil.copy2(REPO_ROOT / "CODEX_CONFIG_EXAMPLE.toml", config)

        agents = (project / "AGENTS.md").read_text().replace(
            "\n  - tdd-workflow", ""
        )
        (project / "AGENTS.md").write_text(agents)
        prompt.write_text(prompt.read_text() + "\nLocal prompt extension.\n")
        config.write_text(config.read_text() + "\n# local config extension\n")
        prompt_hash = sha256(prompt)
        config_hash = sha256(config)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("State: legacy-safe bootstrap", result.stdout)
        self.assertIn("PRESERVE_LEGACY", result.stdout)
        self.assertFalse((project / ".codex/template-state.json").exists())

        self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)
        self.assertEqual(sha256(prompt), prompt_hash)
        self.assertEqual(sha256(config), config_hash)
        self.assertIn("  - tdd-workflow", (project / "AGENTS.md").read_text())

        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(
            state["files"][".codex/config.toml"]["mode"], "project"
        )
        self.assertEqual(
            state["files"][".codex/prompts/fill-project-configuration.md"][
                "mode"
            ],
            "project",
        )

    def test_customized_managed_file_is_preserved(self) -> None:
        project = self.initialize("custom")
        prompt = project / ".codex/prompts/fill-project-configuration.md"
        prompt.write_text(prompt.read_text() + "\nLocal prompt extension.\n")
        prompt_hash = sha256(prompt)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("PRESERVE_CUSTOMIZED", result.stdout)
        self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)
        self.assertEqual(sha256(prompt), prompt_hash)

        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(
            state["files"][".codex/prompts/fill-project-configuration.md"][
                "mode"
            ],
            "project",
        )

    def test_unchanged_managed_file_receives_update_and_is_archived(self) -> None:
        project = self.initialize("managed")
        prompt = project / ".codex/prompts/fill-project-configuration.md"
        state_path = project / ".codex/template-state.json"
        prompt.write_text("# simulated older managed prompt\n")
        prompt.chmod(0o640)

        state = json.loads(state_path.read_text())
        state["files"][".codex/prompts/fill-project-configuration.md"][
            "template_sha256"
        ] = sha256(prompt)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("fill-project-configuration.md: UPDATE", result.stdout)
        self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)

        self.assertEqual(
            prompt.read_text(), (REPO_ROOT / "PROJECT_CONFIG_PROMPT.md").read_text()
        )
        self.assertEqual(prompt.stat().st_mode & 0o777, 0o640)
        archived = list(
            (project / ".codex/archive").glob(
                "upgrade-*/.codex/prompts/fill-project-configuration.md"
            )
        )
        self.assertEqual(len(archived), 1)


if __name__ == "__main__":
    unittest.main()
