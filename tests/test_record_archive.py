import importlib.util
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from datetime import date, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "record-archive"
SCRIPT_RELATIVE = (
    Path("variants")
    / "codex"
    / "home"
    / "skills"
    / SKILL_NAME
    / "scripts"
    / "record_archive.py"
)


def load_archive_module():
    module_name = "record_archive_under_test"
    spec = importlib.util.spec_from_file_location(
        module_name,
        REPO_ROOT / SCRIPT_RELATIVE,
    )
    if spec is None or spec.loader is None:
        raise AssertionError("record archive module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def deferred_item(identifier: str, completed: bool) -> str:
    fixed = "  Fixed At: 2026-07-27 01:00\n" if completed else ""
    return (
        f"- ID: {identifier}\n"
        "  Type: TODO\n"
        "  Discovered At: 2026-07-27 00:00\n"
        f"{fixed}"
        "  Source Task: archive test\n"
        "  Location: docs/test.md\n"
        "  Summary: test record\n"
        + ("  Fix Summary: completed\n" if completed else "")
        + "  Evidence: fixture\n"
    )


def experiment(identifier: str, status: str) -> str:
    decision = {
        "ACCEPTED": "ACCEPT",
        "REJECTED": "REJECT",
        "ROLLED_BACK": "ROLLBACK",
    }.get(status, "NEED_MORE_DATA")
    return (
        f"## {identifier} - Fixture\n\n"
        "Date: 2026-07-27\n"
        f"Status: {status}\n\n"
        "Problem:\nFixture.\n\n"
        "Evidence:\nFixture.\n\n"
        "Hypothesis:\nFixture.\n\n"
        "Solution Attempt:\nFixture.\n\n"
        "Test:\nFixture.\n\n"
        "Success Criteria:\nFixture.\n\n"
        "Result:\nFixture.\n\n"
        f"Decision:\n{decision}\n\n"
        "Notes:\nFixture.\n"
    )


class RecordArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "docs").mkdir()
        (self.root / "governance").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_tool(
        self,
        action: str,
        record: str,
        *extra: str,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_tool_at(self.root, action, record, *extra)

    def run_tool_at(
        self,
        root: Path,
        action: str,
        record: str,
        *extra: str,
    ) -> subprocess.CompletedProcess[str]:
        runner = ("python3",)
        if os.environ.get("RECORD_ARCHIVE_COVERAGE") == "1":
            runner = (
                "python3",
                "-m",
                "coverage",
                "run",
                "--append",
                f"--source={REPO_ROOT / SCRIPT_RELATIVE.parent}",
            )
        return subprocess.run(
            (
                *runner,
                str(REPO_ROOT / SCRIPT_RELATIVE),
                action,
                "--root",
                str(root),
                "--record",
                record,
                *extra,
            ),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_deferred(self, completed_count: int, pending_count: int = 1) -> None:
        pending = "\n".join(
            deferred_item(f"DF-20260727-0000-{index:03d}", False)
            for index in range(1, pending_count + 1)
        )
        completed = "\n".join(
            deferred_item(f"DF-20260727-0100-{index:03d}", True)
            for index in range(1, completed_count + 1)
        )
        (self.root / "docs/DEFERRED_FINDINGS.md").write_text(
            "# Deferred Findings\n\n"
            "## Pending\n\n"
            f"{pending}\n"
            "## Completed\n\n"
            f"{completed}",
            encoding="utf-8",
        )

    def write_experiments(self, terminal_count: int, open_count: int = 1) -> None:
        entries = [
            experiment(f"EXP-20260727-{index:03d}", "ACCEPTED")
            for index in range(1, terminal_count + 1)
        ]
        entries.extend(
            experiment(f"EXP-20260727-{100 + index:03d}", "TESTING")
            for index in range(1, open_count + 1)
        )
        (self.root / "governance/EXPERIMENTS.md").write_text(
            "# Improvement Experiments\n\n" + "\n".join(entries),
            encoding="utf-8",
        )

    def write_changelog(self, date_count: int, lines_per_date: int = 1) -> None:
        sections = []
        for index in range(date_count):
            section_date = date(2026, 7, 31) - timedelta(days=index)
            body = "\n".join(
                f"- [TEST] Entry {index}-{line}" for line in range(lines_per_date)
            )
            sections.append(f"## {section_date.isoformat()}\n\n{body}\n")
        (self.root / "docs/CHANGELOG.md").write_text(
            "# Changelog\n\n" + "\n".join(sections),
            encoding="utf-8",
        )

    def test_check_is_non_mutating_and_reports_below_threshold(self) -> None:
        self.write_deferred(9)
        before = (self.root / "docs/DEFERRED_FINDINGS.md").read_bytes()
        result = self.run_tool("check", "deferred-findings")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BELOW_THRESHOLD", result.stdout)
        self.assertEqual(
            before,
            (self.root / "docs/DEFERRED_FINDINGS.md").read_bytes(),
        )
        self.assertFalse(
            (self.root / "docs/DEFERRED_FINDINGS_ARCHIVE.md").exists()
        )

    def test_deferred_rotation_keeps_pending_and_five_completed(self) -> None:
        self.write_deferred(10, pending_count=2)
        result = self.run_tool("apply", "deferred-findings")
        self.assertEqual(result.returncode, 0, result.stderr)
        active = (self.root / "docs/DEFERRED_FINDINGS.md").read_text()
        archive = (self.root / "docs/DEFERRED_FINDINGS_ARCHIVE.md").read_text()
        self.assertEqual(active.count("- ID: DF-"), 7)
        self.assertEqual(archive.count("- ID: DF-"), 5)
        self.assertIn("DEFERRED_FINDINGS_ARCHIVE.md", active)
        self.assertNotIn("## Pending", archive)
        active_ids = set(re.findall(r"^- ID: (DF-\S+)$", active, re.MULTILINE))
        archive_ids = set(re.findall(r"^- ID: (DF-\S+)$", archive, re.MULTILINE))
        self.assertFalse(active_ids & archive_ids)

    def test_experiment_rotation_keeps_open_and_five_terminal(self) -> None:
        self.write_experiments(10, open_count=2)
        result = self.run_tool("apply", "experiments")
        self.assertEqual(result.returncode, 0, result.stderr)
        active = (self.root / "governance/EXPERIMENTS.md").read_text()
        archive = (self.root / "governance/EXPERIMENTS_ARCHIVE.md").read_text()
        self.assertEqual(active.count("## EXP-"), 7)
        self.assertEqual(archive.count("## EXP-"), 5)
        self.assertEqual(active.count("Status: TESTING"), 2)
        self.assertNotIn("Status: TESTING", archive)
        self.assertIn("EXPERIMENTS_ARCHIVE.md", active)

    def test_experiment_rotation_appends_to_split_archive_part(self) -> None:
        self.write_experiments(10, open_count=0)
        archive_index = (
            "# Improvement Experiments Archive\n\n"
            "[Back to active experiments](EXPERIMENTS.md)\n\n"
            "## Archive Parts\n\n"
            "- [Terminal experiments 001](EXPERIMENTS_ARCHIVE_001.md)\n"
        )
        archive_part = "# Improvement Experiments Archive\n\n" + "\n".join(
            experiment(f"EXP-20260726-{index:03d}", "ACCEPTED")
            for index in range(1, 6)
        )
        index_path = self.root / "governance/EXPERIMENTS_ARCHIVE.md"
        part_path = self.root / "governance/EXPERIMENTS_ARCHIVE_001.md"
        index_path.write_text(archive_index, encoding="utf-8")
        part_path.write_text(archive_part, encoding="utf-8")

        result = self.run_tool("apply", "experiments")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(index_path.read_text(encoding="utf-8"), archive_index)
        self.assertEqual(
            part_path.read_text(encoding="utf-8").count("## EXP-"),
            10,
        )
        self.assertEqual(
            (self.root / "governance/EXPERIMENTS.md")
            .read_text(encoding="utf-8")
            .count("## EXP-"),
            5,
        )

    def test_legacy_experiment_result_is_supported_when_decision_is_explicit(self) -> None:
        (self.root / "governance/EXPERIMENTS.md").write_text(
            "# Experiments\n\n"
            "## EXP-20260727-001 — Legacy fixture\n\n"
            "- Problem: Fixture.\n"
            "- Hypothesis: Fixture.\n"
            "- Solution Attempt: Fixture.\n"
            "- Test: Fixture.\n"
            "- Result: Accepted. Observable behavior passed.\n"
            "- Decision: Keep the implementation.\n",
            encoding="utf-8",
        )
        result = self.run_tool("check", "experiments")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BELOW_THRESHOLD active=1", result.stdout)

    def test_changelog_keeps_twenty_full_dates_and_thirty_archive_links(self) -> None:
        self.write_changelog(55)
        result = self.run_tool("apply", "changelog")
        self.assertEqual(result.returncode, 0, result.stderr)
        active = (self.root / "docs/CHANGELOG.md").read_text()
        archive = (self.root / "docs/CHANGELOG_ARCHIVE.md").read_text()
        self.assertEqual(active.count("\n## 2026-"), 20)
        self.assertEqual(active.count("](CHANGELOG_ARCHIVE.md#"), 30)
        self.assertEqual(archive.count("\n## 2026-"), 35)
        self.assertNotIn("2026-06-11](CHANGELOG_ARCHIVE", active)

    def test_changelog_uses_line_threshold_only_when_rotation_is_possible(self) -> None:
        self.write_changelog(21, lines_per_date=25)
        result = self.run_tool("apply", "changelog")
        self.assertEqual(result.returncode, 0, result.stderr)
        active = (self.root / "docs/CHANGELOG.md").read_text()
        archive = (self.root / "docs/CHANGELOG_ARCHIVE.md").read_text()
        self.assertEqual(active.count("\n## 2026-"), 20)
        self.assertEqual(archive.count("\n## 2026-"), 1)

    def test_headerless_date_changelog_is_supported(self) -> None:
        self.write_changelog(2)
        path = self.root / "docs/CHANGELOG.md"
        path.write_text(
            path.read_text().removeprefix("# Changelog\n\n"),
            encoding="utf-8",
        )
        result = self.run_tool("check", "changelog")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BELOW_THRESHOLD active=2", result.stdout)

    def test_duplicate_ids_fail_closed_without_mutation(self) -> None:
        self.write_deferred(10)
        active_path = self.root / "docs/DEFERRED_FINDINGS.md"
        original = active_path.read_text()
        duplicate = deferred_item("DF-20260727-0100-001", True)
        active_path.write_text(original + "\n" + duplicate)
        before = active_path.read_bytes()
        result = self.run_tool("apply", "deferred-findings")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate", result.stderr.lower())
        self.assertEqual(before, active_path.read_bytes())
        self.assertFalse(
            (self.root / "docs/DEFERRED_FINDINGS_ARCHIVE.md").exists()
        )

    def test_unsupported_changelog_format_fails_closed(self) -> None:
        (self.root / "docs/CHANGELOG.md").write_text(
            "# Changelog\n\n## Unreleased\n\n- change\n",
            encoding="utf-8",
        )
        result = self.run_tool("apply", "changelog")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("UNSUPPORTED_FORMAT", result.stderr)
        self.assertFalse((self.root / "docs/CHANGELOG_ARCHIVE.md").exists())

    def test_apply_is_idempotent(self) -> None:
        self.write_experiments(10)
        first = self.run_tool("apply", "experiments")
        self.assertEqual(first.returncode, 0, first.stderr)
        active_path = self.root / "governance/EXPERIMENTS.md"
        archive_path = self.root / "governance/EXPERIMENTS_ARCHIVE.md"
        before = (active_path.read_bytes(), archive_path.read_bytes())
        second = self.run_tool("apply", "experiments")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("BELOW_THRESHOLD", second.stdout)
        self.assertEqual(
            before,
            (active_path.read_bytes(), archive_path.read_bytes()),
        )

    def test_dirty_managed_files_require_explicit_override(self) -> None:
        self.write_deferred(10)
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        subprocess.run(("git", "add", "docs/DEFERRED_FINDINGS.md"), cwd=self.root, check=True)
        subprocess.run(
            (
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.test",
                "commit",
                "-qm",
                "fixture",
            ),
            cwd=self.root,
            check=True,
        )
        with (self.root / "docs/DEFERRED_FINDINGS.md").open("a") as stream:
            stream.write("\n")
        refused = self.run_tool("apply", "deferred-findings")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("--allow-dirty", refused.stderr)
        allowed = self.run_tool(
            "apply",
            "deferred-findings",
            "--allow-dirty",
        )
        self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_broken_archive_symlink_fails_closed(self) -> None:
        self.write_deferred(10)
        archive_path = self.root / "docs/DEFERRED_FINDINGS_ARCHIVE.md"
        archive_path.symlink_to(self.root / "missing-target.md")
        result = self.run_tool("apply", "deferred-findings")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe managed path", result.stderr)
        self.assertTrue(archive_path.is_symlink())

    def test_managed_parent_symlinks_fail_closed_without_outside_mutation(self) -> None:
        cases = (
            ("governance", "experiments", self.write_experiments, "EXPERIMENTS.md"),
            ("docs", "deferred-findings", self.write_deferred, "DEFERRED_FINDINGS.md"),
        )
        for directory, record, writer, active_name in cases:
            with self.subTest(directory=directory), tempfile.TemporaryDirectory() as outside:
                writer(10)
                managed_directory = self.root / directory
                active_path = managed_directory / active_name
                outside_directory = Path(outside)
                outside_active = outside_directory / active_name
                outside_active.write_bytes(active_path.read_bytes())
                active_path.unlink()
                managed_directory.rmdir()
                managed_directory.symlink_to(outside_directory, target_is_directory=True)
                before = outside_active.read_bytes()

                result = self.run_tool("apply", record)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unsafe managed path", result.stderr)
                self.assertEqual(outside_active.read_bytes(), before)
                self.assertEqual(
                    sorted(path.name for path in outside_directory.iterdir()),
                    [active_name],
                )

                managed_directory.unlink()
                managed_directory.mkdir()

    def test_post_replace_fsync_failure_rolls_back_the_active_file(self) -> None:
        self.write_experiments(10)
        active_path = self.root / "governance/EXPERIMENTS.md"
        archive_path = self.root / "governance/EXPERIMENTS_ARCHIVE.md"
        before = active_path.read_bytes()
        archive_module = load_archive_module()
        plan = archive_module.plan_experiments(self.root)
        real_fsync = os.fsync
        failed_once = False

        def fail_first_directory_fsync(descriptor: int) -> None:
            nonlocal failed_once
            if stat.S_ISDIR(os.fstat(descriptor).st_mode) and not failed_once:
                failed_once = True
                raise OSError("injected directory fsync failure")
            real_fsync(descriptor)

        with mock.patch.object(archive_module.os, "fsync", fail_first_directory_fsync):
            with self.assertRaisesRegex(OSError, "injected directory fsync failure"):
                archive_module.apply_plan(plan, allow_dirty=True)

        self.assertTrue(failed_once)
        self.assertEqual(active_path.read_bytes(), before)
        self.assertFalse(archive_path.exists())


class RecordArchivePackagingTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_is_identical_in_both_runtime_variants(self) -> None:
        codex = self.read(
            "variants/codex/home/skills/record-archive/SKILL.md"
        )
        dolphin = self.read(
            "variants/dolphin/home/skills/record-archive/SKILL.md"
        )
        self.assertEqual(codex, dolphin)
        self.assertEqual(
            (REPO_ROOT / SCRIPT_RELATIVE).read_bytes(),
            (
                REPO_ROOT
                / "variants/dolphin/home/skills/record-archive/scripts/record_archive.py"
            ).read_bytes(),
        )

    def test_skill_defines_sparse_event_triggers_and_retention(self) -> None:
        text = " ".join(self.read(
            "variants/codex/home/skills/record-archive/SKILL.md"
        ).split())
        required = (
            "finding becomes `Completed`",
            "experiment becomes terminal",
            "new changelog date heading",
            "Do not run at every task closure",
            "10",
            "5",
            "30",
            "500",
            "20",
            "check",
            "apply",
            "--allow-dirty",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_global_policy_and_registries_expose_skill(self) -> None:
        for path in (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/dolphin/home/AGENTS.md",
        ):
            with self.subTest(path=path):
                text = self.read(path)
                self.assertIn("Event-Driven Record Archiving", text)
                self.assertIn("record-archive", text)
                self.assertIn("Do not check records at every task closure", text)
        for variant in ("codex", "dolphin"):
            index = self.read(
                f"variants/{variant}/home/registry/SKILLS_INDEX.md"
            )
            self.assertIn("record-archive", index)

    def test_portable_installs_include_skill_and_executable_script(self) -> None:
        installer = REPO_ROOT / "bin/codex-user-install"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in ("codex", "dolphin"):
                runtime = root / variant
                result = subprocess.run(
                    (
                        str(installer),
                        "--runtime-home",
                        str(runtime),
                        "--variant",
                        variant,
                        "--force",
                    ),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    script = (
                        runtime
                        / "skills"
                        / "record-archive"
                        / "scripts"
                        / "record_archive.py"
                    )
                    self.assertTrue(script.is_file())
                    self.assertTrue(os.access(script, os.X_OK))


if __name__ == "__main__":
    unittest.main()
