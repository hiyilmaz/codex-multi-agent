import copy
import importlib.machinery
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "bin/cma-security-core-skills"
EVALS = ROOT / "tests/fixtures/security_core_skills/evals.json"
SKILLS = ("opengrep", "osv-scanner", "betterleaks")
PLATFORMS = ("codex", "claude", "opencode")
SECTIONS = (
    "Governance Metadata", "Purpose", "Use When", "Do Not Use When",
    "Preconditions", "Workflow", "Stop Conditions", "Output Contract",
    "Safety / Authority Boundary", "Tool Unavailable Behavior",
)
ROUTER_ROWS = (
    "| SAST or source security analysis | Opengrep, conditional |",
    "| Dependency CVE or package vulnerability | OSV-Scanner, conditional |",
    "| Secret exposure | Betterleaks, conditional and redacted |",
)


def expected_surfaces() -> list[Path]:
    paths = [VALIDATOR, EVALS]
    paths.extend(ROOT / f"core-skills/skills/{skill}/SKILL.md" for skill in SKILLS)
    for platform in PLATFORMS:
        for skill in SKILLS:
            base = ROOT / f"core-skills/projections/{platform}/{skill}"
            paths.append(base / "SKILL.md")
            if platform == "codex":
                paths.append(base / "agents/openai.yaml")
    return paths


class SecurityCoreSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.temp = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def require_surfaces(self) -> None:
        if any(not path.is_file() for path in expected_surfaces()):
            self.skipTest("Phase 7 production surfaces are not implemented")

    def module(self):
        self.require_surfaces()
        loader = importlib.machinery.SourceFileLoader("security_core", str(VALIDATOR))
        spec = importlib.util.spec_from_loader("security_core", loader)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def candidate(self) -> Path:
        self.require_surfaces()
        root = Path(tempfile.mkdtemp(dir=self.temp)) / "candidate"
        shutil.copytree(ROOT / "core-skills", root / "core-skills")
        target_eval = root / "tests/fixtures/security_core_skills/evals.json"
        target_eval.parent.mkdir(parents=True)
        shutil.copy2(EVALS, target_eval)
        for platform, instructions in (
            ("codex", "AGENTS.md"), ("claude", "CLAUDE.md"),
            ("opencode", "AGENTS.md"),
        ):
            for relative in (
                f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md",
                f"variants/{platform}/home/{instructions}",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
        return root

    def run_cli(self, root: Path = ROOT, *extra: str) -> subprocess.CompletedProcess[str]:
        self.require_surfaces()
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            (sys.executable, str(VALIDATOR), "validate", "--root", str(root),
             "--eval", str(root / "tests/fixtures/security_core_skills/evals.json"),
             *extra),
            cwd=ROOT, env=environment, text=True, capture_output=True, check=False,
        )

    def payload(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return json.loads(result.stdout)

    def assert_candidate_fails(
        self, root: Path, code: str, *, skill: str | None = None,
        platform: str | None = None,
    ) -> None:
        module = self.module()
        findings = module.validate_tree(
            root, root / "tests/fixtures/security_core_skills/evals.json", skill
        )
        matches = [item for item in findings if item["code"] == code]
        self.assertTrue(matches, findings)
        if skill:
            self.assertTrue(any(item.get("skill") == skill for item in matches), findings)
        if platform:
            self.assertTrue(any(item.get("platform") == platform for item in matches), findings)
        extra = ("--skill", skill) if skill else ()
        result = self.run_cli(root, *extra)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = self.payload(result)
        self.assertEqual(payload["status"], "failed")
        self.assertIs(payload["success"], False)

    def test_required_phase7_surfaces_exist_for_meaningful_red(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in expected_surfaces()
                   if not path.is_file()]
        self.assertEqual(missing, [], f"missing {len(missing)} Phase 7 surfaces: {missing}")

    def test_valid_tree_and_each_skill_validate_independently(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_tree(ROOT, EVALS), [])
        self.assertEqual(
            self.payload(self.run_cli()),
            {"findings": [], "status": "passed", "success": True},
        )
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(module.validate_tree(ROOT, EVALS, skill), [])
                self.assertEqual(self.run_cli(ROOT, "--skill", skill).returncode, 0)

    def test_canonical_sections_and_registry_authority(self) -> None:
        module = self.module()
        for skill in SKILLS:
            parsed = module.parse_skill(ROOT / f"core-skills/skills/{skill}/SKILL.md")
            with self.subTest(skill=skill):
                self.assertEqual(tuple(parsed["sections"]), SECTIONS)
                self.assertEqual(parsed["governance"]["Stable Skill ID"], skill)
                self.assertEqual(parsed["governance"]["Core / Protected Status"], "core/protected")
            root = self.candidate()
            path = root / f"core-skills/skills/{skill}/SKILL.md"
            path.write_text(path.read_text().replace(
                "Core / Protected Status: core/protected",
                "Core / Protected Status: custom",
            ), encoding="utf-8")
            self.assert_candidate_fails(root, "REGISTRY_METADATA_MISMATCH", skill=skill)

    def test_eval_prompt_oracle_is_independent_and_covers_boundaries(self) -> None:
        module = self.module()
        payload = module.load_eval(EVALS)
        self.assertGreaterEqual(len(payload["cases"]), 16)
        self.assertEqual(module.validate_eval_cases(payload), [])
        for case in payload["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(module.route_prompt(case["prompt"]), case["expected_primary"])
        renamed = copy.deepcopy(payload)
        for index, case in enumerate(renamed["cases"]):
            case["id"] = f"case-{index}"
        self.assertEqual(module.validate_eval_cases(renamed), [])
        root = self.candidate()
        path = root / "tests/fixtures/security_core_skills/evals.json"
        wrong = json.loads(path.read_text())
        for case in wrong["cases"]:
            case["prompt"] = "List the filenames in this repository."
        path.write_text(json.dumps(wrong), encoding="utf-8")
        self.assert_candidate_fails(root, "INVALID_EVAL")

    def test_required_boundaries_reject_generic_scanner_routing(self) -> None:
        markers = {
            "opengrep": "- Dependency or package vulnerability detection; use OSV-Scanner.",
            "osv-scanner": "- Source-code SAST or security-sensitive source behavior; use Opengrep.",
            "betterleaks": "- General SAST or source security analysis; use Opengrep.",
        }
        for skill, marker in markers.items():
            with self.subTest(skill=skill):
                parsed = self.module().parse_skill(
                    ROOT / f"core-skills/skills/{skill}/SKILL.md"
                )
                self.assertIn(marker, parsed["sections"]["Do Not Use When"])
                root = self.candidate()
                for platform in ("canonical", *PLATFORMS):
                    path = (root / f"core-skills/skills/{skill}/SKILL.md"
                            if platform == "canonical" else
                            root / f"core-skills/projections/{platform}/{skill}/SKILL.md")
                    path.write_text(path.read_text().replace(marker, "- Use for all security work."), encoding="utf-8")
                self.assert_candidate_fails(root, "BOUNDARY_CONTRACT_MISMATCH", skill=skill)

    def test_semantic_parity_is_normalized_not_byte_identity(self) -> None:
        module = self.module()
        for skill in SKILLS:
            fingerprints = module.semantic_fingerprints(ROOT, skill)
            with self.subTest(skill=skill):
                self.assertEqual(len(set(fingerprints.values())), 1)
            root = self.candidate()
            projection = root / f"core-skills/projections/opencode/{skill}/SKILL.md"
            projection.write_text(projection.read_text().replace("## Workflow", "\n\n## Workflow"), encoding="utf-8")
            self.assertEqual(module.validate_tree(root, root / "tests/fixtures/security_core_skills/evals.json", skill), [])
            projection.write_text(projection.read_text().replace("one primary evidence need", "all security evidence"), encoding="utf-8")
            self.assert_candidate_fails(root, "SEMANTIC_DRIFT", skill=skill, platform="opencode")

    def test_native_metadata_is_conditionally_implicit_and_platform_specific(self) -> None:
        module = self.module()
        for skill in SKILLS:
            self.assertEqual(module.validate_native_metadata(ROOT, skill), [])
            root = self.candidate()
            codex = root / f"core-skills/projections/codex/{skill}/agents/openai.yaml"
            codex.write_text(codex.read_text().replace(
                "allow_implicit_invocation: true", "allow_implicit_invocation: false"
            ), encoding="utf-8")
            self.assert_candidate_fails(root, "INVALID_NATIVE_METADATA", skill=skill, platform="codex")
            root = self.candidate()
            claude = root / f"core-skills/projections/claude/{skill}/SKILL.md"
            claude.write_text(claude.read_text().replace(
                "disable-model-invocation: true", "disable-model-invocation: false"
            ), encoding="utf-8")
            self.assert_candidate_fails(root, "INVALID_NATIVE_METADATA", skill=skill, platform="claude")

    def test_routing_is_three_distinct_compact_rows(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_routing(ROOT), [])
        for platform in PLATFORMS:
            text = (ROOT / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md").read_text()
            for row in ROUTER_ROWS:
                self.assertEqual(text.count(row), 1)
            self.assertNotIn("SAST or secret scan", text)
            self.assertNotIn("opengrep scan", text.lower())
        root = self.candidate()
        router = root / "variants/claude/home/registry/modules/CMA_REPO_TOOLS.md"
        router.write_text(router.read_text() + "\nRun opengrep scan automatically.\n", encoding="utf-8")
        self.assert_candidate_fails(root, "ROUTING_CONTRACT_MISMATCH", platform="claude")

    def test_synchronized_wrong_purpose_fails_independent_contract(self) -> None:
        root = self.candidate()
        for platform in ("canonical", *PLATFORMS):
            path = (root / "core-skills/skills/opengrep/SKILL.md" if platform == "canonical"
                    else root / f"core-skills/projections/{platform}/opengrep/SKILL.md")
            path.write_text(path.read_text().replace(
                "SAST and security-sensitive source behavior",
                "dependency CVEs and exposed credentials",
            ), encoding="utf-8")
        self.assert_candidate_fails(root, "PURPOSE_CONTRACT_MISMATCH", skill="opengrep")

    def test_synchronized_blank_required_semantics_fail_independent_contract(self) -> None:
        for heading in ("Use When", "Preconditions", "Workflow", "Stop Conditions"):
            with self.subTest(heading=heading):
                root = self.candidate()
                for platform in ("canonical", *PLATFORMS):
                    path = (root / "core-skills/skills/opengrep/SKILL.md" if platform == "canonical"
                            else root / f"core-skills/projections/{platform}/opengrep/SKILL.md")
                    text = path.read_text()
                    start = text.index(f"## {heading}\n") + len(f"## {heading}\n")
                    end = text.index("\n## ", start)
                    path.write_text(text[:start] + "\n" + text[end:], encoding="utf-8")
                self.assert_candidate_fails(root, "SEMANTIC_CONTRACT_MISMATCH", skill="opengrep")

    def test_eval_rejection_and_overlap_classes_are_enforced(self) -> None:
        module = self.module()
        payload = module.load_eval(EVALS)
        overlap = [case for case in payload["cases"] if case.get("case_type") == "overlap"]
        self.assertGreaterEqual(len(overlap), 3)
        for case in overlap:
            self.assertGreaterEqual(len(module.prompt_signals(case["prompt"])), 2)
        incomplete = copy.deepcopy(payload)
        incomplete["cases"][0]["rejected_skills"] = []
        self.assertTrue(any(item["code"] == "INVALID_EVAL"
                            for item in module.validate_eval_cases(incomplete)))
        mislabeled = copy.deepcopy(payload)
        single_signal = {
            "overlap-opengrep": ("Review this authorization source change.", "opengrep",
                                  ["osv-scanner", "betterleaks"]),
            "overlap-osv": ("Check this vulnerable dependency.", "osv-scanner",
                             ["opengrep", "betterleaks"]),
            "overlap-betterleaks": ("Check this exposed credential.", "betterleaks",
                                     ["opengrep", "osv-scanner"]),
        }
        for case in mislabeled["cases"]:
            if case["id"] in single_signal:
                case["prompt"], case["expected_primary"], case["rejected_skills"] = single_signal[case["id"]]
        self.assertTrue(any(item == {"code": "INVALID_EVAL", "field": "overlap"}
                            for item in module.validate_eval_cases(mislabeled)))


if __name__ == "__main__":
    unittest.main()
