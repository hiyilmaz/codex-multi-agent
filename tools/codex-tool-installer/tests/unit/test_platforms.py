import unittest

from codex_tool_installer.manifest import TOOL_MANIFEST
from codex_tool_installer.platforms import detect_platform, ensure_path_line, install_plan


class PlatformTests(unittest.TestCase):
    def test_supported_platform_matrix_and_install_plans(self):
        mac = detect_platform({}, {"system": "Darwin", "machine": "arm64", "release": "25"})
        intel = detect_platform({}, {"system": "Darwin", "machine": "x86_64"})
        ubuntu22 = detect_platform({}, {"system": "Linux", "distribution": "Ubuntu", "version": "22.04", "machine": "x86_64"})
        ubuntu24 = detect_platform({}, {"system": "Linux", "distribution": "Ubuntu", "version": "24.04", "machine": "aarch64"})
        for info in (mac, intel, ubuntu22, ubuntu24):
            self.assertTrue(info.supported)
        self.assertEqual("brew", install_plan(TOOL_MANIFEST["rg"], mac)[0][0])
        self.assertEqual(("sudo", "apt-get"), install_plan(TOOL_MANIFEST["rg"], ubuntu22)[0][:2])
        self.assertEqual("upgrade", install_plan(TOOL_MANIFEST["rg"], mac, update=True)[0][1])

    def test_unsupported_platforms_fail_closed(self):
        for facts in (
            {"system": "Windows", "machine": "AMD64"},
            {"system": "Darwin", "machine": "ppc"},
            {"system": "Linux", "distribution": "Ubuntu", "version": "24.10"},
            {"system": "Linux", "distribution": "Fedora", "version": "40"},
        ):
            info = detect_platform({}, facts)
            self.assertFalse(info.supported)
            self.assertEqual((), install_plan(TOOL_MANIFEST["rg"], info))

    def test_path_line_is_idempotent(self):
        once = ensure_path_line("# profile\n", "/safe/bin")
        self.assertEqual(once, ensure_path_line(once, "/safe/bin"))
        self.assertEqual(1, once.count('/safe/bin'))


if __name__ == "__main__":
    unittest.main()
