---
name: tdd-workflow
description: Apply RED-GREEN-REFACTOR for features, fixes, and refactors.
---

# TDD Workflow

Map acceptance criteria to observable tests. Run the test before implementation
and confirm a meaningful behavior failure. Implement the smallest production
change, run focused GREEN checks, then the complete regression suite.

## Test Integrity Guardrails

Reject hardcoded success, weakened assertions, skipped or disabled tests,
test-only production branches, excessive mocks, swallowed errors, and checks
that do not prove observable behavior.
