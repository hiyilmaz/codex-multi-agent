import copy
import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "core-skills" / "profiles" / "claude.json"
VALIDATOR = REPO_ROOT / "bin" / "cma-claude-core-skill-profile"
REGISTRY = REPO_ROOT / "core-skills" / "registry.json"
STANDARD = REPO_ROOT / "core-skills" / "STANDARD.md"
CANONICAL_FIELDS = {
    "stable_skill_id", "display_name", "capability_category",
    "core_protected_status", "tool_dependency", "semantic_version", "purpose",
    "use_when", "do_not_use_when", "preconditions", "workflow",
    "stop_conditions", "output_contract", "safety_authority_boundary",
    "tool_unavailable_behavior",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ClaudeCoreSkillProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def profile(self) -> dict:
        return json.loads(PROFILE.read_text(encoding="utf-8"))

    def registry(self) -> dict:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def write_json(self, name: str, value: object) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def load_validator(self, path: Path = VALIDATOR):
        loader = importlib.machinery.SourceFileLoader("claude_profile", str(path))
        spec = importlib.util.spec_from_loader("claude_profile", loader)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_cli(
        self,
        profile: Path = PROFILE,
        *extra: str,
        registry: Path = REGISTRY,
        validator: Path = VALIDATOR,
        suppress_bytecode: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        if suppress_bytecode:
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
        else:
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
        return subprocess.run(
            (
                sys.executable, str(validator), "validate", "--profile",
                str(profile), "--registry", str(registry), *extra,
            ),
            cwd=REPO_ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def payload(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return json.loads(result.stdout)

    def assert_fails(self, candidate: dict, code: str, field: str | None = None) -> None:
        module = self.load_validator()
        findings = module.validate_profile(candidate, self.registry())
        matches = [item for item in findings if item["code"] == code]
        self.assertTrue(matches, findings)
        if field is not None:
            self.assertTrue(any(item.get("field") == field for item in matches), findings)
        result = self.run_cli(self.write_json("candidate.json", candidate))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = self.payload(result)
        self.assertEqual(payload["status"], "failed")
        self.assertIs(payload["success"], False)
        self.assertTrue(any(item["code"] == code for item in payload["findings"]))

    def test_profile_exists_for_meaningful_red(self) -> None:
        self.assertTrue(PROFILE.is_file(), f"missing Claude profile: {PROFILE}")

    def test_validator_exists_for_meaningful_red(self) -> None:
        self.assertTrue(VALIDATOR.is_file(), f"missing Claude validator: {VALIDATOR}")

    def test_valid_profile_maps_all_canonical_fields_once(self) -> None:
        profile = self.profile()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.payload(result), {"findings": [], "status": "passed", "success": True})
        self.assertEqual(self.load_validator().validate_profile(profile, self.registry()), [])
        fields = [item["canonical_field"] for item in profile["field_mappings"]]
        self.assertEqual(set(fields), CANONICAL_FIELDS)
        self.assertEqual(len(fields), len(set(fields)))
        for case in ("missing", "duplicate", "unknown", "unhashable"):
            with self.subTest(case=case):
                candidate = self.profile()
                if case == "missing":
                    candidate["field_mappings"].pop()
                    code = "MISSING_MAPPING"
                elif case == "duplicate":
                    candidate["field_mappings"].append(copy.deepcopy(candidate["field_mappings"][0]))
                    code = "DUPLICATE_MAPPING"
                elif case == "unknown":
                    candidate["field_mappings"].append({
                        "canonical_field": "invented", "canonical_source": "settings.json",
                        "claude_targets": [".mcp.json"],
                    })
                    code = "UNKNOWN_MAPPING"
                else:
                    candidate["field_mappings"][0]["canonical_field"] = []
                    code = "UNKNOWN_MAPPING"
                self.assert_fails(candidate, code)

    def test_registry_is_exact_authority_and_cannot_self_shrink(self) -> None:
        for field in ("display_name", "core_protected_status", "tool_dependency"):
            with self.subTest(field=field):
                candidate = self.profile()
                mapping = next(item for item in candidate["field_mappings"] if item["canonical_field"] == field)
                mapping["canonical_source"] = "SKILL.md.frontmatter"
                self.assert_fails(candidate, "CANONICAL_AUTHORITY_VIOLATION", field)
        module = self.load_validator()
        cases = []
        registry = self.registry()
        candidate = copy.deepcopy(registry)
        candidate["skills"] = candidate["skills"][:1]
        candidate["protected_core_ids"] = [candidate["skills"][0]["id"]]
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["platforms"] = "claude"
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["skills"].append(copy.deepcopy(candidate["skills"][0]))
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["skills"][0]["protected"] = 1
        cases.append(candidate)
        for index, candidate in enumerate(cases):
            findings = module.validate_registry_authority(candidate)
            self.assertTrue(findings)
            path = self.write_json(f"registry-{index}.json", candidate)
            result = self.run_cli(registry=path)
            self.assertEqual(result.returncode, 1)
            self.assertIs(self.payload(result)["success"], False)

    def test_native_structure_and_discovery_are_claude_specific(self) -> None:
        profile = self.profile()
        native = profile["native_skill"]
        self.assertEqual(native["official_required_files"], ["SKILL.md"])
        self.assertEqual(
            native["cma_frontmatter"],
            {"name": "<skill-id>", "description": "required-non-empty", "disable-model-invocation": True, "user-invocable": True},
        )
        discovery = profile["discovery"]
        self.assertIn("~/.claude/skills/<skill-id>/SKILL.md", discovery["scopes"])
        self.assertIn(".claude/skills in CWD and ancestors to repository root", discovery["scopes"])
        self.assertEqual(discovery["standalone_precedence"], ["enterprise", "personal", "project"])
        self.assertEqual(discovery["plugin_namespace"], "/<plugin-name>:<skill-id>")
        candidate = self.profile()
        candidate["discovery"]["scopes"][1] = "$HOME/.agents/skills"
        self.assert_fails(candidate, "UNSUPPORTED_CLAUDE_DISCOVERY", "discovery")
        candidate = self.profile()
        candidate["native_skill"]["official_required_files"].append("agents/openai.yaml")
        self.assert_fails(candidate, "UNSUPPORTED_CLAUDE_STRUCTURE", "native_skill")

    def test_activation_is_inactive_lazy_and_explicit_only(self) -> None:
        activation = self.profile()["activation"]
        self.assertEqual(activation["profile_state"], "inactive-representation-only")
        self.assertEqual(activation["projected_skill_instances"], 0)
        self.assertEqual(activation["default_mode"], "explicit-only")
        self.assertEqual(activation["explicit_invocation"], {"enabled": True, "method": "/<skill-id>"})
        self.assertEqual(activation["implicit_invocation"]["opted_in_skill_ids"], [])
        self.assertEqual(activation["disabled_core_ids"], [])
        self.assertEqual(activation["skill_overrides"], {})
        for field, value in (
            ("disable-model-invocation", False),
            ("disable-model-invocation", 1),
            ("user-invocable", "true"),
        ):
            candidate = self.profile()
            candidate["native_skill"]["cma_frontmatter"][field] = value
            self.assert_fails(candidate, "INVALID_ACTIVATION_POLICY", "native_skill.cma_frontmatter")
        candidate = self.profile()
        candidate["activation"]["implicit_invocation"]["opted_in_skill_ids"] = ["graphify"]
        self.assert_fails(candidate, "INVALID_ACTIVATION_POLICY", "activation")
        candidate = self.profile()
        candidate["activation"]["disabled_core_ids"] = ["graphify"]
        self.assert_fails(candidate, "CORE_DISABLE_FORBIDDEN", "activation.disabled_core_ids")

    def test_claude_metadata_cannot_change_canonical_fingerprint(self) -> None:
        module = self.load_validator()
        profile, registry = self.profile(), self.registry()
        first = module.canonical_fingerprint(profile, registry, {"argument-hint": "[file]"})
        second = module.canonical_fingerprint(profile, registry, {"argument-hint": "[path]"})
        self.assertEqual(first, second)
        for metadata in (
            {"allowed-tools": "Bash(*)"}, {"model": "opus"}, {"context": "fork"},
            {"hooks": {}}, {"disable-model-invocation": False}, {"unknown": "x"},
        ):
            with self.assertRaises(module.InputError):
                module.canonical_fingerprint(profile, registry, metadata)
        candidate = self.profile()
        candidate["claude_metadata"]["nonsemantic_frontmatter"].append("allowed-tools")
        self.assert_fails(candidate, "BEHAVIORAL_METADATA_FORBIDDEN", "claude_metadata")

    def test_tool_unavailable_and_integration_boundaries_fail_closed(self) -> None:
        profile = self.profile()
        unavailable = profile["tool_unavailable_behavior"]
        self.assertEqual(unavailable["none"]["availability"], "not_applicable")
        self.assertIs(unavailable["required"]["success"], False)
        self.assertEqual(unavailable["required"]["action"], "stop")
        self.assertIn("silent-fallback", unavailable["forbidden"])
        candidate = self.profile()
        candidate["tool_unavailable_behavior"]["required"]["success"] = 0
        self.assert_fails(candidate, "INVALID_UNAVAILABLE_BEHAVIOR", "tool_unavailable_behavior")
        boundary = profile["integration_boundaries"]
        self.assertEqual(boundary["plugins"], "future-packaging-only-not-enabled")
        self.assertEqual(boundary["mcp"], "not-configured-or-activated")
        self.assertEqual(boundary["agents"], "not-created-or-preloaded")
        self.assertEqual(boundary["sdk_skill_filter"], "context-filter-not-sandbox")
        candidate = self.profile()
        candidate["integration_boundaries"]["mcp"] = "auto-start"
        self.assert_fails(candidate, "INTEGRATION_BOUNDARY_VIOLATION", "integration_boundaries")

    def test_claude_md_contract_is_routing_only(self) -> None:
        contract = self.profile()["global_instructions"]
        self.assertEqual(contract["mode"], "routing-only")
        self.assertEqual(contract["reference_form"], "evidence need -> /<skill-id> (user invokes)")
        self.assertIs(contract["claude_md"]["reads_agents_md_directly"], False)
        self.assertEqual(contract["claude_md"]["merge"], "concatenate-root-to-CWD; local-after-shared; nested-on-demand")
        candidate = self.profile()
        candidate["global_instructions"]["mode"] = "embedded-skill-body"
        self.assert_fails(candidate, "GLOBAL_ROUTING_VIOLATION", "global_instructions")
        candidate = self.profile()
        candidate["global_instructions"]["claude_md"]["reads_agents_md_directly"] = True
        self.assert_fails(candidate, "GLOBAL_ROUTING_VIOLATION", "global_instructions")

    def test_validator_is_read_only_and_malformed_input_is_structured(self) -> None:
        watched = (PROFILE, REGISTRY, STANDARD)
        before = {path: (digest(path), path.stat().st_mode, path.read_bytes()) for path in watched}
        bin_before = {
            path.relative_to(REPO_ROOT / "bin"): (digest(path), path.stat().st_mode)
            for path in (REPO_ROOT / "bin").rglob("*") if path.is_file()
        }
        self.assertEqual(self.run_cli(suppress_bytecode=False).returncode, 0)
        for flag in ("--apply", "--install", "--sync", "--activate", "--enable-plugin"):
            result = self.run_cli(PROFILE, flag)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
        malformed = self.root / "malformed.json"
        malformed.write_text("{bad", encoding="utf-8")
        result = self.run_cli(malformed)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.payload(result)["status"], "invalid")
        duplicate = self.root / "duplicate.json"
        duplicate.write_text('{"schema_version":"a","schema_version":"b"}\n', encoding="utf-8")
        result = self.run_cli(duplicate)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.payload(result)["status"], "invalid")
        for path, snapshot in before.items():
            self.assertEqual((digest(path), path.stat().st_mode, path.read_bytes()), snapshot)
        bin_after = {
            path.relative_to(REPO_ROOT / "bin"): (digest(path), path.stat().st_mode)
            for path in (REPO_ROOT / "bin").rglob("*") if path.is_file()
        }
        self.assertEqual(bin_after, bin_before)

    def test_secure_registry_dependency_reuse(self) -> None:
        attack = self.root / "attack"
        attack.mkdir()
        linked = attack / VALIDATOR.name
        linked.symlink_to(VALIDATOR)
        marker = attack / "executed"
        (attack / "cma-core-skill-governance").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n",
            encoding="utf-8",
        )
        result = self.run_cli(validator=linked)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists())
        for case in ("missing", "corrupt", "symlink"):
            isolated = self.root / case
            isolated.mkdir()
            copied = isolated / VALIDATOR.name
            shutil.copyfile(VALIDATOR, copied)
            dependency = isolated / "cma-core-skill-governance"
            if case == "corrupt":
                dependency.write_text("invalid python !!!\n", encoding="utf-8")
            elif case == "symlink":
                dependency.symlink_to(REPO_ROOT / "bin" / "cma-core-skill-governance")
            result = self.run_cli(validator=copied)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            payload = self.payload(result)
            self.assertIs(payload["success"], False)
            self.assertNotIn(str(isolated), result.stdout + result.stderr)

    def test_registry_findings_do_not_disclose_candidate_values(self) -> None:
        secret = "SECRET_TOKEN_123"
        candidate = self.registry()
        candidate["schema_version"] = secret
        path = self.write_json("secret-registry.json", candidate)
        result = self.run_cli(registry=path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = self.payload(result)
        self.assertEqual(payload["status"], "failed")
        self.assertIs(payload["success"], False)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertTrue(all(set(item) <= {"code", "field"} for item in payload["findings"]))

    def test_validator_internal_error_paths_are_truthful(self) -> None:
        module = self.load_validator()
        valid = self.write_json("valid.json", self.profile())
        self.assertEqual(module.load_json(valid), self.profile())
        for name, content in (
            ("malformed-direct.json", "{bad"),
            ("duplicate-direct.json", '{"a":1,"a":2}'),
            ("array-direct.json", "[]"),
        ):
            path = self.root / name
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(module.InputError):
                module.load_json(path)
        self.assertEqual(
            module.finding("X", "field", False),
            {"code": "X", "field": "field", "observed": False},
        )

        candidate = self.profile()
        candidate["unknown"] = True
        candidate["schema_version"] = "wrong"
        candidate["field_mappings"] = "not-a-list"
        findings = module.validate_profile(candidate, self.registry())
        self.assertTrue(any(item["code"] == "INVALID_PROFILE_SCHEMA" for item in findings))
        self.assertTrue(any(item["code"] == "MISSING_MAPPING" for item in findings))

        candidate = self.profile()
        candidate["field_mappings"].append("bad-item")
        self.assertTrue(any(item["code"] == "UNKNOWN_MAPPING" for item in module.validate_profile(candidate, self.registry())))
        candidate = self.profile()
        candidate["field_mappings"][0]["claude_targets"] = ["settings.json"]
        self.assert_fails(candidate, "UNSUPPORTED_CLAUDE_MAPPING", "stable_skill_id")
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(candidate, self.registry())
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(self.profile(), self.registry(), {"argument-hint": 1})
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(self.profile(), self.registry(), [])

    def test_main_returns_exact_statuses_without_subprocess_only_coverage(self) -> None:
        module = self.load_validator()
        failed = self.profile()
        failed["activation"]["implicit_invocation"]["opted_in_skill_ids"] = ["graphify"]
        failed_path = self.write_json("failed-main.json", failed)
        invalid_path = self.root / "invalid-main.json"
        invalid_path.write_text("{bad", encoding="utf-8")
        cases = ((PROFILE, 0, "passed", True), (failed_path, 1, "failed", False), (invalid_path, 2, "invalid", False))
        for path, expected_code, expected_status, expected_success in cases:
            with self.subTest(status=expected_status):
                output = io.StringIO()
                argv = [str(VALIDATOR), "validate", "--profile", str(path), "--registry", str(REGISTRY)]
                with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                    self.assertEqual(module.main(), expected_code)
                payload = json.loads(output.getvalue())
                self.assertEqual(payload["status"], expected_status)
                self.assertIs(payload["success"], expected_success)


if __name__ == "__main__":
    unittest.main()
