import json
import os
import re
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_HOME = REPO_ROOT / "variants/claude/home"
LAUNCHER = REPO_ROOT / "variants/claude/bin/claude"
INSTALLER = REPO_ROOT / "bin/codex-user-install"
CHAIN = "planner -> tdd-guide -> code-reviewer -> security-reviewer"
ROLES = ("planner", "tdd-guide", "code-reviewer", "security-reviewer")
CANONICAL_ROLES = {
    "planner": "sonnet",
    "tdd-guide": "sonnet",
    "code-reviewer": "opus",
    "security-reviewer": "opus",
    "explorer": "sonnet",
    "docs-researcher": "sonnet",
    "reviewer": "opus",
    "skill-agent-governor": "opus",
}
ESCALATION_ROLES = {
    "planner-opus": "planner-sol",
    "tdd-guide-opus": "tdd-guide-sol",
    "explorer-opus": "explorer-sol",
    "docs-researcher-opus": "docs-researcher-sol",
}
EXPECTED_AGENT_NAMES = set(CANONICAL_ROLES) | set(ESCALATION_ROLES)
EXPECTED_MODULE_NAMES = {
    "CMA_ORCHESTRATION.md",
    "CMA_TDD.md",
    "CMA_SECURITY.md",
    "CMA_REMOTE_ADMIN.md",
    "CMA_MEMORY_ROUTING.md",
    "CMA_DOCS_RESEARCH.md",
    "CMA_FRONTEND.md",
    "CMA_RECORDS.md",
}
EXPECTED_SKILL_NAMES = {
    "hypothesis-workflow",
    "orchestration-gate",
    "record-archive",
    "tdd-workflow",
}
EXPECTED_HOME_FILES = {
    "CLAUDE.md",
    "README.md",
    "settings.json",
    "prompts/recreate-global-subagents.md",
    *(f"agents/{name}.md" for name in EXPECTED_AGENT_NAMES),
    *(f"skills/{name}/SKILL.md" for name in EXPECTED_SKILL_NAMES),
    "skills/record-archive/scripts/record_archive.py",
    "registry/AGENTS_INDEX.md",
    "registry/AUDIT_LOG.md",
    "registry/ORCHESTRATION.md",
    "registry/SETUP_PREFERENCES.md",
    "registry/SKILLS_INDEX.md",
    "registry/STATUS_MESSAGES.md",
    *(f"registry/modules/{name}" for name in EXPECTED_MODULE_NAMES),
}
BYTE_IDENTICAL_PATHS = {
    "skills/hypothesis-workflow/SKILL.md",
    "skills/record-archive/SKILL.md",
    "skills/record-archive/scripts/record_archive.py",
    "skills/tdd-workflow/SKILL.md",
    "registry/SETUP_PREFERENCES.md",
    "registry/STATUS_MESSAGES.md",
    "registry/modules/CMA_FRONTEND.md",
    "registry/modules/CMA_MEMORY_ROUTING.md",
    "registry/modules/CMA_RECORDS.md",
    "registry/modules/CMA_REMOTE_ADMIN.md",
    "registry/modules/CMA_SECURITY.md",
    "registry/modules/CMA_TDD.md",
}


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0]:
        raise AssertionError(f"invalid frontmatter delimiters: {path}")
    metadata: dict[str, object] = {}
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        key, separator, raw_value = line.partition(":")
        if not separator or key in metadata:
            raise AssertionError(f"invalid or duplicate frontmatter key: {line}")
        value = raw_value.strip()
        if value.startswith("[") and value.endswith("]"):
            metadata[key] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            metadata[key] = value
    return metadata, parts[2].strip()


def adapted_agent_body(source_name: str) -> str:
    source = REPO_ROOT / "variants/codex/home/agents" / f"{source_name}.toml"
    match = re.search(
        r'^developer_instructions = """\n(.*?)\n"""$',
        source.read_text(encoding="utf-8"),
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing agent instructions: {source}")
    body = match.group(1).strip()
    return (
        body.replace("~/.codex", "${CLAUDE_CONFIG_DIR}")
        .replace("Codex", "Claude Code")
        .replace("AGENTS.md", "CLAUDE.md")
        .replace("config.toml", "settings.json")
        .replace("the Sol ", "the Opus ")
        .replace("Sol model", "Opus model")
    )


class ClaudeRuntimeTests(unittest.TestCase):
    def test_claude_home_has_exact_full_parity_manifest(self) -> None:
        actual = {
            str(path.relative_to(CLAUDE_HOME))
            for path in CLAUDE_HOME.rglob("*")
            if path.is_file()
        }
        self.assertEqual(len(EXPECTED_HOME_FILES), 35)
        self.assertEqual(actual, EXPECTED_HOME_FILES)

    def test_recreate_global_subagents_prompt_matches_authoritative_claude_agents_and_token_contract(self) -> None:
        prompt_path = CLAUDE_HOME / "prompts/recreate-global-subagents.md"
        prompt = prompt_path.read_text(encoding="utf-8")
        agents = {}
        for path in sorted((CLAUDE_HOME / "agents").glob("*.md")):
            metadata, body = parse_frontmatter(path)
            identity_match = re.search(r"Identity: You are ([^,]+),", body)
            self.assertIsNotNone(identity_match, path.name)
            agents[metadata["name"]] = (
                identity_match.group(1),
                metadata["model"],
                metadata["effort"],
                ", ".join(metadata["tools"]),
                metadata["permissionMode"],
            )

        self.assertEqual(len(agents), 12)
        for role, values in agents.items():
            row = "| " + " | ".join((f"`{role}`", *values)) + " |"
            with self.subTest(role=role):
                self.assertIn(row, prompt)

        explicit_position = prompt.index("explicit target")
        config_position = prompt.index("`CLAUDE_CONFIG_DIR`")
        fallback_position = prompt.index("`${HOME}/.claude`")
        self.assertLess(explicit_position, config_position)
        self.assertLess(config_position, fallback_position)
        self.assertIn("non-empty", prompt)
        self.assertIn("validate the target before writing", prompt)
        self.assertIn(
            "If an explicit target differs from the effective `CLAUDE_CONFIG_DIR`, stop without writing",
            prompt,
        )
        self.assertIn(
            "Continue only in a new isolated Claude Code process whose `CLAUDE_CONFIG_DIR` resolves to the target",
            prompt,
        )
        self.assertIn(
            "Use `skill-agent-governor` only after the effective `CLAUDE_CONFIG_DIR` equals the resolved target",
            prompt,
        )
        self.assertNotIn("/Users/", prompt)
        self.assertNotIn("iyilmaz", prompt.lower())
        self.assertNotIn("high", prompt.lower())
        self.assertNotIn("gpt-", prompt.lower())
        self.assertNotIn("-sol", prompt)
        self.assertNotIn("TOML", prompt)
        self.assertEqual(prompt.count(CHAIN), 1)
        self.assertNotIn("planner -> tdd-guide -> implementation", prompt)
        self.assertIn("conditional replacements", prompt)
        self.assertIn("authoritative agent files", prompt)
        self.assertIn("inventory-first", prompt)
        self.assertIn("targeted reads", prompt)
        self.assertIn("bounded handoffs", prompt)
        self.assertIn("delta-only repair", prompt)
        self.assertIn("concise", prompt)

    def test_provider_neutral_assets_are_byte_identical(self) -> None:
        codex_home = REPO_ROOT / "variants/codex/home"
        for relative in BYTE_IDENTICAL_PATHS:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (CLAUDE_HOME / relative).read_bytes(),
                    (codex_home / relative).read_bytes(),
                )
        archive_script = CLAUDE_HOME / "skills/record-archive/scripts/record_archive.py"
        self.assertTrue(archive_script.stat().st_mode & stat.S_IXUSR)

    def test_all_agents_match_claude_model_permission_and_body_contract(self) -> None:
        actual_names = {path.stem for path in (CLAUDE_HOME / "agents").glob("*.md")}
        self.assertEqual(actual_names, EXPECTED_AGENT_NAMES)
        allowed_keys = {"name", "description", "tools", "model", "effort", "permissionMode"}
        read_only_tools = {"Read", "Glob", "Grep"}
        for name in sorted(actual_names):
            with self.subTest(name=name):
                metadata, body = parse_frontmatter(CLAUDE_HOME / "agents" / f"{name}.md")
                self.assertEqual(set(metadata), allowed_keys)
                self.assertEqual(metadata["name"], name)
                self.assertEqual(metadata["effort"], "medium")
                self.assertTrue(metadata["description"])
                if name == "skill-agent-governor":
                    self.assertEqual(metadata["permissionMode"], "default")
                    self.assertEqual(set(metadata["tools"]), read_only_tools | {"Edit", "Write"})
                else:
                    self.assertEqual(metadata["permissionMode"], "plan")
                    self.assertTrue(read_only_tools.issubset(set(metadata["tools"])))
                    self.assertTrue({"Edit", "Write"}.isdisjoint(set(metadata["tools"])))
                if name in CANONICAL_ROLES:
                    self.assertEqual(metadata["model"], CANONICAL_ROLES[name])
                    source_name = name
                else:
                    self.assertEqual(metadata["model"], "opus")
                    source_name = ESCALATION_ROLES[name]
                self.assertEqual(body, adapted_agent_body(source_name))

    def test_policy_has_full_core_sections_and_resolvable_lazy_routes(self) -> None:
        codex_policy = (REPO_ROOT / "variants/codex/home/AGENTS.md").read_text(encoding="utf-8")
        claude_policy = (CLAUDE_HOME / "CLAUDE.md").read_text(encoding="utf-8")
        codex_headings = {
            line.split(" ", 1)[1]
            for line in codex_policy.splitlines()
            if line.startswith(("## ", "### "))
        }
        claude_headings = {
            line.split(" ", 1)[1]
            for line in claude_policy.splitlines()
            if line.startswith(("## ", "### "))
        }
        self.assertEqual(claude_headings, codex_headings)
        self.assertIn(CHAIN, claude_policy)
        self.assertIn("${CLAUDE_CONFIG_DIR}/registry/ORCHESTRATION.md", claude_policy)
        for module in EXPECTED_MODULE_NAMES:
            self.assertIn(f"${{CLAUDE_CONFIG_DIR}}/registry/modules/{module}", claude_policy)
            self.assertTrue((CLAUDE_HOME / "registry/modules" / module).is_file())

    def test_registry_indexes_exactly_match_packaged_assets(self) -> None:
        agents_index = (CLAUDE_HOME / "registry/AGENTS_INDEX.md").read_text(encoding="utf-8")
        skills_index = (CLAUDE_HOME / "registry/SKILLS_INDEX.md").read_text(encoding="utf-8")
        orchestration = (CLAUDE_HOME / "registry/ORCHESTRATION.md").read_text(encoding="utf-8")
        indexed_agents = {
            line.split("|")[1].strip().strip("`")
            for line in agents_index.splitlines()
            if line.startswith("|") and "/agents/" in line
        }
        indexed_skills = {
            line.split("|")[1].strip().strip("`")
            for line in skills_index.splitlines()
            if line.startswith("|") and "/skills/" in line
        }
        self.assertEqual(indexed_agents, EXPECTED_AGENT_NAMES)
        self.assertEqual(indexed_skills, EXPECTED_SKILL_NAMES)
        self.assertIn(CHAIN, orchestration)
        routing_sources = {
            "registry": orchestration,
            "module": (CLAUDE_HOME / "registry/modules/CMA_ORCHESTRATION.md").read_text(encoding="utf-8"),
            "gate": (CLAUDE_HOME / "skills/orchestration-gate/SKILL.md").read_text(encoding="utf-8"),
        }
        for name in ESCALATION_ROLES:
            self.assertIn(f"`{name}`", agents_index + orchestration)
            for surface, content in routing_sources.items():
                with self.subTest(role=name, surface=surface):
                    self.assertIn(name, content)
        for module in EXPECTED_MODULE_NAMES:
            self.assertTrue((CLAUDE_HOME / "registry/modules" / module).is_file())
        docs_module = (CLAUDE_HOME / "registry/modules/CMA_DOCS_RESEARCH.md").read_text(encoding="utf-8")
        self.assertIn("official Anthropic sources", docs_module)

    def test_claude_package_excludes_codex_only_and_unsafe_artifacts(self) -> None:
        relative_paths = [str(path.relative_to(CLAUDE_HOME)) for path in CLAUDE_HOME.rglob("*")]
        self.assertFalse(any(path.endswith("openai.yaml") for path in relative_paths))
        self.assertFalse(any(path.endswith(".toml") for path in relative_paths))
        self.assertFalse(any("-sol" in path for path in relative_paths))
        source_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in CLAUDE_HOME.rglob("*")
            if path.is_file()
        )
        for forbidden in (
            "gpt-5.",
            "model_reasoning_effort",
            "sandbox_mode",
            "bypassPermissions",
            "apiKey",
        ):
            self.assertNotIn(forbidden, source_text)

    def test_claude_audit_log_contains_only_evidenced_claude_history(self) -> None:
        audit = (CLAUDE_HOME / "registry/AUDIT_LOG.md").read_text(encoding="utf-8")
        date_headings = {
            line.removeprefix("## ")
            for line in audit.splitlines()
            if line.startswith("## ")
        }
        normalized_audit = " ".join(audit.split())
        self.assertEqual(date_headings, {"2026-08-06"})
        self.assertIn("full Core CMA source parity", normalized_audit)
        self.assertNotIn("managed local Claude Code runtime", normalized_audit)

    def test_claude_source_layout_is_portable(self) -> None:
        self.assertTrue((CLAUDE_HOME / "CLAUDE.md").is_file())
        self.assertTrue((CLAUDE_HOME / "settings.json").is_file())
        self.assertTrue((CLAUDE_HOME / "README.md").is_file())
        self.assertTrue(LAUNCHER.is_file())
        for role in ROLES:
            self.assertTrue((CLAUDE_HOME / "agents" / f"{role}.md").is_file())
        for skill in ("orchestration-gate", "tdd-workflow", "hypothesis-workflow", "record-archive"):
            self.assertTrue((CLAUDE_HOME / "skills" / skill / "SKILL.md").is_file())

    def test_installed_claude_matches_source_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for source in CLAUDE_HOME.rglob("*"):
                if source.is_file():
                    target = runtime / source.relative_to(CLAUDE_HOME)
                    self.assertTrue(target.is_file(), target)
                    self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertTrue((runtime / "bin/llm-claude").stat().st_mode & stat.S_IXUSR)

    def test_claude_policy_preserves_truthful_success_and_exact_chain(self) -> None:
        policy = (CLAUDE_HOME / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn(CHAIN, policy)
        self.assertIn("Do not skip", policy)
        for marker in ("Truthful Success Reporting", "success=true", "success=false", "No evidence means no success"):
            self.assertIn(marker, policy)

    def test_claude_agents_are_markdown_frontmatter_and_distinct(self) -> None:
        bodies = []
        for role in ROLES:
            text = (CLAUDE_HOME / "agents" / f"{role}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {role}", text)
            self.assertIn("tools:", text)
            self.assertNotIn("model_reasoning_effort", text)
            bodies.append(text)
        self.assertEqual(len(set(bodies)), len(ROLES))

    def test_settings_json_is_minimal_and_safe(self) -> None:
        settings = json.loads((CLAUDE_HOME / "settings.json").read_text(encoding="utf-8"))
        serialized = json.dumps(settings).lower()
        self.assertNotIn("bypasspermissions", serialized)
        self.assertNotIn("apikey", serialized)
        self.assertNotIn("hook", serialized)
        self.assertEqual(settings, {"permissions": {"defaultMode": "default"}})

    def test_source_excludes_runtime_and_secret_artifacts(self) -> None:
        forbidden = {"credentials.json", ".credentials.json", "history.jsonl", "stats-cache.json", "session-env"}
        present = {path.name for path in (REPO_ROOT / "variants/claude").rglob("*")}
        self.assertTrue(forbidden.isdisjoint(present))

    def test_launcher_forwards_args_sets_home_and_propagates_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            binary_dir = root / "bin"
            runtime_bin = runtime / "bin"
            binary_dir.mkdir()
            runtime_bin.mkdir(parents=True)
            installed = runtime_bin / "llm-claude"
            installed.write_bytes(LAUNCHER.read_bytes())
            installed.chmod(0o755)
            native = binary_dir / "claude"
            native.write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' \"$CLAUDE_CONFIG_DIR\"\nprintf '<%s>\\n' \"$@\"\nexit 7\n",
                encoding="utf-8",
            )
            native.chmod(0o755)
            environment = {
                **os.environ,
                "PATH": f"{binary_dir}:/usr/bin:/bin",
                "CLAUDE_CONFIG_DIR": "/hostile/inherited/path",
            }
            result = subprocess.run(
                (str(installed), "--model", "test model"),
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.stdout.splitlines()[0], str(runtime))
            self.assertIn("<--model>", result.stdout)
            self.assertIn("<test model>", result.stdout)
            self.assertNotIn("hostile", result.stdout + result.stderr)

    def test_launcher_missing_native_binary_fails_clearly(self) -> None:
        result = subprocess.run(
            ("/bin/bash", str(LAUNCHER)),
            env={"PATH": "/usr/bin:/bin"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("native claude", result.stderr.lower())

    def test_launcher_has_valid_bash_syntax_and_executable_mode(self) -> None:
        result = subprocess.run(("/bin/bash", "-n", str(LAUNCHER)), capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(LAUNCHER.stat().st_mode & stat.S_IXUSR)


if __name__ == "__main__":
    unittest.main()
