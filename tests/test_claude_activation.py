import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "bin/codex-user-install"
CLAUDE_SOURCE = REPO_ROOT / "variants/claude/home"
IMPORT_LINE = "@registry/CMA_GLOBAL.md"


class ClaudeNativeActivationTests(unittest.TestCase):
    def run_installer(
        self,
        home: Path,
        *extra: str,
        repo_root: Path = REPO_ROOT,
        path: str | None = None,
        umask: int | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = {**os.environ, "HOME": str(home)}
        environment.pop("CLAUDE_CONFIG_DIR", None)
        if path is not None:
            environment["PATH"] = path
        return subprocess.run(
            (str(repo_root / "bin/codex-user-install"), "--variant", "claude", *extra),
            cwd=repo_root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            preexec_fn=(lambda: os.umask(umask)) if umask is not None else None,
        )

    def seed_native_home(self, root: Path) -> tuple[Path, bytes, bytes, int, int]:
        home = root / "home"
        native = home / ".claude"
        native.mkdir(parents=True)
        policy = b"# Existing Claude instructions\n\nKeep this content unchanged.\n"
        settings = b'{"theme":"dark","permissions":{"defaultMode":"default"}}\n'
        (native / "CLAUDE.md").write_bytes(policy)
        (native / "settings.json").write_bytes(settings)
        (native / "CLAUDE.md").chmod(0o640)
        (native / "settings.json").chmod(0o600)
        return home, policy, settings, 0o640, 0o600

    def test_catalog_defaults_claude_to_native_home(self) -> None:
        catalog = (REPO_ROOT / "variants/config.toml").read_text(encoding="utf-8")
        claude_block = catalog.split('id = "claude"', 1)[1]
        self.assertIn('default_home = "~/.claude"', claude_block)
        self.assertNotIn('default_home = "~/.llm-runtimes/claude"', claude_block)

    def test_new_native_runtime_uses_owner_only_permissions_even_with_open_umask(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "home"
            home.mkdir()

            result = self.run_installer(home, umask=0o000)

            self.assertEqual(result.returncode, 0, result.stderr)
            native = home / ".claude"
            for relative in (".", "agents", "skills", "registry", "prompts", "bin", "backups"):
                path = native / relative
                with self.subTest(path=path):
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700)
            for relative in (
                "settings.json",
                "registry/CMA_GLOBAL.md",
                "agents/planner.md",
                "skills/tdd-workflow/SKILL.md",
            ):
                path = native / relative
                with self.subTest(path=path):
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertFalse((native / "CLAUDE.md").exists())
            self.assertEqual(stat.S_IMODE((native / "bin/llm-claude").stat().st_mode), 0o700)

    def test_default_activation_preserves_native_policy_and_generates_merge_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home, policy, settings, policy_mode, settings_mode = self.seed_native_home(root)
            legacy = home / ".llm-runtimes/claude"
            legacy.mkdir(parents=True)
            (legacy / "sentinel").write_text("legacy\n", encoding="utf-8")

            result = self.run_installer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            native = home / ".claude"
            self.assertEqual((native / "settings.json").read_bytes(), settings)
            self.assertEqual(stat.S_IMODE((native / "settings.json").stat().st_mode), settings_mode)
            active_policy = (native / "CLAUDE.md").read_bytes()
            self.assertEqual(active_policy, policy)
            self.assertEqual(active_policy.decode().splitlines().count(IMPORT_LINE), 0)
            self.assertEqual(stat.S_IMODE((native / "CLAUDE.md").stat().st_mode), policy_mode)
            self.assertEqual(
                (native / "registry/CMA_GLOBAL.md").read_bytes(),
                (CLAUDE_SOURCE / "CLAUDE.md").read_bytes(),
            )
            self.assertTrue((native / "agents/planner.md").is_file())
            self.assertTrue((native / "skills/tdd-workflow/SKILL.md").is_file())
            self.assertTrue((native / "prompts/recreate-global-subagents.md").is_file())
            self.assertTrue((native / "bin/llm-claude").stat().st_mode & stat.S_IXUSR)
            snapshots = list(
                (native / "backups/instruction-merge").glob(
                    "instruction-merge-*/CLAUDE.md"
                )
            )
            self.assertEqual(len(snapshots), 1)
            self.assertEqual(snapshots[0].read_bytes(), policy)
            merge_prompt = native / "prompts/merge-existing-instructions.md"
            self.assertTrue(merge_prompt.is_file())
            self.assertNotIn("Keep this content unchanged", merge_prompt.read_text())
            self.assertEqual((legacy / "sentinel").read_text(encoding="utf-8"), "legacy\n")

    def test_activation_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home, _, _, _, _ = self.seed_native_home(Path(temporary))
            first = self.run_installer(home)
            self.assertEqual(first.returncode, 0, first.stderr)
            native = home / ".claude"
            first_snapshot = {
                str(path.relative_to(native)): (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
                for path in native.rglob("*")
                if path.is_file()
            }
            second = self.run_installer(home)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_snapshot = {
                str(path.relative_to(native)): (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
                for path in native.rglob("*")
                if path.is_file()
            }
            self.assertEqual(second_snapshot, first_snapshot)
            self.assertEqual((native / "CLAUDE.md").read_text().splitlines().count(IMPORT_LINE), 0)

    def test_code_reference_is_preserved_without_automatic_import(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home, _, _, _, _ = self.seed_native_home(Path(temporary))
            policy = home / ".claude/CLAUDE.md"
            policy.write_text(
                "# Existing\n\n`@registry/CMA_GLOBAL.md`\n\n```text\n@registry/CMA_GLOBAL.md\n```\n"
                "\n<!--\n@registry/CMA_GLOBAL.md\n-->\n",
                encoding="utf-8",
            )
            result = self.run_installer(home, "--runtime-home", str(home / ".claude"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(policy.read_text().splitlines().count(IMPORT_LINE), 2)
            self.assertFalse(policy.read_text().rstrip().endswith("\n" + IMPORT_LINE))

    def test_force_conflicts_and_differing_managed_files_fail_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home, policy, settings, _, _ = self.seed_native_home(root)
            native = home / ".claude"
            conflicting = native / "agents/planner.md"
            conflicting.parent.mkdir()
            conflicting.write_text("user-owned agent\n", encoding="utf-8")
            before = {path: path.read_bytes() for path in (native / "CLAUDE.md", native / "settings.json", conflicting)}

            conflict = self.run_installer(home, "--runtime-home", str(native))
            forced = self.run_installer(home, "--runtime-home", str(native), "--force")

            self.assertNotEqual(conflict.returncode, 0)
            self.assertNotEqual(forced.returncode, 0)
            self.assertEqual((native / "CLAUDE.md").read_bytes(), policy)
            self.assertEqual((native / "settings.json").read_bytes(), settings)
            for path, content in before.items():
                self.assertEqual(path.read_bytes(), content)
            self.assertFalse((native / "registry/CMA_GLOBAL.md").exists())

    def test_equivalent_native_paths_cannot_bypass_force_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for spelling in ("trailing", "dot", "alias"):
                with self.subTest(spelling=spelling):
                    fixture = root / spelling
                    home, policy, settings, _, _ = self.seed_native_home(fixture)
                    native = home / ".claude"
                    if spelling == "trailing":
                        target = f"{native}/"
                    elif spelling == "dot":
                        target = f"{native}/."
                    else:
                        target_path = fixture / "native-alias"
                        target_path.symlink_to(native, target_is_directory=True)
                        target = str(target_path)

                    result = self.run_installer(home, "--runtime-home", target, "--force")

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("--force is not allowed", result.stderr)
                    self.assertEqual((native / "CLAUDE.md").read_bytes(), policy)
                    self.assertEqual((native / "settings.json").read_bytes(), settings)
                    self.assertFalse((native / "registry/CMA_GLOBAL.md").exists())

    def test_symlinked_native_home_fails_without_outside_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            home.mkdir()
            outside = root / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel"
            sentinel.write_text("safe\n", encoding="utf-8")
            (home / ".claude").symlink_to(outside, target_is_directory=True)

            result = self.run_installer(home)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "safe\n")
            self.assertEqual(sorted(path.name for path in outside.iterdir()), ["sentinel"])

    def test_incomplete_source_manifest_fails_before_native_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copied_repo = root / "repo"
            shutil.copytree(
                REPO_ROOT,
                copied_repo,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".graphify"),
            )
            (copied_repo / "variants/claude/home/agents/planner.md").unlink()
            home, policy, settings, _, _ = self.seed_native_home(root / "fixture")

            result = self.run_installer(home, repo_root=copied_repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((home / ".claude/CLAUDE.md").read_bytes(), policy)
            self.assertEqual((home / ".claude/settings.json").read_bytes(), settings)
            self.assertFalse((home / ".claude/registry/CMA_GLOBAL.md").exists())

    def test_late_copy_failure_does_not_leave_partial_activation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for failure in ("late",):
                with self.subTest(failure=failure):
                    fixture = root / failure
                    home, policy, settings, _, _ = self.seed_native_home(fixture)
                    shim_dir = fixture / "shim"
                    shim_dir.mkdir()
                    shim = shim_dir / "cp"
                    shim.write_text(
                        "#!/usr/bin/env bash\n"
                        'for argument in "$@"; do case "$argument" in */agents/planner.md) exit 73 ;; esac; done\n'
                        'exec /bin/cp "$@"\n',
                        encoding="utf-8",
                    )
                    shim.chmod(0o755)

                    result = self.run_installer(
                        home,
                        "--runtime-home",
                        str(home / ".claude"),
                        path=f"{shim_dir}:{os.environ['PATH']}",
                    )

                    native = home / ".claude"
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual((native / "CLAUDE.md").read_bytes(), policy)
                    self.assertEqual((native / "settings.json").read_bytes(), settings)
                    self.assertFalse((native / "registry/CMA_GLOBAL.md").exists())
                    self.assertFalse((native / "agents/planner.md").exists())


if __name__ == "__main__":
    unittest.main()
