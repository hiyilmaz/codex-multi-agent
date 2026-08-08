# Command Reference

Run the commands below from the repository root:

```bash
cd /path/to/Codex-Multi-Agent
```

Use quoted absolute paths when a runtime or project path contains spaces.

## Help And Discovery

```bash
bin/codex-setup --help
bin/codex-user-install --help
bin/codex-user-install --list-variants
bin/codex-project-init --help
bin/codex-project-upgrade --help
```

Available runtime variants:

| Variant | Default runtime home | Launcher |
|---|---|---|
| `codex` | `~/.codex` | Use the normal Codex command. |
| `dolphin` | `~/.llm-runtimes/dolphin` | `~/.llm-runtimes/dolphin/bin/llm-dolphin` |
| `claude` | `~/.claude` | `~/.claude/bin/llm-claude` |
| `opencode` | `~/.llm-runtimes/opencode` | `~/.llm-runtimes/opencode/bin/llm-opencode` |

## Guided Setup

Start the interactive runtime and optional project setup:

```bash
bin/codex-setup
```

Select a variant explicitly:

```bash
bin/codex-setup --variant codex
bin/codex-setup --variant dolphin
bin/codex-setup --variant claude
bin/codex-setup --variant opencode
```

Use a custom runtime home:

```bash
bin/codex-setup --variant codex --runtime-home "/absolute/runtime/path"
```

`--codex-home` is a compatibility alias for `--runtime-home`.

## Runtime Installation

Install the default variant selected in `variants/config.toml`:

```bash
bin/codex-user-install
```

Install a specific variant:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant dolphin
bin/codex-user-install --variant claude
bin/codex-user-install --variant opencode
```

Install to a custom runtime home:

```bash
bin/codex-user-install \
  --variant codex \
  --runtime-home "/absolute/runtime/path"
```

Refresh template-managed runtime files intentionally:

```bash
bin/codex-user-install --variant codex --force
bin/codex-user-install --variant dolphin --force
```

`--force` overwrites existing files managed by the runtime template. Review or
back up locally customized runtime files before using it. Native Claude
activation rejects `--force` and uses a preservation-first overlay instead.

For guided Claude setup, answer `no` when asked whether existing
template-managed files should be overwritten. Selecting `yes` passes `--force`,
which native Claude activation intentionally rejects.

Launch the default Dolphin or Claude installation:

```bash
~/.llm-runtimes/dolphin/bin/llm-dolphin
~/.claude/bin/llm-claude
~/.llm-runtimes/opencode/bin/llm-opencode
```

`llm-opencode` sets `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, and all four XDG
config/data/cache/state homes inside `~/.llm-runtimes/opencode`, rejecting
symlinked state roots before delegating to native `opencode`. This excludes
native configuration and identity state and leaves `~/.config/opencode`
untouched. Verify without a model call using `llm-opencode debug config` and
`llm-opencode debug paths`.

The Claude launcher sets its native runtime as `CLAUDE_CONFIG_DIR` and then
executes the native `claude` binary. Installation preserves existing
`~/.claude/CLAUDE.md` and `settings.json`; it does not install the Agent SDK or
perform login. Explicit alternate `--runtime-home` targets remain isolated.

Native activation writes CMA policy to `~/.claude/registry/CMA_GLOBAL.md` and
adds exactly one functional `@registry/CMA_GLOBAL.md` import to the existing
`~/.claude/CLAUDE.md`. When that file already exists, its recovery copy and
SHA-256 checksum are stored under:

```text
~/.claude/backups/cma-activation-<UTC timestamp>-<suffix>/
```

The command fails closed before overwriting a differing CMA-managed file or
following an unsafe symlink. A copy or backup failure triggers rollback so a
partial native overlay is not reported as active. It does not remove or modify
the legacy isolated Claude runtime.

Restart the active Codex, Dolphin, or Claude session after changing runtime files so the
new instructions, skills, and registry entries are loaded.

## Initialize, Add A Variant, Or Reset

Initialize a project with the default variant:

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
variants can coexist in one project. Codex and Dolphin share
`.codex/config.toml`; Claude adds its bridge/settings; OpenCode adds
`.opencode/opencode.json` and preserves sibling `.opencode` content.

Only an explicit reset recreates the shared structure:

```bash
bin/codex-project-init --reset --variant codex "/absolute/path/to/project"
```

Reset asks for confirmation and writes conflicting files to a private recovery
archive. Normal additive init never resets an existing project.

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
  --variant dolphin \
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

## Task Transition Gate

After completing a distinct task, CMA gives a one- or two-sentence summary,
states and briefly explains the next distinct task (or says that none is
known), then requests explicit approval and waits. The gate does not interrupt
steps within the same explicitly approved bounded task.

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
