# Codex Template V2 — Usage Guide

**Version:** 2.5
**Updated:** 2026-05-22

---

## Requirements

Before using this template, prepare the reusable Codex surface once:

| Component | Location | Required |
|---|---|---|
| Global Codex instructions | `~/.codex/AGENTS.md` | Yes |
| Global Codex config | `~/.codex/config.toml` | Optional |
| User rules | `~/.codex/rules/` | Optional |
| User skills | `~/.codex/skills/` | Optional |
| User agents | `~/.codex/agents/` | Optional |
| User registry | `~/.codex/registry/` | Yes |

---

## Global Codex Surface

The active runtime surface is:

- `~/.codex/AGENTS.md`
- `~/.codex/config.toml`
- `~/.codex/rules/`
- `~/.codex/skills/`
- `~/.codex/agents/`
- `~/.codex/registry/`

Reusable bodies live under `~/.codex`; project `AGENTS.md` files only declare
project-specific deltas.

Install the portable user-global template:

```bash
bin/codex-user-install
```

The installer uses `variants/config.toml` for the default variant and can
install a specific runtime variant:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant dolphin
```

Template paths are rewritten during installation so installed configs and
registry docs point at the selected `--runtime-home`.

Default runtime homes:

- `codex`: `$HOME/.codex`
- `dolphin`: `$HOME/.llm-runtimes/dolphin`

For Dolphin, the launcher is installed inside the runtime home:

```text
<runtime-home>/bin/llm-dolphin
```

For guided installation, use the interactive setup:

```bash
bin/codex-setup
```

The setup wizard asks for:

- runtime home path, defaulting to the selected variant default
- whether to install the portable user-global template
- which runtime variant to install when no `--variant` option is provided
- whether to overwrite existing template-managed files
- whether to enable YOLO mode
- default status messages for error, permission, completed, and decision states
- whether to initialize a project after the user-global setup

YOLO mode may reduce interruptions for low-risk work, but it never bypasses
approval for destructive operations, dependency changes, API contract changes,
DB schema changes, or auth/security code changes.

Use `--force` only when you intentionally want to overwrite template-managed
files:

```bash
bin/codex-user-install --force
```

---

## New Project

### Step 1 — Run project init

```bash
bin/codex-project-init /new-project
```

The command asks for confirmation before writing. When confirmed, it archives
existing project-local Codex files under:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS/
```

Then it creates:

```text
<project>/AGENTS.md
<project>/.codex/config.toml
<project>/.codex/prompts/fill-project-configuration.md
```

### Step 2 — Run the Project Configuration prompt

After init, run this generated prompt with the AI:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

The prompt instructs the AI to inspect the repository and fill only the
`## Project Configuration` block in `AGENTS.md`. If required values are
ambiguous, it must ask the user before editing instead of writing placeholders.

### Step 3 — Review Project Configuration

Review the generated `## Project Configuration` block:

```text
PROJECT_NAME:        My App
PROJECT_SUMMARY:     Backend API for users, products, and orders.

STACK_BACKEND:       Python / FastAPI / PostgreSQL
STACK_FRONTEND:      Next.js / TypeScript / shadcn/ui

CHANGELOG_PATH:      docs/CHANGELOG.md
EVIDENCE_PATH:       docs/reports/

ACTIVE_RULE_SETS:
  - python: coding-style, security, testing, patterns
  - typescript: coding-style, security, testing, patterns
  - web: patterns, performance, security

ACTIVE_SKILLS:
  - orchestration-gate
  - tdd-workflow

ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer

ORCHESTRATION_MODE: ask-approval

DOMAIN_RULES:
  - Every payment request must use an idempotency key
  - Every public API endpoint must enforce rate limiting
```

`orchestration-gate` and `tdd-workflow` are baseline skills packaged by every
runtime variant. Add task-specific skills such as `openai-docs` only when they
are relevant and available in the active Codex session.

The final block should contain no uncertainty placeholders. Unknown required
values should be resolved by asking the user before editing.

### Step 4 — Declare reusable content, do not inline it

Use `ACTIVE_RULE_SETS`, `ACTIVE_SKILLS`, `ACTIVE_AGENT_ROLES`, and
`ORCHESTRATION_MODE` to declare what this project uses.

Valid orchestration modes:

- `skip`: do not use orchestration by default.
- `ask-approval`: ask before running the mandatory chain for non-trivial work.
- `run-chain`: run the mandatory chain for non-trivial work when explicitly
  authorized by the project or user and active tool policy permits it.

Reusable bodies should live in one of these locations:

```text
~/.codex/rules/
~/.codex/skills/
~/.codex/agents/
~/.codex/registry/
```

Load only the minimum relevant files during the task.

### Step 5 — Refresh the Codex session

Start a new session or refresh the current one so Codex reads the project
`AGENTS.md`.

---

## Existing Project

For a project that already has `AGENTS.md`, prefer the upgrade command:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

Project initialization records template ownership in
`.codex/template-state.json`. Upgrade then:

- preserves project-specific `AGENTS.md` values and list additions
- adds only missing baseline fields
- updates template-managed prompt/config files only when their recorded hash
  proves they are unchanged
- preserves locally modified or legacy files, shows a non-applied comparison,
  and marks them project-owned after approval
- archives every changed file under
  `.codex/archive/upgrade-YYYYMMDD_HHMMSS/`

Dry-run is the default and never writes files. Use `--apply` after reviewing the
plan. `--apply --force` skips only the confirmation prompt; it never overwrites
customized files.

Use reset init only when you intentionally want to archive and recreate the
project Codex structure:

1. Read the existing project instruction files if you need to preserve project
   metadata.
2. Run `bin/codex-project-init /path/to/project`.
3. Confirm the reset when prompted.
4. Run the generated prompt:
   `<project>/.codex/prompts/fill-project-configuration.md`.
5. Review the filled `Project Configuration` block.
6. Do not copy reusable rule, skill, or agent bodies into `AGENTS.md`.
7. Put reusable content under `~/.codex/`.

Archived files are stored under:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS/
```

---

## Reusable Source Priority

When a declared reusable item exists in more than one place:

```text
project declaration > user-global in ~/.codex > unavailable/report
```

If a declared item cannot be found, report it before doing work that depends on
that item.

---

## Summary

```text
Run codex-setup for guided installation
        ↓
or install a runtime with codex-user-install [--variant codex|dolphin]
        ↓
For existing projects, run codex-project-upgrade
        ↓
For new/reset projects, run codex-project-init and confirm reset
        ↓
Run generated Project Configuration prompt
        ↓
Review Project Configuration
        ↓
Declare active rules, skills, and agents
        ↓
Store reusable bodies outside project AGENTS.md
        ↓
Refresh Codex session
```

---

# EOF
