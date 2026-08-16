import unittest

from codex_tool_installer.config import ConfigCollision, merge_managed_mcp


class TomlMergeTests(unittest.TestCase):
    def test_complex_config_preserves_all_unrelated_bytes(self):
        original = (
            '# user comment\nmodel = "custom"\napproval_policy = "never"\n\n'
            '[mcp_servers.custom]\ncommand = "custom-server"\n# keep me\n'
        )
        block = {"url": "https://example.invalid/mcp", "enabled": True}
        merged = merge_managed_mcp(original, "deepwiki", block)
        self.assertTrue(merged.startswith(original))
        self.assertIn("[mcp_servers.deepwiki]", merged)
        self.assertEqual(1, merged.count("[mcp_servers.deepwiki]"))
        self.assertEqual(merged, merge_managed_mcp(merged, "deepwiki", block))

    def test_custom_managed_name_collision_is_refused_without_mutation(self):
        original = '[mcp_servers.github]\ncommand = "my-company-github"\n'
        with self.assertRaises(ConfigCollision):
            merge_managed_mcp(
                original,
                "github",
                {"url": "https://api.githubcopilot.com/mcp/", "bearer_token_env_var": "GITHUB_PAT_TOKEN"},
            )
        self.assertEqual('[mcp_servers.github]\ncommand = "my-company-github"\n', original)

    def test_repair_preserves_comments_between_managed_and_next_table(self):
        original = (
            '# Managed by codex-tool-installer\n[mcp_servers.deepwiki]\nurl = "old"\n'
            '\n# unrelated next-table comment\n[mcp_servers.custom]\ncommand = "mine"\n'
        )
        merged = merge_managed_mcp(original, "deepwiki", {"url": "new"})
        self.assertIn('# unrelated next-table comment\n[mcp_servers.custom]\ncommand = "mine"\n', merged)
        self.assertEqual(1, merged.count("# unrelated next-table comment"))

    def test_header_like_text_inside_multiline_string_is_not_a_table(self):
        original = 'message = """\n[mcp_servers.github]\ncommand = "owned text"\n"""\n'
        merged = merge_managed_mcp(original, "github", {"url": "https://example.invalid"})
        self.assertTrue(merged.startswith(original))
        self.assertIn('# Managed by codex-tool-installer\n[mcp_servers.github]', merged)

    def test_escaped_multiline_delimiter_does_not_end_masking(self):
        original = 'message = """before \\""" still text\n[mcp_servers.github]\ncommand = "owned text"\n"""\n'
        merged = merge_managed_mcp(original, "github", {"url": "https://example.invalid"})
        self.assertTrue(merged.startswith(original))
        self.assertEqual(1, merged.count("# Managed by codex-tool-installer"))


if __name__ == "__main__":
    unittest.main()
