from __future__ import annotations

import json
from typing import Mapping, Protocol, Sequence

from .models import CheckResult, Status, ToolDefinition, ToolHealth


MCP_STAGES = ("mcp_config", "mcp_connection", "mcp_tool_names", "mcp_call")


class CodexMcpClient(Protocol):
    def visible(self, name: str) -> bool: ...
    def tools(self, name: str) -> Sequence[str]: ...
    def call_read_only(self, name: str, tool: str, arguments: Mapping[str, object] | None = None) -> bool: ...


WRITE_WORDS = ("create", "push", "issue", "pull_request", "comment", "workflow", "delete", "update")


class McpEndpointMismatch(ValueError):
    pass


class CodexVisibleMcpClient:
    """Uses supported Codex visibility plus an injected MCP JSON-RPC transport."""

    def __init__(self, runner, transport, env=None, *, expected_urls: Mapping[str, str] | None = None):
        self.runner = runner
        self.transport = transport
        self.env = dict(env or {})
        self.expected_urls = expected_urls or {}

    def _json(self, command):
        result = self.runner.run(command, env=self.env)
        if result.returncode:
            raise RuntimeError("Codex MCP probe failed")
        return json.loads(result.stdout)

    def visible(self, name: str) -> bool:
        payload = self._json(("codex", "mcp", "get", name, "--json"))
        if not payload or payload.get("name", name) != name or payload.get("enabled", True) is False:
            return False
        expected_url = self.expected_urls.get(name)
        if expected_url is not None:
            transport = payload.get("transport")
            if not isinstance(transport, dict) or transport.get("type") != "streamable_http" or transport.get("url") != expected_url:
                raise McpEndpointMismatch
        return True

    def tools(self, name: str) -> Sequence[str]:
        payload = self.transport.request(name, "tools/list", {}, self.env)
        entries = payload["tools"] if isinstance(payload, dict) else payload
        if not isinstance(entries, list):
            raise ValueError("Invalid MCP tools/list result")
        names = tuple(entry["name"] for entry in entries)
        if not all(isinstance(tool, str) and tool for tool in names):
            raise ValueError("Invalid MCP tool name")
        return names

    def call_read_only(self, name: str, tool: str, arguments=None) -> bool:
        if any(word in tool.lower() for word in WRITE_WORDS):
            return False
        payload = self.transport.request(name, "tools/call", {"name": tool, "arguments": dict(arguments or {})}, self.env)
        evidence = payload.get("content") or payload.get("structuredContent")
        return bool(evidence) and not payload.get("isError", False)


def check_visibility(name: str, client: CodexMcpClient) -> CheckResult:
    try:
        if not client.visible(name):
            return CheckResult(Status.INVALID_CONFIG.value, "Codex cannot load MCP or the registration is disabled")
    except McpEndpointMismatch:
        return CheckResult(Status.INVALID_CONFIG.value, "Codex MCP endpoint does not match the manifest")
    except Exception as exc:
        return CheckResult(Status.BROKEN.value, f"Codex MCP visibility check failed: {exc.__class__.__name__}")
    return CheckResult(Status.HEALTHY.value, "Codex can read the enabled registration")


def verify_mcp(definition: ToolDefinition, client: CodexMcpClient, credential_available: bool = True) -> ToolHealth:
    checks = {stage: CheckResult("NOT_CHECKED") for stage in MCP_STAGES}

    def fail(stage: str, status: Status, detail: str) -> ToolHealth:
        checks[stage] = CheckResult(status.value, detail)
        return ToolHealth(definition.name, status, detail, checks=checks)

    if definition.credential_env and not credential_available:
        return ToolHealth(definition.name, Status.AUTH_REQUIRED, f"{definition.credential_env} unavailable", checks=checks)
    visibility = checks["mcp_config"] = check_visibility(definition.name, client)
    if visibility.status != Status.HEALTHY.value:
        return ToolHealth(definition.name, Status(visibility.status), visibility.detail, checks=checks)
    try:
        actual = set(client.tools(definition.name))
    except Exception as exc:
        return fail("mcp_connection", Status.BROKEN, f"MCP connection or tools/list failed: {exc.__class__.__name__}")
    checks["mcp_connection"] = CheckResult(Status.HEALTHY.value, "Manifest endpoint responded to tools/list")
    definition_mcp = definition.mcp or {}
    calls = definition_mcp.get("functional_calls", ())
    expected = set(definition_mcp.get("expected_tools", ())) | {tool for tool, _ in calls}
    missing = expected - actual
    if missing:
        return fail(
            "mcp_tool_names", Status.BROKEN,
            f"Upstream MCP tool names changed; missing={','.join(sorted(missing))} "
            f"expected={json.dumps(sorted(expected))} actual={json.dumps(sorted(actual))}",
        )
    if expected:
        checks["mcp_tool_names"] = CheckResult(Status.HEALTHY.value, ", ".join(sorted(expected)))
    if not calls:
        return fail("mcp_call", Status.BROKEN, "No read-only functional validation defined")
    for tool, arguments in calls:
        if any(word in tool.lower() for word in WRITE_WORDS):
            return fail("mcp_call", Status.FAILED, "Unsafe functional validation refused")
        detail = f"Read-only MCP validation failed: {tool}"
        try:
            if not client.call_read_only(definition.name, tool, arguments):
                return fail("mcp_call", Status.BROKEN, detail)
        except Exception as exc:
            return fail("mcp_call", Status.BROKEN, f"{detail}: {exc.__class__.__name__}")
    checks["mcp_call"] = CheckResult(Status.HEALTHY.value, ", ".join(tool for tool, _ in calls))
    return ToolHealth(definition.name, Status.HEALTHY, checks=checks)
