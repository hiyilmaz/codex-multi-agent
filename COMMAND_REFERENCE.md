# Command Reference

Run the commands below from the repository root:

```bash
cd /path/to/Codex-Multi-Agent
```

Use quoted absolute paths when a runtime or project path contains spaces.

## Help And Discovery

```bash
bin/codex-setup --help
bin/codex-setup --list-variants
bin/codex-user-install --help
bin/codex-user-install --list-variants
bin/codex-project-init --help
bin/codex-project-upgrade --help
bin/cma-tools --help
```

Available runtime variants:

| Variant | Default runtime home | Launcher |
|---|---|---|
| `codex` | `~/.codex` | Use the normal Codex command. |
| `claude` | `~/.claude` | `~/.claude/bin/llm-claude` |
| `opencode` | `~/.config/opencode` | Native `opencode` command. |

Each variant packages the same Evidence-First Objectivity behavior for claims,
recommendations, material choices, and disputed topics. It favors verifiable,
independent evidence; includes counterevidence, conflict, risk, and uncertainty;
and does not impose research on routine coding, editing, translation, or
operational tasks.

## Guided Setup

Start the interactive runtime and optional project setup:

```bash
bin/codex-setup
```

Mutating setup requires Node.js 22 or newer and `npx`; help and variant
discovery bypass this preflight. Before completion, the wizard offers the
default-yes official `npx ctx7 setup` flow. Context7 owns authentication and
updates the detected Claude Code, OpenCode, and Codex global MCP, rule, and
skill locations under the process `HOME`. `--runtime-home` does not redirect
those Context7 targets. CMA does not put an API key in command arguments, and a
failed Context7 process keeps its exit status and suppresses completion.
Because Context7 runs last, that failure does not roll back earlier CMA writes.

Without `--variant`, this asks whether to install all active catalog variants.
Yes installs all without individual prompts; no asks once per variant. A custom
runtime home requires an explicit single `--variant`.

Select a variant explicitly:

```bash
bin/codex-setup --variant codex
bin/codex-setup --variant claude
bin/codex-setup --variant opencode
```

Use a custom runtime home:

```bash
bin/codex-setup --variant codex --runtime-home "/absolute/runtime/path"
```

`--codex-home` is a compatibility alias for `--runtime-home`.

For the native Codex target only (`$HOME/.codex`), setup delegates to
`bin/codex-native-activate` after template installation. It installs the ten
protected core tools additively, makes Context7 required/lazy, keeps cplt
explicit-only, and leaves xcodebuildmcp disabled. Custom runtime homes and
other variants remain isolated; restart Codex after installation.

Optionally check or install development tools during native Codex setup:

```bash
bin/codex-setup --variant codex --tools-mode check
bin/codex-setup --variant codex --tools-mode install
```

The default is `--tools-mode skip`. Tool mode is rejected for custom runtime
homes and non-Codex variants.

## Independent Development Tools

CMA-owned use keeps MCP configuration read-only:

```bash
bin/cma-tools check
bin/cma-tools dry-run
bin/cma-tools install
```

The install action requires `uv`, installs the bundled Python 3.11 package,
then installs/verifies CLI tools while keeping MCP in `verify-only` mode.
Read-only modes never bootstrap missing dependencies.

Standalone use is independent of CMA after installation:

```bash
uv tool install ./tools/codex-tool-installer
codex-tools --version
codex-tools --mcp-mode manage check
```

Standalone `manage` mode writes only missing or installer-marker-owned MCP
tables; user-owned collisions fail closed.

Remove the independent installer command without removing third-party tools:

```bash
uv tool uninstall codex-tool-installer
```

## Runtime Installation

Direct mutating `codex-user-install` calls also require Node.js 22 or newer and
`npx`. Its `--help` and `--list-variants` commands remain read-only and do not
require either executable. The standalone installer does not itself run
`npx ctx7 setup`; that interactive global step belongs to `codex-setup`.

Install the default variant selected in `variants/config.toml`:

```bash
bin/codex-user-install
```

Install a specific variant:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant claude
bin/codex-user-install --variant opencode
```

Install to a custom runtime home:

```bash
bin/codex-user-install \
  --variant codex \
  --runtime-home "/absolute/runtime/path"
```

Inspect the native activation command directly:

```bash
bin/codex-native-activate --help
```

Refresh template-managed runtime files intentionally:

```bash
bin/codex-user-install --variant codex --force
```

`--force` overwrites existing non-policy files managed by the runtime template.
Existing global instruction files remain unchanged and receive a private
snapshot plus `prompts/merge-existing-instructions.md`. Native Claude
activation rejects `--force` and uses a preservation-first overlay instead.

For guided Claude setup, answer `no` when asked whether existing
template-managed files should be overwritten. Selecting `yes` passes `--force`,
which native Claude activation intentionally rejects.

Launch the default Claude installation:

```bash
~/.claude/bin/llm-claude
```

OpenCode activation uses `~/.config/opencode/skills`, preserves unrelated
configuration and identity state, and refuses symlinked or conflicting managed
targets. Verify without a model call using `opencode mcp list` and
`opencode debug config`.

The Claude launcher sets its native runtime as `CLAUDE_CONFIG_DIR` and then
executes the native `claude` binary. Installation preserves existing
`~/.claude/CLAUDE.md` and `settings.json`; it does not install the Agent SDK or
perform login. Explicit alternate `--runtime-home` targets remain isolated.

Native activation writes the CMA candidate to
`~/.claude/registry/CMA_GLOBAL.md` without importing it automatically. When
`~/.claude/CLAUDE.md` exists, its private snapshot and merge prompt are stored
under:

```text
~/.claude/backups/instruction-merge/
~/.claude/prompts/merge-existing-instructions.md
```

The command fails closed before overwriting a differing CMA-managed file or
following an unsafe symlink. A copy or backup failure triggers rollback so a
partial native overlay is not reported as active. It does not remove or modify
the legacy isolated Claude runtime.

Restart the active Codex, Claude, or OpenCode session after changing runtime files so the
new instructions, skills, and registry entries are loaded.

## Initialize, Add A Variant, Or Reset

Interactively initialize a project with all or individually selected variants:

```bash
bin/codex-project-init "/absolute/path/to/project"
```

Initialize or add a specific runtime variant:

```bash
bin/codex-project-init \
  --variant codex \
  "/absolute/path/to/project"
```

For existing projects, init is additive: it preserves `AGENTS.md`, shared
prompts, customized files, and other variant surfaces. Multiple runtime
variants can coexist in one project. Codex uses
`.codex/config.toml`; Claude adds its bridge/settings; OpenCode adds
`.opencode/opencode.json` and preserves sibling `.opencode` content.

Only an explicit reset recreates the shared structure:

```bash
bin/codex-project-init --reset --variant codex "/absolute/path/to/project"
```

Reset asks for confirmation and writes conflicting files to a private recovery
archive. Normal additive init never resets an existing project.

When existing instructions are present, additive init creates a private,
content-addressed snapshot under `.codex/archive/instruction-merge/` and a
path-only `.codex/prompts/merge-existing-instructions.md`. Claude receives a
separate Claude merge prompt when applicable. The prompts return proposed diffs
for user approval and do not write files.
If the requested prompt filename already has different content, it is preserved
and the generated prompt uses a content-hash suffix reported by the command.

After initialization, use this generated prompt in the project Codex session:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

## Existing Project Upgrade

Preview an upgrade without writing files:

```bash
bin/codex-project-upgrade --dry-run "/absolute/path/to/project"
```

`--dry-run` is the default, so this is equivalent:

```bash
bin/codex-project-upgrade "/absolute/path/to/project"
```

Apply the reviewed upgrade plan:

```bash
bin/codex-project-upgrade --apply "/absolute/path/to/project"
```

Apply without the confirmation prompt:

```bash
bin/codex-project-upgrade \
  --apply \
  --force \
  "/absolute/path/to/project"
```

For project upgrades, `--force` skips confirmation only. Customized project
files are still preserved. Applied changes are archived under
`<project>/.codex/archive/upgrade-YYYYMMDD_HHMMSS_microseconds/`.

Record a different runtime variant while upgrading:

```bash
bin/codex-project-upgrade \
  --apply \
  --variant opencode \
  "/absolute/path/to/project"
```

## Local Codex Documentation Index

Refresh the compact local index from official OpenAI Codex documentation:

```bash
scripts/update-openai-codex-docs
```

This command requires network access and writes the refreshed index under
`docs/openai-codex/`.

## Repository Verification

Validate shell scripts:

```bash
bash -n \
  bin/codex-setup \
  bin/codex-user-install \
  bin/codex-project-init
```

Run the Python tests without creating bytecode files:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Check patch whitespace and inspect pending changes:

```bash
git diff --check
git status --short
git diff --stat
```

## Main Plan Execution

Approve a disclosed main plan once; CMA then executes its planned phases
continuously. Auxiliary discoveries and recommendations are reported without
expanding the plan. The approval covers disclosed non-destructive Low/Medium
work and planned orchestration. Destructive and High/Critical operations still
require separate approval.
Work discovered outside the approved plan stays on an auxiliary list and is
not executed unless it is required to continue. A required deviation is
reported and approved before the plan changes. Recommended work is reported
separately and is never added to the main plan automatically.

## Recommended Workflows

Fresh guided setup:

```bash
bin/codex-setup
```

Install Codex runtime and initialize a new project:

```bash
bin/codex-user-install --variant codex
bin/codex-project-init --variant codex "/absolute/path/to/project"
```

Safely update an existing initialized project:

```bash
bin/codex-project-upgrade --dry-run "/absolute/path/to/project"
bin/codex-project-upgrade --apply "/absolute/path/to/project"
```
