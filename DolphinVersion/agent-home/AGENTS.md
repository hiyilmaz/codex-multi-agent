# DolphinVersion Runtime Instructions

**Version:** 1.2
**Updated:** 2026-06-10

---

## Purpose

This file defines the isolated DolphinVersion agent runtime. It is scoped to
the local `DolphinVersion/agent-home` directory and must not depend on any
user-global runtime home.

---

## Runtime Surface

Runtime root:

```text
AGENT_HOME: DolphinVersion/agent-home
```

Runtime ownership:

- `DolphinVersion/agent-home` owns reusable rules, agents, registry indexes,
  runtime config, sessions, logs, caches, and local state for this variant.
- Project `AGENTS.md` files own only project identity, active declarations,
  domain constraints, and local deltas.

Resolution priority:

```text
project declaration
  -> DolphinVersion/agent-home override
  -> unavailable/report
```

Active reusable assets and governance indexes live under:

- `DolphinVersion/agent-home/agents/`
- `DolphinVersion/agent-home/skills/`
- `DolphinVersion/agent-home/registry/`

---

## Model Boundary

Endpoint:

```text
https://lm.backstage8.com/v1/
```

Model:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

Treat this as a remote LM-compatible chat provider. Do not assume hosted
tooling or provider-specific reasoning features are available.

---

## Core Rules

### 1. Language

- User dialogue: **Turkish**
- Code, comments, commits, docs, agent prompts: **English**

### 2. Scope Lock

- Do only what is requested.
- When done: report result, stop, and wait for the next instruction.

### 3. Runtime Isolation

- Do not read from, write to, install into, or synchronize with any user-global
  runtime home.
- Keep DolphinVersion runtime state under `DolphinVersion/agent-home`.
- Do not modify parent runtime templates unless the user explicitly asks.

### 4. Destructive Operations

The following require explicit user approval:

- `DROP`, `DELETE *`, `TRUNCATE`, broad file deletion, hard git resets, and
  force pushes
- Adding dependencies
- Changing API contracts
- Database schema changes
- Auth or security code changes

### 5. Changelog

- Location: `DolphinVersion/docs/CHANGELOG.md`
- Format: `## YYYY-MM-DD` plus `- [TAG] Description`
- Tags: `[API]`, `[UI]`, `[DB]`, `[FIX]`, `[FEAT]`, `[REFACTOR]`, `[DOCS]`,
  `[TEST]`, `[INFRA]`

### 6. File Size

- Target: 200-400 lines
- Warning: 500+ lines
- Hard limit: 800 lines

### 7. Commit Rules

- Never auto-commit.
- Suggest a commit message only at full task closure.
- Format: `git commit -m "type(scope): description"`

### 8. Bounded Execution

- Max 5 steps per task without interim report.
- Max 3 retries for the same failing action.
- No infinite loops, unbounded polling, or sleeps longer than 10 seconds.

---

## Workflow

Simple tasks:

```text
pre-flight -> implement -> verify -> changelog -> report -> stop
```

Complex tasks:

```text
Phase 1: read-only discovery
Phase 2: scoped execution after findings are clear
```

---

## Agent Workflow

If orchestration is used for non-trivial implementation, bugfix, refactor,
security, or test-driven work, follow this chain:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

Do not skip or reorder stages once orchestration is used.

---

## Reusable Resolution

Expected local locations:

- `DolphinVersion/agent-home/rules/`
- `DolphinVersion/agent-home/skills/`
- `DolphinVersion/agent-home/agents/`
- `DolphinVersion/agent-home/registry/`

Load only the minimum relevant files for the current task.

---

## Evidence

- Evidence files: `DolphinVersion/docs/reports/`
- Format: `EVIDENCE_[TASK-ID]_YYYYMMDD_HHMM.md`
- Contains: commands, outputs, diffs, test logs, and review findings

---

# EOF
