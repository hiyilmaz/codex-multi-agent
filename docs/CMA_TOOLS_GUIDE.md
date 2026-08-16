# CMA Tools Usage Guide

`bin/cma-tools` is the CMA-owned adapter for the bundled `codex-tools`
package. It always forces MCP `verify-only` mode, so CMA remains responsible
for MCP configuration.

## Requirements

- Python 3.11 or newer for `check` and `dry-run`
- `uv` only for `install`
- A local checkout containing `tools/codex-tool-installer`

Run commands from the repository root:

```bash
bin/cma-tools check
bin/cma-tools dry-run
bin/cma-tools install --yes
```

Use an alternate Codex runtime home when required:

```bash
bin/cma-tools check --codex-home /path/to/.codex
```

## Command Behavior

### `check`

Runs the bundled Python package directly from
`tools/codex-tool-installer/src`. It performs a read-only health check and
does not use an ambient `codex-tools` executable from `PATH`.

### `dry-run`

Runs the same bundled source with `--dry-run`. It reports intended installer
actions without applying them and keeps MCP access in `verify-only` mode.

### `install`

Requires confirmation, or `--yes` in non-interactive use. The adapter runs:

```bash
uv tool install --force --python 3.11 ./tools/codex-tool-installer
```

It then executes the exact `codex-tools` entry point published in UV's tool
bin directory. It does not substitute another executable found in `PATH`.

## Setup Integration

The Codex setup flow is opt-in:

```bash
bin/codex-setup --variant codex --tools-mode check
bin/codex-setup --variant codex --tools-mode install
```

The default is `--tools-mode skip`. Tool modes are rejected for non-Codex
variants.

## Standalone Package Use

Standalone use is independent of the CMA adapter and defaults to MCP `manage`
mode:

```bash
uv tool install ./tools/codex-tool-installer
codex-tools --version
codex-tools --mcp-mode manage check
```

Use standalone `manage` mode only when the package, rather than CMA, should
own missing or installer-marker-owned MCP tables.

## Troubleshooting

- `Python 3.11 or newer is required`: install a supported Python runtime and
  retry. On Ubuntu 24.04, the system `python3` is suitable.
- `uv is required`: install UV separately, then rerun `install --yes`.
- `bundled codex-tools package is unavailable`: run the adapter from a complete
  CMA checkout; `check` and `dry-run` intentionally do not fall back to an old
  global installation.
- An old global `codex-tools` rejects `--mcp-mode`: use `bin/cma-tools check`
  for CMA-owned verification, or reinstall the standalone package with the UV
  command above.
