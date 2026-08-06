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
