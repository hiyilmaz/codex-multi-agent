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

## Decision Precedence

Apply the first matching rule:

1. Explicit orchestration request: `run-chain`, subject to higher-priority tool
   approval policy.
2. Configured `run-chain` for non-trivial work: run or ask according to tool
   approval policy.
3. Non-trivial or risk-triggering work in `ask-approval` mode: `ask-approval`.
4. Only a task that is both simple and read-only or answer-only: `skip`.

Read-only does not override explicit orchestration, non-triviality, security,
runtime, database, API, test, or cross-module risk triggers.

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

Implementation is not a chain stage. Never insert `implementation`, the main
agent, or any review lens into the four-role chain string.

## Model And Reasoning Escalation

Agent files define defaults, and agent-file values take precedence over parent
or spawn configuration; all custom subagents use `medium` reasoning. When a
model-quality trigger applies to a Terra role, select its static Sol variant:

- `planner-sol`: `gpt-5.6-sol` / `medium` for architecture, unclear scope,
  high-impact runtime, or security-sensitive planning.
- `tdd-guide-sol`: `gpt-5.6-sol` / `medium` for complex test architecture,
  safety-critical behavior, weak-test detection, or hardcoded-success traps.
- `code-reviewer`: keep `gpt-5.6-sol` / `medium`; no separate variant.
- `security-reviewer`: keep `gpt-5.6-sol` / `medium`; no separate variant. The
  stage still returns `NO_SECURITY_IMPACT` when appropriate.
- `explorer-sol`: `gpt-5.6-sol` / `medium` for complex incidents, unclear root causes,
  or conflicting evidence.
- `docs-researcher-sol`: `gpt-5.6-sol` / `medium` for conflicting migration,
  security, API, or release-note evidence.

Selecting a Sol variant must not bypass approval, sandbox, scope, or the
mandatory chain. Sol variants replace only the corresponding invocation; they
do not add a chain stage or change the canonical chain string.

## Output

Use this exact shape:

```text
Decision: skip | ask-approval | run-chain
Reason: [one short reason]
Chain: planner -> tdd-guide -> code-reviewer -> security-reviewer
```

If the decision is `ask-approval`, ask the user for approval before spawning
subagents.
