import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "bin/codex-user-install"
POLICIES = (
    "GLOBAL_AGENTS_TEMPLATE.md",
    "variants/codex/home/AGENTS.md",
    "variants/claude/home/CLAUDE.md",
    "variants/opencode/home/AGENTS.md",
)


class TaskTransitionGateTests(unittest.TestCase):
    def main_plan_section(self, text: str) -> str:
        start = text.index("### Main Plan Execution")
        end = text.find("\n### ", start + 1)
        return text[start : end if end >= 0 else len(text)]

    def assert_task_transition_gate(self, text: str) -> None:
        normalized = " ".join(self.main_plan_section(text).split())
        required = (
            "### Main Plan Execution",
            "Before non-trivial implementation, analyze and verify the request",
            "create one ordered main plan",
            "obtain explicit approval for that plan once",
            "execute every disclosed phase and planned subtask",
            "without task-boundary approval pauses",
            "summarize material main-list updates briefly",
            "auxiliary list",
            "Do not execute it unless it is required to continue",
            "report a required deviation and obtain approval before changing the plan",
            "report truthful success or failure",
            "completed subtasks",
            "deferred auxiliary tasks",
            "user-relevant details",
            "Recommended work is reported separately",
            "never added to the main plan automatically",
            "destructive, High, or Critical operations",
            "explicit approval requirements remain independent and mandatory",
        )
        for marker in required:
            self.assertIn(" ".join(marker.split()), normalized)

        forbidden = (
            "Treat each distinct task as a hard stop",
            "Ask for explicit user approval before starting that next task",
            "plan approval authorizes destructive",
            "execute recommended work automatically",
            "change the plan before approval",
            "always report success",
        )
        lowered = normalized.lower()
        for marker in forbidden:
            self.assertNotIn(marker.lower(), lowered)

    def assert_english_guide_contract(self, section: str) -> None:
        normalized = " ".join(section.split())
        for marker in (
            "Main Plan Execution",
            "disclosed non-destructive Low/Medium work",
            "planned orchestration",
            "Work discovered outside the approved plan stays on an auxiliary list",
            "not executed unless it is required to continue",
            "A required deviation is reported and approved before the plan changes",
            "Recommended work is reported separately",
            "never added to the main plan automatically",
            "Destructive and High/Critical",
            "separate approval",
        ):
            self.assertIn(marker, normalized)

    def test_all_canonical_policies_define_the_complete_gate(self) -> None:
        self.assertEqual(len(POLICIES), 4)
        self.assertIn("variants/opencode/home/AGENTS.md", POLICIES)
        sections = []
        for relative in POLICIES:
            with self.subTest(path=relative):
                text = (REPO_ROOT / relative).read_text(encoding="utf-8")
                self.assert_task_transition_gate(text)
                normalized = " ".join(text.split())
                self.assertIn(
                    "Approval of an explicitly disclosed main plan satisfies "
                    "this requirement for its named non-destructive Low or "
                    "Medium risk changes",
                    normalized,
                )
                self.assertIn(
                    "approval satisfies `ask-approval` for the planned "
                    "orchestration only",
                    normalized,
                )
                sections.append(" ".join(self.main_plan_section(text).split()))
        self.assertEqual(len(set(sections)), 1)

    def test_partial_or_every_step_gate_is_rejected(self) -> None:
        partial = (
            "### Main Plan Execution\n"
            "Obtain explicit approval for that plan once.\n"
        )
        with self.assertRaises(AssertionError):
            self.assert_task_transition_gate(partial)

        canonical = (REPO_ROOT / POLICIES[0]).read_text(encoding="utf-8")
        for claim in (
            "Plan approval authorizes destructive operations.",
            "Execute recommended work automatically.",
            "Change the plan before approval.",
            "Always report success.",
        ):
            contradictory = canonical.replace(
                "### Truthful Success Reporting",
                f"{claim}\n\n### Truthful Success Reporting",
            )
            with self.subTest(claim=claim), self.assertRaises(AssertionError):
                self.assert_task_transition_gate(contradictory)

    def test_each_main_plan_acceptance_clause_is_mandatory(self) -> None:
        canonical = (REPO_ROOT / POLICIES[0]).read_text(encoding="utf-8")
        normalized = " ".join(self.main_plan_section(canonical).split())
        acceptance_markers = (
            "Before non-trivial implementation, analyze and verify the request",
            "create one ordered main plan",
            "execute every disclosed phase and planned subtask",
            "summarize material main-list updates briefly",
            "Record discovered work outside the plan in an auxiliary list",
            "obtain approval before changing the plan",
            "report truthful success or failure",
            "Recommended work is reported separately",
            "explicit approval requirements remain independent and mandatory",
        )
        for marker in acceptance_markers:
            with self.subTest(marker=marker):
                mutated = normalized.replace(marker, "", 1)
                self.assertNotEqual(mutated, normalized)
                with self.assertRaises(AssertionError):
                    self.assert_task_transition_gate(mutated)

    def test_portable_installs_expose_the_complete_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in ("codex", "claude", "opencode"):
                runtime = root / variant
                result = subprocess.run(
                    (
                        str(INSTALLER),
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
                    policy = "CLAUDE.md" if variant == "claude" else "AGENTS.md"
                    self.assert_task_transition_gate(
                        (runtime / policy).read_text(encoding="utf-8")
                    )

    def test_user_guides_explain_the_main_plan_contract(self) -> None:
        english = {
            "README.md": ("### Main Plan Execution", "\n\nInstallable runtime variants"),
            "USAGE_GUIDE.md": ("## Main Plan Execution", "\n---"),
            "COMMAND_REFERENCE.md": (
                "## Main Plan Execution",
                "\n## Recommended Workflows",
            ),
        }
        for relative, (start_marker, end_marker) in english.items():
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                start = text.index(start_marker)
                end = text.index(end_marker, start)
                section = " ".join(text[start:end].split())
                self.assert_english_guide_contract(section)
                for marker in (
                    "A required deviation is reported and approved before the plan changes",
                    "never added to the main plan automatically",
                ):
                    mutated = section.replace(marker, "", 1)
                    with self.subTest(marker=marker), self.assertRaises(
                        AssertionError
                    ):
                        self.assert_english_guide_contract(mutated)

        turkish = (REPO_ROOT / "TURKCE_KURULUM_REHBERI.md").read_text(
            encoding="utf-8"
        )
        start = turkish.index("### Ana Plan Yürütme")
        end = turkish.index("\n`orchestration-gate`", start)
        turkish = " ".join(turkish[start:end].split())
        for marker in (
            "Ana Plan Yürütme",
            "başlangıçta bir kez açık kullanıcı onayı",
            "yeniden onay istemeden",
            "Destructive",
            "ayrı açık onay zorunluluğu",
            "Low/Medium",
            "planlanmış orkestrasyonu",
            "yardımcı görev listesinde tutulur",
            "zorunlu değilse uygulanmaz",
            "plan değiştirilmeden önce raporlanır ve onaylanır",
            "Önerilen görevler ayrı raporlanır",
            "hiçbir zaman otomatik eklenmez",
        ):
            self.assertIn(marker, turkish)


if __name__ == "__main__":
    unittest.main()
