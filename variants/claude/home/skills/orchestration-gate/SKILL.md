---
name: orchestration-gate
description: Decide whether work skips orchestration, requires approval, or runs the mandatory chain.
---

# Orchestration Gate

Read the project `ORCHESTRATION_MODE`. Simple answers and read-only status work
may skip. For `ask-approval`, request approval before non-trivial work. Once
approved, preserve exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

Do not skip, replace, reorder, or insert stages. Approval waiting is not task
completion and never proves PASS.
