# Codex Template V2

**Version:** 2.5
**Updated:** 2026-05-22

---

## Purpose

This is a Codex-native project instruction template for new or existing
repositories.

It is self-contained and does not depend on another agent runtime.

---

## Files

| File | Purpose |
|---|---|
| `GLOBAL_AGENTS_TEMPLATE.md` | Copy to `~/.codex/AGENTS.md` |
| `PROJECT_AGENTS_TEMPLATE.md` | Copy to a project as `AGENTS.md` |
| `USAGE_GUIDE.md` | How to apply the template to new or existing projects |
| `COMMAND_REFERENCE.md` | Consolidated runtime, project, and verification commands |
| `CODEX_CONFIG_EXAMPLE.toml` | Optional project `.codex/config.toml` example |
| `PROJECT_CONFIG_PROMPT.md` | Prompt copied into projects after init |
| `REGISTRY_MANAGEMENT.md` | User-global skill/agent registry model |
| `variants/` | Installable runtime variants and default variant config |
| `TURKCE_KURULUM_REHBERI.md` | Turkish quick setup guide |
| `docs/openai-codex/` | Local updateable index of official OpenAI Codex docs |
| `bin/` | User-global and project init helper scripts |

---

## Runtime Model

The active reusable runtime surface lives under `~/.codex/`. Project
`AGENTS.md` files declare what is active but do not store reusable bodies.

Reusable content locations:

- User-global rules: `~/.codex/rules`
- User-global skills: `~/.codex/skills`
- User-global agents: `~/.codex/agents`
- User-global registry: `~/.codex/registry`

Reusable bodies should not be copied into project `AGENTS.md`.

Project orchestration behavior is declared with:

```text
ORCHESTRATION_MODE: skip | ask-approval | run-chain
```

The default project template uses `ask-approval`. The `orchestration-gate`
skill decides whether a task should skip orchestration, ask for approval, or
run the mandatory chain. It must not bypass active tool or approval policy.

Every runtime variant packages `tdd-workflow`. The `tdd-guide` agent defines
the focused test strategy, and the skill enforces the test-first
RED-GREEN-refactor workflow during implementation.

Every runtime variant also packages `hypothesis-workflow`. It remains inactive
for routine first-pass work and escalates only failed, unclear, competing,
regressing, measurement-dependent, or explicitly requested improvements into a
traceable experiment.

The mandatory chain uses bounded handoffs: each agent consumes prior evidence,
avoids repeated discovery, returns a concise result, and stops. Codex chain
agents default to `medium` reasoning. Passing tests alone do not prove
completion; review also checks acceptance criteria, observable behavior, and
test integrity.

### Task Transition Gate

After completing a distinct task, CMA gives a one- or two-sentence summary,
states and briefly explains the next distinct task (or says that none is
known), then requests explicit approval and waits. The gate does not interrupt
steps within the same explicitly approved bounded task.

Installable runtime variants live under `variants/`:

- `variants/codex/home/` — Default Codex runtime template
- `variants/dolphin/home/` — DolphinVersion runtime template
- `variants/claude/home/` — Claude Agent native CLI runtime template
- `variants/opencode/home/` — isolated OpenCode runtime template
- `variants/config.toml` — default variant selection

---

## Quick Start

Install or refresh the default Codex runtime:

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

The installer rewrites installed template paths to the selected target
`--runtime-home`.

Default targets:

- `codex` -> `$HOME/.codex`
- `dolphin` -> `$HOME/.llm-runtimes/dolphin`
- `claude` -> `$HOME/.claude`
- `opencode` -> `$HOME/.llm-runtimes/opencode`

Variant launchers are installed as:

```text
<runtime-home>/bin/llm-dolphin
<runtime-home>/bin/llm-claude
<runtime-home>/bin/llm-opencode
```

The OpenCode launcher sets `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, and all
XDG config/data/cache/state roots inside `~/.llm-runtimes/opencode`, then
delegates to the native `opencode` binary. Symlinked state roots fail closed.
This prevents native global settings and identity state from merging into CMA.
It never writes `~/.config/opencode`, selects a model or provider, installs
plugins, or performs authentication. Validate with `llm-opencode debug config`
and `llm-opencode debug paths`.

The default Claude installation uses its native user-global directory. It
preserves existing `CLAUDE.md` content through a backed-up import overlay,
leaves existing `settings.json` unchanged, and rejects `--force`. Explicit
alternate `--runtime-home` targets remain available for isolated testing.
`llm-claude` sets `CLAUDE_CONFIG_DIR` to its installed runtime home and delegates
to an already installed native `claude` command; it does not install the Claude
Agent SDK or authenticate.

Native activation adds exactly one functional `@registry/CMA_GLOBAL.md` import
to `~/.claude/CLAUDE.md`. Before changing an existing instruction file, it saves
the original and its SHA-256 checksum under
`~/.claude/backups/cma-activation-<UTC timestamp>-<suffix>/`. Existing
CMA-managed files must match the packaged source; conflicts, unsafe symlinks,
incomplete sources, or copy failures stop the activation without leaving a
partial overlay. Any legacy isolated Claude runtime is not removed or modified.

Run the interactive setup:

```bash
bin/codex-setup
```

Initialize a project or add a runtime variant:

```bash
bin/codex-project-init /path/to/project
```

On a new project, init creates the shared project instructions and the selected
variant surface. On an existing project, init is additive: it preserves
`AGENTS.md`, shared prompts, customized files, and every existing variant while
adding only the requested surface. Multiple runtime variants can coexist and
are recorded in `.codex/template-state.json`.

Codex and Dolphin share `.codex/config.toml`; Claude adds `CLAUDE.md` and
`.claude/settings.json`; OpenCode adds `.opencode/opencode.json`. Use `--reset`
only for an intentional destructive reinitialization; it displays and privately
archives conflicting files before recreating the project structure.

After init, run the generated prompt:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

That prompt tells the AI to inspect the project and fill only the
`AGENTS.md` `Project Configuration` block. If required values are ambiguous, it
must ask the user before editing instead of writing placeholders.

Upgrade an already initialized project without resetting its `AGENTS.md`:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

Dry-run is the default. Upgrade preserves project-specific values and additions,
merges only missing baseline fields into `AGENTS.md`, updates unchanged
template-managed files, and leaves locally modified files untouched. Every
applied change is archived under
`.codex/archive/upgrade-YYYYMMDD_HHMMSS_microseconds/`.

## Local Codex Docs

Refresh the local OpenAI Codex documentation index:

```bash
scripts/update-openai-codex-docs
```

The index is stored under `docs/openai-codex/`.

---

# EOF
