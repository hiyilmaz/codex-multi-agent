import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "bin" / "cma-core-skill-governance"
REGISTRY = REPO_ROOT / "core-skills" / "registry.json"
EXPECTED_IDS = {
    "graphify",
    "serena",
    "ast-grep",
    "deepwiki",
    "github",
    "opengrep",
    "osv-scanner",
    "betterleaks",
    "cplt",
    "context7",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CoreSkillGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def canonical(self) -> dict:
        self.assertTrue(REGISTRY.is_file(), "missing canonical core skill registry")
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def write_json(
        self, name: str, data: object, *, indent: int | None = 2, sort: bool = True
    ) -> Path:
        path = self.root / name
        path.write_text(
            json.dumps(data, indent=indent, sort_keys=sort) + "\n",
            encoding="utf-8",
        )
        return path

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        self.assertTrue(CLI.is_file(), "missing core skill governance validator")
        return subprocess.run(
            (sys.executable, str(CLI), *arguments),
            cwd=REPO_ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )

    def parse_result(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return json.loads(result.stdout)

    def assert_failure(
        self,
        result: subprocess.CompletedProcess[str],
        code: str,
        *,
        skill_id: str | None = None,
        platform: str | None = None,
        field: str | None = None,
    ) -> dict:
        self.assertEqual(result.returncode, 1, result.stderr)
        payload = self.parse_result(result)
        self.assertFalse(payload["success"])
        self.assertEqual(payload["status"], "failed")
        self.assertNotIn('"success": true', result.stdout.lower())
        matches = [finding for finding in payload["findings"] if finding["code"] == code]
        self.assertTrue(matches, payload)
        if skill_id is not None:
            self.assertTrue(any(item.get("skill_id") == skill_id for item in matches))
        if platform is not None:
            self.assertTrue(any(item.get("platform") == platform for item in matches))
        if field is not None:
            self.assertTrue(any(item.get("field") == field for item in matches))
        return payload

    def inventory(self, platform: str) -> dict:
        skills = []
        for record in self.canonical()["skills"]:
            item = copy.deepcopy(record)
            item["native_metadata"] = {
                "platform": platform,
                "path": f"native/{platform}/{record['id']}",
            }
            skills.append(item)
        if platform == "claude":
            skills.reverse()
        elif platform == "opencode":
            skills = skills[3:] + skills[:3]
        return {"platform": platform, "skills": skills}

    def inventory_paths(self) -> dict[str, Path]:
        return {
            "codex": self.write_json(
                "codex.json", self.inventory("codex"), indent=None, sort=False
            ),
            "claude": self.write_json(
                "claude.json", self.inventory("claude"), indent=4, sort=True
            ),
            "opencode": self.write_json(
                "opencode.json", self.inventory("opencode"), indent=2, sort=False
            ),
        }

    def compare_variants(self, paths: dict[str, Path]) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            "compare-variants",
            "--registry",
            str(REGISTRY),
            "--codex",
            str(paths["codex"]),
            "--claude",
            str(paths["claude"]),
            "--opencode",
            str(paths["opencode"]),
        )

    def test_valid_core_registry(self) -> None:
        registry = self.canonical()
        result = self.run_cli("validate", "--registry", str(REGISTRY))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = self.parse_result(result)
        self.assertEqual(payload, {"findings": [], "status": "passed", "success": True})
        self.assertEqual({item["id"] for item in registry["skills"]}, EXPECTED_IDS)
        self.assertEqual(set(registry["protected_core_ids"]), EXPECTED_IDS)
        self.assertEqual(registry["platforms"], ["codex", "claude", "opencode"])
        self.assertEqual(registry["policies"]["semantic_parity"], "required")
        self.assertEqual(registry["policies"]["parity_basis"], "normalized-semantics")
        self.assertFalse(registry["policies"]["byte_identity_required"])
        self.assertFalse(registry["policies"]["automatic_pruning"])
        for item in registry["skills"]:
            with self.subTest(skill_id=item["id"]):
                self.assertIs(item["core"], True)
                self.assertIs(item["protected"], True)
                self.assertEqual(item["tool_dependency"]["mode"], "required")
                self.assertEqual(item["capability_status"], "required")

    def test_registry_roster_and_status_policy_cannot_self_shrink(self) -> None:
        empty = self.canonical()
        empty["skills"] = []
        empty["protected_core_ids"] = []
        empty_path = self.write_json("empty-registry.json", empty)
        self.assert_failure(
            self.run_cli("validate", "--registry", str(empty_path)),
            "MISSING_PROTECTED",
            skill_id="graphify",
        )
        mutations = (
            ("graphify", "capability_status", "optional"),
            ("context7", "capability_status", "optional"),
            ("serena", "tool_dependency.mode", "optional"),
        )
        for skill_id, field, value in mutations:
            with self.subTest(skill_id=skill_id, field=field):
                data = self.canonical()
                record = next(item for item in data["skills"] if item["id"] == skill_id)
                if field == "tool_dependency.mode":
                    record["tool_dependency"]["mode"] = value
                else:
                    record[field] = value
                path = self.write_json(f"policy-{skill_id}-{field}.json", data)
                self.assert_failure(
                    self.run_cli("validate", "--registry", str(path)),
                    "INVALID_CORE_METADATA",
                    skill_id=skill_id,
                    field=field,
                )

    def test_missing_protected_skill_detection(self) -> None:
        for platform, skill_id in (
            ("codex", "graphify"),
            ("claude", "serena"),
            ("opencode", "ast-grep"),
        ):
            with self.subTest(platform=platform, skill_id=skill_id):
                paths = self.inventory_paths()
                data = json.loads(paths[platform].read_text())
                data["skills"] = [item for item in data["skills"] if item["id"] != skill_id]
                paths[platform] = self.write_json(f"{platform}-missing.json", data)
                self.assert_failure(
                    self.compare_variants(paths),
                    "MISSING_PROTECTED",
                    skill_id=skill_id,
                    platform=platform,
                )

    def test_accidental_removal_requires_explicit_approval(self) -> None:
        baseline = self.write_json("baseline.json", self.canonical())
        for remove_protected_id in (False, True):
            with self.subTest(remove_protected_id=remove_protected_id):
                candidate_data = self.canonical()
                candidate_data["skills"] = [
                    item
                    for item in candidate_data["skills"]
                    if item["id"] != "graphify"
                ]
                if remove_protected_id:
                    candidate_data["protected_core_ids"].remove("graphify")
                candidate = self.write_json(
                    f"candidate-{remove_protected_id}.json", candidate_data
                )
                before = {path: sha256(path) for path in (baseline, candidate)}
                result = self.run_cli(
                    "compare-registry",
                    "--baseline",
                    str(baseline),
                    "--candidate",
                    str(candidate),
                )
                payload = self.assert_failure(
                    result, "REMOVAL_REQUIRES_APPROVAL", skill_id="graphify"
                )
                finding = next(
                    item
                    for item in payload["findings"]
                    if item["code"] == "REMOVAL_REQUIRES_APPROVAL"
                )
                self.assertIs(finding["approval_required"], True)
                self.assertEqual(before, {path: sha256(path) for path in before})

    def test_duplicate_skill_ids_are_rejected(self) -> None:
        for conflicting in (False, True):
            with self.subTest(conflicting=conflicting):
                data = self.canonical()
                duplicate = copy.deepcopy(data["skills"][0])
                if conflicting:
                    duplicate["capability_category"] = "conflicting-category"
                data["skills"].append(duplicate)
                path = self.write_json(f"duplicate-{conflicting}.json", data)
                self.assert_failure(
                    self.run_cli("validate", "--registry", str(path)),
                    "DUPLICATE_ID",
                    skill_id=duplicate["id"],
                )

    def test_invalid_core_and_protected_metadata_is_rejected(self) -> None:
        mutations = (
            ("core", False),
            ("core", "true"),
            ("protected", False),
            ("protected", 1),
            ("display_name", ""),
            ("capability_category", ""),
            ("capability_status", "enabled"),
        )
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                data = self.canonical()
                data["skills"][0][field] = value
                path = self.write_json(f"invalid-{field}-{value!s}.json", data)
                self.assert_failure(
                    self.run_cli("validate", "--registry", str(path)),
                    "INVALID_CORE_METADATA",
                    skill_id="graphify",
                    field=field,
                )
        data = self.canonical()
        data["skills"][0]["tool_dependency"]["tool_id"] = ""
        path = self.write_json("invalid-dependency.json", data)
        self.assert_failure(
            self.run_cli("validate", "--registry", str(path)),
            "INVALID_CORE_METADATA",
            skill_id="graphify",
            field="tool_dependency.tool_id",
        )

    def test_boolean_type_confusion_fails_closed(self) -> None:
        for field in ("automatic_pruning", "byte_identity_required"):
            with self.subTest(policy=field):
                data = self.canonical()
                data["policies"][field] = 0
                path = self.write_json(f"numeric-policy-{field}.json", data)
                self.assert_failure(
                    self.run_cli("validate", "--registry", str(path)),
                    "INVALID_REGISTRY_POLICY",
                    field="policies",
                )
        for field in ("core", "protected"):
            with self.subTest(inventory=field):
                paths = self.inventory_paths()
                data = json.loads(paths["codex"].read_text())
                next(item for item in data["skills"] if item["id"] == "graphify")[
                    field
                ] = 1
                paths["codex"] = self.write_json(f"numeric-{field}.json", data)
                self.assert_failure(
                    self.compare_variants(paths),
                    "SEMANTIC_DRIFT",
                    skill_id="graphify",
                    platform="codex",
                    field=field,
                )

    def test_user_custom_skills_are_not_protected_core(self) -> None:
        paths = self.inventory_paths()
        custom = {
            "id": "user-helper",
            "classification": "custom",
            "core": False,
            "protected": False,
            "native_metadata": {"owner": "user"},
        }
        codex = json.loads(paths["codex"].read_text())
        codex["skills"].append(custom)
        paths["codex"] = self.write_json("codex-custom.json", codex)
        before = paths["codex"].read_bytes()
        result = self.compare_variants(paths)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(paths["codex"].read_bytes(), before)
        codex["skills"][-1]["protected"] = True
        paths["codex"] = self.write_json("codex-custom-protected.json", codex)
        self.assert_failure(
            self.compare_variants(paths),
            "CUSTOM_PROTECTION_FORBIDDEN",
            skill_id="user-helper",
            platform="codex",
        )
        paths = self.inventory_paths()
        collision = json.loads(paths["claude"].read_text())
        graphify = next(item for item in collision["skills"] if item["id"] == "graphify")
        graphify["classification"] = "custom"
        paths["claude"] = self.write_json("claude-custom-collision.json", collision)
        self.assert_failure(
            self.compare_variants(paths),
            "CUSTOM_CORE_COLLISION",
            skill_id="graphify",
            platform="claude",
        )

    def test_multiple_independent_findings_are_reported(self) -> None:
        paths = self.inventory_paths()
        data = json.loads(paths["opencode"].read_text())
        data["skills"] = [item for item in data["skills"] if item["id"] != "github"]
        next(item for item in data["skills"] if item["id"] == "serena")[
            "capability_category"
        ] = "drift"
        paths["opencode"] = self.write_json("opencode-two-findings.json", data)
        payload = self.assert_failure(
            self.compare_variants(paths),
            "MISSING_PROTECTED",
            skill_id="github",
            platform="opencode",
        )
        self.assertTrue(
            any(
                item["code"] == "SEMANTIC_DRIFT"
                and item.get("skill_id") == "serena"
                and item.get("field") == "capability_category"
                for item in payload["findings"]
            ),
            payload,
        )

    def test_semantic_versions_are_validated(self) -> None:
        for version in ("1.0.0", "1.0.0-alpha.1+build.5"):
            with self.subTest(valid=version):
                data = self.canonical()
                data["skills"][0]["semantic_version"] = version
                path = self.write_json(f"valid-{version}.json", data)
                result = self.run_cli("validate", "--registry", str(path))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for version in ("1.0", "v1.0.0", "01.0.0", "1.0.0-alpha..1", "", None):
            with self.subTest(invalid=version):
                data = self.canonical()
                data["skills"][0]["semantic_version"] = version
                path = self.write_json(f"invalid-version-{str(version)}.json", data)
                self.assert_failure(
                    self.run_cli("validate", "--registry", str(path)),
                    "INVALID_SEMVER",
                    skill_id="graphify",
                    field="semantic_version",
                )

    def test_semantic_parity_ignores_native_bytes_and_metadata(self) -> None:
        paths = self.inventory_paths()
        self.assertEqual(len({sha256(path) for path in paths.values()}), 3)
        result = self.compare_variants(paths)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.parse_result(result),
            {"findings": [], "status": "passed", "success": True},
        )

    def test_semantic_drift_is_field_specific(self) -> None:
        mutations = (
            ("display_name", "Unrelated Skill"),
            ("capability_category", "drifted"),
            ("semantic_version", "2.0.0"),
            ("core", False),
            ("protected", False),
            ("capability_status", "optional"),
            ("tool_dependency.tool_id", "different-tool"),
            ("tool_dependency.mode", "optional"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                paths = self.inventory_paths()
                data = json.loads(paths["claude"].read_text())
                record = next(item for item in data["skills"] if item["id"] == "graphify")
                if field.startswith("tool_dependency."):
                    record["tool_dependency"][field.split(".", 1)[1]] = value
                else:
                    record[field] = value
                paths["claude"] = self.write_json(f"claude-drift-{field}.json", data)
                self.assert_failure(
                    self.compare_variants(paths),
                    "SEMANTIC_DRIFT",
                    skill_id="graphify",
                    platform="claude",
                    field=field,
                )

    def test_registry_governance_drift_is_rejected(self) -> None:
        baseline = self.write_json("registry-baseline.json", self.canonical())
        data = self.canonical()
        data["skills"][0]["display_name"] = "Graphify Drift"
        candidate = self.write_json("registry-drift.json", data)
        self.assert_failure(
            self.run_cli(
                "compare-registry",
                "--baseline",
                str(baseline),
                "--candidate",
                str(candidate),
            ),
            "REGISTRY_DRIFT",
            skill_id="graphify",
            field="display_name",
        )

    def test_no_prune_and_no_mutation_on_failure(self) -> None:
        paths = self.inventory_paths()
        custom = {
            "id": "keep-me",
            "classification": "custom",
            "core": False,
            "protected": False,
            "content": "must remain",
        }
        data = json.loads(paths["opencode"].read_text())
        data["skills"].append(custom)
        data["skills"] = [item for item in data["skills"] if item["id"] != "github"]
        paths["opencode"] = self.write_json("opencode-no-prune.json", data)
        before = {
            path: (sha256(path), path.stat().st_mode, path.read_bytes())
            for path in (REGISTRY, *paths.values())
        }
        listing = sorted(item.name for item in self.root.iterdir())
        self.assert_failure(
            self.compare_variants(paths),
            "MISSING_PROTECTED",
            skill_id="github",
            platform="opencode",
        )
        self.assertEqual(listing, sorted(item.name for item in self.root.iterdir()))
        for path, snapshot in before.items():
            self.assertEqual(
                (sha256(path), path.stat().st_mode, path.read_bytes()), snapshot
            )
        misuse = self.run_cli("validate", "--registry", str(REGISTRY), "--prune")
        self.assertEqual(misuse.returncode, 2)
        self.assertNotIn("Traceback", misuse.stderr)
        self.assertEqual(before[REGISTRY], (sha256(REGISTRY), REGISTRY.stat().st_mode, REGISTRY.read_bytes()))

    def test_malformed_json_is_usage_error_without_traceback(self) -> None:
        malformed = self.root / "malformed.json"
        malformed.write_text("{not-json", encoding="utf-8")
        result = self.run_cli("validate", "--registry", str(malformed))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        payload = self.parse_result(result)
        self.assertFalse(payload["success"])
        self.assertEqual(payload["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
