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

Installable runtime variants live under `variants/`:

- `variants/codex/home/` — Default Codex runtime template
- `variants/dolphin/home/` — DolphinVersion runtime template
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
```

The installer rewrites installed template paths to the selected target
`--runtime-home`.

Default targets:

- `codex` -> `$HOME/.codex`
- `dolphin` -> `$HOME/.llm-runtimes/dolphin`

The Dolphin launcher is installed as:

```text
<runtime-home>/bin/llm-dolphin
```

Run the interactive setup:

```bash
bin/codex-setup
```

Initialize a project:

```bash
bin/codex-project-init /path/to/project
```

The init command asks for confirmation, archives existing project-local Codex
files, resets the project Codex structure, and creates a fresh project
`AGENTS.md`. It also records the selected runtime variant, template version,
and managed-file hashes in `.codex/template-state.json`.

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
applied change is archived under `.codex/archive/upgrade-YYYYMMDD_HHMMSS/`.

## Local Codex Docs

Refresh the local OpenAI Codex documentation index:

```bash
scripts/update-openai-codex-docs
```

The index is stored under `docs/openai-codex/`.

---

# EOF
