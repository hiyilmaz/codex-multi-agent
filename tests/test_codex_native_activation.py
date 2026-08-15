import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
ACTIVATOR = ROOT / "bin" / "codex-native-activate"
SKILLS = (
    "graphify", "serena", "ast-grep", "deepwiki", "github", "opengrep",
    "osv-scanner", "betterleaks", "context7", "cplt",
)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return "missing"
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root)).encode()
        digest.update(relative)
        digest.update(str(path.lstat().st_mode).encode())
        if path.is_file() and not path.is_symlink():
            digest.update(path.read_bytes())
    return digest.hexdigest()


class CodexNativeActivationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.codex = self.home / ".codex"
        self.agents = self.home / ".agents" / "skills"
        self.codex.mkdir(parents=True)
        legacy = self.codex / "skills" / "graphify"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("custom graphify\n", encoding="utf-8")
        self.graphify_before = tree_digest(legacy)
        (self.codex / "config.toml").write_text(
            "# keep-comment\nprivate_marker = \"ACTIVATION_PRIVATE_SENTINEL\"\n\n"
            "[mcp_servers.serena]\ncommand = \"serena\"\n\n"
            "[mcp_servers.deepwiki]\nurl = \"https://example.invalid/deepwiki\"\n\n"
            "[mcp_servers.github]\nbearer_token_env_var = \"GITHUB_PAT_TOKEN\"\n\n"
            "[mcp_servers.context7]\nbearer_token_env_var = \"CONTEXT7_API_KEY\"\n\n"
            "[plugins.\"build-ios-apps@openai-curated-remote\".mcp_servers.xcodebuildmcp]\n"
            "enabled = false\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_activation(self, *extra: str, fail_after: str | None = None) -> subprocess.CompletedProcess[str]:
        environment = {**os.environ, "HOME": str(self.home), "CODEX_HOME": str(self.codex)}
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        if fail_after:
            environment["CMA_ACTIVATE_FAIL_AFTER"] = fail_after
        return subprocess.run(
            (sys.executable, str(ACTIVATOR), "--runtime-home", str(self.codex),
             "--user-home", str(self.home), "--source-root", str(ROOT), *extra),
            cwd=ROOT, env=environment, text=True, capture_output=True, check=False,
        )

    def module(self):
        loader = importlib.machinery.SourceFileLoader("codex_native_activate", str(ACTIVATOR))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_activator_exists_for_meaningful_red(self) -> None:
        self.assertTrue(ACTIVATOR.is_file(), f"missing native activator: {ACTIVATOR}")

    def test_additive_activation_preserves_graphify_and_config(self) -> None:
        result = self.run_activation()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("ACTIVATION_PRIVATE_SENTINEL", result.stdout + result.stderr)
        self.assertEqual(tree_digest(self.codex / "skills" / "graphify"), self.graphify_before)
        self.assertFalse((self.agents / "graphify").exists())
        self.assertEqual({path.name for path in self.agents.iterdir()}, set(SKILLS) - {"graphify"})
        config = (self.codex / "config.toml").read_text(encoding="utf-8")
        self.assertIn("ACTIVATION_PRIVATE_SENTINEL", config)
        context = config.split("[mcp_servers.context7]", 1)[1].split("[", 1)[0]
        self.assertIn("enabled = true", context)
        self.assertIn("required = true", context)
        xcode = config.split("xcodebuildmcp]", 1)[1]
        self.assertIn("enabled = false", xcode)
        self.assertTrue((self.codex / "registry/modules/CMA_REPO_TOOLS.md").is_file())
        backups = list((self.codex / "backups").glob("cma-core-tools-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(stat.S_IMODE(backups[0].stat().st_mode), 0o700)
        for path in backups[0].rglob("*"):
            if path.is_file():
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_conflict_and_symlink_fail_before_writes(self) -> None:
        for kind in ("conflict", "symlink", "dangling-symlink"):
            with self.subTest(kind=kind):
                target = self.agents / "serena"
                target.parent.mkdir(parents=True, exist_ok=True)
                if kind == "conflict":
                    target.mkdir()
                    (target / "SKILL.md").write_text("different\n", encoding="utf-8")
                elif kind == "symlink":
                    outside = self.root / "outside"
                    outside.mkdir()
                    target.symlink_to(outside, target_is_directory=True)
                else:
                    target.symlink_to(self.root / "missing", target_is_directory=True)
                before = tree_digest(self.codex)
                result = self.run_activation()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(tree_digest(self.codex), before)
                if target.is_symlink():
                    target.unlink()
                else:
                    for child in target.iterdir():
                        child.unlink()
                    target.rmdir()

    def assert_parent_symlink_fails(self, parent: Path, name: str) -> None:
        target = parent / name
        outside = self.root / f"outside-{name}"
        outside.mkdir()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(outside, target_is_directory=True)
        before = tree_digest(self.home)
        result = self.run_activation()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(tree_digest(self.home), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_skill_parent_fails_before_writes(self) -> None:
        self.assert_parent_symlink_fails(self.home / ".agents", "skills")

    def test_symlinked_router_parent_fails_before_writes(self) -> None:
        self.assert_parent_symlink_fails(self.codex / "registry", "modules")

    def test_symlinked_backup_parent_fails_before_writes(self) -> None:
        self.assert_parent_symlink_fails(self.codex, "backups")

    def test_partial_skill_copy_failure_leaves_no_staging_tree(self) -> None:
        module = self.module()
        before = tree_digest(self.home)
        original = module._copy_regular_at

        def partial_copy(source_fd, destination_fd, digest=None):
            os.write(destination_fd, b"partial\n")
            raise OSError("injected partial copy failure")

        with mock.patch.object(module, "_copy_regular_at", side_effect=partial_copy):
            with self.assertRaises(OSError):
                module.activate(ROOT, self.codex, self.home)
        self.assertEqual(tree_digest(self.home), before)
        self.assertFalse(any(self.home.rglob("*.cma-*")))
        self.assertTrue(callable(original))

    def test_failure_rolls_back_and_success_is_idempotent(self) -> None:
        before = tree_digest(self.home)
        failed = self.run_activation(fail_after="config")
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(tree_digest(self.home), before)
        self.assertEqual(self.run_activation().returncode, 0)
        after = tree_digest(self.home)
        backups = list((self.codex / "backups").glob("cma-core-tools-*"))
        self.assertEqual(self.run_activation().returncode, 0)
        self.assertEqual(tree_digest(self.home), after)
        self.assertEqual(list((self.codex / "backups").glob("cma-core-tools-*")), backups)

    def test_last_step_router_publish_failure_rolls_back_earlier_changes(self) -> None:
        module = self.module()
        before = tree_digest(self.home)
        original = module._atomic_bytes_at

        def reject_router(data, parent_fd, name, mode):
            if name == "CMA_REPO_TOOLS.md":
                raise OSError("injected router publish failure")
            return original(data, parent_fd, name, mode)

        with mock.patch.object(module, "_atomic_bytes_at", side_effect=reject_router):
            with self.assertRaises(OSError):
                module.activate(ROOT, self.codex, self.home)
        self.assertEqual(tree_digest(self.home), before)

    def test_activation_never_executes_tool_payloads(self) -> None:
        poison = self.root / "poison"
        poison.mkdir()
        marker = self.root / "executed"
        for command in SKILLS:
            path = poison / command
            path.write_text(f"#!/bin/sh\ntouch '{marker}'\n", encoding="utf-8")
            path.chmod(0o700)
        environment_path = os.environ.get("PATH", "")
        with mock.patch.dict(os.environ, {"PATH": f"{poison}:{environment_path}"}):
            result = self.run_activation()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists())

    def test_direct_activation_and_config_error_branches(self) -> None:
        module = self.module()
        self.assertIs(module.activate(ROOT, self.codex, self.home), True)
        self.assertIs(module.activate(ROOT, self.codex, self.home), False)
        config = (self.codex / "config.toml").read_text(encoding="utf-8")
        with self.assertRaises(module.ActivationError):
            module._merge_mcp_flags(config.replace("enabled = false", "enabled = true"))
        merged_missing_context7 = module._merge_mcp_flags(
            config.replace("[mcp_servers.context7]", "[mcp_servers.context7-missing]")
        )
        self.assertIn("[mcp_servers.context7]", merged_missing_context7)
        self.assertIn('url = "https://mcp.context7.com/mcp"', merged_missing_context7)
        with self.assertRaises(module.ActivationError):
            module._merge_mcp_flags(config + "\n[mcp_servers.context7]\n")
        for conflicting_section in (
            '[mcp_servers]\nserena={ command = "custom" }\n',
            '[mcp_servers]\nserena   = { command = "custom" }\n',
            '[mcp_servers]\n"serena"={ command = "custom" }\n',
            '[mcp_servers."serena"]\ncommand = "custom"\n',
            '["mcp_servers"]\nserena={ command = "custom" }\n',
            '[mcp_servers . serena]\ncommand = "custom"\n',
            '["mcp_servers"."serena"]\ncommand = "custom"\n',
            'mcp_servers = { serena = { command = "custom" } }\n',
            '"mcp_servers" = { context7 = { url = "https://example.invalid" } }\n',
        ):
            with self.subTest(conflicting_section=conflicting_section):
                with self.assertRaises(module.ActivationError):
                    module._merge_mcp_flags(conflicting_section)

    def test_direct_rollback_conflict_and_main_status_branches(self) -> None:
        module = self.module()
        before = tree_digest(self.home)
        with mock.patch.dict(os.environ, {"CMA_ACTIVATE_FAIL_AFTER": "config"}):
            with self.assertRaises(module.ActivationError):
                module.activate(ROOT, self.codex, self.home)
        self.assertEqual(tree_digest(self.home), before)

        conflict = self.agents / "serena"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("different\n", encoding="utf-8")
        with self.assertRaises(module.ActivationError):
            module.activate(ROOT, self.codex, self.home)
        shutil_target = conflict / "SKILL.md"
        shutil_target.unlink()
        conflict.rmdir()

        config = (self.codex / "config.toml").read_text(encoding="utf-8")
        with self.assertRaises(module.ActivationError):
            module._merge_mcp_flags(config.replace("command = \"serena\"", "enabled = maybe"))
        with self.assertRaises(module.ActivationError):
            module._merge_mcp_flags(config.replace("command = \"serena\"", "enabled = true\nenabled = true"))

        output = io.StringIO()
        argv = [str(ACTIVATOR), "--runtime-home", str(self.codex),
                "--user-home", str(self.home), "--source-root", str(ROOT)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            self.assertEqual(module.main(), 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "passed")
        output = io.StringIO()
        bad_argv = [str(ACTIVATOR), "--runtime-home", "/", "--user-home", str(self.home),
                    "--source-root", str(ROOT)]
        with mock.patch.object(sys, "argv", bad_argv), contextlib.redirect_stdout(output):
            self.assertEqual(module.main(), 1)
        self.assertEqual(json.loads(output.getvalue())["code"], "unsafe_runtime_home")

    def test_quoted_and_multiline_managed_toml_fail_without_mutation(self) -> None:
        config_path = self.codex / "config.toml"
        baseline = config_path.read_text(encoding="utf-8")
        xcode_block = (
            '[plugins."build-ios-apps@openai-curated-remote".mcp_servers.xcodebuildmcp]\n'
            "enabled = false\n"
        )
        dotted_xcode = baseline.replace(xcode_block, "").replace(
            "# keep-comment\n",
            '# keep-comment\nplugins."build-ios-apps@openai-curated-remote".'
            "mcp_servers.xcodebuildmcp.enabled = true\n",
        )
        inline_xcode = baseline.replace(
            xcode_block,
            '[plugins."build-ios-apps@openai-curated-remote".mcp_servers]\n'
            "xcodebuildmcp = { enabled = true }\n",
        )
        candidates = (
            baseline.replace("command = \"serena\"", '"enabled" = false'),
            baseline.replace("enabled = false", '"enabled" = true'),
            baseline.replace(
                "[plugins.\"build-ios-apps@openai-curated-remote\".mcp_servers.xcodebuildmcp]",
                '[plugins.\"build-ios-apps@openai-curated-remote\".mcp_servers."xcodebuildmcp"]',
            ).replace("enabled = false", "enabled = true"),
            baseline.replace(
                "mcp_servers.xcodebuildmcp",
                'mcp_servers . "xcodebuildmcp"',
            ).replace("enabled = false", "enabled = true"),
            baseline.replace(
                "mcp_servers.xcodebuildmcp",
                '"mcp_servers"."xcodebuildmcp"',
            ).replace("enabled = false", "enabled = true"),
            baseline.replace(
                "xcodebuildmcp",
                'xcode\\u0062uildmcp',
            ).replace("enabled = false", "enabled = true"),
            baseline.replace("enabled = false", '"ena\\u0062led" = true'),
            dotted_xcode,
            inline_xcode,
            baseline.replace(
                "command = \"serena\"",
                'note = """\nenabled = false\nnot a real key\n"""',
            ),
        )
        for candidate in candidates:
            with self.subTest(candidate=candidate[:32]):
                config_path.write_text(candidate, encoding="utf-8")
                before = tree_digest(self.home)
                result = self.run_activation()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(tree_digest(self.home), before)
        config_path.write_text(baseline, encoding="utf-8")

    def test_managed_file_replacement_never_overwrites_concurrent_config(self) -> None:
        module = self.module()
        self.assertTrue(hasattr(module, "_atomic_replace_bytes_at"))
        descriptor = os.open(self.codex, os.O_RDONLY | os.O_DIRECTORY)
        original, mode, identity = module._read_file_at(descriptor, "config.toml", 2_000_000)
        replacement = self.codex / "replacement.toml"
        replacement.write_text("concurrent = true\n", encoding="utf-8")

        original_swap = module._renameatx
        swapped = False

        def concurrent_swap(parent_fd, source, target, flags):
            nonlocal swapped
            if target == "config.toml" and flags == module.RENAME_SWAP and not swapped:
                os.replace(replacement, self.codex / "config.toml")
                swapped = True
            original_swap(parent_fd, source, target, flags)

        try:
            with mock.patch.object(module, "_renameatx", side_effect=concurrent_swap):
                with self.assertRaises(module.ActivationError):
                    module._atomic_replace_bytes_at(
                        descriptor, "config.toml", b"managed = true\n", mode, identity,
                    )
        finally:
            os.close(descriptor)
        self.assertEqual((self.codex / "config.toml").read_text(), "concurrent = true\n")
        self.assertNotEqual(original, b"concurrent = true\n")

    def test_validated_skill_source_swap_fails_closed(self) -> None:
        module = self.module()
        source = self.root / "source"
        shutil.copytree(ROOT / "core-skills", source / "core-skills")
        router = source / "variants/codex/home/registry/modules"
        router.mkdir(parents=True)
        shutil.copy2(
            ROOT / "variants/codex/home/registry/modules/CMA_REPO_TOOLS.md",
            router / "CMA_REPO_TOOLS.md",
        )
        original = module._copy_tree_at
        swapped = False

        def swap_after_validation(path, parent_fd, name, *args):
            nonlocal swapped
            if not swapped:
                displaced = path.with_name(f"{path.name}-reviewed")
                path.rename(displaced)
                path.mkdir()
                (path / "SKILL.md").write_text("attacker controlled\n", encoding="utf-8")
                swapped = True
            return original(path, parent_fd, name, *args)

        before = tree_digest(self.home)
        with mock.patch.object(module, "_copy_tree_at", side_effect=swap_after_validation):
            with self.assertRaises(module.ActivationError):
                module.activate(source, self.codex, self.home)
        self.assertTrue(swapped)
        self.assertEqual(tree_digest(self.home), before)

    def test_skill_tree_is_hidden_until_copy_completes(self) -> None:
        module = self.module()
        original = module._copy_dir_contents
        observed = []

        def inspect_during_copy(source_fd, destination_fd, digest, prefix=""):
            if not observed:
                observed.append((self.agents / "serena").exists())
            return original(source_fd, destination_fd, digest, prefix)

        with mock.patch.object(module, "_copy_dir_contents", side_effect=inspect_during_copy):
            self.assertTrue(module.activate(ROOT, self.codex, self.home))
        self.assertTrue(observed)
        self.assertFalse(any(observed))
        self.assertTrue((self.agents / "serena" / "SKILL.md").is_file())

    def test_existing_router_mode_is_preserved(self) -> None:
        router = self.codex / "registry/modules/CMA_REPO_TOOLS.md"
        router.parent.mkdir(parents=True)
        router.write_text("old router\n", encoding="utf-8")
        router.chmod(0o600)
        result = self.run_activation()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(stat.S_IMODE(router.stat().st_mode), 0o600)

    def test_directory_fd_write_stays_anchored_after_parent_swap(self) -> None:
        module = self.module()
        parent = self.root / "anchor"
        parent.mkdir()
        descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        moved = self.root / "anchor-original"
        outside = self.root / "outside-anchor"
        try:
            parent.rename(moved)
            outside.mkdir()
            parent.symlink_to(outside, target_is_directory=True)
            module._atomic_bytes_at(b"safe\n", descriptor, "owned.txt", 0o600)
        finally:
            os.close(descriptor)
        self.assertEqual((moved / "owned.txt").read_bytes(), b"safe\n")
        self.assertEqual(list(outside.iterdir()), [])

    def test_rollback_identity_mismatch_never_deletes_replacement(self) -> None:
        module = self.module()
        parent = self.root / "rollback-parent"
        parent.mkdir()
        target = parent / "owned"
        target.mkdir()
        (target / "original").write_text("original\n", encoding="utf-8")
        descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        expected = module._identity_at(descriptor, "owned")
        displaced = parent / "displaced"
        target.rename(displaced)
        target.mkdir()
        (target / "replacement").write_text("replacement\n", encoding="utf-8")
        try:
            with self.assertRaises(module.ActivationError):
                module._remove_tree_at(descriptor, "owned", expected)
        finally:
            os.close(descriptor)
        self.assertTrue((target / "replacement").is_file())


if __name__ == "__main__":
    unittest.main()
