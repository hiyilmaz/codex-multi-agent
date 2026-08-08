# CMA Orchestration Module

## Load When

Load for orchestration decisions, subagents, agent handoffs, review chains,
model selection, reasoning escalation, or multi-agent governance.

## Do Not Load When

Do not load for simple answers, translations, or direct read-only inspection
that does not use subagents.

## Rules

- Run `orchestration-gate` when the project declares `ORCHESTRATION_MODE`.
- Available roles do not start agents.
- Respect explicit user approval and higher-priority tool policy.
- Once approved, preserve exactly:
  `planner -> tdd-guide -> code-reviewer -> security-reviewer`.
- The main agent implements after TDD guidance and before review.
- Implementation is not a chain stage and never appears inside the chain
  string.
- Do not skip, replace, reorder, or add stages.
- A blocking finding reopens only the affected scoped implementation and
  review stages, within the retry limit.

Decision map:

Apply explicit orchestration and risk triggers before the simple/read-only
rule. Read-only is `skip` only when the task is also simple and no higher-risk
trigger applies.

| Task | Route |
|---|---|
| Simple answer or translation | `skip` |
| Read-only audit | `skip`; add `CMA_MEMORY_ROUTING` when prior context is material |
| Small tested bugfix | main agent plus TDD |
| Multi-file feature | `ask-approval` |
| Explicit CMA request | `run-chain` after scope and tool-policy checks |

For a combined request, classify every component and use the union of required
modules without loading unrelated module bodies.

Routing notes:

- Route auth, secrets, sandboxing, destructive operations, and other changed
  trust boundaries through the mandatory security-reviewer stage.
- Use the declared roles without model-specific aliases. Provider, model, and
  reasoning settings are inherited from the active OpenCode session.

Load `~/.llm-runtimes/opencode/registry/ORCHESTRATION.md` only when detailed stage contracts or
the complete role matrix are needed.
