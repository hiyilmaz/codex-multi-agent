import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
MODULES = (
    "CMA_ORCHESTRATION.md",
    "CMA_TDD.md",
    "CMA_SECURITY.md",
    "CMA_REMOTE_ADMIN.md",
    "CMA_MEMORY_ROUTING.md",
    "CMA_DOCS_RESEARCH.md",
    "CMA_FRONTEND.md",
    "CMA_RECORDS.md",
)
AGENTS = {
    "planner": ("Pete", "gpt-5.6-terra", "medium"),
    "tdd-guide": ("Ted", "gpt-5.6-terra", "medium"),
    "code-reviewer": ("Cody", "gpt-5.6-sol", "medium"),
    "security-reviewer": ("Sec", "gpt-5.6-sol", "medium"),
    "explorer": ("Scout", "gpt-5.6-terra", "medium"),
    "docs-researcher": ("Doc", "gpt-5.6-terra", "medium"),
    "reviewer": ("Simon", "gpt-5.6-sol", "medium"),
    "skill-agent-governor": ("Sam", "gpt-5.6-sol", "medium"),
}
SOL_AGENTS = {
    "planner-sol": "Pete",
    "tdd-guide-sol": "Ted",
    "explorer-sol": "Scout",
    "docs-researcher-sol": "Doc",
}


class CmaLazyRuntimeContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def assert_evidence_validator_claim_contract(self, text: str) -> None:
        required = (
            "For every new or materially updated evidence report:",
            "Include the exact heading `## Claims`.",
            "Put exactly one bullet under it for each material claim.",
            "Keep supporting proof outside the `## Claims` section.",
            "Apply this requirement prospectively; do not rewrite historical evidence reports solely to adopt it.",
        )
        for marker in required:
            self.assertIn(marker, text)

    def assert_temporal_tdd_evidence_contract(self, text: str) -> None:
        required = (
            "records both an expected TDD RED result and a final verification result",
            "Include the exact heading `## Initial RED Evidence`.",
            "Include the exact heading `## Final Verification Evidence`.",
            "Treat Initial RED Evidence as historical pre-fix proof, not as the final status.",
            "Support final-success claims only with proof from `## Final Verification Evidence`.",
            "Use each temporal heading exactly once and keep Initial RED Evidence before Final Verification Evidence.",
            "Treat temporal headings inside fenced or quoted evidence as proof text, not as report structure.",
            "Do not require these temporal headings for one-phase or non-TDD evidence reports.",
        )
        for marker in required:
            self.assertIn(marker, text)
        self.assertNotIn("## Acceptance Criteria", text)
        self.assertNotIn("Acceptance Criteria ID", text)
        self.assertNotIn("acceptance mapping table", text.lower())

    def test_records_module_defines_evidence_validator_claim_contract(self) -> None:
        self.assert_evidence_validator_claim_contract(
            self.read("variants/codex/home/registry/modules/CMA_RECORDS.md")
        )

    def test_partial_evidence_claim_contract_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_evidence_validator_claim_contract(
                "Include the exact heading `## Claims`."
            )

    def test_records_module_defines_conditional_temporal_tdd_contract(self) -> None:
        text = self.read("variants/codex/home/registry/modules/CMA_RECORDS.md")
        self.assert_evidence_validator_claim_contract(text)
        self.assert_temporal_tdd_evidence_contract(text)

    def test_temporal_tdd_contract_rejects_headings_without_semantics(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_temporal_tdd_evidence_contract(
                "## Initial RED Evidence\n\n## Final Verification Evidence\n"
            )

    def test_global_policy_is_compact_and_routes_lazy_modules(self) -> None:
        text = self.read("GLOBAL_AGENTS_TEMPLATE.md")
        self.assertLessEqual(len(text.splitlines()), 280)
        self.assertIn(CHAIN, text)
        self.assertIn("Load only the minimum relevant module", text)
        self.assertIn("file-list-first", text)
        self.assertIn("index-first", text)
        for module in MODULES:
            with self.subTest(module=module):
                self.assertIn(f"registry/modules/{module}", text)

    def test_managed_modules_have_bounded_load_contracts(self) -> None:
        root = REPO_ROOT / "variants/codex/home/registry/modules"
        self.assertEqual(
            sorted(path.name for path in root.glob("*.md")), sorted(MODULES)
        )
        for module in MODULES:
            text = (root / module).read_text(encoding="utf-8")
            with self.subTest(module=module):
                self.assertIn("## Load When", text)
                self.assertIn("## Do Not Load When", text)
                self.assertIn("## Rules", text)

    def test_agent_metadata_and_model_matrix_are_supported(self) -> None:
        for role, (identity, model, effort) in AGENTS.items():
            path = f"variants/codex/home/agents/{role}.toml"
            text = self.read(path)
            with self.subTest(path=path):
                self.assertNotIn("display_name", text)
                self.assertIn(f'name = "{role}"', text.splitlines())
                self.assertIn(f'model = "{model}"', text.splitlines())
                self.assertIn(
                    f'model_reasoning_effort = "{effort}"', text.splitlines()
                )
                self.assertIn(f"Identity: You are {identity},", text)
                if role in {
                    "planner",
                    "tdd-guide",
                    "code-reviewer",
                    "security-reviewer",
                }:
                    self.assertNotIn("gpt-5.6-luna", text)

    def test_all_agents_use_medium_and_only_four_sol_variants_exist(self) -> None:
        root = REPO_ROOT / "variants/codex/home/agents"
        expected = sorted(f"{role}.toml" for role in {*AGENTS, *SOL_AGENTS})
        self.assertEqual(sorted(path.name for path in root.glob("*.toml")), expected)
        for path in root.glob("*.toml"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn('model_reasoning_effort = "medium"', text.splitlines())
                self.assertNotIn('model_reasoning_effort = "high"', text)
                self.assertNotIn("-high", path.stem)

    def test_sol_variants_make_model_escalation_operational(self) -> None:
        for role, identity in SOL_AGENTS.items():
            path = f"variants/codex/home/agents/{role}.toml"
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn(f'name = "{role}"', text.splitlines())
                self.assertIn('model = "gpt-5.6-sol"', text.splitlines())
                self.assertIn('model_reasoning_effort = "medium"', text.splitlines())
                self.assertIn(f"Identity: You are {identity},", text)

    def test_orchestration_policy_routes_to_medium_sol_variants(self) -> None:
        paths = (
            "variants/codex/home/registry/ORCHESTRATION.md",
            "variants/codex/home/skills/orchestration-gate/SKILL.md",
        )
        required = (
            "planner-sol",
            "tdd-guide-sol",
            "explorer-sol",
            "docs-researcher-sol",
            "gpt-5.6-sol",
            "medium",
            "all custom subagents use `medium`",
            "NO_SECURITY_IMPACT",
            "agent-file values take precedence",
        )
        for path in paths:
            text = self.read(path)
            with self.subTest(path=path):
                for marker in required:
                    self.assertIn(marker, text)

    def test_orchestration_gate_defines_decision_precedence(self) -> None:
        text = self.read(
            "variants/codex/home/skills/orchestration-gate/SKILL.md"
        )
        self.assertIn("## Decision Precedence", text)
        self.assertIn("Explicit orchestration request", text)
        self.assertIn("Read-only does not override", text)
        self.assertIn("simple and read-only", text)

    def test_chain_rendering_never_inserts_implementation_stage(self) -> None:
        paths = (
            "GLOBAL_AGENTS_TEMPLATE.md",
            "variants/codex/home/registry/ORCHESTRATION.md",
            "variants/codex/home/registry/modules/CMA_ORCHESTRATION.md",
            "variants/codex/home/skills/orchestration-gate/SKILL.md",
        )
        for path in paths:
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("Implementation is not a chain stage", text)
                self.assertNotIn("planner -> tdd-guide -> implementation", text)

    def test_lazy_orchestration_module_contains_decision_and_escalation_map(self) -> None:
        text = self.read(
            "variants/codex/home/registry/modules/CMA_ORCHESTRATION.md"
        )
        required = (
            "Simple answer",
            "Read-only audit",
            "Small tested bugfix",
            "Multi-file feature",
            "Explicit CMA request",
            "ask-approval",
            "run-chain",
            "auth, secrets, sandboxing",
            "hardcoded-success traps",
            "gpt-5.6-sol` / `medium",
            "CMA_MEMORY_ROUTING",
            "combined request",
        )
        for marker in required:
            self.assertIn(marker, text)

    def test_portable_codex_install_contains_lazy_modules(self) -> None:
        installer = REPO_ROOT / "bin/codex-user-install"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "codex"
            environment = {**os.environ, "HOME": str(root / "home")}
            result = subprocess.run(
                (
                    str(installer),
                    "--runtime-home",
                    str(runtime),
                    "--variant",
                    "codex",
                    "--force",
                ),
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for module in MODULES:
                with self.subTest(module=module):
                    self.assertTrue((runtime / "registry/modules" / module).is_file())
            self.assert_evidence_validator_claim_contract(
                (runtime / "registry/modules/CMA_RECORDS.md").read_text(
                    encoding="utf-8"
                )
            )
            installed_records = (
                runtime / "registry/modules/CMA_RECORDS.md"
            ).read_text(encoding="utf-8")
            source_records = self.read(
                "variants/codex/home/registry/modules/CMA_RECORDS.md"
            )
            self.assertEqual(installed_records, source_records)
            self.assert_temporal_tdd_evidence_contract(installed_records)
            installed_agents = sorted(
                path.name for path in (runtime / "agents").glob("*.toml")
            )
            self.assertEqual(
                installed_agents,
                sorted(f"{role}.toml" for role in {*AGENTS, *SOL_AGENTS}),
            )
            for path in (runtime / "agents").glob("*.toml"):
                self.assertIn(
                    'model_reasoning_effort = "medium"',
                    path.read_text(encoding="utf-8"),
                )
            self.assertLessEqual(
                len((runtime / "AGENTS.md").read_text().splitlines()), 280
            )


if __name__ == "__main__":
    unittest.main()
