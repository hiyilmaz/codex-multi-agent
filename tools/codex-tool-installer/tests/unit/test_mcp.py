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
    deepwiki_tools = ("ask_wiki_question", "read_wiki_contents", "read_wiki_structure")

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
        client = Client(tools=("ask_question", *self.deepwiki_tools[1:]))
        state = verify_mcp(TOOL_MANIFEST["deepwiki"], client)
        self.assertEqual(Status.BROKEN, state.status)
        self.assertIn("missing=ask_wiki_question", state.detail)
        self.assertIn('expected=["ask_wiki_question", "read_wiki_contents", "read_wiki_structure"]', state.detail)
        self.assertIn('actual=["ask_question", "read_wiki_contents", "read_wiki_structure"]', state.detail)
        self.assertEqual("HEALTHY", state.checks["mcp_connection"].status)
        self.assertEqual("BROKEN", state.checks["mcp_tool_names"].status)
        self.assertEqual("NOT_CHECKED", state.checks["mcp_call"].status)
        self.assertEqual([], client.calls)

    def test_deepwiki_connection_failure_identifies_the_list_stage(self):
        class DisconnectedClient(Client):
            def tools(self, name):
                raise TimeoutError("private transport detail")

        client = DisconnectedClient()
        state = verify_mcp(TOOL_MANIFEST["deepwiki"], client)
        self.assertEqual(Status.BROKEN, state.status)
        self.assertIn("connection or tools/list failed: TimeoutError", state.detail)
        self.assertNotIn("private transport detail", state.detail)
        self.assertEqual("HEALTHY", state.checks["mcp_config"].status)
        self.assertEqual("BROKEN", state.checks["mcp_connection"].status)
        self.assertEqual("NOT_CHECKED", state.checks["mcp_tool_names"].status)
        self.assertEqual([], client.calls)

    def test_deepwiki_requires_a_successful_read_only_call(self):
        for succeeds, status in ((True, Status.HEALTHY), (False, Status.BROKEN)):
            with self.subTest(succeeds=succeeds):
                client = Client(tools=self.deepwiki_tools, succeeds=succeeds)
                state = verify_mcp(TOOL_MANIFEST["deepwiki"], client)
                self.assertEqual(status, state.status)
                self.assertEqual(status.value, state.checks["mcp_call"].status)
                self.assertEqual([("deepwiki", "read_wiki_structure", {"repoName": "openai/codex"})], client.calls)
                if not succeeds:
                    self.assertIn("Read-only MCP validation failed: read_wiki_structure", state.detail)

    def test_empty_functional_result_fails_closed(self):
        class EmptyClient(Client):
            def call_read_only(self, name, tool, arguments=None): return False
        state = verify_mcp(TOOL_MANIFEST["github"], EmptyClient(tools=("search_repositories",)))
        self.assertEqual(Status.BROKEN, state.status)


if __name__ == "__main__": unittest.main()
