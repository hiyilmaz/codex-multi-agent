from __future__ import annotations

import platform
from pathlib import Path
from typing import Mapping

from .models import PlatformInfo, ToolDefinition


def detect_platform(environ: Mapping[str, str], facts: Mapping[str, str] | None = None) -> PlatformInfo:
    facts = facts or {}
    system = facts.get("system", platform.system())
    machine = facts.get("machine", platform.machine())
    release = facts.get("release", platform.release())
    shell = environ.get("SHELL", "")
    path = environ.get("PATH", "")
    if system == "Darwin":
        supported = machine in {"arm64", "x86_64"}
        return PlatformInfo(system, release, machine, shell, path, supported, "macos", "" if supported else "Unsupported macOS architecture")
    if system == "Linux":
        os_release = facts.get("os_release", "")
        if not os_release and Path("/etc/os-release").exists():
            os_release = Path("/etc/os-release").read_text(errors="replace")
        ubuntu = "Ubuntu" in os_release or facts.get("distribution") == "Ubuntu"
        version = facts.get("version", "")
        if not version:
            for line in os_release.splitlines():
                if line.startswith("VERSION_ID="):
                    version = line.split("=", 1)[1].strip('"')
        supported = ubuntu and version in {"22.04", "24.04"}
        key = f"ubuntu-{version}" if ubuntu else "linux-unsupported"
        return PlatformInfo(system, version or release, machine, shell, path, supported, key, "" if supported else "Only Ubuntu 22.04/24.04 is supported")
    return PlatformInfo(system, release, machine, shell, path, False, "unsupported", "Unsupported operating system")


def install_plan(tool: ToolDefinition, platform_info: PlatformInfo, update: bool = False) -> tuple[tuple[str, ...], ...]:
    if not platform_info.supported or tool.kind not in {"cli", "cli_mcp"}:
        return ()
    key = "macos" if platform_info.platform_key == "macos" else "ubuntu"
    commands = tool.installs.get(key, ())
    if update and commands:
        first = commands[0]
        if first[:2] == ("brew", "install"):
            return (("brew", "upgrade", *first[2:]),)
    return tuple(commands)


def ensure_path_line(content: str, directory: str) -> str:
    line = f'export PATH="{directory}:$PATH"'
    if any(existing.strip() == line for existing in content.splitlines()):
        return content
    separator = "" if not content or content.endswith("\n") else "\n"
    return content + separator + line + "\n"
