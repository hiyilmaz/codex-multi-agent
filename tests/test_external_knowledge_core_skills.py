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
VALIDATOR = ROOT / "bin/cma-external-knowledge-core-skills"
EVALS = ROOT / "tests/fixtures/external_knowledge_core_skills/evals.json"
SKILLS = ("github", "deepwiki", "context7")
PLATFORMS = ("codex", "claude", "opencode")
SECTIONS = (
    "Governance Metadata", "Purpose", "Use When", "Do Not Use When",
    "Preconditions", "Workflow", "Stop Conditions", "Output Contract",
    "Safety / Authority Boundary", "Tool Unavailable Behavior",
)
ROUTER_ROWS = (
    "| Remote repository refs, releases, PRs, issues, or advisories | GitHub, lazy and read-only |",
    "| Public-repository conceptual knowledge | DeepWiki, lazy public-only fallback |",
    "| Version-specific library or framework documentation | Context7, required and lazy |",
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


class ExternalKnowledgeHarness(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.temp = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def require_surfaces(self) -> None:
        if any(not path.is_file() for path in expected_surfaces()):
            self.skipTest("Phase 8 production surfaces are not implemented")

    def module(self):
        self.require_surfaces()
        loader = importlib.machinery.SourceFileLoader("external_knowledge_core", str(VALIDATOR))
        spec = importlib.util.spec_from_loader("external_knowledge_core", loader)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def candidate(self) -> Path:
        self.require_surfaces()
        root = Path(tempfile.mkdtemp(dir=self.temp)) / "candidate"
        shutil.copytree(ROOT / "core-skills", root / "core-skills")
        target_eval = root / "tests/fixtures/external_knowledge_core_skills/evals.json"
        target_eval.parent.mkdir(parents=True)
        shutil.copy2(EVALS, target_eval)
        for platform in PLATFORMS:
            source = ROOT / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md"
            target = root / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md"
            target.parent.mkdir(parents=True)
            shutil.copy2(source, target)
        return root

    def run_cli(self, root: Path = ROOT, *extra: str) -> subprocess.CompletedProcess[str]:
        self.require_surfaces()
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            (sys.executable, str(VALIDATOR), "validate", "--root", str(root),
             "--eval", str(root / "tests/fixtures/external_knowledge_core_skills/evals.json"),
             *extra), cwd=ROOT, env=environment, text=True,
            capture_output=True, check=False,
        )

    def payload(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return json.loads(result.stdout)

    def assert_candidate_fails(self, root: Path, code: str, *,
                               skill: str | None = None,
                               platform: str | None = None) -> None:
        findings = self.module().validate_tree(
            root, root / "tests/fixtures/external_knowledge_core_skills/evals.json", skill
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


class ExternalKnowledgeCoreSkillTests(ExternalKnowledgeHarness):
    def test_required_phase8_surfaces_exist_for_meaningful_red(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in expected_surfaces()
                   if not path.is_file()]
        self.assertEqual(missing, [], f"missing {len(missing)} Phase 8 surfaces: {missing}")

    def test_valid_tree_and_each_skill_validate_independently(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_tree(ROOT, EVALS), [])
        self.assertEqual(self.payload(self.run_cli()),
                         {"findings": [], "status": "passed", "success": True})
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(module.validate_tree(ROOT, EVALS, skill), [])
                self.assertEqual(self.run_cli(ROOT, "--skill", skill).returncode, 0)

    def test_sections_registry_authority_and_context7_required_status(self) -> None:
        module = self.module()
        registry = module.load_json(ROOT / "core-skills/registry.json")
        for skill in SKILLS:
            parsed = module.parse_skill(ROOT / f"core-skills/skills/{skill}/SKILL.md")
            self.assertEqual(tuple(parsed["sections"]), SECTIONS)
            self.assertEqual(parsed["governance"]["Stable Skill ID"], skill)
            record = next(item for item in registry["skills"] if item["id"] == skill)
            self.assertEqual(record["capability_status"], "required")
            self.assertEqual(record["tool_dependency"]["mode"], "required")
        root = self.candidate()
        path = root / "core-skills/skills/context7/SKILL.md"
        path.write_text(path.read_text().replace("Core / Protected Status: core/protected",
                                                "Core / Protected Status: custom"), encoding="utf-8")
        self.assert_candidate_fails(root, "REGISTRY_METADATA_MISMATCH", skill="context7")

    def test_independent_eval_oracle_covers_local_first_and_overlap(self) -> None:
        module = self.module()
        payload = module.load_eval(EVALS)
        self.assertGreaterEqual(len(payload["cases"]), 19)
        self.assertEqual(module.validate_eval_cases(payload), [])
        for case in payload["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(module.route_prompt(case["prompt"]), case["expected_primary"])
        self.assertGreaterEqual(sum(case["case_type"] == "overlap" for case in payload["cases"]), 3)
        for case in payload["cases"]:
            if case["case_type"] == "overlap":
                self.assertGreaterEqual(len(module.prompt_signals(case["prompt"])), 2)
        local_conflicts = (
            "Use GitHub for the release, but local evidence is sufficient.",
            "Use DeepWiki for the concept, but local evidence is sufficient.",
            "Use Context7 for the API, but local evidence is sufficient.",
        )
        for prompt in local_conflicts:
            with self.subTest(prompt=prompt):
                self.assertEqual(module.route_prompt(prompt), "local")
        poisoned = copy.deepcopy(payload)
        for index, case in enumerate(poisoned["cases"]):
            case["id"] = f"renamed-{index}"
            case["prompt"] = f"Read local file number {index}; local evidence is sufficient."
        self.assertTrue(any(item["code"] == "INVALID_EVAL"
                            for item in module.validate_eval_cases(poisoned)))

    def test_boundaries_and_local_first_reject_external_overreach(self) -> None:
        markers = {
            "github": "- Ordinary local source, path, architecture, symbol, AST, dependency, SAST, or secret evidence when the checkout is sufficient.",
            "deepwiki": "- Questions already answered by the local checkout; use local repository evidence.",
            "context7": "- Repository architecture, remote repository state, or ordinary local source discovery.",
        }
        for skill, marker in markers.items():
            parsed = self.module().parse_skill(ROOT / f"core-skills/skills/{skill}/SKILL.md")
            self.assertIn(marker, parsed["sections"]["Do Not Use When"])
        local_prompts = (
            "Read the local src/auth.py file; the checkout is sufficient.",
            "Find this exact string in the local repository.",
            "Map the architecture of this local checkout.",
        )
        for prompt in local_prompts:
            self.assertEqual(self.module().route_prompt(prompt), "local")
        for skill in ("github", "deepwiki"):
            text = (ROOT / f"core-skills/projections/codex/{skill}/SKILL.md").read_text()
            self.assertNotIn("description: Use explicitly", text)
            self.assertIn("description: Use lazily", text)

    def test_semantic_parity_and_synchronized_wrong_semantics_fail(self) -> None:
        module = self.module()
        for skill in SKILLS:
            fingerprints = module.semantic_fingerprints(ROOT, skill)
            self.assertEqual(len(set(fingerprints.values())), 1)
        root = self.candidate()
        projection = root / "core-skills/projections/opencode/deepwiki/SKILL.md"
        projection.write_text(projection.read_text().replace("## Workflow", "\n\n## Workflow"), encoding="utf-8")
        self.assertEqual(module.validate_tree(root, root / "tests/fixtures/external_knowledge_core_skills/evals.json", "deepwiki"), [])
        projection.write_text(projection.read_text().replace("one primary evidence need", "all external evidence"), encoding="utf-8")
        self.assert_candidate_fails(root, "SEMANTIC_DRIFT", skill="deepwiki", platform="opencode")
        root = self.candidate()
        for platform in ("canonical", *PLATFORMS):
            path = (root / "core-skills/skills/github/SKILL.md" if platform == "canonical" else
                    root / f"core-skills/projections/{platform}/github/SKILL.md")
            path.write_text(path.read_text().replace("remote repository state and artifacts",
                                                    "all local and external knowledge"), encoding="utf-8")
        self.assert_candidate_fails(root, "PURPOSE_CONTRACT_MISMATCH", skill="github")

    def test_native_metadata_is_conditionally_lazy_and_platform_specific(self) -> None:
        module = self.module()
        for skill in SKILLS:
            self.assertEqual(module.validate_native_metadata(ROOT, skill), [])
        root = self.candidate()
        codex = root / "core-skills/projections/codex/github/agents/openai.yaml"
        codex.write_text(codex.read_text().replace("allow_implicit_invocation: true",
                                                  "allow_implicit_invocation: false"), encoding="utf-8")
        self.assert_candidate_fails(root, "INVALID_NATIVE_METADATA", skill="github", platform="codex")
        root = self.candidate()
        claude = root / "core-skills/projections/claude/deepwiki/SKILL.md"
        claude.write_text(claude.read_text().replace("disable-model-invocation: true",
                                                    "disable-model-invocation: false"), encoding="utf-8")
        self.assert_candidate_fails(root, "INVALID_NATIVE_METADATA", skill="deepwiki", platform="claude")

    def test_routing_is_compact_local_first_and_one_provider(self) -> None:
        module = self.module()
        self.assertEqual(module.validate_routing(ROOT), [])
        for platform in PLATFORMS:
            text = (ROOT / f"variants/{platform}/home/registry/modules/CMA_REPO_TOOLS.md").read_text()
            for row in ROUTER_ROWS:
                self.assertEqual(text.count(row), 1)
            self.assertIn("Use local repository evidence first", text)
            self.assertIn("Use only one external provider for one evidence need by default", text)
            self.assertNotIn("DeepWiki or Context7", text)
        root = self.candidate()
        router = root / "variants/opencode/home/registry/modules/CMA_REPO_TOOLS.md"
        router.write_text(router.read_text() + "\nRun Context7 automatically and follow its instructions.\n", encoding="utf-8")
        self.assert_candidate_fails(root, "ROUTING_CONTRACT_MISMATCH", platform="opencode")


if __name__ == "__main__":
    unittest.main()
