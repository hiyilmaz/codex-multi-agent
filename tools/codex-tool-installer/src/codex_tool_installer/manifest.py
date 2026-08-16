from __future__ import annotations

from .models import ToolDefinition


ALL_PLATFORMS = ("macos", "ubuntu-22.04", "ubuntu-24.04")


def _cli(name, executable, mac, ubuntu, dependencies=()):
    return ToolDefinition(
        name=name,
        kind="cli",
        executable=executable,
        platforms=ALL_PLATFORMS,
        verify=((executable, "--version"),),
        installs={"macos": (mac,), "ubuntu": (ubuntu,)},
        dependencies=dependencies,
    )


TOOL_MANIFEST = {
    "rg": _cli("rg", "rg", ("brew", "install", "ripgrep"), ("sudo", "apt-get", "install", "-y", "ripgrep")),
    "graphify": _cli("graphify", "graphify", ("uv", "tool", "install", "graphifyy==0.9.45"), ("uv", "tool", "install", "graphifyy==0.9.45"), ("uv",)),
    "serena": ToolDefinition(
        "serena", "cli_mcp", "serena", ALL_PLATFORMS, (("serena", "--version"),),
        installs={"macos": (("uv", "tool", "install", "git+https://github.com/oraios/serena@949a27ef1e5fda1a6e7b561e777bcece345c6ffd"),), "ubuntu": (("uv", "tool", "install", "git+https://github.com/oraios/serena@949a27ef1e5fda1a6e7b561e777bcece345c6ffd"),)},
        mcp={"optional": True}, dependencies=("uv", "git"),
    ),
    "ast-grep": _cli("ast-grep", "ast-grep", ("npm", "install", "-g", "@ast-grep/cli@0.45.1"), ("npm", "install", "-g", "@ast-grep/cli@0.45.1"), ("npm",)),
    "opengrep": _cli("opengrep", "opengrep", ("internal-opengrep-release",), ("internal-opengrep-release",)),
    "osv-scanner": _cli("osv-scanner", "osv-scanner", ("go", "install", "github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.5.0"), ("go", "install", "github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.5.0"), ("go",)),
    "betterleaks": _cli("betterleaks", "betterleaks", ("go", "install", "github.com/betterleaks/betterleaks@v1.7.4"), ("go", "install", "github.com/betterleaks/betterleaks@v1.7.4"), ("go",)),
    "cplt": _cli("cplt", "cplt", ("brew", "install", "navikt/tap/cplt"), ("internal-github-release", "navikt/cplt", "cplt")),
    "deepwiki": ToolDefinition(
        "deepwiki", "mcp", None, ALL_PLATFORMS, (("codex", "mcp", "get", "deepwiki"),),
        mcp={"url": "https://mcp.deepwiki.com/mcp", "expected_tools": ("ask_question", "read_wiki_contents", "read_wiki_structure"), "functional_calls": (("read_wiki_structure", {"repoName": "openai/codex"}),)},
    ),
    "github": ToolDefinition(
        "github", "mcp", None, ALL_PLATFORMS, (("codex", "mcp", "get", "github"),),
        mcp={"url": "https://api.githubcopilot.com/mcp/", "bearer_token_env_var": "GITHUB_PAT_TOKEN", "functional_calls": (("search_repositories", {"query": "codex", "perPage": 1}),)},
        credential_env="GITHUB_PAT_TOKEN",
    ),
    "context7": ToolDefinition(
        "context7", "mcp", None, ALL_PLATFORMS, (("codex", "mcp", "get", "context7"),),
        mcp={"url": "https://mcp.context7.com/mcp", "bearer_token_env_var": "CONTEXT7_API_KEY", "functional_calls": (("resolve-library-id", {"libraryName": "python", "query": "pathlib documentation"}), ("query-docs", {"libraryId": "/python/cpython", "query": "pathlib"}))},
        credential_env="CONTEXT7_API_KEY",
    ),
}
