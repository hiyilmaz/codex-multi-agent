import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
ROLES = ("planner", "tdd-guide", "code-reviewer", "security-reviewer")
EVIDENCE_FIRST_SECTION = """### Evidence-First Objectivity

When evaluating claims, options, recommendations, or disputed topics:

- Optimize for evidential accuracy, not user agreement or satisfaction.
- Base conclusions on reliable, verifiable evidence. Prefer current primary
  sources, official records, reproducible data, and relevant real-world
  findings.
- When the decision is material, compare multiple independent sources where
  available. Do not manufacture source diversity or treat repeated reporting
  of the same underlying claim as independent confirmation.
- Include credible counterevidence, limitations, risks, and plausible
  alternative explanations.
- Distinguish verified facts, source claims, reasoned inferences, and opinions.
- If sources conflict, describe the conflict and explain which evidence is
  stronger and why.
- State uncertainty and evidence gaps explicitly. Do not guess or imply
  certainty when verification is unavailable.
- Present the conclusion best supported by the evidence, even when it conflicts
  with the user’s assumptions, preferences, or expected outcome.
- Do not require research for routine coding, file editing, translation, or
  operational tasks unless the task independently requires current evidence.
"""
TURKISH_DIALOGUE_MARKERS = (
    "User dialogue: always Turkish.",
    "questions, status updates, error explanations, approval requests, and final reports",
    "Never switch user dialogue to another language",
    "request, source material, tool output, or project content uses another language",
)
SIMPLE_DECISION_BLOCK = """CRITICAL DECISION
Konu: [kısa karar]
Risk: Low / Medium / High / Critical
Seçenekler: A) [kısa seçenek] B) [kısa seçenek]
Öneri: [seçenek ve tek kısa neden]
Karar bekleniyor."""
SIMPLE_DECISION_RULES = (
    "Use plain Turkish.",
    "Give exactly two short, concrete options and one short recommendation sentence.",
    "Omit background and technical detail unless needed to choose.",
)


class OrchestrationContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def assert_document_version(self, text: str, expected: str) -> None:
        match = re.search(r"(?m)^\*\*Version:\*\*\s+([^\s]+)$", text)
        self.assertIsNotNone(match, "missing document version")
        self.assertEqual(match.group(1), expected)

    def assert_truthful_outcome_contract(self, text: str) -> None:
        normalized = " ".join(text.split())
        required = (
            "Truthful Success Reporting",
            "explicitly reporting the outcome of a task, operation, or test",
            "Ordinary conversation does not require a status field or JSON response.",
            "`passed`",
            "`success=true`",
            "was actually executed",
            "real output was captured and reviewed",
            "all defined success criteria were satisfied",
            "no critical error, failed assertion, or unmet requirement remains",
            "concrete, verifiable evidence",
            "`failed`",
            "`unverified`",
            "`not_executed`",
            "must always use `success=false`",
            "No evidence means no success.",
        )
        for marker in required:
            self.assertIn(" ".join(marker.split()), normalized)

    def assert_evidence_first_objectivity_contract(self, text: str) -> None:
        match = re.search(
            r"^### Evidence-First Objectivity\n(?P<section>.*?)(?=^### |\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, "missing Evidence-First Objectivity section")
        normalized = " ".join(match.group("section").lower().split())
        required = (
            "when evaluating claims, options, recommendations, or disputed topics",
            "evidential accuracy, not user agreement or satisfaction",
            "reliable, verifiable evidence",
            "current primary sources",
            "official records",
            "reproducible data",
            "relevant real-world findings",
            "decision is material",
            "multiple independent sources where available",
            "repeated reporting of the same underlying claim as independent confirmation",
            "credible counterevidence",
            "limitations",
            "risks",
            "plausible alternative explanations",
            "verified facts, source claims, reasoned inferences, and opinions",
            "sources conflict",
            "which evidence is stronger and why",
            "uncertainty and evidence gaps explicitly",
            "do not guess or imply certainty when verification is unavailable",
            "conclusion best supported by the evidence",
            "user’s assumptions, preferences, or expected outcome",
            "do not require research for routine coding, file editing, translation, or operational tasks",
        )
        for marker in required:
            self.assertIn(marker, normalized)
        routine_boundary = (
            "do not require research for routine coding, file editing, translation, "
            "or operational tasks unless the task independently requires current evidence."
        )
        contradiction_scan = normalized.replace(routine_boundary, "")
        forbidden = (
            r"(?:every|all) tasks?.{0,40}research|research.{0,40}(?:every|all) tasks?",
            r"\balways (?:perform )?research\b|\bresearch (?:is )?always\b",
            r"\bresearch.{0,80}\broutine\b|\broutine\b.{0,80}\bresearch\b",
        )
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, contradiction_scan))

    def assert_turkish_dialogue_and_simple_decision_contract(self, text: str) -> None:
        normalized = " ".join(text.split())
        for marker in TURKISH_DIALOGUE_MARKERS:
            self.assertIn(" ".join(marker.lower().split()), normalized.lower())
        self.assertIn(SIMPLE_DECISION_BLOCK, text)
        self.assertIn("Use plain Turkish", normalized)
        self.assertIn("exactly two short, concrete options", normalized)
        self.assertIn("one short recommendation sentence", normalized)
        self.assertIn("Omit background and technical detail unless needed to choose", normalized)
        self.assertNotIn("Topic: [description]", text)
        self.assertNotIn("Options: A) [...] B) [...]", text)
        self.assertNotIn("Awaiting decision.", text)
        forbidden = (
            r"switch (?:the )?user dialogue to english",
            r"user dialogue.{0,40}unless the request is in english",
            r"provide detailed background.{0,40}(?:every|all) decisions?",
            r"add (?:a )?third option",
        )
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, normalized.lower()))

    def test_global_template_and_codex_variant_stay_identical(self) -> None:
        self.assertEqual(
            self.read("GLOBAL_AGENTS_TEMPLATE.md"),
            self.read("variants/codex/home/AGENTS.md"),
        )

    def test_global_and_project_cma_versions_are_independent(self) -> None:
        global_paths = (
            "README.md",
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/claude/home/CLAUDE.md",
            "variants/opencode/home/AGENTS.md",
        )
        for path in global_paths:
            with self.subTest(path=path):
                self.assert_document_version(self.read(path), "2.7")
        self.assert_document_version(self.read("PROJECT_AGENTS_TEMPLATE.md"), "2.2")

    def test_version_contract_rejects_stale_or_false_project_bumps(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_document_version("**Version:** 2.6\n", "2.7")
        with self.assertRaises(AssertionError):
            self.assert_document_version("**Version:** 2.3\n", "2.2")

    def test_evidence_first_objectivity_contract(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/claude/home/CLAUDE.md",
            "variants/opencode/home/AGENTS.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assert_evidence_first_objectivity_contract(self.read(path))

    def test_runtime_policies_require_turkish_dialogue_and_simple_decisions(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/claude/home/CLAUDE.md",
            "variants/opencode/home/AGENTS.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assert_turkish_dialogue_and_simple_decision_contract(self.read(path))

    def test_orchestration_skills_require_simple_turkish_decisions(self) -> None:
        for variant in ("codex", "claude", "opencode"):
            path = f"variants/{variant}/home/skills/orchestration-gate/SKILL.md"
            with self.subTest(path=path):
                self.assert_turkish_dialogue_and_simple_decision_contract(self.read(path))

    def test_partial_or_english_dialogue_contract_is_rejected(self) -> None:
        partials = (
            "- User dialogue: Turkish.\n",
            "- User dialogue: Turkish unless the request is in English.\n",
            SIMPLE_DECISION_BLOCK,
        )
        for partial in partials:
            with self.subTest(partial=partial):
                with self.assertRaises(AssertionError):
                    self.assert_turkish_dialogue_and_simple_decision_contract(partial)

    def test_old_or_verbose_decision_contract_is_rejected(self) -> None:
        valid = (
            "\n".join(TURKISH_DIALOGUE_MARKERS)
            + "\n"
            + SIMPLE_DECISION_BLOCK
            + "\n"
            + "\n".join(SIMPLE_DECISION_RULES)
        )
        invalid_contracts = (
            valid.replace("Konu: [kısa karar]", "Topic: [description]"),
            valid + "\nProvide detailed background for every decision.",
            valid + "\nSwitch the user dialogue to English when requested.",
            valid + "\nAdd a third option when useful.",
        )
        for invalid in invalid_contracts:
            with self.subTest(invalid=invalid):
                with self.assertRaises(AssertionError):
                    self.assert_turkish_dialogue_and_simple_decision_contract(invalid)

    def test_diluted_or_overbroad_objectivity_contract_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_evidence_first_objectivity_contract(
                "### Evidence-First Objectivity\n\nBe objective and use reliable sources.\n"
            )
        with self.assertRaises(AssertionError):
            self.assert_evidence_first_objectivity_contract(
                EVIDENCE_FIRST_SECTION + "\nResearch every task before acting.\n"
            )
        for contradiction in (
            "Always research before acting.",
            "Research routine coding, editing, translation, and operational tasks before acting.",
        ):
            with self.subTest(contradiction=contradiction):
                with self.assertRaises(AssertionError):
                    self.assert_evidence_first_objectivity_contract(
                        EVIDENCE_FIRST_SECTION + "\n" + contradiction + "\n"
                    )

    def test_each_objectivity_clause_is_required(self) -> None:
        clauses = [
            block
            for block in EVIDENCE_FIRST_SECTION.split("\n-")
            if block.strip() and not block.startswith("###")
        ]
        self.assertEqual(len(clauses), 9)
        for clause in clauses:
            mutant = EVIDENCE_FIRST_SECTION.replace("\n-" + clause, "", 1)
            with self.subTest(clause=clause.splitlines()[0]):
                with self.assertRaises(AssertionError):
                    self.assert_evidence_first_objectivity_contract(mutant)

    def test_portable_installs_include_objectivity_contract(self) -> None:
        installer = REPO_ROOT / "bin/codex-user-install"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant, policy_name in (
                ("codex", "AGENTS.md"),
                ("claude", "CLAUDE.md"),
                ("opencode", "AGENTS.md"),
            ):
                runtime = root / variant
                result = subprocess.run(
                    (
                        str(installer),
                        "--runtime-home",
                        str(runtime),
                        "--variant",
                        variant,
                    ),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assert_evidence_first_objectivity_contract(
                        (runtime / policy_name).read_text(encoding="utf-8")
                    )
                    self.assert_turkish_dialogue_and_simple_decision_contract(
                        (runtime / policy_name).read_text(encoding="utf-8")
                    )

    def test_codex_approval_wait_is_exact_and_not_completion(self) -> None:
        policy = self.read("GLOBAL_AGENTS_TEMPLATE.md")
        skill = self.read("variants/codex/home/skills/orchestration-gate/SKILL.md")
        policy = " ".join(policy.split())
        skill = " ".join(skill.split())
        required = (
            "final assistant message must contain only the exact six-line `CRITICAL DECISION` block",
            "applies only to the current Stop invocation",
            "does not mean `PASS`, validation, or task completion",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, policy)
                self.assertIn(marker, skill)

    def test_runtime_policies_define_truthful_outcome_contract(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/claude/home/CLAUDE.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assert_truthful_outcome_contract(self.read(path))

    def test_partial_or_hardcoded_contract_is_rejected(self) -> None:
        partial = "`passed` means `success=true`."
        with self.assertRaises(AssertionError):
            self.assert_truthful_outcome_contract(partial)

    def test_mandatory_chain_is_preserved_in_runtime_policies(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/registry/ORCHESTRATION.md",
            "variants/claude/home/CLAUDE.md",
            "variants/claude/home/registry/ORCHESTRATION.md",
        )
        for path in paths:
            with self.subTest(path=path):
                text = self.read(path)
                self.assertIn(CHAIN, text)
                self.assertIn("Do not skip", text)

    def test_codex_core_agents_default_to_medium_reasoning(self) -> None:
        for role in ROLES:
            path = f"variants/codex/home/agents/{role}.toml"
            with self.subTest(path=path):
                text = self.read(path)
                self.assertIn(
                    'model_reasoning_effort = "medium"',
                    text.splitlines(),
                    msg=f"{path} must use medium reasoning",
                )

    def test_each_agent_has_bounded_handoff_contract(self) -> None:
        required = (
            "Input:",
            "Output:",
            "Do not repeat",
            "Stop condition:",
        )
        for variant in ("codex", "claude"):
            for role in ROLES:
                extension = "md" if variant == "claude" else "toml"
                path = f"variants/{variant}/home/agents/{role}.{extension}"
                text = self.read(path)
                with self.subTest(path=path):
                    for marker in required:
                        self.assertIn(marker, text)

    def test_role_contracts_are_distinct(self) -> None:
        role_markers = {
            "planner": (
                "acceptance criteria",
                "prohibited shortcuts",
            ),
            "tdd-guide": (
                "acceptance-to-test mapping",
                "dummy implementation",
            ),
            "code-reviewer": (
                "hardcoded success",
                "weakened assertions",
                "test-only production branches",
            ),
            "security-reviewer": (
                "fail-open",
                "authorization bypass",
                "NO_SECURITY_IMPACT",
            ),
        }
        for variant in ("codex", "claude"):
            for role, markers in role_markers.items():
                extension = "md" if variant == "claude" else "toml"
                path = f"variants/{variant}/home/agents/{role}.{extension}"
                text = self.read(path).lower()
                with self.subTest(path=path):
                    for marker in markers:
                        self.assertIn(marker.lower(), text)

    def test_tdd_workflow_rejects_false_positive_tests(self) -> None:
        paths = (
            "variants/codex/home/skills/tdd-workflow/SKILL.md",
        )
        required = (
            "Test Integrity Guardrails",
            "hardcoded success",
            "weaken assertions",
            "skip or disable tests",
            "test-only production branches",
            "observable behavior",
        )
        for path in paths:
            text = self.read(path)
            with self.subTest(path=path):
                for marker in required:
                    self.assertIn(marker, text)

    def test_agent_files_remain_minimal_toml_contracts(self) -> None:
        for variant in ("codex",):
            for role in ROLES:
                path = f"variants/{variant}/home/agents/{role}.toml"
                text = self.read(path)
                with self.subTest(path=path):
                    self.assertEqual(len(re.findall(r"^name =", text, re.MULTILINE)), 1)
                    self.assertEqual(
                        len(re.findall(r"^developer_instructions =", text, re.MULTILINE)),
                        1,
                    )
                    self.assertIn('sandbox_mode = "read-only"', text)

    def test_portable_installs_preserve_orchestration_contract(self) -> None:
        installer = REPO_ROOT / "bin/codex-user-install"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in ("codex", "claude"):
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
                    policy_name = "CLAUDE.md" if variant == "claude" else "AGENTS.md"
                    extension = "md" if variant == "claude" else "toml"
                    runtime_policy = (runtime / policy_name).read_text()
                    self.assertIn(CHAIN, runtime_policy)
                    self.assert_truthful_outcome_contract(runtime_policy)
                    for role in ROLES:
                        agent = (runtime / "agents" / f"{role}.{extension}").read_text()
                        self.assertIn("Do not repeat", agent)
                    if variant == "codex":
                        self.assertIn(
                            'model_reasoning_effort = "medium"',
                            (runtime / "agents/planner.toml").read_text(),
                        )


if __name__ == "__main__":
    unittest.main()
