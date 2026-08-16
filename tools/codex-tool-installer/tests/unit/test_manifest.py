import unittest

from codex_tool_installer.manifest import TOOL_MANIFEST


class ManifestTests(unittest.TestCase):
    def test_manifest_contains_exactly_all_11_tools(self):
        expected = {
            "rg", "graphify", "serena", "ast-grep", "deepwiki", "github",
            "opengrep", "osv-scanner", "betterleaks", "cplt", "context7",
        }
        self.assertEqual(expected, set(TOOL_MANIFEST))
        for name, tool in TOOL_MANIFEST.items():
            self.assertEqual(name, tool.name)
            self.assertTrue(tool.platforms)
            self.assertTrue(tool.verify)
            self.assertFalse(tool.project_init_required)
        self.assertEqual("ast-grep", TOOL_MANIFEST["ast-grep"].executable)
        forbidden = {"init", "trust", "scan", "index"}
        for tool in TOOL_MANIFEST.values():
            flattened = " ".join(part for command in tool.verify for part in command)
            self.assertTrue(forbidden.isdisjoint(flattened.split()))

    def test_install_sources_are_immutable_or_internal_verified_releases(self):
        flattened = [
            " ".join(command)
            for tool in TOOL_MANIFEST.values()
            for platform_commands in tool.installs.values()
            for command in platform_commands
        ]
        self.assertFalse(any("@latest" in command for command in flattened))
        self.assertIn("uv tool install graphifyy==0.9.45", flattened)
        self.assertIn("npm install -g @ast-grep/cli@0.45.1", flattened)
        self.assertIn("go install github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.5.0", flattened)
        self.assertIn("go install github.com/betterleaks/betterleaks@v1.7.4", flattened)
        serena = next(command for command in flattened if "oraios/serena" in command)
        self.assertRegex(serena, r"@[0-9a-f]{40}$")
        self.assertTrue(all("internal-opengrep-release" in command for command in flattened if "opengrep" in command))


if __name__ == "__main__":
    unittest.main()
