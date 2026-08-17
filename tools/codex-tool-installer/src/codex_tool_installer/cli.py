from __future__ import annotations

import argparse
import os
import shutil
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Mapping, Sequence

from .config import ConfigTransactionError, restore_config_exact, update_config_transactionally
from .credentials import LibsecretStore, MacOSKeychainStore, MaskedPrompt, ProtectedFileStore, resolve_credential
from .dependencies import dependency_plan
from .discovery import discover, managed_bin_environment, preflight
from .execution import LifecycleExecutor, LifecycleStatusError, PendingTransaction, default_selection, interactive_selection, parse_selection
from .manifest import TOOL_MANIFEST
from .models import Status, ToolHealth
from .mcp import CodexVisibleMcpClient, verify_mcp
from .platforms import install_plan
from .process import ProcessRunner
from .releases import install_cplt_release, install_opengrep_release
from .reporting import discovery_payload, render_json, render_summary, summarize
from .transport import HttpMcpTransport
from . import __version__


def _add_global_options(parser, *, suppress_defaults=False):
    default = argparse.SUPPRESS if suppress_defaults else False
    parser.add_argument("--dry-run", action="store_true", default=default, help="show intended operations without mutation")
    parser.add_argument("--json", action="store_true", default=default, help="emit stable JSON output")
    parser.add_argument("--non-interactive", action="store_true", default=default, help="never prompt")
    parser.add_argument("--update", action="store_true", default=default, help="update selected installed tools without downgrading")
    parser.add_argument("--mcp-mode", choices=("manage", "verify-only"), default=argparse.SUPPRESS if suppress_defaults else "manage")
    parser.add_argument("--codex-home", default=argparse.SUPPRESS if suppress_defaults else None)


def build_parser():
    parser = argparse.ArgumentParser(prog="codex-tools", description="Install and verify Codex development tools safely")
    _add_global_options(parser)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    check = subparsers.add_parser("check", help="read-only health check")
    _add_global_options(check, suppress_defaults=True)
    repair = subparsers.add_parser("repair", help="repair unhealthy tools only")
    _add_global_options(repair, suppress_defaults=True)
    install = subparsers.add_parser("install", help="install selected tools")
    install.add_argument("tools", nargs="*")
    _add_global_options(install, suppress_defaults=True)
    return parser


def _codex_validate(path: Path, runner: ProcessRunner, environ: Mapping[str, str]) -> bool:
    validation_env = dict(environ)
    validation_env["CODEX_CONFIG"] = str(path)
    validation_env["CODEX_HOME"] = str(path.parent)
    return runner.run(("codex", "mcp", "list"), env=validation_env).returncode == 0


def _internet_available() -> bool:
    try:
        request = urllib.request.Request("https://github.com", method="HEAD")
        with urllib.request.urlopen(request, timeout=10) as response:
            return 200 <= response.status < 500
    except Exception:
        return False


def _read_config_bytes(path: Path) -> tuple[bool, bytes | None]:
    try:
        return (True, path.read_bytes()) if path.exists() else (True, None)
    except OSError:
        return False, None


def main(argv: Sequence[str] | None = None, *, environ: Mapping[str, str] | None = None, platform_facts: Mapping[str, str] | None = None, runner: ProcessRunner | None = None, connectivity_probe=None, mcp_transport=None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    environ = dict(os.environ if environ is None else environ)
    if args.codex_home:
        environ["CODEX_HOME"] = str(Path(args.codex_home).expanduser())
    runner = runner or ProcessRunner()
    environ = managed_bin_environment(environ, runner)
    initial = discover(environ, runner, platform_facts)
    config_parent = Path(initial.config_path).parent
    config_path = Path(initial.config_path)
    try:
        free_bytes = shutil.disk_usage(config_parent if config_parent.exists() else Path(environ.get("HOME", "."))).free
        writable = os.access(config_parent if config_parent.exists() else config_parent.parent, os.W_OK)
    except OSError:
        free_bytes, writable = 0, False
    connectivity = (connectivity_probe or _internet_available)()
    okay, issues = preflight(initial, free_bytes=free_bytes, connectivity=connectivity, writable=writable)
    command = args.command or "install"
    requested = getattr(args, "tools", ())
    try:
        selected = parse_selection(requested, TOOL_MANIFEST) if requested else default_selection(TOOL_MANIFEST)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    actions = []
    for name in selected:
        health = initial.tools[name]
        if health.status == Status.HEALTHY and not args.update:
            continue
        definition = TOOL_MANIFEST[name]
        if definition.kind in {"cli", "cli_mcp"}:
            actions.extend(" ".join(command) for command in install_plan(definition, initial.platform, args.update))
        elif args.mcp_mode == "manage":
            actions.append(f"merge managed MCP table: {name}")
    readonly = args.dry_run
    if command == "install" and not readonly and not requested and not args.non_interactive and sys.stdin.isatty():
        preview = discovery_payload(initial, selected, actions)
        print(render_summary(preview))
        choice = interactive_selection(TOOL_MANIFEST)
        if choice is None:
            return 0
        selected = choice
    if not okay or readonly:
        payload = discovery_payload(initial, selected, actions)
        payload["issues"] = list(issues)
        print(render_json(payload) if args.json else render_summary(payload))
        return 0 if okay and all(item.status == Status.HEALTHY for item in initial.tools.values()) else 1
    config_captured, config_before = _read_config_bytes(config_path)
    if not config_captured:
        payload = discovery_payload(initial, selected, actions)
        payload["issues"] = [*payload["issues"], "Codex config pre-state could not be captured safely"]
        print(render_json(payload) if args.json else render_summary(payload))
        return 1

    def install(definition):
        plans = install_plan(definition, initial.platform, args.update)
        if not plans:
            raise RuntimeError("No supported official installation strategy")
        command_plan = plans[0]
        for dependency in definition.dependencies:
            if initial.capabilities.get(dependency, False):
                continue
            plans_for_dependency = dependency_plan(dependency, initial.platform.platform_key)
            if not plans_for_dependency or runner.run(plans_for_dependency[0], env=environ, timeout=300).returncode:
                raise RuntimeError("Dependency installation failed: " + dependency)
            refreshed = managed_bin_environment(environ, runner)
            environ.clear()
            environ.update(refreshed)
        if command_plan[0] == "internal-github-release":
            destination = Path(environ.get("HOME", str(Path.home()))) / ".local" / "bin"
            install_cplt_release(initial.platform.machine, destination)
            return
        if command_plan[0] == "internal-opengrep-release":
            destination = Path(environ.get("HOME", str(Path.home()))) / ".local" / "bin"
            install_opengrep_release(initial.platform.platform_key, initial.platform.machine, destination)
            return
        result = runner.run(command_plan, env=environ, timeout=300)
        if result.returncode:
            raise RuntimeError("Package installation failed")

    def configure(definition):
        if definition.kind not in {"mcp", "cli_mcp"} or not definition.mcp or definition.mcp.get("optional"):
            return
        store = None
        credential = None
        credential_name = definition.credential_env
        previous_credential = environ.get(credential_name) if credential_name else None
        had_previous_credential = bool(credential_name and credential_name in environ)
        config_pre_state = config_path.read_bytes() if config_path.exists() else None
        if credential_name:
            if initial.platform.platform_key == "macos" and initial.capabilities.get("security"):
                store = MacOSKeychainStore(runner)
            elif initial.capabilities.get("secret-tool"):
                store = LibsecretStore(runner)
            else:
                codex_home = Path(environ.get("CODEX_HOME", str(Path(environ.get("HOME", str(Path.home()))) / ".codex")))
                store = ProtectedFileStore(codex_home / "credentials")
            credential = resolve_credential(credential_name, environ, store, None if args.non_interactive else MaskedPrompt(), args.non_interactive)
            if not credential.available:
                raise LifecycleStatusError(Status.AUTH_REQUIRED, f"{credential_name} unavailable")
            environ[credential_name] = credential.value or ""
        try:
            update_config_transactionally(
                config_path, definition.name, dict(definition.mcp or {}),
                lambda path: _codex_validate(path, runner, environ), datetime.now().strftime("%Y%m%d-%H%M%S"),
            )
            config_managed_state = config_path.read_bytes()
            config_managed_inode = config_path.stat(follow_symlinks=False).st_ino
        except Exception:
            if credential_name:
                if had_previous_credential:
                    environ[credential_name] = previous_credential or ""
                else:
                    environ.pop(credential_name, None)
            raise

        def rollback():
            try:
                restore_config_exact(
                    config_path,
                    config_pre_state,
                    expected_current=config_managed_state,
                    expected_inode=config_managed_inode,
                )
            finally:
                if credential_name:
                    if had_previous_credential:
                        environ[credential_name] = previous_credential or ""
                    else:
                        environ.pop(credential_name, None)

        def commit():
            if credential_name and credential and credential.source == "prompt" and store:
                store.set(credential_name, credential.value or "")

        return PendingTransaction(commit=commit, rollback=rollback)

    def verify(definition):
        if definition.kind == "mcp":
            return verify_mcp(definition, CodexVisibleMcpClient(runner, mcp_transport or HttpMcpTransport(), environ), not definition.credential_env or bool(environ.get(definition.credential_env)))
        return all(runner.run(command, env=environ).returncode == 0 for command in definition.verify)

    results = LifecycleExecutor(install, verify, configure).execute(
        TOOL_MANIFEST.values(), initial.tools, mode=command, selected=selected, mcp_mode=args.mcp_mode
    )
    final = discover(environ, runner, platform_facts)
    final_tools = dict(final.tools)
    for name, result in results.items():
        if result.status in {Status.FAILED, Status.BLOCKED, Status.SKIPPED, Status.BROKEN, Status.AUTH_REQUIRED, Status.INVALID_CONFIG}:
            final_tools[name] = result
    final = final.__class__(final.platform, final_tools, final.codex_installed, final.config_path, final.config_valid, final.capabilities, final.credentials, final.issues)
    payload = discovery_payload(final, selected)
    config_after_captured, config_after = _read_config_bytes(config_path)
    if not config_after_captured:
        payload["issues"] = [*payload["issues"], "Codex config post-state could not be captured safely"]
    run_summary = summarize(
        final,
        initial,
        config_preserved=config_after_captured and config_before == config_after,
        selected=selected,
    )
    payload["summary"] = {
        "installed": run_summary.installed, "repaired": run_summary.repaired,
        "already_healthy": run_summary.already_healthy, "failed": run_summary.failed,
        "auth_required": run_summary.auth_required,
        "config_valid": run_summary.config_valid, "config_preserved": run_summary.config_preserved,
    }
    print(render_json(payload) if args.json else render_summary(payload))
    return 0 if config_after_captured and all(final.tools[name].status == Status.HEALTHY for name in selected) else 1


def entrypoint():
    raise SystemExit(main())
