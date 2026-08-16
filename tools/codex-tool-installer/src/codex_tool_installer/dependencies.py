from __future__ import annotations


DEPENDENCY_PLANS = {
    "macos": {
        "uv": (("brew", "install", "uv"),),
        "git": (("brew", "install", "git"),),
        "npm": (("brew", "install", "node"),),
        "pipx": (("brew", "install", "pipx"),),
        "go": (("brew", "install", "go"),),
        "curl": (("brew", "install", "curl"),),
    },
    "ubuntu": {
        "uv": (("python3", "-m", "pip", "install", "--user", "uv"),),
        "git": (("sudo", "apt-get", "install", "-y", "git"),),
        "npm": (("sudo", "apt-get", "install", "-y", "npm"),),
        "pipx": (("sudo", "apt-get", "install", "-y", "pipx"),),
        "go": (("sudo", "apt-get", "install", "-y", "golang-go"),),
        "curl": (("sudo", "apt-get", "install", "-y", "curl"),),
    },
}


def dependency_plan(name: str, platform_key: str):
    family = "macos" if platform_key == "macos" else "ubuntu"
    return DEPENDENCY_PLANS.get(family, {}).get(name, ())
