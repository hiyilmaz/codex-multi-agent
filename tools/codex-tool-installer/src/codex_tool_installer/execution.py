from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping

from .models import Status, ToolDefinition, ToolHealth


class LifecycleStatusError(RuntimeError):
    def __init__(self, status: Status, detail: str):
        super().__init__(detail)
        self.status = status
        self.detail = detail


@dataclass(frozen=True)
class PendingTransaction:
    commit: Callable[[], None]
    rollback: Callable[[], None]


class LifecycleExecutor:
    def __init__(self, install: Callable[[ToolDefinition], None], verify: Callable[[ToolDefinition], bool], configure: Callable[[ToolDefinition], None] | None = None):
        self.install = install
        self.verify = verify
        self.configure = configure or (lambda _: None)

    def _verification(self, tool: ToolDefinition, false_status: Status) -> ToolHealth:
        result = self.verify(tool)
        if isinstance(result, ToolHealth):
            return result
        return ToolHealth(tool.name, Status.HEALTHY if result else false_status)

    def execute(
        self,
        tools: Iterable[ToolDefinition],
        health: Mapping[str, ToolHealth],
        *,
        mode: str = "install",
        selected: set[str] | None = None,
        mcp_mode: str = "manage",
    ):
        if mcp_mode not in {"manage", "verify-only"}:
            raise ValueError(f"Unsupported MCP mode: {mcp_mode}")
        definitions = list(tools)
        selected = selected if selected is not None else {tool.name for tool in definitions}
        results = dict(health)
        for tool in definitions:
            if tool.name not in selected:
                results[tool.name] = ToolHealth(tool.name, Status.SKIPPED)
                continue
            current = health.get(tool.name, ToolHealth(tool.name, Status.MISSING))
            if any(dep in results and results[dep].status in {Status.FAILED, Status.BLOCKED, Status.MISSING} for dep in tool.dependencies):
                results[tool.name] = ToolHealth(tool.name, Status.BLOCKED, "Required dependency unavailable")
                continue
            if current.status == Status.HEALTHY and tool.kind not in {"mcp", "cli_mcp"}:
                results[tool.name] = current
                continue
            if tool.kind == "mcp" and mcp_mode == "verify-only":
                if current.status in {Status.HEALTHY, Status.BROKEN}:
                    try:
                        results[tool.name] = self._verification(tool, Status.BROKEN)
                    except Exception as exc:
                        results[tool.name] = ToolHealth(tool.name, Status.BROKEN, f"{exc.__class__.__name__}: verification failed")
                else:
                    results[tool.name] = current
                continue
            if mode == "check":
                if tool.kind == "mcp" and current.status not in {Status.MISSING, Status.AUTH_REQUIRED, Status.INVALID_CONFIG}:
                    try:
                        results[tool.name] = self._verification(tool, Status.BROKEN)
                    except Exception as exc:
                        results[tool.name] = ToolHealth(tool.name, Status.BROKEN, f"{exc.__class__.__name__}: verification failed")
                else:
                    results[tool.name] = current
                continue
            if mode == "repair" and current.status not in {Status.BROKEN, Status.INVALID_CONFIG, Status.AUTH_REQUIRED}:
                results[tool.name] = ToolHealth(tool.name, Status.SKIPPED)
                continue
            transaction = None
            try:
                if current.status in {Status.MISSING, Status.BROKEN} and tool.kind in {"cli", "cli_mcp"}:
                    self.install(tool)
                if (
                    mcp_mode == "manage"
                    and tool.kind in {"mcp", "cli_mcp"}
                    and current.status != Status.HEALTHY
                ):
                    transaction = self.configure(tool)
                verified = self._verification(tool, Status.FAILED)
                if verified.status != Status.HEALTHY:
                    raise LifecycleStatusError(verified.status, verified.detail or "functional verification failed")
                if isinstance(transaction, PendingTransaction):
                    transaction.commit()
                results[tool.name] = ToolHealth(tool.name, Status.HEALTHY)
            except Exception as exc:
                rollback_failed = False
                if isinstance(transaction, PendingTransaction):
                    try:
                        transaction.rollback()
                    except Exception:
                        rollback_failed = True
                if rollback_failed:
                    results[tool.name] = ToolHealth(tool.name, Status.FAILED, "Rollback failed")
                elif isinstance(exc, LifecycleStatusError):
                    results[tool.name] = ToolHealth(tool.name, exc.status, exc.detail)
                else:
                    results[tool.name] = ToolHealth(tool.name, Status.FAILED, f"{exc.__class__.__name__}: operation failed")
        return results


def default_selection(tool_names: Iterable[str]) -> set[str]:
    return set(tool_names)


def parse_selection(requested: Iterable[str], available: Iterable[str]) -> set[str]:
    allowed = set(available)
    selected = set(requested)
    unknown = selected - allowed
    if unknown:
        raise ValueError("Unknown tools: " + ", ".join(sorted(unknown)))
    return selected


def interactive_selection(tool_names: Iterable[str], input_fn=input, output_fn=print) -> set[str] | None:
    available = tuple(tool_names)
    output_fn("Actions: Continue / Customize selection / Cancel")
    action = input_fn("Choose [C/u/x]: ").strip().lower()
    if action in {"x", "cancel"}:
        return None
    if action not in {"u", "customize"}:
        return set(available)
    output_fn("Enter comma-separated tool names to keep selected.")
    raw = input_fn("Tools: ")
    requested = [part.strip() for part in raw.split(",") if part.strip()]
    return parse_selection(requested, available)
