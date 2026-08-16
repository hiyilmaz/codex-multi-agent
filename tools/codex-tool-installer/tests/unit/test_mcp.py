import unittest

from codex_tool_installer.manifest import TOOL_MANIFEST
from codex_tool_installer.mcp import verify_mcp
from codex_tool_installer.models import Status


class Client:
    def __init__(self, visible=True, tools=(), succeeds=True): self.is_visible, self.tool_names, self.succeeds, self.calls = visible, tools, succeeds, []
    def visible(self, name): return self.is_visible
    def tools(self, name): return self.tool_names
    def call_read_only(self, name, tool, arguments=None): self.calls.append((name, tool, arguments)); return self.succeeds


class McpTests(unittest.TestCase):
    def test_credentials_and_codex_visibility_are_required(self):
        self.assertEqual(Status.AUTH_REQUIRED, verify_mcp(TOOL_MANIFEST["github"], Client(), False).status)
        self.assertEqual(Status.INVALID_CONFIG, verify_mcp(TOOL_MANIFEST["github"], Client(False), True).status)

    def test_read_only_functional_validation(self):
        github = Client(tools=("search_repositories",))
        self.assertEqual(Status.HEALTHY, verify_mcp(TOOL_MANIFEST["github"], github).status)
        self.assertEqual("search_repositories", github.calls[0][1])
        context = Client(tools=("resolve-library-id", "query-docs"), succeeds=False)
        self.assertEqual(Status.BROKEN, verify_mcp(TOOL_MANIFEST["context7"], context).status)

    def test_deepwiki_renames_are_reported_without_false_pass(self):
        state = verify_mcp(TOOL_MANIFEST["deepwiki"], Client(tools=("renamed",)))
        self.assertEqual(Status.BROKEN, state.status)
        self.assertIn("changed", state.detail)

    def test_empty_functional_result_fails_closed(self):
        class EmptyClient(Client):
            def call_read_only(self, name, tool, arguments=None): return False
        state = verify_mcp(TOOL_MANIFEST["github"], EmptyClient(tools=("search_repositories",)))
        self.assertEqual(Status.BROKEN, state.status)


if __name__ == "__main__": unittest.main()
