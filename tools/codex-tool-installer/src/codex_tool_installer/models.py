from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class Status(str, Enum):
    HEALTHY = "HEALTHY"
    MISSING = "MISSING"
    INSTALLING = "INSTALLING"
    CONFIGURING = "CONFIGURING"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    INVALID_CONFIG = "INVALID_CONFIG"
    BROKEN = "BROKEN"
    BLOCKED = "BLOCKED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    kind: str
    executable: str | None
    platforms: tuple[str, ...]
    verify: tuple[tuple[str, ...], ...]
    installs: Mapping[str, tuple[tuple[str, ...], ...]] = field(default_factory=dict)
    mcp: Mapping[str, object] | None = None
    credential_env: str | None = None
    dependencies: tuple[str, ...] = ()
    project_init_required: bool = False


@dataclass(frozen=True)
class ToolHealth:
    name: str
    status: Status
    detail: str = ""
    version: str | None = None


@dataclass(frozen=True)
class PlatformInfo:
    system: str
    release: str
    machine: str
    shell: str
    path: str
    supported: bool
    platform_key: str
    reason: str = ""


@dataclass(frozen=True)
class DiscoveryResult:
    platform: PlatformInfo
    tools: Mapping[str, ToolHealth]
    codex_installed: bool
    config_path: str
    config_valid: bool
    capabilities: Mapping[str, bool]
    credentials: Mapping[str, bool]
    issues: Sequence[str] = ()


@dataclass(frozen=True)
class TransactionResult:
    changed: bool
    backup_path: str | None = None


@dataclass(frozen=True)
class RunSummary:
    tools: Mapping[str, ToolHealth]
    installed: int = 0
    repaired: int = 0
    already_healthy: int = 0
    failed: int = 0
    config_valid: bool = True
    config_preserved: bool = True
    credentials: Mapping[str, bool] = field(default_factory=dict)
    issues: Sequence[str] = ()
