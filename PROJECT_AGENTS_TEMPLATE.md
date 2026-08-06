# Codex — Project Instructions

**Version:** 2.2
**Updated:** 2026-07-14

---

## Project Configuration

> Fill this block for the project. Global behavior is defined in
> `~/.codex/AGENTS.md`.

```text
PROJECT_NAME:        [Project name]
PROJECT_SUMMARY:     [1-2 sentences: what it does, what problem it solves]

STACK_BACKEND:       [e.g. Python / FastAPI / PostgreSQL / Redis]
STACK_FRONTEND:      [e.g. Next.js / TypeScript / shadcn/ui]

CHANGELOG_PATH:      [e.g. docs/CHANGELOG.md]
EVIDENCE_PATH:       [e.g. docs/reports/]
EVIDENCE_MODE: disable

ACTIVE_RULE_SETS:
  - [e.g. python: coding-style, security, testing, patterns]
  - [e.g. typescript: coding-style, security, testing, patterns]
  - [e.g. web: patterns, performance, security]

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
  - [Project-specific rule 1]
  - [Project-specific rule 2]
  - [Remove these lines if not needed]
```

---

## Project Overview

`PROJECT_NAME`: `PROJECT_SUMMARY`

Stack: `STACK_BACKEND` | `STACK_FRONTEND`

Detailed requirements should come from the project's PRD or equivalent source.

---

## Local Delta

Global Codex behavior comes from `~/.codex/AGENTS.md`.

This project file defines only:

- project identity
- stack and evidence paths
- active reusable declarations
- project-specific domain rules
- local exceptions explicitly required for this project

Reusable rules, skills, and agents must stay outside this file.

---

## Reusable Resolution

Declared rules, skills, and agents resolve in this order:

```text
~/.codex/ overrides
  -> unavailable/report
```

Expected user-global locations:

- `~/.codex/rules/`
- `~/.codex/skills/`
- `~/.codex/agents/`
- `~/.codex/registry/`

Load only the minimum relevant files for the current task.

---

# EOF
