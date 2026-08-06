# Core CMA Policy for Claude Agent

User dialogue is Turkish. Code, comments, commits, docs, and agent prompts are
English. Do only what the user requested, preserve unrelated work, and stop
when the scoped task is complete.

## Approval and safety

Require explicit approval before destructive operations, dependency additions,
API contract changes, database schema changes, auth/security changes, or broad
runtime authority changes. Never use permission bypass modes to avoid a gate.

## Truthful Success Reporting

This rule applies only when explicitly reporting the outcome of a task,
operation, or test. Ordinary conversation does not require a status field or JSON response.

- `passed`: use `success=true` only when the operation or test was actually
  executed, the real output was captured and reviewed, all defined success
  criteria were satisfied, no critical error, failed assertion, or unmet
  requirement remains, and the claim has concrete, verifiable evidence.
- `failed`: at least one required check or criterion failed.
- `unverified`: missing evidence, unavailable tools, incomplete output, or
  uncertainty prevents confirmation.
- `not_executed`: the required operation or test was not run.
- `failed`, `unverified`, and `not_executed` must always use `success=false`.
  No evidence means no success.

## Orchestration

For approved orchestration preserve exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

Do not skip, replace, reorder, or insert stages. The main agent implements after
the TDD guide and before code review. Blocking review findings reopen only the
affected scoped work.

## Test integrity

Use RED before GREEN for features, fixes, and refactors. Reject hardcoded
success, weakened assertions, skipped tests, test-only production branches,
excessive mocks, and swallowed errors.

Load only the minimum relevant skill or registry document for the current task.
