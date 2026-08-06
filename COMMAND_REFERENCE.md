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
| `claude` | `~/.llm-runtimes/claude` | `~/.llm-runtimes/claude/bin/llm-claude` |

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
bin/codex-user-install --variant claude --force
```

`--force` overwrites existing files managed by the runtime template. Review or
back up locally customized runtime files before using it.

Launch the default Dolphin installation:

```bash
~/.llm-runtimes/dolphin/bin/llm-dolphin
~/.llm-runtimes/claude/bin/llm-claude
```

The Claude launcher sets the isolated runtime as `CLAUDE_CONFIG_DIR` and then
executes the native `claude` binary. It does not install the Agent SDK, perform
login, or modify active `~/.claude` files.

Restart the active Codex or Dolphin session after changing runtime files so the
new instructions, skills, and registry entries are loaded.

## New Or Reset Project

Initialize a project with the default variant:

```bash
bin/codex-project-init "/absolute/path/to/project"
```

Record a specific runtime variant:

```bash
bin/codex-project-init \
  --variant codex \
  "/absolute/path/to/project"
```

For Claude projects, replace `codex` with `claude`. The confirmed init adds a
minimal `CLAUDE.md` bridge (`@AGENTS.md`) and `.claude/settings.json`; unrelated
`.claude` files are not reset.

Project initialization asks for confirmation, archives conflicting local Codex
files, and recreates the standard project structure. Use project upgrade for an
already configured project unless an intentional reset is required.

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
`<project>/.codex/archive/upgrade-YYYYMMDD_HHMMSS/`.

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
