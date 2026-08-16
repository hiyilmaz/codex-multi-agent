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

    def catalog_variants(self) -> list[str]:
        return [
            line.split('"', 2)[1]
            for line in (REPO_ROOT / "variants/config.toml").read_text(
                encoding="utf-8"
            ).splitlines()
            if line.startswith("id = ")
        ]

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

    def test_dolphin_project_init_is_rejected_without_creating_state(self) -> None:
        project = self.root / "fresh"
        project.mkdir()
        result = self.run_command(
            PROJECT_INIT, "--variant", "dolphin", project, input_text="y\n", check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((project / ".codex/template-state.json").exists())

    def test_interactive_init_all_models_creates_every_catalog_surface(self) -> None:
        project = self.root / "all-models"
        project.mkdir()

        result = self.run_command(PROJECT_INIT, project, input_text="y\ny\n")

        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["variants"], self.catalog_variants())
        self.assertTrue((project / ".codex/config.toml").is_file())
        self.assertTrue((project / "CLAUDE.md").is_file())
        self.assertTrue((project / ".claude/settings.json").is_file())
        self.assertTrue((project / ".opencode/opencode.json").is_file())
        self.assertNotIn("codex kurulsun mu?", result.stdout + result.stderr)

    def test_interactive_init_individual_models_creates_selected_subset(self) -> None:
        project = self.root / "selected-models"
        project.mkdir()

        result = self.run_command(
            PROJECT_INIT, project, input_text="n\ny\nn\ny\ny\n"
        )

        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["variants"], ["codex", "opencode"])
        self.assertTrue((project / ".codex/config.toml").is_file())
        self.assertTrue((project / ".opencode/opencode.json").is_file())
        self.assertFalse((project / "CLAUDE.md").exists())
        self.assertFalse((project / ".claude/settings.json").exists())
        prompts = result.stdout + result.stderr
        for variant in self.catalog_variants():
            self.assertEqual(prompts.count(f"{variant} kurulsun mu?"), 1)

    def test_interactive_all_models_adds_variants_without_replacing_shared_files(
        self,
    ) -> None:
        project = self.initialize("add-all-interactive")
        agents = project / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nLocal sentinel.\n")
        shared_hash = sha256(agents)
        archives = sorted((project / ".codex/archive").glob("init-*"))

        self.run_command(PROJECT_INIT, project, input_text="y\ny\n")

        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["variants"], self.catalog_variants())
        self.assertEqual(sha256(agents), shared_hash)
        self.assertEqual(sorted((project / ".codex/archive").glob("init-*")), archives)

    def test_claude_init_creates_minimal_bridge_and_state(self) -> None:
        project = self.initialize("claude-project", "claude")
        bridge = (project / "CLAUDE.md").read_text(encoding="utf-8")
        settings = json.loads((project / ".claude/settings.json").read_text())
        state = json.loads((project / ".codex/template-state.json").read_text())

        self.assertEqual(bridge.strip(), "@AGENTS.md")
        self.assertEqual(settings, {"permissions": {"defaultMode": "default"}})
        self.assertEqual(state["variants"], ["claude"])
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

    def test_upgrade_dry_run_rejects_symlinked_managed_parent(self) -> None:
        project = self.initialize("symlink-prompts-dry-run")
        prompts = project / ".codex/prompts"
        outside = self.root / "outside-prompts-dry-run"
        prompts.rename(outside)
        prompts.symlink_to(outside, target_is_directory=True)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)

    def test_upgrade_apply_rejects_symlinked_managed_parent(self) -> None:
        project = self.initialize("symlink-prompts-apply")
        prompts = project / ".codex/prompts"
        outside = self.root / "outside-prompts-apply"
        prompts.rename(outside)
        prompts.symlink_to(outside, target_is_directory=True)
        prompt = outside / "fill-project-configuration.md"
        prompt.write_text("# simulated managed prompt\n", encoding="utf-8")
        state_path = project / ".codex/template-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["files"][".codex/prompts/fill-project-configuration.md"][
            "template_sha256"
        ] = sha256(prompt)
        state_path.write_text(
            json.dumps(state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        before = prompt.read_bytes()

        result = self.run_command(
            PROJECT_UPGRADE, "--apply", "--force", project, check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(prompt.read_bytes(), before)

    def test_record_initial_state_rejects_symlinked_managed_parent(self) -> None:
        project = self.root / "symlink-prompts-record"
        prompts = project / ".codex/prompts"
        outside = self.root / "outside-prompts-record"
        outside.mkdir()
        project.joinpath(".codex").mkdir(parents=True)
        prompts.symlink_to(outside, target_is_directory=True)
        shutil.copy2(REPO_ROOT / "PROJECT_AGENTS_TEMPLATE.md", project / "AGENTS.md")
        shutil.copy2(
            REPO_ROOT / "CODEX_CONFIG_EXAMPLE.toml",
            project / ".codex/config.toml",
        )
        shutil.copy2(
            REPO_ROOT / "PROJECT_CONFIG_PROMPT.md",
            outside / "fill-project-configuration.md",
        )

        result = self.run_command(
            PROJECT_UPGRADE,
            "--record-initial-state",
            "--variant",
            "codex",
            project,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertFalse((project / ".codex/template-state.json").exists())

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

    def test_opencode_init_preserves_siblings_and_manages_project_config(self) -> None:
        project = self.root / "opencode-init"
        plugins = project / ".opencode/plugins"
        plugins.mkdir(parents=True)
        plugin = plugins / "local.js"
        plugin.write_text("export default {}\n", encoding="utf-8")

        self.run_command(
            PROJECT_INIT, "--variant", "opencode", project, input_text="y\n"
        )

        self.assertEqual(plugin.read_text(encoding="utf-8"), "export default {}\n")
        self.assertTrue((project / ".opencode/opencode.json").is_file())
        self.assertFalse((project / ".codex/config.toml").exists())
        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["variants"], ["opencode"])
        self.assertEqual(state["files"][".opencode/opencode.json"]["mode"], "managed")

    def test_existing_project_init_adds_all_variants_without_resetting_shared_files(
        self,
    ) -> None:
        project = self.initialize("multi-variant", "codex")
        initial_archives = sorted((project / ".codex/archive").glob("init-*"))
        agents = project / "AGENTS.md"
        config = project / ".codex/config.toml"
        prompt = project / ".codex/prompts/fill-project-configuration.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + "\nProject-specific instruction.\n",
            encoding="utf-8",
        )
        shared_hashes = {
            "AGENTS.md": sha256(agents),
            ".codex/config.toml": sha256(config),
            ".codex/prompts/fill-project-configuration.md": sha256(prompt),
        }

        for variant in ("claude", "opencode"):
            result = self.run_command(
                PROJECT_INIT, "--variant", variant, project, input_text="y\n"
            )
            self.assertIn("variant", result.stdout.lower())

        self.assertEqual(sha256(agents), shared_hashes["AGENTS.md"])
        self.assertEqual(sha256(config), shared_hashes[".codex/config.toml"])
        self.assertEqual(
            sha256(prompt),
            shared_hashes[".codex/prompts/fill-project-configuration.md"],
        )
        self.assertTrue((project / "CLAUDE.md").is_file())
        self.assertTrue((project / ".claude/settings.json").is_file())
        self.assertTrue((project / ".opencode/opencode.json").is_file())
        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["schema_version"], 2)
        self.assertEqual(
            state["variants"], ["codex", "claude", "opencode"]
        )
        self.assertIn(".codex/config.toml", state["files"])
        self.assertIn(".claude/settings.json", state["files"])
        self.assertIn(".opencode/opencode.json", state["files"])
        self.assertEqual(
            sorted((project / ".codex/archive").glob("init-*")), initial_archives
        )

    def test_additive_init_migrates_schema_one_manifest(self) -> None:
        project = self.initialize("schema-one-migration", "codex")
        state_path = project / ".codex/template-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["schema_version"] = 1
        state["variant"] = "codex"
        state.pop("variants", None)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        agents_hash = sha256(project / "AGENTS.md")
        config_hash = sha256(project / ".codex/config.toml")

        self.run_command(
            PROJECT_INIT, "--variant", "opencode", project, input_text="y\n"
        )

        migrated = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(migrated["variants"], ["codex", "opencode"])
        self.assertNotIn("variant", migrated)
        self.assertEqual(sha256(project / "AGENTS.md"), agents_hash)
        self.assertEqual(sha256(project / ".codex/config.toml"), config_hash)
        self.assertTrue((project / ".opencode/opencode.json").is_file())

    def test_upgrade_migrates_schema_one_without_adding_a_variant(self) -> None:
        project = self.initialize("schema-one-upgrade", "codex")
        state_path = project / ".codex/template-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["schema_version"] = 1
        state["variant"] = "codex"
        state.pop("variants", None)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

        result = self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)

        self.assertIn(".codex/template-state.json: UPDATE", result.stdout)
        migrated = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(migrated["variants"], ["codex"])
        self.assertNotIn("variant", migrated)

    def test_additive_init_preserves_customized_variant_config(self) -> None:
        project = self.initialize("customized-multi-variant", "opencode")
        opencode_config = project / ".opencode/opencode.json"
        opencode_config.write_text(
            '{"$schema":"https://opencode.ai/config.json","theme":"local"}\n',
            encoding="utf-8",
        )
        config_hash = sha256(opencode_config)

        self.run_command(
            PROJECT_INIT, "--variant", "codex", project, input_text="y\n"
        )
        self.run_command(
            PROJECT_INIT, "--variant", "opencode", project, input_text="y\n"
        )

        self.assertEqual(sha256(opencode_config), config_hash)
        self.assertTrue((project / ".codex/config.toml").is_file())
        state = json.loads((project / ".codex/template-state.json").read_text())
        self.assertEqual(state["variants"], ["codex", "opencode"])
        self.assertEqual(state["files"][".opencode/opencode.json"]["mode"], "project")

    def test_existing_project_requires_explicit_reset_to_replace_agents(self) -> None:
        project = self.initialize("explicit-reset", "codex")
        initial_archives = sorted((project / ".codex/archive").glob("init-*"))
        agents = project / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + "\nReset sentinel.\n",
            encoding="utf-8",
        )
        sentinel_hash = sha256(agents)

        self.run_command(
            PROJECT_INIT, "--variant", "opencode", project, input_text="y\n"
        )
        self.assertEqual(sha256(agents), sentinel_hash)

        self.run_command(
            PROJECT_INIT,
            "--reset",
            "--variant",
            "opencode",
            project,
            input_text="y\n",
        )

        self.assertNotEqual(sha256(agents), sentinel_hash)
        archives = sorted((project / ".codex/archive").glob("init-*"))
        new_archives = [archive for archive in archives if archive not in initial_archives]
        self.assertEqual(len(new_archives), 1)
        self.assertEqual(new_archives[0].stat().st_mode & 0o777, 0o700)
        self.assertEqual(sha256(new_archives[0] / "AGENTS.md"), sentinel_hash)

    def test_repeated_explicit_resets_use_distinct_private_archives(self) -> None:
        project = self.initialize("repeated-reset", "codex")
        initial_archives = sorted((project / ".codex/archive").glob("init-*"))
        agents = project / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + "\nFirst reset sentinel.\n",
            encoding="utf-8",
        )
        sentinel_hash = sha256(agents)

        self.run_command(
            PROJECT_INIT,
            "--reset",
            "--variant",
            "codex",
            project,
            input_text="y\n",
        )
        self.run_command(
            PROJECT_INIT,
            "--reset",
            "--variant",
            "codex",
            project,
            input_text="y\n",
        )

        archives = sorted((project / ".codex/archive").glob("init-*"))
        new_archives = [archive for archive in archives if archive not in initial_archives]
        self.assertEqual(len(new_archives), 2)
        self.assertNotEqual(new_archives[0], new_archives[1])
        self.assertEqual(new_archives[0].stat().st_mode & 0o777, 0o700)
        self.assertEqual(new_archives[1].stat().st_mode & 0o777, 0o700)
        self.assertEqual(sha256(new_archives[0] / "AGENTS.md"), sentinel_hash)

    def test_guides_define_additive_multi_variant_init_and_explicit_reset(self) -> None:
        for relative in ("README.md", "USAGE_GUIDE.md", "COMMAND_REFERENCE.md"):
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            normalized = " ".join(text.split())
            with self.subTest(path=relative):
                self.assertIn("additive", normalized.lower())
                self.assertIn("multiple runtime variants", normalized.lower())
                self.assertIn("--reset", normalized)
                self.assertIn("preserves `AGENTS.md`", normalized)

        turkish = (REPO_ROOT / "TURKCE_KURULUM_REHBERI.md").read_text(
            encoding="utf-8"
        )
        turkish = " ".join(turkish.split())
        self.assertIn("eklemeli", turkish.lower())
        self.assertIn("birden fazla runtime varyantı", turkish.lower())
        self.assertIn("--reset", turkish)
        self.assertIn("`AGENTS.md` dosyasını korur", turkish)

    def test_opencode_customized_config_is_preserved(self) -> None:
        project = self.initialize("opencode-custom", "opencode")
        config = project / ".opencode/opencode.json"
        config.write_text('{"$schema":"https://opencode.ai/config.json","theme":"local"}\n')
        before = sha256(config)

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("PRESERVE_CUSTOMIZED", result.stdout)
        self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)
        self.assertEqual(sha256(config), before)

    def test_opencode_customized_config_secrets_are_omitted_from_summaries(self) -> None:
        project = self.initialize("opencode-secret", "opencode")
        config = project / ".opencode/opencode.json"
        secret = "TEST_SECRET_MUST_NOT_APPEAR"
        config.write_text(
            json.dumps(
                {
                    "$schema": "https://opencode.ai/config.json",
                    "provider": {"example": {"options": {"apiKey": secret}}},
                }
            )
            + "\n"
        )

        dry_run = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn("PRESERVE_CUSTOMIZED", dry_run.stdout)
        self.assertIn("Content diff omitted", dry_run.stdout)
        self.assertNotIn(secret, dry_run.stdout)

        applied = self.run_command(
            PROJECT_UPGRADE, "--apply", "--force", project
        )
        self.assertNotIn(secret, applied.stdout)
        summaries = list(
            (project / ".codex/archive").glob("upgrade-*/UPGRADE_SUMMARY.md")
        )
        self.assertEqual(len(summaries), 1)
        self.assertNotIn(secret, summaries[0].read_text(encoding="utf-8"))
        self.assertEqual(summaries[0].stat().st_mode & 0o777, 0o600)
        self.assertIn(secret, config.read_text(encoding="utf-8"))

    def test_opencode_init_rejects_symlinked_config_directory(self) -> None:
        project = self.root / "opencode-symlink"
        outside = self.root / "outside-opencode"
        project.mkdir()
        outside.mkdir()
        (project / ".opencode").symlink_to(outside, target_is_directory=True)

        result = self.run_command(
            PROJECT_INIT,
            "--variant",
            "opencode",
            project,
            input_text="y\n",
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertFalse((project / "AGENTS.md").exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_opencode_init_archives_secret_config_under_private_directory(self) -> None:
        project = self.root / "opencode-secret-init"
        config = project / ".opencode/opencode.json"
        config.parent.mkdir(parents=True)
        secret = "INIT_SECRET_MUST_NOT_APPEAR"
        config.write_text(
            json.dumps({"provider": {"example": {"apiKey": secret}}}) + "\n"
        )
        config.chmod(0o644)

        result = self.run_command(
            PROJECT_INIT, "--variant", "opencode", project, input_text="y\n"
        )

        self.assertNotIn(secret, result.stdout)
        archives = list((project / ".codex/archive").glob("init-*"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].stat().st_mode & 0o777, 0o700)
        archived = archives[0] / ".opencode/opencode.json"
        self.assertIn(secret, archived.read_text(encoding="utf-8"))

    def test_opencode_unchanged_config_updates_and_archives(self) -> None:
        project = self.initialize("opencode-managed", "opencode")
        config = project / ".opencode/opencode.json"
        state_path = project / ".codex/template-state.json"
        secret = "MANAGED_SECRET_MUST_NOT_APPEAR"
        config.write_text(
            '{"$schema":"https://opencode.ai/config.json","old":true,'
            f'"apiKey":"{secret}"}}\n'
        )
        config.chmod(0o640)
        state = json.loads(state_path.read_text())
        state["files"][".opencode/opencode.json"]["template_sha256"] = sha256(config)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

        result = self.run_command(PROJECT_UPGRADE, "--dry-run", project)
        self.assertIn(".opencode/opencode.json: UPDATE", result.stdout)
        self.assertIn("Content diff omitted", result.stdout)
        self.assertNotIn(secret, result.stdout)
        applied = self.run_command(PROJECT_UPGRADE, "--apply", "--force", project)
        self.assertNotIn(secret, applied.stdout)

        self.assertEqual(
            config.read_bytes(),
            (REPO_ROOT / "OPENCODE_PROJECT_CONFIG_EXAMPLE.json").read_bytes(),
        )
        self.assertEqual(config.stat().st_mode & 0o777, 0o640)
        archived = list(
            (project / ".codex/archive").glob(
                "upgrade-*/.opencode/opencode.json"
            )
        )
        self.assertEqual(len(archived), 1)
        self.assertIn(secret, archived[0].read_text(encoding="utf-8"))
        summary = archived[0].parents[1] / "UPGRADE_SUMMARY.md"
        self.assertNotIn(secret, summary.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
