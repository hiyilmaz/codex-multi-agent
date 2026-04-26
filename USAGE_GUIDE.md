# Codex Template V2 — Usage Guide

**Version:** 2.3
**Updated:** 2026-04-27

---

## Requirements

Before using this template, prepare the reusable Codex/ECC surface once:

| Component | Location | Required |
|---|---|---|
| Global Codex instructions | `~/.codex/AGENTS.md` | Yes |
| Global Codex config | `~/.codex/config.toml` | Optional |
| Base ECC root | `~/Codex-ECC` | Yes |
| User rules | `~/.codex/rules/` | Optional |
| User skills | `~/.codex/skills/` | Optional |
| User agents | `~/.codex/agents/` | Optional |

---

## Global ECC Install

Run once:

```bash
bin/codex-ecc-install
```

This prepares:

- `~/Codex-ECC`
- `~/.codex/AGENTS.md`
- `~/.codex/config.toml`
- `~/.codex/rules/`
- `~/.codex/skills/`
- `~/.codex/agents/`

Existing global files are not overwritten by default.

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

ECC_ROOT:            $ECC_ROOT

ACTIVE_RULE_SETS:
  - python: coding-style, security, testing, patterns
  - typescript: coding-style, security, testing, patterns
  - web: patterns, performance, security

ACTIVE_SKILLS:
  - openai-docs

ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer

DOMAIN_RULES:
  - Every payment request must use an idempotency key
  - Every public API endpoint must enforce rate limiting
```

The final block should contain no uncertainty placeholders. Unknown required
values should be resolved by asking the user before editing.

### Step 4 — Declare reusable ECC content, do not inline it

Use `ACTIVE_RULE_SETS`, `ACTIVE_SKILLS`, and `ACTIVE_AGENT_ROLES` to declare
what this project uses.

Reusable bodies should live in one of these locations:

```text
~/.codex/rules/
~/.codex/skills/
~/.codex/agents/
$ECC_ROOT/rules/
$ECC_ROOT/skills/
$ECC_ROOT/agents/
```

Load only the minimum relevant files during the task.

### Step 5 — Refresh the Codex session

Start a new session or refresh the current one so Codex reads the project
`AGENTS.md`.

---

## Existing Project

1. Read the existing project instruction files if you need to preserve project
   metadata.
2. Run `bin/codex-project-init /path/to/project`.
3. Confirm the reset when prompted.
4. Run the generated prompt:
   `<project>/.codex/prompts/fill-project-configuration.md`.
5. Review the filled `Project Configuration` block.
6. Do not copy reusable rule, skill, or agent bodies into `AGENTS.md`.
7. Put user reusable content under `~/.codex/`; keep base ECC content under
   `ECC_ROOT`.

Archived files are stored under:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS/
```

---

## ECC Source Priority

When a declared reusable item exists in more than one place:

```text
user-global override in ~/.codex/ > base ECC in ECC_ROOT > unavailable/report
```

If a declared item cannot be found, report it before doing work that depends on
that item.

---

## Summary

```text
Install/update global ECC
        ↓
Run codex-project-init and confirm reset
        ↓
Run generated Project Configuration prompt
        ↓
Review Project Configuration
        ↓
Declare active ECC rules, skills, and agents
        ↓
Store reusable bodies outside project AGENTS.md
        ↓
Refresh Codex session
```

---

# EOF
