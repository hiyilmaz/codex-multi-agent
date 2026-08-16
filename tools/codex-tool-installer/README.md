# Codex Tool Installer & Verifier

A self-contained Python 3.11+ CLI that discovers, installs, repairs, and
verifies 11 Codex development tools. It has no runtime dependency on CMA,
ToolSmith, or benchmark artifacts. It preserves healthy tools and unrelated
Codex configuration, and defaults to repair rather than upgrade.

## Installation

From a CMA checkout:

```console
uv tool install ./tools/codex-tool-installer
codex-tools --version
```

The installed command is independent of the checkout after installation.
Copying this directory to another machine and installing that local path works
the same way.

Remove only the installer package with:

```console
uv tool uninstall codex-tool-installer
```

Third-party tools installed by `codex-tools` remain owned by their package
managers and must be removed explicitly with those managers.

## Commands

```console
PYTHONPATH=src python3 -m codex_tool_installer
PYTHONPATH=src python3 -m codex_tool_installer install github context7 serena
PYTHONPATH=src python3 -m codex_tool_installer check
PYTHONPATH=src python3 -m codex_tool_installer repair
PYTHONPATH=src python3 -m codex_tool_installer --dry-run --json
PYTHONPATH=src python3 -m codex_tool_installer --update
PYTHONPATH=src python3 -m codex_tool_installer --non-interactive
PYTHONPATH=src python3 -m codex_tool_installer --mcp-mode verify-only check
PYTHONPATH=src python3 -m codex_tool_installer --codex-home /path/to/.codex check
```

The default interactive flow prints discovery results with all tools selected,
then offers Continue, Customize, or Cancel. `check` and `--dry-run` never write,
install, prompt for credentials, or touch secure storage. In non-interactive
mode, a missing credential remains `AUTH_REQUIRED`.

`--mcp-mode manage` is the standalone default. It may add missing MCP tables
or update only tables marked `# Managed by codex-tool-installer`; a colliding
user-owned table fails closed. `--mcp-mode verify-only` never configures MCP,
prompts for MCP credentials, or writes credential storage. CMA always uses
`verify-only`, because CMA owns its MCP configuration.

## Safety model

- Existing executables are functionally checked before any install is planned.
- Only macOS arm64/x86_64 and Ubuntu 22.04/24.04 are accepted.
- Commands are argument vectors executed without a shell.
- Package elevation is scoped to the Ubuntu package command.
- Config input and generated candidates are TOML-parsed.
- Only installer-marked MCP tables may be repaired; user-owned collisions fail.
- Changed config is backed up, atomically replaced, validated through Codex, and
  rolled back on failure. No-op merges create no backup.
- Credentials resolve in environment → secure store → masked prompt order.
  macOS Keychain and Ubuntu libsecret adapters pass writes through stdin. A
  protected-file fallback enforces mode `0600`.
- GitHub, Context7, DeepWiki, and Serena validation is read-only. The installer
  never initializes or scans a project.
- Direct `cplt` downloads use a pinned release tag and SHA-256 checksum.

The JSON output schema has top-level `platform`, `codex`, `tools`,
`selected_count`, `credentials`, `issues`, and `planned_actions` fields. Secret
values are never part of this schema.

## Tests

All external behavior is faked and all filesystem behavior uses temporary
directories:

```console
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
PYTHONPATH=src python3 -m coverage run --branch -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src python3 -m coverage report --fail-under=80
```

Real package installation, real credentials, host keychains, global Codex
configuration, repository scans, commits, and pushes are intentionally absent
from the test suite.
