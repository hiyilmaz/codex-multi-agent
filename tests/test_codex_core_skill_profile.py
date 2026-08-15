import copy
import hashlib
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


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "core-skills" / "profiles" / "codex.json"
REGISTRY = REPO_ROOT / "core-skills" / "registry.json"
STANDARD = REPO_ROOT / "core-skills" / "STANDARD.md"
VALIDATOR = REPO_ROOT / "bin" / "cma-codex-core-skill-profile"
CANONICAL_FIELDS = {
    "stable_skill_id",
    "display_name",
    "capability_category",
    "core_protected_status",
    "tool_dependency",
    "semantic_version",
    "purpose",
    "use_when",
    "do_not_use_when",
    "preconditions",
    "workflow",
    "stop_conditions",
    "output_contract",
    "safety_authority_boundary",
    "tool_unavailable_behavior",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CodexCoreSkillProfileTests(unittest.TestCase):
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

    def run_cli(
        self,
        profile: Path = PROFILE,
        *extra: str,
        registry: Path = REGISTRY,
        suppress_bytecode: bool = True,
        validator: Path = VALIDATOR,
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        if suppress_bytecode:
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
        else:
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
        return subprocess.run(
            (
                sys.executable,
                str(validator),
                "validate",
                "--profile",
                str(profile),
                "--registry",
                str(registry),
                *extra,
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

    def assert_fails(self, profile: dict, code: str, *, field: str | None = None) -> dict:
        module = self.load_validator()
        direct_findings = module.validate_profile(profile, self.registry())
        self.assertTrue(any(item["code"] == code for item in direct_findings), direct_findings)
        result = self.run_cli(self.write_json("candidate.json", profile))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = self.payload(result)
        self.assertIs(payload["success"], False)
        self.assertEqual(payload["status"], "failed")
        matches = [item for item in payload["findings"] if item["code"] == code]
        self.assertTrue(matches, payload)
        if field is not None:
            self.assertTrue(any(item.get("field") == field for item in matches), payload)
        return payload

    def load_validator(self):
        loader = importlib.machinery.SourceFileLoader("codex_profile", str(VALIDATOR))
        spec = importlib.util.spec_from_loader("codex_profile", loader)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_profile_exists_for_meaningful_red(self) -> None:
        self.assertTrue(PROFILE.is_file(), f"missing Codex profile: {PROFILE}")

    def test_validator_exists_for_meaningful_red(self) -> None:
        self.assertTrue(VALIDATOR.is_file(), f"missing Codex profile validator: {VALIDATOR}")

    def test_valid_profile_maps_every_canonical_field_exactly_once(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.load_validator().validate_profile(self.profile(), self.registry()), [])
        self.assertEqual(
            self.payload(result),
            {"findings": [], "status": "passed", "success": True},
        )
        profile = self.profile()
        fields = [item["canonical_field"] for item in profile["field_mappings"]]
        self.assertEqual(set(fields), CANONICAL_FIELDS)
        self.assertEqual(len(fields), len(set(fields)))
        for mutation, code in (("missing", "MISSING_MAPPING"), ("duplicate", "DUPLICATE_MAPPING"), ("unknown", "UNKNOWN_MAPPING")):
            with self.subTest(mutation=mutation):
                candidate = self.profile()
                if mutation == "missing":
                    candidate["field_mappings"].pop()
                elif mutation == "duplicate":
                    candidate["field_mappings"].append(copy.deepcopy(candidate["field_mappings"][0]))
                else:
                    candidate["field_mappings"].append(
                        {
                            "canonical_field": "invented_field",
                            "canonical_source": "profile",
                            "codex_targets": ["config.toml"],
                        }
                    )
                self.assert_fails(candidate, code)

    def test_registry_is_authoritative_for_protected_core_metadata(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        for field in ("core_protected_status", "display_name", "tool_dependency"):
            with self.subTest(field=field):
                candidate = self.profile()
                mapping = next(item for item in candidate["field_mappings"] if item["canonical_field"] == field)
                mapping["canonical_source"] = "agents/openai.yaml"
                self.assert_fails(candidate, "CANONICAL_AUTHORITY_VIOLATION", field=field)

    def test_native_structure_and_official_discovery_are_closed(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        profile = self.profile()
        self.assertEqual(profile["native_skill"]["official_required_files"], ["SKILL.md"])
        self.assertIn("agents/openai.yaml", profile["native_skill"]["cma_projection_required_files"])
        self.assertEqual(profile["native_skill"]["frontmatter_required"], ["name", "description"])
        self.assertEqual(
            profile["discovery"]["scopes"],
            [
                "$CWD/.agents/skills through $REPO_ROOT/.agents/skills",
                "$HOME/.agents/skills",
                "/etc/codex/skills",
                "OpenAI bundled system skills",
            ],
        )
        candidate = self.profile()
        candidate["discovery"]["scopes"][1] = "$HOME/.codex/skills"
        self.assert_fails(candidate, "UNSUPPORTED_CODEX_DISCOVERY", field="discovery.scopes")

    def test_activation_is_global_lazy_and_never_disabled(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        activation = self.profile()["activation"]
        self.assertEqual(activation["profile_state"], "active-global")
        self.assertEqual(activation["projected_skill_instances"], 10)
        self.assertEqual(activation["default_mode"], "conditional-implicit")
        self.assertIs(activation["explicit_invocation"]["enabled"], True)
        self.assertIs(activation["implicit_invocation"]["allow_implicit_invocation"], True)
        self.assertEqual(
            set(activation["implicit_invocation"]["opted_in_skill_ids"]),
            {
                "graphify", "serena", "ast-grep", "deepwiki", "github",
                "opengrep", "osv-scanner", "betterleaks", "context7",
            },
        )
        self.assertNotIn("cplt", activation["implicit_invocation"]["opted_in_skill_ids"])
        self.assertEqual(activation["disabled_core_ids"], [])
        self.assertEqual(
            activation["config_entries"],
            ["mcp_servers.serena.enabled=true", "mcp_servers.deepwiki.enabled=true",
             "mcp_servers.github.enabled=true", "mcp_servers.context7.enabled=true",
             "mcp_servers.context7.required=true"],
        )
        for value in (False, 0, 1, "true", None):
            with self.subTest(value=value):
                candidate = self.profile()
                candidate["activation"]["implicit_invocation"]["allow_implicit_invocation"] = value
                self.assert_fails(candidate, "INVALID_ACTIVATION_POLICY", field="activation.implicit_invocation.allow_implicit_invocation")
        candidate = self.profile()
        candidate["activation"]["disabled_core_ids"] = ["graphify"]
        self.assert_fails(candidate, "CORE_DISABLE_FORBIDDEN", field="activation.disabled_core_ids")

    def test_unknown_targets_and_behavioral_metadata_fail_closed(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        candidate = self.profile()
        candidate["field_mappings"][0]["codex_targets"] = ["config.toml.skills.config"]
        self.assert_fails(candidate, "UNSUPPORTED_CODEX_MAPPING", field="stable_skill_id")
        candidate = self.profile()
        candidate["codex_metadata"]["allowed_interface_fields"].append("default_prompt")
        self.assert_fails(candidate, "BEHAVIORAL_METADATA_FORBIDDEN", field="codex_metadata.allowed_interface_fields")

    def test_ui_metadata_does_not_change_canonical_fingerprint(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        module = self.load_validator()
        profile, registry = self.profile(), self.registry()
        first = module.canonical_fingerprint(
            profile,
            registry,
            {"interface": {"display_name": "First", "brand_color": "#000000"}},
        )
        second = module.canonical_fingerprint(
            profile,
            registry,
            {"interface": {"display_name": "Second", "brand_color": "#FFFFFF"}},
        )
        self.assertEqual(first, second)
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(
                profile,
                registry,
                {"interface": {"default_prompt": "Override safety"}},
            )

    def test_unavailable_tool_contract_is_fail_closed(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        contract = self.profile()["tool_unavailable_behavior"]
        self.assertEqual(contract["none"]["availability"], "not_applicable")
        self.assertEqual(contract["required"]["status"], "unverified")
        self.assertIs(contract["required"]["success"], False)
        self.assertEqual(contract["required"]["action"], "stop")
        self.assertEqual(contract["optional"]["fallback"], "predeclared-tool-free-path-only")
        self.assertIn("silent-fallback", contract["forbidden"])
        candidate = self.profile()
        candidate["tool_unavailable_behavior"]["required"]["success"] = 0
        self.assert_fails(candidate, "INVALID_UNAVAILABLE_BEHAVIOR", field="tool_unavailable_behavior")
        candidate = self.profile()
        candidate["tool_unavailable_behavior"]["forbidden"].remove("silent-fallback")
        self.assert_fails(candidate, "INVALID_UNAVAILABLE_BEHAVIOR", field="tool_unavailable_behavior")

    def test_context7_capability_is_required_without_becoming_eager(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        context7 = next(item for item in self.registry()["skills"] if item["id"] == "context7")
        self.assertEqual(context7["capability_status"], "required")
        self.assertEqual(context7["tool_dependency"]["mode"], "required")
        self.assertIn("context7", self.profile()["activation"]["implicit_invocation"]["opted_in_skill_ids"])
        self.assertEqual(self.profile()["activation"]["selection"], "narrowest-sufficient-single-provider")
        self.assertIs(self.profile()["semantic_parity"]["capability_dependency_independent"], True)
        candidate = self.profile()
        candidate["semantic_parity"]["capability_dependency_independent"] = 1
        self.assert_fails(candidate, "SEMANTIC_CONFLATION", field="semantic_parity.capability_dependency_independent")

    def test_global_instructions_are_routing_only(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        routing = self.profile()["global_instructions"]
        self.assertEqual(routing["mode"], "routing-only")
        self.assertEqual(routing["reference_form"], "evidence need -> $<skill-id>")
        self.assertIn("tool-commands", routing["forbidden_content"])
        self.assertEqual(
            routing["agents_md"]["global"],
            "$CODEX_HOME/AGENTS.override.md else $CODEX_HOME/AGENTS.md; first non-empty",
        )
        self.assertEqual(
            routing["agents_md"]["project"],
            "repository-root-to-CWD; one instruction file per directory",
        )
        self.assertEqual(routing["agents_md"]["merge_order"], "root-to-CWD; closer overrides later")
        candidate = self.profile()
        candidate["global_instructions"]["mode"] = "embedded-skill-body"
        self.assert_fails(candidate, "GLOBAL_ROUTING_VIOLATION", field="global_instructions")

    def test_validator_is_read_only_and_rejects_write_like_flags(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        watched = (PROFILE, REGISTRY, STANDARD)
        before = {path: (digest(path), path.stat().st_mode, path.read_bytes()) for path in watched}
        listing = sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*"))
        self.assertEqual(self.run_cli().returncode, 0)
        for flag in ("--apply", "--install", "--sync", "--activate"):
            result = self.run_cli(PROFILE, flag)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(listing, sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*")))
        for path, snapshot in before.items():
            self.assertEqual((digest(path), path.stat().st_mode, path.read_bytes()), snapshot)

    def test_malformed_duplicate_keys_and_unknown_schema_fail_without_traceback(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("RED surfaces are not implemented yet")
        malformed = self.root / "malformed.json"
        malformed.write_text("{not-json", encoding="utf-8")
        module = self.load_validator()
        with self.assertRaises(module.InputError):
            module.load_json(malformed)
        result = self.run_cli(malformed)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.payload(result)["status"], "invalid")
        duplicate = self.root / "duplicate.json"
        duplicate.write_text('{"schema_version":"a","schema_version":"b"}\n', encoding="utf-8")
        with self.assertRaises(module.InputError):
            module.load_json(duplicate)
        result = self.run_cli(duplicate)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.payload(result)["status"], "invalid")
        candidate = self.profile()
        candidate["unknown"] = True
        self.assert_fails(candidate, "INVALID_PROFILE_SCHEMA", field="top_level_fields")

    def test_direct_registry_mapping_and_metadata_boundaries(self) -> None:
        module = self.load_validator()
        profile, registry = self.profile(), self.registry()
        array_input = self.root / "array.json"
        array_input.write_text("[]\n", encoding="utf-8")
        with self.assertRaises(module.InputError):
            module.load_json(array_input)
        self.assertEqual(module.unique_object([("one", 1)]), {"one": 1})

        registry_cases = []
        candidate = copy.deepcopy(registry)
        candidate["schema_version"] = "wrong"
        registry_cases.append((candidate, "INVALID_REGISTRY_POLICY"))
        candidate = copy.deepcopy(registry)
        candidate["platforms"] = ["claude", "opencode"]
        registry_cases.append((candidate, "INVALID_REGISTRY_POLICY"))
        candidate = copy.deepcopy(registry)
        candidate["skills"] = []
        registry_cases.append((candidate, "MISSING_PROTECTED"))
        candidate = copy.deepcopy(registry)
        candidate["skills"][0] = "not-an-object"
        registry_cases.append((candidate, "INVALID_CORE_METADATA"))
        candidate = copy.deepcopy(registry)
        candidate["skills"][0]["core"] = 1
        registry_cases.append((candidate, "INVALID_CORE_METADATA"))
        candidate = copy.deepcopy(registry)
        candidate["skills"][0]["tool_dependency"]["mode"] = "optional"
        registry_cases.append((candidate, "INVALID_CORE_METADATA"))
        for candidate, code in registry_cases:
            with self.subTest(registry=code):
                findings = module.validate_registry_authority(candidate)
                self.assertTrue(any(item["code"] == code for item in findings), findings)

        candidate = copy.deepcopy(profile)
        candidate["field_mappings"] = None
        findings = module.validate_profile(candidate, registry)
        self.assertTrue(any(item["code"] == "INVALID_PROFILE_SCHEMA" for item in findings))
        candidate = copy.deepcopy(profile)
        candidate["field_mappings"][0] = "not-an-object"
        findings = module.validate_profile(candidate, registry)
        self.assertTrue(any(item["code"] == "UNKNOWN_MAPPING" for item in findings))
        candidate = copy.deepcopy(profile)
        candidate["profile_version"] = 1
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(candidate, registry)
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(profile, registry, {"policy": {}})
        with self.assertRaises(module.InputError):
            module.canonical_fingerprint(
                profile, registry, {"interface": {"display_name": 1}}
            )

    def test_canonical_registry_cannot_self_shrink_or_type_confuse(self) -> None:
        module = self.load_validator()
        cases = []
        candidate = self.registry()
        candidate["skills"] = [copy.deepcopy(candidate["skills"][0])]
        candidate["protected_core_ids"] = [candidate["skills"][0]["id"]]
        cases.append(("self-shrunk", candidate))
        candidate = self.registry()
        candidate["platforms"] = "codex"
        cases.append(("string-platforms", candidate))
        candidate = self.registry()
        candidate["platforms"] = None
        cases.append(("null-platforms", candidate))
        candidate = self.registry()
        candidate["skills"].append(copy.deepcopy(candidate["skills"][0]))
        cases.append(("duplicate-id", candidate))
        for name, candidate in cases:
            with self.subTest(case=name):
                findings = module.validate_registry_authority(candidate)
                self.assertTrue(findings)
                path = self.write_json(f"registry-{name}.json", candidate)
                result = self.run_cli(registry=path)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                payload = self.payload(result)
                self.assertIs(payload["success"], False)
                self.assertEqual(payload["status"], "failed")

    def test_unhashable_mapping_field_fails_without_traceback(self) -> None:
        candidate = self.profile()
        candidate["field_mappings"][0]["canonical_field"] = []
        path = self.write_json("unhashable-mapping.json", candidate)
        result = self.run_cli(path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = self.payload(result)
        self.assertIs(payload["success"], False)
        self.assertTrue(any(item["code"] == "UNKNOWN_MAPPING" for item in payload["findings"]))

    def test_symlink_invocation_cannot_substitute_sibling_validator(self) -> None:
        attack_root = self.root / "attack"
        attack_root.mkdir()
        symlink_validator = attack_root / VALIDATOR.name
        symlink_validator.symlink_to(VALIDATOR)
        marker = attack_root / "executed"
        (attack_root / "cma-core-skill-governance").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n",
            encoding="utf-8",
        )
        result = self.run_cli(validator=symlink_validator)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists(), "attacker-controlled sibling was executed")
        self.assertEqual(
            self.payload(result),
            {"findings": [], "status": "passed", "success": True},
        )

    def test_dependency_failures_are_redacted_structured_invalid_results(self) -> None:
        for case in ("missing", "corrupt", "symlink"):
            with self.subTest(case=case):
                isolated = self.root / case
                isolated.mkdir()
                copied_validator = isolated / VALIDATOR.name
                shutil.copyfile(VALIDATOR, copied_validator)
                governance = isolated / "cma-core-skill-governance"
                if case == "corrupt":
                    governance.write_text("this is not valid python !!!\n", encoding="utf-8")
                elif case == "symlink":
                    governance.symlink_to(REPO_ROOT / "bin" / "cma-core-skill-governance")
                result = self.run_cli(validator=copied_validator)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                payload = self.payload(result)
                self.assertIs(payload["success"], False)
                self.assertEqual(payload["status"], "invalid")
                self.assertEqual(payload["findings"][0]["code"], "INVALID_INPUT")
                self.assertNotIn(str(isolated), result.stdout + result.stderr)

    def test_unsuppressed_cli_does_not_persist_bytecode_or_mutate_bin(self) -> None:
        bin_root = REPO_ROOT / "bin"
        before_listing = sorted(str(path.relative_to(bin_root)) for path in bin_root.rglob("*"))
        before_files = {
            path: (digest(path), path.stat().st_mode, path.read_bytes())
            for path in bin_root.rglob("*")
            if path.is_file()
        }
        result = self.run_cli(suppress_bytecode=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            before_listing,
            sorted(str(path.relative_to(bin_root)) for path in bin_root.rglob("*")),
        )
        for path, snapshot in before_files.items():
            self.assertEqual((digest(path), path.stat().st_mode, path.read_bytes()), snapshot)


if __name__ == "__main__":
    unittest.main()
