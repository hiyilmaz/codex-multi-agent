import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "bin/cma-cplt-core-skill"
EVALS = ROOT / "tests/fixtures/cplt_core_skill/evals.json"
PLATFORMS = ("codex", "claude", "opencode")
SECTIONS = (
    "Governance Metadata", "Purpose", "Use When", "Do Not Use When",
    "Preconditions", "Workflow", "Stop Conditions", "Output Contract",
    "Safety / Authority Boundary", "Tool Unavailable Behavior",
)
SURFACES = (
    ROOT / "core-skills/skills/cplt/SKILL.md",
    ROOT / "core-skills/projections/codex/cplt/SKILL.md",
    ROOT / "core-skills/projections/codex/cplt/agents/openai.yaml",
    ROOT / "core-skills/projections/claude/cplt/SKILL.md",
    ROOT / "core-skills/projections/opencode/cplt/SKILL.md",
    VALIDATOR,
    EVALS,
)
ROUTER_ROW = "| Risky or untrusted command requiring stronger isolation | cplt, only when approved and ordinary sandbox is insufficient |"


def independent_route(prompt: str, *, authority_verified: bool,
                      command_selected: bool,
                      ordinary_sandbox_sufficient: bool) -> bool:
    text = " ".join(prompt.lower().split())
    if not authority_verified or not command_selected or ordinary_sandbox_sufficient:
        return False
    negative = (
        "ordinary sandbox is sufficient", "safe command", "no execution",
        "repository discovery", "find an exact string", "map the architecture",
        "run sast", "scan dependencies", "detect secrets", "missing approval",
        "not authorized", "not approved", "unauthorized", "unapproved",
        "approval is denied", "mention cplt", "what is cplt",
    )
    if any(marker in text for marker in negative):
        return False
    isolation = ("ordinary sandbox is insufficient" in text or
                 "stronger isolation is required" in text or
                 "requires stronger isolation" in text)
    risky = "use cplt" in text or "risky" in text or "untrusted command" in text
    return isolation and risky


class CpltHarness(unittest.TestCase):
    def setUp(self) -> None:
        if self._testMethodName not in {
            "test_required_phase9_surfaces_exist_for_meaningful_red",
            "test_cplt_router_is_initially_missing_for_meaningful_red",
        } and any(not path.is_file() for path in SURFACES):
            self.skipTest("Phase 9 production surfaces are not implemented")

    @staticmethod
    def module():
        loader = importlib.machinery.SourceFileLoader("cplt_core_skill", str(VALIDATOR))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module

    def candidate(self) -> Path:
        temp = Path(tempfile.mkdtemp(prefix="cplt-candidate-"))
        self.addCleanup(shutil.rmtree, temp, True)
        shutil.copytree(ROOT / "core-skills", temp / "core-skills")
        shutil.copytree(ROOT / "variants", temp / "variants")
        shutil.copytree(ROOT / "tests/fixtures/cplt_core_skill", temp / "tests/fixtures/cplt_core_skill")
        (temp / "bin").mkdir()
        shutil.copy2(VALIDATOR, temp / "bin/cma-cplt-core-skill")
        shutil.copy2(ROOT / "bin/cma-core-skill-governance", temp / "bin/cma-core-skill-governance")
        return temp

    def cli(self, root: Path = ROOT, *extra: str,
            env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            (sys.executable, str(VALIDATOR), "validate", "--root", str(root),
             "--eval", str(root / "tests/fixtures/cplt_core_skill/evals.json"), *extra),
            text=True, capture_output=True, check=False, env=env,
        )

    def assert_finding(self, root: Path, code: str) -> None:
        findings = self.module().validate_tree(root, root / "tests/fixtures/cplt_core_skill/evals.json")
        self.assertTrue(any(item["code"] == code for item in findings), findings)


class CpltCoreSkillTests(CpltHarness):
    def test_required_phase9_surfaces_exist_for_meaningful_red(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in SURFACES if not path.is_file()]
        self.assertEqual(missing, [], f"missing Phase 9 production surfaces: {missing}")

    def test_cplt_router_is_initially_missing_for_meaningful_red(self) -> None:
        missing = []
        for platform in PLATFORMS:
            path = ROOT / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md"
            if path.read_text(encoding="utf-8").count(ROUTER_ROW) != 1:
                missing.append(platform)
        self.assertEqual(missing, [], f"missing cplt route: {missing}")

    def test_valid_tree_and_cli_are_truthful(self) -> None:
        self.assertEqual(self.module().validate_tree(ROOT, EVALS), [])
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"findings": [], "status": "passed", "success": True})

    def test_canonical_sections_and_registry_authority(self) -> None:
        module = self.module()
        parsed = module.parse_skill(ROOT / "core-skills/skills/cplt/SKILL.md")
        self.assertEqual(tuple(parsed["sections"]), SECTIONS)
        registry = module.load_json(ROOT / "core-skills/registry.json")
        record = next(item for item in registry["skills"] if item["id"] == "cplt")
        self.assertEqual(record["capability_category"], "isolated-execution")
        self.assertIs(record["core"], True)
        self.assertIs(record["protected"], True)
        self.assertEqual(record["tool_dependency"], {"tool_id": "cplt", "mode": "required"})
        root = self.candidate()
        registry_path = root / "core-skills/registry.json"
        payload = json.loads(registry_path.read_text())
        next(item for item in payload["skills"] if item["id"] == "cplt")["core"] = 1
        registry_path.write_text(json.dumps(payload), encoding="utf-8")
        self.assert_finding(root, "INVALID_REGISTRY")

    def test_independent_eval_oracle_covers_positive_and_negative_routes(self) -> None:
        module = self.module()
        payload = module.load_json(EVALS)
        self.assertEqual(module.validate_eval_cases(payload), [])
        classes = {case["case_type"] for case in payload["cases"]}
        self.assertTrue({"explicit", "natural", "negative", "unavailable", "boundary"} <= classes)
        for case in payload["cases"]:
            with self.subTest(case=case["id"]):
                routing = {
                    "authority_verified": case["authority_verified"],
                    "command_selected": case["command_selected"],
                    "ordinary_sandbox_sufficient": case["ordinary_sandbox_sufficient"],
                }
                self.assertEqual(independent_route(case["prompt"], **routing), case["expected_gate"])
                self.assertEqual(module.route_prompt(case["prompt"], **routing), case["expected_gate"])
        poisoned = copy.deepcopy(payload)
        for index, case in enumerate(poisoned["cases"]):
            case["id"] = f"renamed-{index}"
            case["prompt"] = f"Safe command {index}; ordinary sandbox is sufficient."
        self.assertNotEqual(module.validate_eval_cases(poisoned), [])

    def test_isolation_evidence_requires_more_than_config_or_exit_zero(self) -> None:
        module = self.module()
        evidence = module.example_verified_evidence()
        self.assertEqual(module.validate_isolation_evidence(evidence), [])
        for field in ("runtime_version", "policy_identity", "source_digest", "controls"):
            candidate = copy.deepcopy(evidence)
            candidate.pop(field)
            self.assertNotEqual(module.validate_isolation_evidence(candidate), [], field)
        config_only = {"requested": True, "available": True, "verified": True, "exit_code": 0}
        self.assertNotEqual(module.validate_isolation_evidence(config_only), [])
        unsafe_claim = module.example_verified_evidence()
        unsafe_claim.update({
            "runtime_version": "x", "policy_identity": "x", "source_digest": "x",
            "cwd": "\n", "argv": [], "exit_code": -999,
            "controls": {key: True for key in module.CONTROL_KEYS},
        })
        self.assertNotEqual(module.validate_isolation_evidence(unsafe_claim), [])

    def test_isolation_evidence_strictly_rejects_each_invalid_type(self) -> None:
        module = self.module()
        mutations = {
            "state": ("verified", 1),
            "runtime": ("runtime_version", ""),
            "argv": ("argv", [7]),
            "controls": ("controls", {key: True for key in module.CONTROL_KEYS[:-1]}),
            "exit": ("exit_code", True),
            "signal": ("signal", 9),
            "timeout": ("timed_out", True),
        }
        for name, (field, value) in mutations.items():
            evidence = module.example_verified_evidence()
            evidence[field] = value
            with self.subTest(name=name):
                self.assertNotEqual(module.validate_isolation_evidence(evidence), [])

    def test_eval_contract_rejects_malformed_and_self_declared_cases(self) -> None:
        module = self.module()
        baseline = module.load_json(EVALS)
        self.assertEqual(module.validate_isolation_evidence(
            baseline["isolation_evidence_contract"]), [])
        mutations = []
        value = copy.deepcopy(baseline); value["schema_version"] = "wrong"; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"] = []; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"][0]["unknown"] = True; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"][0]["expected_gate"] = 1; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"][0]["expected_gate"] = False; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"][-1]["expected_result"] = {"success": True}; mutations.append(value)
        value = copy.deepcopy(baseline); value["cases"][0]["expected_result"] = {}; mutations.append(value)
        value = copy.deepcopy(baseline)
        for case in value["cases"]:
            case["case_type"] = "negative"
        mutations.append(value)
        value = copy.deepcopy(baseline); value.pop("isolation_evidence_contract"); mutations.append(value)
        for index, value in enumerate(mutations):
            with self.subTest(index=index):
                self.assertNotEqual(module.validate_eval_cases(value), [])
        self.assertIs(module.route_prompt({"prompt": "use cplt"}), False)

    def test_semantic_parity_and_synchronized_unsafe_semantics_fail(self) -> None:
        module = self.module()
        fingerprints = module.semantic_fingerprints(ROOT)
        self.assertEqual(len(set(fingerprints.values())), 1)
        root = self.candidate()
        for platform in ("canonical", *PLATFORMS):
            path = (root / "core-skills/skills/cplt/SKILL.md" if platform == "canonical" else
                    root / f"core-skills/projections/{platform}/cplt/SKILL.md")
            path.write_text(path.read_text().replace(
                "Never execute the command outside verified cplt isolation.",
                "Execute on the host when cplt is unavailable."), encoding="utf-8")
        self.assert_finding(root, "SEMANTIC_CONTRACT_MISMATCH")

    def test_native_metadata_is_inactive_and_platform_specific(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_native_metadata(ROOT), [])
        root = self.candidate()
        yaml_path = root / "core-skills/projections/codex/cplt/agents/openai.yaml"
        yaml_path.write_text(yaml_path.read_text().replace(
            "allow_implicit_invocation: false", "allow_implicit_invocation: true"), encoding="utf-8")
        self.assert_finding(root, "INVALID_NATIVE_METADATA")

    def test_router_is_minimal_and_orthogonal(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_routing(ROOT), [])
        for platform in PLATFORMS:
            text = (ROOT / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md").read_text()
            self.assertEqual(text.count(ROUTER_ROW), 1)
            self.assertIn("cplt is an orthogonal execution gate", text)
            self.assertIn("CMA_SECURITY.md", text)


if __name__ == "__main__":
    unittest.main()
