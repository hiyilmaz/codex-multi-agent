import os
import re
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility
    import tomli as tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
COMMON_MODULES = (
    "CMA_ORCHESTRATION.md", "CMA_TDD.md",
    "CMA_SECURITY.md", "CMA_REMOTE_ADMIN.md",
    "CMA_MEMORY_ROUTING.md", "CMA_DOCS_RESEARCH.md",
    "CMA_FRONTEND.md", "CMA_RECORDS.md",
)
CODEX_ONLY_MODULES = ("CMA_REPO_TOOLS.md",)
CODEX_MODULES = COMMON_MODULES + CODEX_ONLY_MODULES
REPOSITORY_TOOL_ROWS = (
    "| Exact text or path | `rg` |", "| Architecture or cross-file dependency | Graphify |",
    "| Structural AST pattern | `ast-grep` |", "| Symbol references or refactor radius | Serena, explicit and lazy |",
    "| Dependency vulnerability | OSV-Scanner |", "| SAST or secret scan | Opengrep or Betterleaks, security-triggered |",
    "| GitHub source, release, or advisory | GitHub MCP, gated read-only |", "| Public-repo or versioned-doc fallback | DeepWiki or Context7, explicit |",
)
REPOSITORY_TOOL_RULES = (
    "Use the narrowest sufficient tool.", "Do not query multiple discovery tools for the same question.",
    "Stop discovery when sufficient evidence exists.", "Keep MCP providers and scanners outside the default task path.",
    "Report unavailable tools; never silently widen the route.",
)
REPOSITORY_TOOL_BOUNDARY_RULES = (
    "Source-check Graphify output before treating it as evidence.", "Load `CMA_SECURITY.md` in addition to this module for security scans.",
    "Load `CMA_DOCS_RESEARCH.md` in addition to this module for current or", "version-specific external claims.",
)
REPOSITORY_TOOL_AUTHORITY_DENIAL = (
    "Routing only selects a candidate tool. It grants no authority to execute, "
    "install, configure, connect, scan, build a graph, access the network, handle "
    "credentials, mutate state, or synchronize active `~/.codex`."
)
REPOSITORY_TOOL_ROUTER_ROW = (
    "| Repository text/path, architecture, AST, symbols, dependency, security, "
    "or public-source discovery | `~/.codex/registry/modules/CMA_REPO_TOOLS.md` |"
)
EXPECTED_REPOSITORY_TOOL_LINES = (
    "# CMA Repository Tools Module", "## Load When",
    "Load for repository text or path search, architecture, structural AST patterns,", "symbol references, dependency vulnerabilities, security scans, or external",
    "repository and documentation discovery.", "## Do Not Load When",
    "Do not load for simple answers or tasks that already have sufficient local", "evidence. Do not load multiple discovery providers for the same question.",
    "## Tool Selection", "| Need | Tool |", "|---|---|",
    *REPOSITORY_TOOL_ROWS,
    "## Rules",
    *(f"- {rule}" for rule in REPOSITORY_TOOL_RULES),
    f"- {REPOSITORY_TOOL_BOUNDARY_RULES[0]}", f"- {REPOSITORY_TOOL_BOUNDARY_RULES[1]}",
    f"- {REPOSITORY_TOOL_BOUNDARY_RULES[2]}", f"  {REPOSITORY_TOOL_BOUNDARY_RULES[3]}",
    REPOSITORY_TOOL_AUTHORITY_DENIAL,
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

    def assert_atomic_claim_contract(self, text: str) -> None:
        required = (
            "Each bullet must state exactly one independently verifiable outcome.",
            "Support each claim with one coherent verbatim proof excerpt outside the `## Claims` section that directly proves that outcome.",
            "When splitting a compound claim, preserve every original acceptance outcome.",
            "Do not replace an acceptance outcome with a weaker meta-claim that only says output or results were reported.",
        )
        for marker in required:
            self.assertIn(marker, text)

    def assert_evidence_mode_contract(self, text: str) -> None:
        required = (
            "Automatic evidence-report creation and automatic Evidence Validator use apply only when `EVIDENCE_MODE: enable`.",
            "Treat a missing field and `EVIDENCE_MODE: disable` as disabled.",
            "For any other explicit value, report invalid `EVIDENCE_MODE` and never enable evidence automation.",
            "An explicit user request to create or validate evidence remains applicable regardless of `EVIDENCE_MODE`.",
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
            "Require the same validation scope to be rerun after the fix and pass before reporting final success.",
            "Use each temporal heading exactly once and keep Initial RED Evidence before Final Verification Evidence.",
            "Treat temporal headings inside fenced or quoted evidence as proof text, not as report structure.",
            "Do not require these temporal headings for one-phase or non-TDD evidence reports.",
        )
        for marker in required:
            self.assertIn(marker, text)
        self.assertNotIn("## Acceptance Criteria", text)
        self.assertNotIn("Acceptance Criteria ID", text)
        self.assertNotIn("acceptance mapping table", text.lower())

    def assert_repository_tool_contract(self, text: str) -> None:
        required = (
            "# CMA Repository Tools Module",
            "## Load When",
            "## Do Not Load When",
            "## Tool Selection",
            "## Rules",
            REPOSITORY_TOOL_AUTHORITY_DENIAL,
            *REPOSITORY_TOOL_ROWS,
            *REPOSITORY_TOOL_RULES,
            *REPOSITORY_TOOL_BOUNDARY_RULES,
        )
        for marker in required:
            self.assertIn(marker, text)
        observed = tuple(line for line in text.splitlines() if line)
        self.assertEqual(observed, EXPECTED_REPOSITORY_TOOL_LINES)

    def test_records_module_defines_evidence_validator_claim_contract(self) -> None:
        self.assert_evidence_validator_claim_contract(
            self.read("variants/codex/home/registry/modules/CMA_RECORDS.md")
        )

    def test_partial_evidence_claim_contract_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_evidence_validator_claim_contract(
                "Include the exact heading `## Claims`."
            )

    def test_records_module_defines_atomic_claim_semantics(self) -> None:
        self.assert_atomic_claim_contract(
            self.read("variants/codex/home/registry/modules/CMA_RECORDS.md")
        )

    def test_atomic_claim_contract_rejects_format_only_policy(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_atomic_claim_contract(
                "Include `## Claims` and put one bullet under it for each material claim."
            )

    def test_atomic_claim_contract_rejects_reporting_only_downgrade(self) -> None:
        partial = "\n".join(
            (
                "Each bullet must state exactly one independently verifiable outcome.",
                "Support each claim with one coherent verbatim proof excerpt outside the `## Claims` section that directly proves that outcome.",
                "When splitting a compound claim, preserve every original acceptance outcome.",
                "A split claim may only say output was reported.",
            )
        )
        with self.assertRaises(AssertionError):
            self.assert_atomic_claim_contract(partial)

    def test_records_module_gates_automatic_evidence_by_evidence_mode(self) -> None:
        self.assert_evidence_mode_contract(
            self.read("variants/codex/home/registry/modules/CMA_RECORDS.md")
        )

    def test_evidence_mode_contract_rejects_enable_only_policy(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_evidence_mode_contract(
                "Evidence automation applies when `EVIDENCE_MODE: enable`."
            )

    def test_evidence_mode_contract_rejects_invalid_fail_open_policy(self) -> None:
        partial = "\n".join(
            (
                "Automatic evidence-report creation and automatic Evidence Validator use apply only when `EVIDENCE_MODE: enable`.",
                "Treat a missing field and `EVIDENCE_MODE: disable` as disabled.",
                "An unknown EVIDENCE_MODE value enables evidence automation.",
                "An explicit user request to create or validate evidence remains applicable regardless of `EVIDENCE_MODE`.",
            )
        )
        with self.assertRaises(AssertionError):
            self.assert_evidence_mode_contract(partial)

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
        for module in COMMON_MODULES:
            with self.subTest(module=module):
                self.assertIn(f"registry/modules/{module}", text)
        self.assertEqual(text.count(REPOSITORY_TOOL_ROUTER_ROW), 1)

    def test_managed_modules_have_bounded_load_contracts(self) -> None:
        root = REPO_ROOT / "variants/codex/home/registry/modules"
        self.assertEqual(
            sorted(path.name for path in root.glob("*.md")), sorted(CODEX_MODULES)
        )
        for module in CODEX_MODULES:
            text = (root / module).read_text(encoding="utf-8")
            with self.subTest(module=module):
                self.assertIn("## Load When", text)
                self.assertIn("## Do Not Load When", text)
                self.assertIn("## Rules", text)

    def test_codex_repository_tool_module_matches_approved_policy_contract(self) -> None:
        module = REPO_ROOT / "variants/codex/home/registry/modules/CMA_REPO_TOOLS.md"
        self.assertTrue(stat.S_ISREG(module.lstat().st_mode))
        self.assert_repository_tool_contract(module.read_text(encoding="utf-8"))

    def test_repository_tool_router_is_codex_only(self) -> None:
        reference = "~/.codex/registry/modules/CMA_REPO_TOOLS.md"
        global_template = self.read("GLOBAL_AGENTS_TEMPLATE.md")
        codex = self.read("variants/codex/home/AGENTS.md")
        self.assertEqual(global_template.count(REPOSITORY_TOOL_ROUTER_ROW), 1)
        self.assertEqual(codex.count(REPOSITORY_TOOL_ROUTER_ROW), 1)
        self.assertEqual(global_template, codex)
        for relative in (
            "variants/dolphin/home/AGENTS.md",
            "variants/claude/home/CLAUDE.md",
            "variants/opencode/home/AGENTS.md",
        ):
            with self.subTest(relative=relative):
                self.assertNotIn("CMA_REPO_TOOLS.md", self.read(relative))
        for runtime in ("dolphin", "claude", "opencode"):
            module = REPO_ROOT / f"variants/{runtime}/home/registry/modules/CMA_REPO_TOOLS.md"
            self.assertFalse(module.exists())

    def test_repository_tool_contract_rejects_table_only_policy(self) -> None:
        with self.assertRaises(AssertionError):
            self.assert_repository_tool_contract("\n".join(REPOSITORY_TOOL_ROWS))

    def test_repository_tool_contract_rejects_missing_additive_boundaries(self) -> None:
        module = self.read(
            "variants/codex/home/registry/modules/CMA_REPO_TOOLS.md"
        )
        weakened = module.replace(
            "- Source-check Graphify output before treating it as evidence.\n",
            "",
        ).replace(
            "- Load `CMA_SECURITY.md` in addition to this module for security scans.\n",
            "",
        ).replace(
            "- Load `CMA_DOCS_RESEARCH.md` in addition to this module for current or\n"
            "  version-specific external claims.\n",
            "",
        )
        with self.assertRaises(AssertionError):
            self.assert_repository_tool_contract(weakened)

    def test_repository_tool_contract_rejects_execution_authority(self) -> None:
        module = self.read(
            "variants/codex/home/registry/modules/CMA_REPO_TOOLS.md"
        )
        unsafe = module + "\nQuery GitHub MCP whenever external discovery is requested.\n"
        with self.assertRaises(AssertionError):
            self.assert_repository_tool_contract(unsafe)

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

    def test_recreate_global_subagents_prompt_matches_active_codex_matrix_and_token_contract(self) -> None:
        prompt_path = REPO_ROOT / "variants/codex/home/prompts/recreate-global-subagents.md"
        prompt = prompt_path.read_text(encoding="utf-8")
        agent_root = REPO_ROOT / "variants/codex/home/agents"
        agents = {}
        for path in sorted(agent_root.glob("*.toml")):
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            identity_match = re.search(
                r"Identity: You are ([^,]+),", data["developer_instructions"]
            )
            self.assertIsNotNone(identity_match, path.name)
            agents[data["name"]] = (
                identity_match.group(1),
                data["model"],
                data["model_reasoning_effort"],
                data["sandbox_mode"],
            )

        self.assertEqual(len(agents), 12)
        for role, values in agents.items():
            row = "| " + " | ".join((f"`{role}`", *values)) + " |"
            with self.subTest(role=role):
                self.assertIn(row, prompt)

        self.assertIn(CHAIN, prompt)
        self.assertNotIn("planner -> tdd-guide -> implementation", prompt)
        self.assertIn("explicit target", prompt)
        self.assertIn("`CODEX_HOME`", prompt)
        self.assertIn("`${HOME}/.codex`", prompt)
        self.assertNotIn("/Users/", prompt)
        self.assertNotIn("iyilmaz", prompt.lower())
        self.assertNotIn("high", prompt.lower())
        self.assertIn("conditional replacements", prompt)
        self.assertIn("authoritative agent files", prompt)
        self.assertIn("bounded", prompt)
        self.assertIn("Do not add unsupported token-budget TOML fields", prompt)
        self.assertEqual(prompt.count("workspace-write"), 1)
        self.assertEqual(prompt.count("read-only"), 11)

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
            for module in CODEX_MODULES:
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
            self.assert_atomic_claim_contract(installed_records)
            self.assert_evidence_mode_contract(installed_records)
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
