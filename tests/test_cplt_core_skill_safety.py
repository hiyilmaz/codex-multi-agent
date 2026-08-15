import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import unittest

from test_cplt_core_skill import CpltHarness, EVALS, ROOT, VALIDATOR


class CpltCoreSkillSafetyTests(CpltHarness):
    def test_unavailable_is_exact_and_has_no_host_fallback(self) -> None:
        parsed = self.module().parse_skill(ROOT / "core-skills/skills/cplt/SKILL.md")
        text = parsed["sections"]["Tool Unavailable Behavior"]
        for marker in ("`availability=unavailable`", "`status=unverified`",
                       "`success=false`", "`action=stop`", "`host_fallback=false`"):
            self.assertIn(marker, text)
        self.assertIn("Never execute the command outside verified cplt isolation.", text)

    def test_prompt_and_command_content_never_executes_fake_tools(self) -> None:
        temp = Path(tempfile.mkdtemp(prefix="cplt-path-poison-"))
        self.addCleanup(shutil.rmtree, temp, True)
        marker = temp / "executed"
        for name in ("cplt", "sh", "bash"):
            executable = temp / name
            executable.write_text(f"#!/bin/sh\ntouch '{marker}'\n", encoding="utf-8")
            executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        env = os.environ.copy()
        env["PATH"] = str(temp)
        result = self.cli(env=env)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(marker.exists())

    def test_symlink_deep_json_and_wrong_types_fail_redacted(self) -> None:
        module = self.module()
        root = self.candidate()
        target = root / "core-skills/skills/cplt/SKILL.md"
        original = target.with_name("real-skill.md")
        target.rename(original)
        target.symlink_to(original)
        with self.assertRaises(module.InputError):
            module.validate_tree(root, root / "tests/fixtures/cplt_core_skill/evals.json")
        root = self.candidate()
        eval_path = root / "tests/fixtures/cplt_core_skill/evals.json"
        eval_path.write_text("[" * 1800 + "]" * 1800, encoding="utf-8")
        result = self.cli(root)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout), {
            "findings": [{"code": "INVALID_INPUT"}], "status": "invalid", "success": False})
        self.assertNotIn(str(root), result.stdout + result.stderr)

    def test_cli_rejects_execution_and_mutation_flags(self) -> None:
        for flag in ("--run", "--execute", "--apply", "--install", "--configure",
                     "--activate", "--sync", "--permission"):
            result = self.cli(ROOT, flag)
            self.assertNotEqual(result.returncode, 0, flag)
        self.assertNotIn("subprocess", VALIDATOR.read_text(encoding="utf-8"))
        self.assertNotIn("socket", VALIDATOR.read_text(encoding="utf-8"))

    def test_findings_redact_candidate_content_and_validation_is_read_only(self) -> None:
        root = self.candidate()
        sentinel = "PHASE9_SECRET_SENTINEL_DO_NOT_ECHO"
        path = root / "core-skills/skills/cplt/SKILL.md"
        path.write_text(path.read_text() + f"\n{sentinel}\n", encoding="utf-8")
        before = {p.relative_to(root): (p.read_bytes(), p.stat().st_mode)
                  for p in root.rglob("*") if p.is_file()}
        result = self.cli(root)
        after = {p.relative_to(root): (p.read_bytes(), p.stat().st_mode)
                 for p in root.rglob("*") if p.is_file()}
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
