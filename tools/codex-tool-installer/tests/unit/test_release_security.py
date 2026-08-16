import hashlib
import io
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from codex_tool_installer.releases import (
    CURRENT_OPENGREP_ASSETS,
    ReleaseInstallError,
    install_cplt_release,
    install_opengrep_release,
)


def release_archive(payload=b"binary"):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        info = tarfile.TarInfo("cplt")
        info.size = len(payload)
        archive.addfile(info, io.BytesIO(payload))
    return buffer.getvalue()


class Response(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class ReleaseSecurityTests(unittest.TestCase):
    def test_opengrep_release_is_versioned_and_checksum_verified(self):
        payload = b"opengrep-binary"
        seen = []

        def opener(url, timeout):
            seen.append(url)
            return Response(payload)

        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(
            CURRENT_OPENGREP_ASSETS,
            {("ubuntu", "x86_64"): ("opengrep_manylinux_x86", hashlib.sha256(payload).hexdigest())},
            clear=True,
        ):
            install_opengrep_release("ubuntu-24.04", "x86_64", Path(directory), opener=opener)
            self.assertIn("/v1.27.1/", seen[0])
            target = Path(directory) / "opengrep"
            self.assertEqual(payload, target.read_bytes())
            self.assertFalse(target.is_symlink())

    def test_release_requires_exact_version_and_checksum(self):
        archive = release_archive()
        seen = []

        def opener(url, timeout):
            seen.append(url)
            return Response(archive)

        with tempfile.TemporaryDirectory() as directory:
            install_cplt_release(
                "x86_64",
                Path(directory),
                version="0.3.0",
                checksums={"x86_64": hashlib.sha256(archive).hexdigest()},
                opener=opener,
            )
            self.assertNotIn("latest", seen[0])
            self.assertIn("/0.3.0/", seen[0])
            self.assertEqual(b"binary", (Path(directory) / "cplt").read_bytes())

    def test_checksum_failure_preserves_existing_binary(self):
        archive = release_archive(b"replacement")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            target = destination / "cplt"
            target.write_bytes(b"existing")
            with self.assertRaises(ReleaseInstallError):
                install_cplt_release(
                    "x86_64",
                    destination,
                    version="0.3.0",
                    checksums={"x86_64": "0" * 64},
                    opener=lambda *_args, **_kwargs: Response(archive),
                )
            self.assertEqual(b"existing", target.read_bytes())

    def test_hostile_predictable_temp_symlink_cannot_overwrite_target(self):
        archive = release_archive(b"replacement")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            victim = destination / "victim"
            victim.write_bytes(b"preserved")
            (destination / ".cplt.tmp").symlink_to(victim)
            install_cplt_release(
                "x86_64",
                destination,
                version="0.3.0",
                checksums={"x86_64": hashlib.sha256(archive).hexdigest()},
                opener=lambda *_args, **_kwargs: Response(archive),
            )
            self.assertEqual(b"preserved", victim.read_bytes())
            self.assertFalse((destination / "cplt").is_symlink())
            self.assertEqual(b"replacement", (destination / "cplt").read_bytes())

    def test_unsupported_architecture_does_not_open_network(self):
        calls = []
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ReleaseInstallError):
            install_cplt_release(
                "mips",
                Path(directory),
                version="0.3.0",
                checksums={},
                opener=lambda *_args, **_kwargs: calls.append(True),
            )
        self.assertEqual([], calls)


if __name__ == "__main__":
    unittest.main()
