import contextlib
import copy
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
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "core-skills" / "profiles" / "opencode.json"
VALIDATOR = REPO_ROOT / "bin" / "cma-opencode-core-skill-profile"
REGISTRY = REPO_ROOT / "core-skills" / "registry.json"
STANDARD = REPO_ROOT / "core-skills" / "STANDARD.md"
VARIANT = REPO_ROOT / "variants" / "opencode"
CANONICAL_FIELDS = {
    "stable_skill_id", "display_name", "capability_category",
    "core_protected_status", "tool_dependency", "semantic_version", "purpose",
    "use_when", "do_not_use_when", "preconditions", "workflow",
    "stop_conditions", "output_contract", "safety_authority_boundary",
    "tool_unavailable_behavior",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_manifest(root: Path) -> dict[str, tuple[str, int]]:
    if not root.exists():
        return {}
    return {
        str(path.relative_to(root)): (digest(path), path.stat().st_mode)
        for path in root.rglob("*") if path.is_file()
    }


class OpenCodeCoreSkillProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def require_surfaces(self) -> None:
        if not PROFILE.is_file() or not VALIDATOR.is_file():
            self.skipTest("Phase 5 profile surfaces are not implemented yet")

    def profile(self) -> dict:
        self.require_surfaces()
        return json.loads(PROFILE.read_text(encoding="utf-8"))

    def registry(self) -> dict:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def write_json(self, name: str, value: object) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def load_validator(self, path: Path = VALIDATOR):
        self.require_surfaces()
        loader = importlib.machinery.SourceFileLoader("opencode_profile", str(path))
        spec = importlib.util.spec_from_loader("opencode_profile", loader)
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
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        self.require_surfaces()
        process_environment = dict(os.environ)
        if suppress_bytecode:
            process_environment["PYTHONDONTWRITEBYTECODE"] = "1"
        else:
            process_environment.pop("PYTHONDONTWRITEBYTECODE", None)
        if environment:
            process_environment.update(environment)
        return subprocess.run(
            (
                sys.executable, str(validator), "validate", "--profile",
                str(profile), "--registry", str(registry), *extra,
            ),
            cwd=REPO_ROOT,
            env=process_environment,
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
        self.assertTrue(PROFILE.is_file(), f"missing OpenCode profile: {PROFILE}")

    def test_validator_exists_for_meaningful_red(self) -> None:
        self.assertTrue(VALIDATOR.is_file(), f"missing OpenCode validator: {VALIDATOR}")

    def test_valid_profile_maps_all_canonical_fields_once(self) -> None:
        profile = self.profile()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.payload(result), {"findings": [], "status": "passed", "success": True})
        self.assertEqual(self.load_validator().validate_profile(profile, self.registry()), [])
        fields = [item["canonical_field"] for item in profile["field_mappings"]]
        self.assertEqual(set(fields), CANONICAL_FIELDS)
        self.assertEqual(len(fields), len(set(fields)))
        for case in ("missing", "duplicate", "unknown", "unhashable", "unsupported"):
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
                        "canonical_field": "invented",
                        "canonical_source": "opencode.json",
                        "opencode_targets": ["plugin"],
                    })
                    code = "UNKNOWN_MAPPING"
                elif case == "unhashable":
                    candidate["field_mappings"][0]["canonical_field"] = []
                    code = "UNKNOWN_MAPPING"
                else:
                    candidate["field_mappings"][0]["opencode_targets"] = ["opencode.json.permission"]
                    code = "UNSUPPORTED_OPENCODE_MAPPING"
                self.assert_fails(candidate, code)

    def test_registry_is_exact_authority_and_type_safe(self) -> None:
        for field in ("display_name", "core_protected_status", "tool_dependency"):
            with self.subTest(field=field):
                candidate = self.profile()
                mapping = next(item for item in candidate["field_mappings"] if item["canonical_field"] == field)
                mapping["canonical_source"] = "SKILL.md.frontmatter.metadata"
                self.assert_fails(candidate, "CANONICAL_AUTHORITY_VIOLATION", field)
        module = self.load_validator()
        registry = self.registry()
        cases = []
        candidate = copy.deepcopy(registry)
        candidate["skills"] = candidate["skills"][:1]
        candidate["protected_core_ids"] = [candidate["skills"][0]["id"]]
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["platforms"] = ["opencode"]
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["skills"].append(copy.deepcopy(candidate["skills"][0]))
        cases.append(candidate)
        candidate = copy.deepcopy(registry)
        candidate["skills"][0]["core"] = 1
        cases.append(candidate)
        for index, candidate in enumerate(cases):
            self.assertTrue(module.validate_registry_authority(candidate))
            result = self.run_cli(registry=self.write_json(f"registry-{index}.json", candidate))
            self.assertEqual(result.returncode, 1)
            self.assertIs(self.payload(result)["success"], False)

    def test_native_structure_and_discovery_are_stable_v1_only(self) -> None:
        profile = self.profile()
        self.assertEqual(profile["runtime_target"]["channel"], "stable-v1")
        self.assertEqual(profile["runtime_target"]["executable"], "opencode")
        self.assertEqual(profile["runtime_target"]["excluded_beta_executable"], "opencode2")
        native = profile["native_skill"]
        self.assertEqual(native["official_required_files"], ["SKILL.md"])
        self.assertEqual(native["frontmatter"]["required"], ["name", "description"])
        self.assertEqual(native["frontmatter"]["optional"], ["license", "compatibility", "metadata"])
        self.assertEqual(native["frontmatter"]["metadata_type"], "string-to-string-map")
        discovery = profile["discovery"]
        for path in (
            ".opencode/skills/<skill-id>/SKILL.md",
            "~/.config/opencode/skills/<skill-id>/SKILL.md",
            ".claude/skills/<skill-id>/SKILL.md",
            "~/.claude/skills/<skill-id>/SKILL.md",
            ".agents/skills/<skill-id>/SKILL.md",
            "~/.agents/skills/<skill-id>/SKILL.md",
        ):
            self.assertIn(path, discovery["scopes"])
        candidate = self.profile()
        candidate["runtime_target"]["executable"] = "opencode2"
        self.assert_fails(candidate, "UNSUPPORTED_OPENCODE_VERSION", "runtime_target")
        candidate = self.profile()
        candidate["native_skill"]["frontmatter"]["optional"].append("slash")
        self.assert_fails(candidate, "UNSUPPORTED_V2_FIELD", "native_skill")
        candidate = self.profile()
        candidate["discovery"]["scopes"][0] = ".codex/skills/<skill-id>/SKILL.md"
        self.assert_fails(candidate, "UNSUPPORTED_OPENCODE_DISCOVERY", "discovery")

    def test_activation_is_inactive_lazy_and_truthful_about_v1_limit(self) -> None:
        activation = self.profile()["activation"]
        self.assertEqual(activation["profile_state"], "inactive-representation-only")
        self.assertEqual(activation["projected_skill_instances"], 0)
        self.assertEqual(activation["loading"], {"mechanism": "native-skill-tool", "body": "on-demand"})
        self.assertEqual(activation["routing"], {"mode": "exact-id-user-request", "direct_runtime_command": None})
        self.assertEqual(
            activation["explicit_only"],
            {"officially_supported": False, "documented_switch": None, "claim": "not-made"},
        )
        self.assertEqual(activation["future_permission_gate"]["effect"], "ask")
        self.assertEqual(
            activation["future_permission_gate"]["supported_effects"],
            ["allow", "ask", "deny"],
        )
        self.assertEqual(activation["future_permission_gate"]["status"], "profile-only-not-written")
        self.assertEqual(activation["implicit_activation"]["opted_in_skill_ids"], [])
        self.assertEqual(activation["disabled_core_ids"], [])
        self.assertEqual(activation["config_entries"], [])
        for mutate in ("zero", "allow", "slash", "autoinvoke", "implicit", "disabled", "config"):
            with self.subTest(mutate=mutate):
                candidate = self.profile()
                if mutate == "zero":
                    candidate["activation"]["explicit_only"]["officially_supported"] = 0
                elif mutate == "allow":
                    candidate["activation"]["future_permission_gate"]["effect"] = "allow"
                elif mutate == "slash":
                    candidate["activation"]["routing"]["direct_runtime_command"] = "/<skill-id>"
                elif mutate == "autoinvoke":
                    candidate["activation"]["explicit_only"]["documented_switch"] = "opencode/autoinvoke:false"
                elif mutate == "implicit":
                    candidate["activation"]["implicit_activation"]["opted_in_skill_ids"] = ["graphify"]
                elif mutate == "disabled":
                    candidate["activation"]["disabled_core_ids"] = ["graphify"]
                else:
                    candidate["activation"]["config_entries"] = ["permission.skill.graphify=ask"]
                code = "CORE_DISABLE_FORBIDDEN" if mutate == "disabled" else "INVALID_ACTIVATION_POLICY"
                self.assert_fails(candidate, code)

    def test_protection_and_semantic_parity_are_preserved(self) -> None:
        profile = self.profile()
        protected = profile["protected_identification"]
        self.assertEqual(protected["authority"], "core-skills/registry.json")
        self.assertEqual(protected["removal"], "explicit-user-approval-required")
        self.assertIs(protected["automatic_pruning"], False)
        parity = profile["semantic_parity"]
        self.assertEqual(set(parity["canonical_fields"]), CANONICAL_FIELDS)
        self.assertIs(parity["byte_identity_required"], False)
        self.assertIs(parity["stable_v1_only"], True)
        for section, key, value, code in (
            ("protected_identification", "automatic_pruning", 0, "INVALID_PROTECTED_IDENTIFICATION"),
            ("semantic_parity", "byte_identity_required", 0, "SEMANTIC_CONFLATION"),
            ("semantic_parity", "codex_format_copied", True, "SEMANTIC_CONFLATION"),
        ):
            with self.subTest(section=section, key=key):
                candidate = self.profile()
                candidate[section][key] = value
                self.assert_fails(candidate, code, section)

    def test_opencode_metadata_is_nonsemantic_and_strict(self) -> None:
        module = self.load_validator()
        profile, registry = self.profile(), self.registry()
        first = module.canonical_fingerprint(profile, registry, {
            "license": "MIT", "compatibility": "opencode",
            "metadata": {"audience": "maintainers"},
        })
        second = module.canonical_fingerprint(profile, registry, {
            "license": "Apache-2.0", "compatibility": "stable-v1",
            "metadata": {"audience": "developers"},
        })
        self.assertEqual(first, second)
        for metadata in (
            {"metadata": {"audience": 1}}, {"slash": True},
            {"metadata": {"opencode/autoinvoke": "false"}},
            {"permission": "allow"}, [],
        ):
            with self.assertRaises(module.InputError):
                module.canonical_fingerprint(profile, registry, metadata)
        candidate = self.profile()
        candidate["opencode_metadata"]["nonsemantic_fields"].append("permission")
        self.assert_fails(candidate, "BEHAVIORAL_METADATA_FORBIDDEN", "opencode_metadata")

    def test_tool_unavailable_behavior_fails_closed(self) -> None:
        unavailable = self.profile()["tool_unavailable_behavior"]
        self.assertEqual(unavailable["none"]["availability"], "not_applicable")
        self.assertIs(unavailable["required"]["success"], False)
        self.assertEqual(unavailable["required"]["action"], "stop")
        self.assertIn("silent-fallback", unavailable["forbidden"])
        candidate = self.profile()
        candidate["tool_unavailable_behavior"]["required"]["success"] = 0
        self.assert_fails(candidate, "INVALID_UNAVAILABLE_BEHAVIOR", "tool_unavailable_behavior")
        candidate = self.profile()
        candidate["tool_unavailable_behavior"]["forbidden"].remove("silent-fallback")
        self.assert_fails(candidate, "INVALID_UNAVAILABLE_BEHAVIOR", "tool_unavailable_behavior")

    def test_instructions_and_integrations_are_routing_only(self) -> None:
        profile = self.profile()
        instructions = profile["global_instructions"]
        self.assertEqual(instructions["mode"], "routing-only")
        self.assertEqual(instructions["reference_form"], "evidence need -> exact skill ID (user requests it)")
        self.assertEqual(instructions["rules"]["primary"], "AGENTS.md")
        boundaries = profile["integration_boundaries"]
        self.assertEqual(boundaries["agents"], "separate-not-created-or-used-as-skill-wrapper")
        self.assertEqual(boundaries["plugins"], "not-configured-or-loaded")
        self.assertEqual(boundaries["mcp"], "not-configured-or-activated")
        self.assertEqual(boundaries["runtime_config"], "not-written")
        candidate = self.profile()
        candidate["global_instructions"]["mode"] = "embedded-skill-body"
        self.assert_fails(candidate, "GLOBAL_ROUTING_VIOLATION", "global_instructions")
        candidate = self.profile()
        candidate["integration_boundaries"]["plugins"] = "auto-install"
        self.assert_fails(candidate, "INTEGRATION_BOUNDARY_VIOLATION", "integration_boundaries")

    def test_validator_is_read_only_and_malformed_input_is_structured(self) -> None:
        self.require_surfaces()
        home = self.root / "home"
        xdg = self.root / "xdg"
        home.mkdir()
        xdg.mkdir()
        (home / "sentinel").write_text("unchanged\n", encoding="utf-8")
        watched = (PROFILE, REGISTRY, STANDARD)
        before = {path: (digest(path), path.stat().st_mode, path.read_bytes()) for path in watched}
        bin_before = tree_manifest(REPO_ROOT / "bin")
        variant_before = tree_manifest(VARIANT)
        runtime_before = tree_manifest(home)
        environment = {"HOME": str(home), "XDG_CONFIG_HOME": str(xdg)}
        self.assertEqual(self.run_cli(suppress_bytecode=False, environment=environment).returncode, 0)
        for flag in ("--apply", "--install", "--sync", "--activate", "--configure", "--permission"):
            result = self.run_cli(PROFILE, flag, environment=environment)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
        malformed = self.root / "malformed.json"
        malformed.write_text("{bad", encoding="utf-8")
        self.assertEqual(self.payload(self.run_cli(malformed))["status"], "invalid")
        duplicate = self.root / "duplicate.json"
        duplicate.write_text('{"schema_version":"a","schema_version":"b"}\n', encoding="utf-8")
        self.assertEqual(self.payload(self.run_cli(duplicate))["status"], "invalid")
        for path, snapshot in before.items():
            self.assertEqual((digest(path), path.stat().st_mode, path.read_bytes()), snapshot)
        self.assertEqual(tree_manifest(REPO_ROOT / "bin"), bin_before)
        self.assertEqual(tree_manifest(VARIANT), variant_before)
        self.assertEqual(tree_manifest(home), runtime_before)
        self.assertEqual(tree_manifest(xdg), {})

    def test_secure_registry_dependency_reuse_and_redaction(self) -> None:
        self.require_surfaces()
        attack = self.root / "attack"
        attack.mkdir()
        linked = attack / VALIDATOR.name
        linked.symlink_to(VALIDATOR)
        marker = attack / "executed"
        (attack / "cma-core-skill-governance").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_cli(validator=linked).returncode, 0)
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
        secret = "SECRET_TOKEN_456"
        candidate = self.registry()
        candidate["schema_version"] = secret
        result = self.run_cli(registry=self.write_json("secret-registry.json", candidate))
        self.assertEqual(result.returncode, 1)
        payload = self.payload(result)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertTrue(all(set(item) <= {"code", "field"} for item in payload["findings"]))

    def test_deep_or_oversized_json_is_rejected_without_traceback(self) -> None:
        self.require_surfaces()
        deep = self.root / "deep.json"
        deep.write_text("[" * 2000 + "0" + "]" * 2000, encoding="utf-8")
        depth_limited = self.root / "depth-limited.json"
        depth_limited.write_text(
            '{"x":' + "[" * 65 + "0" + "]" * 65 + "}", encoding="utf-8"
        )
        node_limited = self.root / "node-limited.json"
        node_limited.write_text(
            '{"x":[' + ",".join(["0"] * 50_001) + "]}", encoding="utf-8"
        )
        oversized = self.root / "oversized.json"
        oversized.write_text(
            json.dumps({"x": "a" * 1_048_576}), encoding="utf-8"
        )
        symlinked = self.root / "symlinked.json"
        symlinked.symlink_to(PROFILE)
        for path in (deep, depth_limited, node_limited, oversized, symlinked):
            with self.subTest(path=path.name):
                result = self.run_cli(path)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(
                    self.payload(result),
                    {
                        "findings": [{"code": "INVALID_INPUT"}],
                        "status": "invalid",
                        "success": False,
                    },
                )
                self.assertNotIn(str(REPO_ROOT), result.stdout + result.stderr)
        module = self.load_validator()
        replacement = self.root / "replacement.json"
        replacement.write_text("{}", encoding="utf-8")
        with mock.patch.object(module.os, "lstat", return_value=replacement.stat()):
            with self.assertRaises(module.InputError):
                module.load_json(PROFILE)

    def test_validator_internal_and_main_status_paths(self) -> None:
        module = self.load_validator()
        valid = self.write_json("valid.json", self.profile())
        self.assertEqual(module.load_json(valid), self.profile())
        for name, content in (("bad.json", "{bad"), ("dupe.json", '{"a":1,"a":2}'), ("array.json", "[]")):
            path = self.root / name
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(module.InputError):
                module.load_json(path)
        candidate = self.profile()
        candidate["unknown"] = True
        candidate["schema_version"] = "wrong"
        candidate["field_mappings"] = "not-a-list"
        findings = module.validate_profile(candidate, self.registry())
        self.assertTrue(any(item["code"] == "INVALID_PROFILE_SCHEMA" for item in findings))
        self.assertTrue(any(item["code"] == "MISSING_MAPPING" for item in findings))
        failed = self.profile()
        failed["activation"]["implicit_activation"]["opted_in_skill_ids"] = ["graphify"]
        failed_path = self.write_json("failed-main.json", failed)
        invalid_path = self.root / "invalid-main.json"
        invalid_path.write_text("{bad", encoding="utf-8")
        cases = ((PROFILE, 0, "passed", True), (failed_path, 1, "failed", False), (invalid_path, 2, "invalid", False))
        for path, expected_code, expected_status, expected_success in cases:
            output = io.StringIO()
            argv = [str(VALIDATOR), "validate", "--profile", str(path), "--registry", str(REGISTRY)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(module.main(), expected_code)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["status"], expected_status)
            self.assertIs(payload["success"], expected_success)


if __name__ == "__main__":
    unittest.main()
