# Codex — Project Instructions

**Version:** 2.0
**Updated:** 2026-04-26

---

## Project Configuration

> Fill this block for the project. Global behavior is defined in
> `~/.codex/AGENTS.md`.

```text
PROJECT_NAME:        Codex Template V2
PROJECT_SUMMARY:     Codex-native project instruction template and helper scripts for initializing project AGENTS.md files, Codex config, prompts, and reusable ECC structure.

STACK_BACKEND:       Bash scripts / Markdown templates / TOML config examples
STACK_FRONTEND:      Not applicable; documentation and CLI template project

CHANGELOG_PATH:      docs/CHANGELOG.md
EVIDENCE_PATH:       docs/reports/

ECC_ROOT:            $ECC_ROOT

ACTIVE_RULE_SETS:
  - shell: scripting, safety, testing
  - markdown: documentation, templates
  - toml: configuration

ACTIVE_SKILLS:
  - openai-docs

ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer

DOMAIN_RULES:
  - Project AGENTS.md files declare project deltas only; do not inline reusable ECC rule, skill, or agent bodies.
  - Helper scripts must preserve existing global or project Codex files unless the documented confirmation or force flag is used.
  - Keep Codex config examples valid for Codex config.toml schema; do not add custom reserved runtime metadata tables.
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
- active ECC declarations
- project-specific domain rules
- local exceptions explicitly required for this project

Reusable rules, skills, and agents must stay outside this file.

---

## ECC Resolution

Declared rules, skills, and agents resolve in this order:

```text
~/.codex/ overrides
  -> ECC_ROOT base content
  -> unavailable/report
```

Expected user-global locations:

- `~/.codex/rules/`
- `~/.codex/skills/`
- `~/.codex/agents/`

Expected base ECC locations:

- `$ECC_ROOT/rules/`
- `$ECC_ROOT/skills/`
- `$ECC_ROOT/agents/`

Load only the minimum relevant files for the current task.

---

# EOF
