import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG = REPO_ROOT / "variants/config.toml"
INSTALLER = REPO_ROOT / "bin/codex-user-install"
SETUP = REPO_ROOT / "bin/codex-setup"


class VariantInstallTests(unittest.TestCase):
    def variants(self) -> list[dict]:
        variants: list[dict] = []
        current: dict | None = None
        for raw_line in CATALOG.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line == "[[variants]]":
                current = {}
                variants.append(current)
            elif current is not None and "=" in line and not line.startswith("#"):
                key, value = (part.strip() for part in line.split("=", 1))
                if value.startswith('"') and value.endswith('"'):
                    current[key] = value[1:-1]
        return variants

    def assert_default_runtime_active(self, home: Path, variant: dict) -> None:
        if variant["id"] == "opencode":
            self.assertTrue((home / "skills/opencode-docs/SKILL.md").is_file())
        else:
            self.assertTrue((home / variant["policy_file"]).is_file())
            self.assertTrue((home / variant["settings_file"]).is_file())

    def test_catalog_registers_three_complete_unique_variants(self) -> None:
        variants = self.variants()
        self.assertEqual(
            [item["id"] for item in variants],
            ["codex", "claude", "opencode"],
        )
        self.assertEqual(len({item["id"] for item in variants}), len(variants))
        required = {"name", "home", "default_home", "policy_file", "settings_file", "agent_format"}
        for variant in variants:
            with self.subTest(variant=variant["id"]):
                self.assertTrue(required.issubset(variant))
                source = (REPO_ROOT / variant["home"]).resolve()
                self.assertTrue(source.is_relative_to(REPO_ROOT.resolve()))
                self.assertTrue((source / variant["policy_file"]).is_file())
                self.assertTrue((source / variant["settings_file"]).is_file())

    def test_list_variants_is_catalog_driven(self) -> None:
        result = subprocess.run(
            (str(INSTALLER), "--list-variants"),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        listed = [line.split("\t", 1)[0] for line in result.stdout.splitlines()]
        self.assertEqual(listed, [item["id"] for item in self.variants()])

    def test_setup_all_models_installs_every_catalog_variant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            result = subprocess.run(
                (str(SETUP),),
                cwd=REPO_ROOT,
                env=environment,
                input="y\n\ny\nn\n\ny\nn\n\ny\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            prompts = result.stdout + result.stderr
            self.assertEqual(prompts.count("Tüm modeller kurulsun mu?"), 1)
            for variant in self.variants():
                home = root / "home" / variant["default_home"].removeprefix("~/")
                with self.subTest(variant=variant["id"]):
                    self.assert_default_runtime_active(home, variant)
                    status = (home / "registry/STATUS_MESSAGES.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertIn("| blocked | İlerleyemiyorum, kararını bekliyorum. |", status)
                    self.assertNotIn(f"{variant['id']} kurulsun mu?", prompts)

    def test_setup_individual_models_installs_selected_subset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            result = subprocess.run(
                (str(SETUP),),
                cwd=REPO_ROOT,
                env=environment,
                input="n\ny\nn\ny\n\ny\nn\n\ny\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            prompts = result.stdout + result.stderr
            selected = {"codex", "opencode"}
            for variant in self.variants():
                home = root / "home" / variant["default_home"].removeprefix("~/")
                self.assertEqual(prompts.count(f"{variant['id']} kurulsun mu?"), 1)
                with self.subTest(variant=variant["id"]):
                    if variant["id"] in selected:
                        self.assert_default_runtime_active(home, variant)
                    else:
                        self.assertFalse(home.exists())

    def test_setup_rejects_symlinked_registry_before_status_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            outside = root / "outside"
            runtime.mkdir()
            outside.mkdir()
            (runtime / "registry").symlink_to(outside, target_is_directory=True)

            result = subprocess.run(
                (str(SETUP), "--variant", "codex", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(root / "home")},
                input="\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stderr.lower())
            self.assertFalse((outside / "STATUS_MESSAGES.md").exists())
            self.assertFalse((outside / "SETUP_PREFERENCES.md").exists())

    def test_setup_preserves_existing_registry_file_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            registry = runtime / "registry"
            registry.mkdir(parents=True)
            for name in ("STATUS_MESSAGES.md", "SETUP_PREFERENCES.md"):
                path = registry / name
                path.write_text("local\n", encoding="utf-8")
                path.chmod(0o600)

            result = subprocess.run(
                (str(SETUP), "--variant", "codex", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(root / "home")},
                input="\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ("STATUS_MESSAGES.md", "SETUP_PREFERENCES.md"):
                self.assertEqual((registry / name).stat().st_mode & 0o777, 0o600)

    def test_setup_respects_restrictive_umask_for_new_registry_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            result = subprocess.run(
                (str(SETUP), "--variant", "codex", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(root / "home")},
                input="\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
                preexec_fn=lambda: os.umask(0o077),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ("STATUS_MESSAGES.md", "SETUP_PREFERENCES.md"):
                self.assertEqual(
                    (runtime / "registry" / name).stat().st_mode & 0o777, 0o600
                )

    def test_retired_dolphin_variant_is_rejected_without_touching_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "dolphin-runtime"
            runtime.mkdir()
            marker = runtime / "preserve.txt"
            marker.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                (str(INSTALLER), "--variant", "dolphin", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown variant", result.stderr.lower())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_each_provider_installs_declared_policy_and_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in self.variants():
                runtime = root / variant["id"]
                result = subprocess.run(
                    (
                        str(INSTALLER),
                        "--runtime-home",
                        str(runtime),
                        "--variant",
                        variant["id"],
                    ),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant["id"]):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue((runtime / variant["policy_file"]).is_file())
                    self.assertTrue((runtime / variant["settings_file"]).is_file())
                    other_policy = "CLAUDE.md" if variant["policy_file"] == "AGENTS.md" else "AGENTS.md"
                    self.assertFalse((runtime / other_policy).exists())

    def test_variant_prompts_install_to_explicit_runtime_and_match_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_config = root / "active-claude"
            fake_home = root / "home"
            environment = {
                **os.environ,
                "CLAUDE_CONFIG_DIR": str(fake_config),
                "HOME": str(fake_home),
            }
            for variant in ("codex", "claude"):
                runtime = root / variant
                result = subprocess.run(
                    (str(INSTALLER), "--runtime-home", str(runtime), "--variant", variant),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                installed = runtime / "prompts/recreate-global-subagents.md"
                source = REPO_ROOT / f"variants/{variant}/home/prompts/recreate-global-subagents.md"
                with self.subTest(variant=variant):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(installed.is_file())
                    self.assertEqual(installed.read_bytes(), source.read_bytes())
            self.assertFalse((fake_config / "prompts/recreate-global-subagents.md").exists())
            self.assertFalse((fake_home / ".claude/prompts/recreate-global-subagents.md").exists())

    def test_codex_home_environment_selects_default_codex_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for configured_home in (root / "configured", None):
                home = root / ("fallback-home" if configured_home is None else "other-home")
                environment = {**os.environ, "HOME": str(home)}
                if configured_home is None:
                    environment.pop("CODEX_HOME", None)
                    expected = home / ".codex"
                else:
                    environment["CODEX_HOME"] = str(configured_home)
                    expected = configured_home
                result = subprocess.run(
                    (str(INSTALLER), "--variant", "codex"),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(configured_home=configured_home):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue((expected / "AGENTS.md").is_file())
                    self.assertTrue(
                        (expected / "prompts/recreate-global-subagents.md").is_file()
                    )

    def test_native_codex_default_install_activates_core_tools(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            environment = {**os.environ, "HOME": str(home)}
            environment.pop("CODEX_HOME", None)
            result = subprocess.run(
                (str(INSTALLER), "--variant", "codex"),
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".codex/AGENTS.md").is_file())
            for skill in ("serena", "ast-grep", "context7", "cplt"):
                with self.subTest(skill=skill):
                    self.assertTrue((home / ".agents/skills" / skill / "SKILL.md").is_file())

    def test_existing_native_codex_config_receives_missing_managed_mcp_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            config = home / ".codex/config.toml"
            config.parent.mkdir(parents=True)
            config.write_text('private_marker = "preserved"\n', encoding="utf-8")
            environment = {**os.environ, "HOME": str(home)}
            environment.pop("CODEX_HOME", None)
            result = subprocess.run(
                (str(INSTALLER), "--variant", "codex"),
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            merged = config.read_text(encoding="utf-8")
            self.assertIn('private_marker = "preserved"', merged)
            self.assertIn("[mcp_servers.serena]", merged)
            self.assertIn("[mcp_servers.context7]", merged)
            self.assertIn("required = true", merged)

    def test_native_codex_setup_propagates_core_tool_activation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            environment = {**os.environ, "HOME": str(home)}
            environment.pop("CODEX_HOME", None)
            result = subprocess.run(
                (str(SETUP), "--variant", "codex"),
                cwd=REPO_ROOT,
                env=environment,
                input="\ny\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".agents/skills/context7/SKILL.md").is_file())

    def test_custom_codex_runtime_does_not_activate_core_tools(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            runtime = root / "custom-codex"
            result = subprocess.run(
                (str(INSTALLER), "--variant", "codex", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(home)},
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((runtime / "AGENTS.md").is_file())
            self.assertFalse((home / ".agents/skills").exists())

    def test_native_activation_failure_is_terminal_for_installer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            conflict = home / ".agents/skills/serena/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("conflicting managed skill\n", encoding="utf-8")
            environment = {**os.environ, "HOME": str(home)}
            environment.pop("CODEX_HOME", None)
            result = subprocess.run(
                (str(INSTALLER), "--variant", "codex"),
                cwd=REPO_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Variant installed: codex", result.stdout)

    def test_existing_variant_prompt_is_untouched_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for variant in ("codex", "claude"):
                runtime = root / variant
                prompt = runtime / "prompts/recreate-global-subagents.md"
                prompt.parent.mkdir(parents=True)
                prompt.write_text("local prompt\n", encoding="utf-8")
                prompt.chmod(0o640)
                result = subprocess.run(
                    (str(INSTALLER), "--runtime-home", str(runtime), "--variant", variant),
                    cwd=REPO_ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(prompt.read_text(encoding="utf-8"), "local prompt\n")
                    self.assertEqual(prompt.stat().st_mode & 0o777, 0o640)

    def test_installer_refuses_variant_prompts_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for variant, policy_name in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
                runtime = root / variant
                outside = root / f"outside-{variant}"
                runtime.mkdir()
                outside.mkdir()
                policy = runtime / policy_name
                policy.write_text("local policy\n", encoding="utf-8")
                sentinel = outside / "sentinel"
                sentinel.write_text("outside\n", encoding="utf-8")
                (runtime / "prompts").symlink_to(outside, target_is_directory=True)
                result = subprocess.run(
                    (
                        str(INSTALLER),
                        "--runtime-home",
                        str(runtime),
                        "--variant",
                        variant,
                        "--force",
                    ),
                    cwd=REPO_ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant):
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("symbolic link", result.stderr)
                    self.assertEqual(policy.read_text(encoding="utf-8"), "local policy\n")
                    self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside\n")
                    self.assertFalse((outside / "recreate-global-subagents.md").exists())

    def test_unknown_variant_fails_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "missing"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(runtime.exists())

    def test_malformed_variant_metadata_fails_before_target_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "fixture"
            (fixture / "bin").mkdir(parents=True)
            shutil.copy2(INSTALLER, fixture / "bin/codex-user-install")
            shutil.copytree(REPO_ROOT / "variants", fixture / "variants")
            catalog = fixture / "variants/config.toml"
            catalog.write_text(
                catalog.read_text().replace('settings_file = "settings.json"\n', "", 1),
                encoding="utf-8",
            )
            target = Path(temporary) / "target"
            result = subprocess.run(
                (
                    str(fixture / "bin/codex-user-install"),
                    "--runtime-home",
                    str(target),
                    "--variant",
                    "claude",
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("incomplete metadata", result.stderr)
            self.assertFalse(target.exists())

    def test_escaping_launcher_name_fails_before_target_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "fixture"
            (fixture / "bin").mkdir(parents=True)
            shutil.copy2(INSTALLER, fixture / "bin/codex-user-install")
            shutil.copytree(REPO_ROOT / "variants", fixture / "variants")
            catalog = fixture / "variants/config.toml"
            catalog.write_text(
                catalog.read_text().replace('launcher_name = "llm-claude"', 'launcher_name = "../../escaped"'),
                encoding="utf-8",
            )
            target = Path(temporary) / "target"
            result = subprocess.run(
                (str(fixture / "bin/codex-user-install"), "--runtime-home", str(target), "--variant", "claude"),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe launcher name", result.stderr)
            self.assertFalse(target.exists())
            self.assertFalse((Path(temporary) / "escaped").exists())

    def test_setup_explicit_claude_variant_installs_claude(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "claude"
            environment = {**os.environ, "HOME": str(root / "home")}
            result = subprocess.run(
                (str(SETUP), "--variant", "claude", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env=environment,
                input="\ny\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((runtime / "CLAUDE.md").is_file())
            self.assertTrue((runtime / "bin/llm-claude").is_file())

    def test_setup_explicit_opencode_variant_installs_opencode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "opencode"
            environment = {**os.environ, "HOME": str(root / "home")}
            result = subprocess.run(
                (str(SETUP), "--variant", "opencode", "--runtime-home", str(runtime)),
                cwd=REPO_ROOT,
                env=environment,
                input="\ny\nn\nn\n\n\n\n\nn\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((runtime / "AGENTS.md").is_file())
            self.assertTrue((runtime / "opencode.json").is_file())
            self.assertTrue((runtime / "bin/llm-opencode").is_file())

    def test_existing_provider_files_are_untouched_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            runtime.mkdir()
            sentinel = runtime / "CLAUDE.md"
            sentinel.write_text("local policy\n", encoding="utf-8")
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(sentinel.read_text(), "local policy\n")

    def test_installer_refuses_managed_file_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            runtime.mkdir()
            outside = root / "outside"
            outside.write_text("outside\n", encoding="utf-8")
            (runtime / "CLAUDE.md").symlink_to(outside)
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude", "--force"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stderr)
            self.assertEqual(outside.read_text(), "outside\n")

    def test_installer_refuses_managed_parent_directory_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            outside = root / "outside"
            runtime.mkdir()
            outside.mkdir()
            sentinel = outside / "planner.md"
            sentinel.write_text("outside agent\n", encoding="utf-8")
            (runtime / "agents").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude", "--force"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stderr)
            self.assertEqual(sentinel.read_text(), "outside agent\n")
            self.assertFalse((outside / "tdd-guide.md").exists())

    def test_existing_launcher_mode_is_untouched_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary) / "runtime"
            launcher = runtime / "bin/llm-claude"
            launcher.parent.mkdir(parents=True)
            launcher.write_text("local launcher\n", encoding="utf-8")
            launcher.chmod(0o600)
            result = subprocess.run(
                (str(INSTALLER), "--runtime-home", str(runtime), "--variant", "claude"),
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(launcher.read_text(), "local launcher\n")
            self.assertEqual(launcher.stat().st_mode & 0o777, 0o600)

    def test_runtime_docs_describe_claude_commands_and_boundaries(self) -> None:
        paths = ("README.md", "USAGE_GUIDE.md", "COMMAND_REFERENCE.md", "TURKCE_KURULUM_REHBERI.md")
        for path in paths:
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("claude", text.lower())
                self.assertIn("llm-claude", text)
                self.assertIn("CLAUDE_CONFIG_DIR", text)
                self.assertIn("Agent SDK", text)
                self.assertIn(".claude", text)
                self.assertNotIn(".llm-runtimes/claude", text)

    def test_runtime_docs_describe_native_codex_core_tool_activation(self) -> None:
        paths = (
            "README.md", "USAGE_GUIDE.md", "COMMAND_REFERENCE.md",
            "TURKCE_KURULUM_REHBERI.md", "variants/codex/home/README.md",
        )
        for path in paths:
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("codex-native-activate", text)
                self.assertIn("Context7", text)
                self.assertIn("xcodebuildmcp", text)
                self.assertIn("cplt", text)

    def test_runtime_home_and_codex_home_aliases_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for option, target in (("--runtime-home", root / "runtime"), ("--codex-home", root / "alias")):
                result = subprocess.run(
                    (str(INSTALLER), option, str(target), "--variant", "codex"),
                    cwd=REPO_ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((target / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
