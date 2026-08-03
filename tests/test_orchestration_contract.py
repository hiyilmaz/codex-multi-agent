import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
ROLES = ("planner", "tdd-guide", "code-reviewer", "security-reviewer")


class OrchestrationContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

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

    def test_global_template_and_codex_variant_stay_identical(self) -> None:
        self.assertEqual(
            self.read("GLOBAL_AGENTS_TEMPLATE.md"),
            self.read("variants/codex/home/AGENTS.md"),
        )

    def test_runtime_policies_define_truthful_outcome_contract(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/AGENTS.md",
            "variants/dolphin/home/AGENTS.md",
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
            "variants/dolphin/home/AGENTS.md",
            "variants/dolphin/home/registry/ORCHESTRATION.md",
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
        for variant in ("codex", "dolphin"):
            for role in ROLES:
                path = f"variants/{variant}/home/agents/{role}.toml"
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
        for variant in ("codex", "dolphin"):
            for role, markers in role_markers.items():
                path = f"variants/{variant}/home/agents/{role}.toml"
                text = self.read(path).lower()
                with self.subTest(path=path):
                    for marker in markers:
                        self.assertIn(marker.lower(), text)

    def test_tdd_workflow_rejects_false_positive_tests(self) -> None:
        paths = (
            "variants/codex/home/skills/tdd-workflow/SKILL.md",
            "variants/dolphin/home/skills/tdd-workflow/SKILL.md",
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
        for variant in ("codex", "dolphin"):
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
                    runtime_policy = (runtime / "AGENTS.md").read_text()
                    self.assertIn(CHAIN, runtime_policy)
                    self.assert_truthful_outcome_contract(runtime_policy)
                    for role in ROLES:
                        agent = (runtime / "agents" / f"{role}.toml").read_text()
                        self.assertIn("Do not repeat", agent)
                    if variant == "codex":
                        self.assertIn(
                            'model_reasoning_effort = "medium"',
                            (runtime / "agents/planner.toml").read_text(),
                        )


if __name__ == "__main__":
    unittest.main()
