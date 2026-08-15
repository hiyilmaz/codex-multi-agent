import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "hypothesis-workflow"
TRIGGERS = (
    "failed attempt",
    "unclear evidence",
    "competing hypotheses",
    "regression",
    "measured comparison",
    "core runtime",
    "explicitly requests",
)
NON_TRIGGERS = (
    "routine first-pass",
    "typo",
    "formatting",
    "clear deterministic fix",
)


class HypothesisWorkflowContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def skill_path(self, variant: str) -> Path:
        return (
            REPO_ROOT
            / "variants"
            / variant
            / "home"
            / "skills"
            / SKILL_NAME
            / "SKILL.md"
        )

    def test_codex_skill_is_packaged(self) -> None:
        self.assertTrue(self.skill_path("codex").is_file())

    def test_skill_defines_positive_and_negative_activation_contracts(self) -> None:
        text = self.skill_path("codex").read_text(encoding="utf-8").lower()
        for marker in (*TRIGGERS, *NON_TRIGGERS):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertIn("do not activate", text)
        self.assertIn("do not create", text)

    def test_skill_preserves_existing_project_records_and_test_integrity(self) -> None:
        text = self.skill_path("codex").read_text(encoding="utf-8")
        required = (
            "governance/EXPERIMENTS.md",
            "CHANGELOG_PATH",
            "EVIDENCE_PATH",
            "hardcoded success",
            "weaken assertions",
            "dummy implementation",
            "type(scope): EXP-YYYYMMDD-XXX description",
            "Do not create `governance/CHANGELOG.md`",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_global_policy_is_conditional_without_project_declaration(self) -> None:
        policies = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
        )
        for policy in policies:
            text = self.read(policy)
            with self.subTest(policy=policy):
                self.assertIn("Conditional Hypothesis Escalation", text)
                self.assertIn(SKILL_NAME, text)
                self.assertIn("Do not activate", text)
        self.assertNotIn(SKILL_NAME, self.read("PROJECT_AGENTS_TEMPLATE.md"))

    def test_registries_and_orchestration_policy_expose_the_skill(self) -> None:
        for variant in ("codex",):
            with self.subTest(variant=variant):
                index = self.read(
                    f"variants/{variant}/home/registry/SKILLS_INDEX.md"
                )
                orchestration = self.read(
                    f"variants/{variant}/home/registry/ORCHESTRATION.md"
                )
                self.assertIn(SKILL_NAME, index)
                self.assertIn("Conditional Experiment Escalation", orchestration)
                self.assertIn(SKILL_NAME, orchestration)

    def test_portable_installs_include_the_conditional_skill(self) -> None:
        installer = REPO_ROOT / "bin/codex-user-install"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in ("codex",):
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
                    installed = runtime / "skills" / SKILL_NAME / "SKILL.md"
                    self.assertTrue(installed.is_file())
                    self.assertIn("Do not activate", installed.read_text())

    def test_bootstrap_experiment_records_accepted_result(self) -> None:
        active = self.read("governance/EXPERIMENTS.md")
        archive_index = self.read("governance/EXPERIMENTS_ARCHIVE.md")
        archive_parts = re.findall(
            r"\]\((EXPERIMENTS_ARCHIVE_\d{3}\.md)\)", archive_index
        )
        self.assertTrue(archive_parts)
        text = "\n".join(
            (
                active,
                archive_index,
                *(self.read(f"governance/{part}") for part in archive_parts),
            )
        )
        records = re.findall(
            r"(?ms)^## EXP-20260727-001\b.*?(?=^## EXP-|\Z)", text
        )
        self.assertEqual(len(records), 1)
        bootstrap_record = records[0]
        self.assertIn("Status: ACCEPTED", bootstrap_record)
        self.assertIn("Decision:\nACCEPT", bootstrap_record)
        self.assertIn("does not alter approval", bootstrap_record)
        tasks = self.read("docs/ORCHESTRATION_IMPROVEMENT_TASKS.md")
        self.assertIn("- [x] ORCH-005", tasks)


if __name__ == "__main__":
    unittest.main()
