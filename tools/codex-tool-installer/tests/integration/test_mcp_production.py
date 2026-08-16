import json
import unittest

from codex_tool_installer.manifest import TOOL_MANIFEST
from codex_tool_installer.mcp import CodexVisibleMcpClient, verify_mcp
from codex_tool_installer.models import Status
from codex_tool_installer.process import CommandResult


class Runner:
    def __init__(self): self.calls = []
    def run(self, command, **kwargs):
        self.calls.append(tuple(command))
        if command[2] == "get": return CommandResult(0, json.dumps({"name": command[3]}))
        return CommandResult(1)


class Transport:
    def __init__(self): self.calls = []
    def request(self, name, method, params, environ):
        self.calls.append((name, method, params))
        if method == "tools/list": return {"tools": [{"name": "search_repositories"}]}
        return {"content": [{"type": "text", "text": "read-only result"}], "isError": False}


class ProductionMcpTests(unittest.TestCase):
    def test_github_uses_codex_visibility_listing_and_read_only_call(self):
        runner = Runner()
        transport = Transport()
        state = verify_mcp(TOOL_MANIFEST["github"], CodexVisibleMcpClient(runner, transport), True)
        self.assertEqual(Status.HEALTHY, state.status)
        self.assertEqual(("codex", "mcp", "get", "github", "--json"), runner.calls[0])
        self.assertEqual("tools/list", transport.calls[0][1])
        self.assertEqual("tools/call", transport.calls[-1][1])
        self.assertEqual("codex", transport.calls[-1][2]["arguments"]["query"])


if __name__ == "__main__": unittest.main()
