import unittest

from helpers import ADAPTER_ROOT  # noqa: F401
from claude_agent_sdk_adapter.permissions import DISALLOWED_BUILTIN_TOOLS, build_options
from claude_agent_sdk_adapter.runner import QueryRequest


EXPECTED_DENY = (
    "AskUserQuestion", "Bash", "Edit", "Glob", "Grep", "KillShell",
    "NotebookEdit", "Read", "Skill", "Task", "TaskOutput", "TodoWrite",
    "WebFetch", "WebSearch", "Write",
)


class PermissionTests(unittest.TestCase):
    def test_builds_fail_closed_options(self):
        options = build_options(QueryRequest(prompt="hello"))
        self.assertEqual(options.tools, [])
        self.assertEqual(options.allowed_tools, [])
        self.assertEqual(options.setting_sources, [])
        self.assertEqual(options.permission_mode, "dontAsk")
        self.assertEqual(tuple(options.disallowed_tools), EXPECTED_DENY)
        self.assertEqual(DISALLOWED_BUILTIN_TOOLS, EXPECTED_DENY)
        self.assertTrue(options.strict_mcp_config)
        self.assertEqual(options.mcp_servers, {})

    def test_restrictions_are_not_request_overrides(self):
        fields = QueryRequest.__dataclass_fields__
        for forbidden in ("tools", "allowed_tools", "setting_sources", "permission_mode"):
            self.assertNotIn(forbidden, fields)


if __name__ == "__main__":
    unittest.main()
