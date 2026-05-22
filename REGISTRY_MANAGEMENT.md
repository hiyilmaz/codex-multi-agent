# Codex Registry Management

**Version:** 1.0
**Updated:** 2026-05-22

---

## Purpose

The active reusable Codex surface is `~/.codex`.

This project no longer uses an external runtime layer, source-priority layer,
or required external dependency.

---

## Directory Model

User-global Codex:

```text
~/.codex/
  AGENTS.md
  config.toml
  rules/
  skills/
  agents/
  registry/
```

Project:

```text
<project>/
  AGENTS.md
  .codex/config.toml
  .codex/prompts/fill-project-configuration.md
  .codex/archive/           # init backups
```

Portable template:

```text
codex-home-template/
  AGENTS.md
  config.toml
  agents/
  skills/
  registry/
```

Install the portable template with:

```bash
bin/codex-user-install
```

---

## Registry Files

```text
~/.codex/registry/AGENTS_INDEX.md
~/.codex/registry/SKILLS_INDEX.md
~/.codex/registry/ORCHESTRATION.md
~/.codex/registry/AUDIT_LOG.md
```

The registry indexes active reusable agents and skills. It also documents
orchestration policy, reasoning-effort policy, and controlled self-improvement.

---

## Governor

`~/.codex/agents/skill-agent-governor.toml` owns automatic reusable skill and
agent creation.

The governor may create and activate new reusable skills and agents without
user approval when they are narrow, non-destructive, indexed, and logged.

The governor must not edit protected core policy:

- `~/.codex/AGENTS.md`
- `~/.codex/config.toml`
- the mandatory orchestration chain
- approval rules
- destructive-operation rules
- auth/security policy
- model/runtime defaults

Protected policy changes require explicit user approval.

---

## Resolution Priority

```text
project declaration
  -> user-global content in ~/.codex/
  -> unavailable/report or governor-created asset
```

---

# EOF
