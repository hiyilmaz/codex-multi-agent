from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Mapping, Protocol, Sequence

from .models import Status, ToolDefinition, ToolHealth


class CodexMcpClient(Protocol):
    def visible(self, name: str) -> bool: ...
    def tools(self, name: str) -> Sequence[str]: ...
    def call_read_only(self, name: str, tool: str, arguments: Mapping[str, object] | None = None) -> bool: ...


WRITE_WORDS = ("create", "push", "issue", "pull_request", "comment", "workflow", "delete", "update")


class CodexVisibleMcpClient:
    """Uses supported Codex visibility plus an injected MCP JSON-RPC transport."""

    def __init__(self, runner, transport, env=None): self.runner, self.transport, self.env = runner, transport, dict(env or {})

    def _json(self, command):
        result = self.runner.run(command, env=self.env)
        if result.returncode:
            raise RuntimeError("Codex MCP probe failed")
        return json.loads(result.stdout)

    def visible(self, name: str) -> bool:
        payload = self._json(("codex", "mcp", "get", name, "--json"))
        return bool(payload) and payload.get("name", name) == name

    def tools(self, name: str) -> Sequence[str]:
        payload = self.transport.request(name, "tools/list", {}, self.env)
        entries = payload.get("tools", payload if isinstance(payload, list) else [])
        return tuple(item["name"] if isinstance(item, dict) else str(item) for item in entries)

    def call_read_only(self, name: str, tool: str, arguments=None) -> bool:
        if any(word in tool.lower() for word in WRITE_WORDS):
            return False
        payload = self.transport.request(name, "tools/call", {"name": tool, "arguments": dict(arguments or {})}, self.env)
        evidence = payload.get("content") or payload.get("structuredContent")
        return bool(evidence) and not payload.get("isError", False)


def verify_mcp(definition: ToolDefinition, client: CodexMcpClient, credential_available: bool = True) -> ToolHealth:
    if definition.credential_env and not credential_available:
        return ToolHealth(definition.name, Status.AUTH_REQUIRED, f"{definition.credential_env} unavailable")
    try:
        if not client.visible(definition.name):
            return ToolHealth(definition.name, Status.INVALID_CONFIG, "Codex cannot load MCP")
        actual = set(client.tools(definition.name))
        expected = set(definition.mcp.get("expected_tools", ())) if definition.mcp else set()
        functional_calls = definition.mcp.get("functional_calls", ()) if definition.mcp else ()
        if expected and not expected.issubset(actual):
            return ToolHealth(definition.name, Status.BROKEN, "Upstream MCP tool names changed; expected=" + ",".join(sorted(expected)))
        if not functional_calls:
            return ToolHealth(definition.name, Status.BROKEN, "No read-only functional validation defined")
        for tool, arguments in functional_calls:
            if any(word in tool.lower() for word in WRITE_WORDS):
                return ToolHealth(definition.name, Status.FAILED, "Unsafe functional validation refused")
            if tool not in actual or not client.call_read_only(definition.name, tool, arguments):
                return ToolHealth(definition.name, Status.BROKEN, f"Read-only MCP validation failed: {tool}")
        return ToolHealth(definition.name, Status.HEALTHY)
    except Exception as exc:
        return ToolHealth(definition.name, Status.BROKEN, f"MCP validation failed: {exc.__class__.__name__}")
