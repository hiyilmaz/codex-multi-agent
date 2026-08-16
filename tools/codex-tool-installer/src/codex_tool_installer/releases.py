from __future__ import annotations

import os
import hashlib
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path


class ReleaseInstallError(RuntimeError):
    pass


CURRENT_CPLT_VERSION = "2026.08.12-081645-3ee02c8"
CURRENT_CPLT_CHECKSUMS = {
    "x86_64": "4cdad6d9608913dda024f679dae7d04d27bd75577b107307cfa2f37ffbefa523",
    "aarch64": "87b5459e7746d7f0231d30e2d30e18bcbabae6e24d9517d3897c8277eb6a4878",
}
CURRENT_OPENGREP_VERSION = "v1.27.1"
CURRENT_OPENGREP_ASSETS = {
    ("macos", "aarch64"): ("opengrep_osx_arm64", "e0cf2287c00f9e559b5ad28f5731924fc5ec7778f35363d2e15f94e15880a6de"),
    ("macos", "x86_64"): ("opengrep_osx_x86", "0e96abde66eda9dcfe8b81b2c616d71deadae0ec62fe026b9e199498ce1aac10"),
    ("ubuntu", "aarch64"): ("opengrep_manylinux_aarch64", "96ee2caddd5f17821ae6952774a91c8781778bfa9af1ace83645444c0edc6c97"),
    ("ubuntu", "x86_64"): ("opengrep_manylinux_x86", "58053da76672bbeb5b0a5441021c58338707052e10f81d777140ca879bd491ce"),
}


def _normalized_architecture(machine: str) -> str | None:
    return {"x86_64": "x86_64", "amd64": "x86_64", "aarch64": "aarch64", "arm64": "aarch64"}.get(machine.lower())


def _publish_verified_binary(source: Path, destination: Path, target_name: str) -> None:
    if destination.is_symlink():
        raise ReleaseInstallError(f"Refusing symbolic link destination: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink() or not destination.is_dir():
        raise ReleaseInstallError(f"Unsafe release destination: {destination}")
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{target_name}.", suffix=".tmp", dir=destination)
    temp = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as outgoing, source.open("rb") as incoming:
            shutil.copyfileobj(incoming, outgoing)
            outgoing.flush()
            os.fsync(outgoing.fileno())
        temp.chmod(0o755)
        os.replace(temp, destination / target_name)
        temp = None
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def install_opengrep_release(
    platform_key: str,
    machine: str,
    destination: Path,
    *,
    opener=urllib.request.urlopen,
) -> None:
    platform = "macos" if platform_key == "macos" else "ubuntu" if platform_key.startswith("ubuntu-") else None
    architecture = _normalized_architecture(machine)
    locked = CURRENT_OPENGREP_ASSETS.get((platform, architecture)) if platform and architecture else None
    if not locked:
        raise ReleaseInstallError(f"Unsupported Opengrep platform: {platform_key}/{machine}")
    asset, expected = locked
    url = f"https://github.com/opengrep/opengrep/releases/download/{CURRENT_OPENGREP_VERSION}/{asset}"
    with tempfile.TemporaryDirectory(prefix="codex-tools-opengrep-") as directory:
        binary = Path(directory) / asset
        try:
            with opener(url, timeout=60) as response, binary.open("wb") as output:
                if getattr(response, "status", 200) != 200:
                    raise ReleaseInstallError("Official Opengrep release download failed")
                shutil.copyfileobj(response, output)
            if hashlib.sha256(binary.read_bytes()).hexdigest() != expected:
                raise ReleaseInstallError("Opengrep release checksum verification failed")
            _publish_verified_binary(binary, destination, "opengrep")
        except ReleaseInstallError:
            raise
        except OSError as exc:
            raise ReleaseInstallError(f"Official Opengrep release installation failed: {exc}") from exc


def install_cplt_release(
    machine: str,
    destination: Path,
    *,
    version: str = CURRENT_CPLT_VERSION,
    checksums: dict[str, str] | None = None,
    opener=urllib.request.urlopen,
) -> None:
    arch = _normalized_architecture(machine)
    if not arch:
        raise ReleaseInstallError(f"Unsupported cplt architecture: {machine}")
    checksums = CURRENT_CPLT_CHECKSUMS if checksums is None else checksums
    expected = checksums.get(arch)
    if not expected or len(expected) != 64:
        raise ReleaseInstallError(f"Missing pinned cplt checksum for architecture: {arch}")
    if not version or "/" in version:
        raise ReleaseInstallError("Invalid pinned cplt version")
    url = f"https://github.com/navikt/cplt/releases/download/{version}/cplt-{arch}-unknown-linux-gnu.tar.gz"
    with tempfile.TemporaryDirectory(prefix="codex-tools-cplt-") as directory:
        archive = Path(directory) / "release.tar.gz"
        try:
            with opener(url, timeout=60) as response, archive.open("wb") as output:
                if getattr(response, "status", 200) != 200:
                    raise ReleaseInstallError("Official release download failed")
                shutil.copyfileobj(response, output)
            actual = hashlib.sha256(archive.read_bytes()).hexdigest()
            if actual != expected:
                raise ReleaseInstallError("cplt release checksum verification failed")
            with tarfile.open(archive, "r:gz") as bundle:
                members = [member for member in bundle.getmembers() if member.isfile() and Path(member.name).name == "cplt"]
                if len(members) != 1 or members[0].name != Path(members[0].name).name:
                    raise ReleaseInstallError("Release archive has an unsafe layout")
                source = Path(directory) / "cplt"
                with bundle.extractfile(members[0]) as incoming, source.open("wb") as outgoing:
                    shutil.copyfileobj(incoming, outgoing)
            source.chmod(0o755)
            _publish_verified_binary(source, destination, "cplt")
        except ReleaseInstallError:
            raise
        except (OSError, tarfile.TarError) as exc:
            raise ReleaseInstallError(f"Official cplt release installation failed: {exc}") from exc
