# Codex Template V2 — Usage Guide

**Version:** 2.6
**Updated:** 2026-08-15

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
bin/codex-user-install --variant claude
bin/codex-user-install --variant opencode
```

Template paths are rewritten during installation so installed configs and
registry docs point at the selected `--runtime-home`.

Native Codex installation to exactly `$HOME/.codex` also runs
`bin/codex-native-activate` after the template succeeds. This additively makes
the ten protected tools available; Context7 is required but lazy, cplt remains
explicit-only, and xcodebuildmcp stays disabled. Alternate runtime homes and
non-Codex variants do not receive this activation. Restart Codex afterwards.

Default runtime homes:

- `codex`: `$HOME/.codex`
- `claude`: `$HOME/.claude`
- `opencode`: `$HOME/.config/opencode`

For Claude, the launcher is installed inside the runtime home:

```text
<runtime-home>/bin/llm-claude
<runtime-home>/bin/llm-opencode
```

OpenCode uses its official user-global skill location,
`~/.config/opencode/skills`. Native activation installs the approved skills
additively, preserves unrelated configuration and identity state, and refuses
symlinked or conflicting managed paths. It does not choose a provider/model,
install a plugin, authenticate, or write credentials. Use `opencode mcp list`
and `opencode debug config` for validation.

The default Claude path is the native user-global surface. Activation preserves
existing instructions with a backed-up CMA import overlay, does not rewrite an
existing `settings.json`, and rejects `--force`. The launcher sets
`CLAUDE_CONFIG_DIR` to its installed home and requires an existing native
`claude` executable. It does not install the Claude Agent SDK or authenticate.

The native overlay installs policy at `~/.claude/registry/CMA_GLOBAL.md` and
adds exactly one functional `@registry/CMA_GLOBAL.md` import to
`~/.claude/CLAUDE.md`. If the instruction file already exists, its recovery copy
and SHA-256 checksum are stored under
`~/.claude/backups/cma-activation-<UTC timestamp>-<suffix>/`. Differing
CMA-managed files, unsafe symlinks, incomplete sources, and backup or copy
failures stop activation; transactional rollback prevents a partial overlay.
The legacy isolated Claude runtime remains untouched.

For guided installation, use the interactive setup:

```bash
bin/codex-setup
```

The setup wizard asks whether to install all catalog models first. Answering
yes installs every active variant without individual variant prompts; answering
no asks once for each variant. An explicit `--variant` keeps the single-variant
flow. The wizard then asks for:

- runtime home path, defaulting to the selected variant default
- whether to install the portable user-global template
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

This overwrite flow applies to Codex. Native Claude activation
rejects `--force`; in guided Claude setup, decline the overwrite prompt.

---

## New Project Or Additive Variant Activation

### Step 1 — Run project init

```bash
bin/codex-project-init /new-project
```

Without `--variant`, project init asks whether to apply all active catalog
variants; declining presents one choice per variant. For a new project, the
command asks for confirmation and creates the shared project surface plus the
selected variant surfaces. For an existing project, init is additive: it preserves
`AGENTS.md`, shared prompts, customized configuration, and other variant files.
Multiple runtime variants can coexist in one project and are recorded together
in `.codex/template-state.json`.

Use an explicit reset only when the shared project structure should be replaced:

```bash
bin/codex-project-init --reset --variant codex /path/to/project
```

Reset conflicts are listed before confirmation and privately archived under
`<project>/.codex/archive/init-YYYYMMDD_HHMMSS-PID/`. Normal additive init does not
archive or replace shared files.

A fresh Codex project creates:

```text
<project>/AGENTS.md
<project>/.codex/config.toml
<project>/.codex/prompts/fill-project-configuration.md
```

With `--variant claude`, init adds `CLAUDE.md` containing `@AGENTS.md` and
`.claude/settings.json` while preserving existing project surfaces.

With `--variant opencode`, init adds `.opencode/opencode.json`. It preserves
Codex configuration plus sibling files and directories under
`.opencode`.

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

Declare only skills that resolve from an active project, user, admin, system,
or session-provided surface. Entries found only in a disabled plugin or an
inactive/on-demand registry are unavailable until they are activated and
verified.

The final block should contain no uncertainty placeholders. Unknown required
values should be resolved by asking the user before editing.

### Step 4 — Declare reusable content, do not inline it

Use `ACTIVE_RULE_SETS`, `ACTIVE_SKILLS`, `ACTIVE_AGENT_ROLES`, and
`ORCHESTRATION_MODE` to declare what this project uses.

Valid orchestration modes:

- `skip`: do not use orchestration by default.
- `ask-approval`: include the mandatory chain in the main plan and obtain the
  single initial plan approval before running it for non-trivial work.
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
  `.codex/archive/upgrade-YYYYMMDD_HHMMSS_microseconds/`

Dry-run is the default and never writes files. Use `--apply` after reviewing the
plan. `--apply --force` skips only the confirmation prompt; it never overwrites
customized files.

Use reset init only when you intentionally want to archive and recreate the
project Codex structure:

1. Read the existing project instruction files if you need to preserve project
   metadata.
2. Run `bin/codex-project-init --reset /path/to/project`.
3. Confirm the reset when prompted.
4. Run the generated prompt:
   `<project>/.codex/prompts/fill-project-configuration.md`.
5. Review the filled `Project Configuration` block.
6. Do not copy reusable rule, skill, or agent bodies into `AGENTS.md`.
7. Put reusable content under `~/.codex/`.

Archived files are stored under:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS-PID/
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

## Main Plan Execution

CMA asks for approval once for a disclosed main plan, then executes every
planned phase and subtask without task-boundary pauses. Material list updates,
auxiliary discoveries, recommended work, and the truthful terminal result are
reported. The initial approval covers disclosed non-destructive Low/Medium work
and planned orchestration. Destructive and High/Critical operations still
require separate approval.
Work discovered outside the approved plan stays on an auxiliary list and is
not executed unless it is required to continue. A required deviation is
reported and approved before the plan changes. Recommended work is reported
separately and is never added to the main plan automatically.

---

## Summary

```text
Run codex-setup for guided installation
        ↓
or install a runtime with codex-user-install [--variant codex|claude|opencode]
        ↓
For existing projects, run codex-project-upgrade
        ↓
For new projects or additive variants, run codex-project-init
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
