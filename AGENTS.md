# Codex — Project Instructions

**Version:** 2.1
**Updated:** 2026-05-22

---

## Project Configuration

> Fill this block for the project. Global behavior is defined in
> `~/.codex/AGENTS.md`.

```text
PROJECT_NAME:        Codex Template V2
PROJECT_SUMMARY:     Codex-native project instruction template and helper scripts for initializing project AGENTS.md files, Codex config, prompts, user-global skill/agent registry structure, and a local index of official OpenAI Codex docs.

STACK_BACKEND:       Python docs indexer / Bash scripts / Markdown templates / TOML config examples
STACK_FRONTEND:      Documentation and CLI template project

CHANGELOG_PATH:      docs/CHANGELOG.md
EVIDENCE_PATH:       docs/reports/

ACTIVE_RULE_SETS:
  - python: scripting, documentation-indexing, testing
  - shell: scripting, safety, testing
  - markdown: documentation, templates
  - toml: configuration

ACTIVE_SKILLS:
  - tdd-workflow
  - openai-docs

ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer

DOMAIN_RULES:
  - Project AGENTS.md files declare project deltas only; do not inline reusable rule, skill, or agent bodies.
  - Helper scripts must preserve existing global or project Codex files unless the documented confirmation or force flag is used.
  - Keep Codex config examples valid for Codex config.toml schema; do not add custom reserved runtime metadata tables.
  - Local OpenAI Codex docs entries are compact indexes only; official OpenAI docs remain authoritative.
  - External runtime/vendor layers are not part of the active resolution model.
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
