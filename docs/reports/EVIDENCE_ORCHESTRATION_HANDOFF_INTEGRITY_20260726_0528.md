# Orchestration Handoff and Integrity Evidence

**Date:** 2026-07-26 05:28 +03
**Scope:** Mandatory chain handoffs, false-completion controls, and Codex
subagent reasoning defaults.

## Result

The mandatory chain remains unchanged:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

The main agent implements after `tdd-guide` and before `code-reviewer`. Each
agent now has explicit input, output, no-repeat, and stop contracts so work
continues through concise handoffs instead of repeated broad discovery.

The four mandatory Codex agents now use:

```toml
model_reasoning_effort = "medium"
```

Dolphin agent prompts received the same bounded contracts without adding an
unsupported reasoning setting.

## Integrity Controls

- Acceptance criteria and prohibited shortcuts are defined before implementation.
- Tests must fail against dummy or hardcoded-success behavior.
- Passing tests alone do not prove completion.
- Review checks hardcoded success, weakened assertions, skipped tests,
  excessive mocks, test-only production paths, swallowed errors, and missing
  observable behavior.
- Security review checks changed trust boundaries and may return a concise
  `NO_SECURITY_IMPACT`.
- Blocking findings reopen scoped implementation and affected review stages
  within the existing retry limit.

## Verification

```text
PASS parsed 24 agent TOML files
PASS 12/12 unittest tests
PASS temporary Codex runtime installation
PASS temporary Dolphin runtime installation
PASS GLOBAL_AGENTS_TEMPLATE.md matches Codex variant AGENTS.md
PASS git diff --check
PASS no high reasoning remains in the four Codex chain agents
```

The active runtime files match the validated Codex variant for the four agent
definitions, orchestration registry, and TDD workflow skill.

## Archive

Previous active runtime files:

```text
~/.codex/archive/orchestration-contract-20260726_052849/
```

## Remaining Measurement

Static contracts and installation behavior are verified. Real elapsed-time,
token-use, and missed-finding comparisons require representative tasks in new
sessions and remain tracked as `ORCH-006`.
