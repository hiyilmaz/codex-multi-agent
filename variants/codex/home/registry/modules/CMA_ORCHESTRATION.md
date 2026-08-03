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

Escalation map:

- Use `planner-sol` for planner architecture or high-impact scope.
- Use `tdd-guide-sol` for tdd-guide safety-critical behavior or
  hardcoded-success traps.
- Keep code-reviewer and security-reviewer on `gpt-5.6-sol` / `medium`; they do
  not need separate variants.
- Route auth, secrets, sandboxing, destructive operations, and other changed
  trust boundaries through the mandatory security-reviewer stage.
- Use `explorer-sol` for explorer complex incidents or conflicting evidence,
  and `docs-researcher-sol` for conflicting migration or security guidance.
- Keep default model/reasoning for routine work. Escalation is an explicit
  static role selection, not a persistent default change. All custom subagents
  use `medium`, and Sol variants pin
  `gpt-5.6-sol` / `medium` because agent-file values take precedence.

Load `~/.codex/registry/ORCHESTRATION.md` only when detailed stage contracts or
the complete role matrix are needed.
