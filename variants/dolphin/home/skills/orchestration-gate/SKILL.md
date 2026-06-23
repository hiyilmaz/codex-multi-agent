---
name: "orchestration-gate"
description: "Decide whether a task should skip orchestration, ask for approval, or run the mandatory orchestration chain. Use when a project AGENTS.md declares ORCHESTRATION_MODE, when the user asks about orchestration, or before non-trivial implementation, bugfix, refactor, security, or test-driven work."
---

# Orchestration Gate

Use this skill as a decision gate before orchestration. It produces a decision;
it does not spawn subagents or bypass tool policy.

## Inputs

Read the minimum relevant context:

1. User request
2. Project `AGENTS.md` `## Project Configuration`
3. Current task scope from already inspected files, if available

Look for:

```text
ORCHESTRATION_MODE: skip | ask-approval | run-chain
ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer
```

If `ORCHESTRATION_MODE` is missing, treat it as `ask-approval` for
non-trivial tasks.

## Decision Rules

Return `skip` when:

- The task is simple, local, read-only, or answer-only.
- The user asks for a short command, explanation, or direct inspection.
- The configured mode is `skip` and the user did not explicitly request
  orchestration.

Return `ask-approval` when:

- The task is non-trivial and the configured mode is `ask-approval`.
- The task likely affects more than 3 files, architecture, security, database
  behavior, API contracts, runtime setup, tests, or cross-module behavior.
- The configured mode is unclear and starting subagents would require explicit
  user approval.

Return `run-chain` when:

- The user explicitly asks to use orchestration, subagents, delegation, parallel
  agent work, or the named chain.
- The configured mode is `run-chain`, the task is non-trivial, and active tool
  policy permits orchestration without a separate user approval.

If active tool policy requires explicit user approval before subagents are
spawned, return `ask-approval` even when the configured mode is `run-chain`.

## Mandatory Chain

When the result is `run-chain`, the required order is:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

Do not skip, reorder, or add stages to this chain.

## Output

Use this exact shape:

```text
Decision: skip | ask-approval | run-chain
Reason: [one short reason]
Chain: planner -> tdd-guide -> code-reviewer -> security-reviewer
```

If the decision is `ask-approval`, ask the user for approval before spawning
subagents.
