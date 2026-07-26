# Orchestration Registry

**Status:** Active
**Owner:** `variants/dolphin/home/AGENTS.md`

---

`variants/dolphin/home/AGENTS.md` remains the source of truth for this
isolated runtime policy.

## Mandatory Chain

Project `AGENTS.md` files may declare:

```text
ORCHESTRATION_MODE: skip | ask-approval | run-chain
```

Use `orchestration-gate` to classify non-trivial work before deciding whether
to skip orchestration, ask for approval, or run the chain.

Mode behavior:

- `skip`: skip orchestration unless the user explicitly requests it.
- `ask-approval`: ask before starting the chain for non-trivial work.
- `run-chain`: run the chain for non-trivial work when project configuration or
  user wording explicitly authorizes orchestration and active tool policy
  permits it. If tool policy requires explicit user approval, ask first.

When orchestration is explicitly requested or approved, preserve this chain:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

During the TDD stage, `tdd-guide` defines the focused verification strategy and
the required `tdd-workflow` skill enforces test-first implementation.

Do not skip, replace, reorder, or weaken this chain.

`ACTIVE_AGENT_ROLES` declares available roles only. It does not start agents by
itself.

`ORCHESTRATION_MODE` must not bypass higher-priority tool or approval policy.

## Stage Responsibilities

### planner

- Input: user request, project instructions, and scoped discovery handoff
- Output: acceptance criteria, affected files, risks, approvals, and prohibited
  shortcuts
- Stop after the plan handoff; do not repeat broad discovery without an
  evidence gap

### tdd-guide

- Input: planner handoff and existing test evidence
- Output: acceptance-to-test mapping with positive, negative, boundary, and
  regression checks
- Stop after the test contract; do not repeat implementation planning

### main agent

- Implement after `tdd-guide` and before `code-reviewer`
- Return the scoped diff and test evidence; passing tests alone do not prove
  completion

### code-reviewer

- Review the diff, acceptance criteria, and test integrity
- Reject hardcoded success, weakened assertions, skipped tests, excessive
  mocks, test-only production branches, and swallowed errors
- Return only blocking findings or a concise `PASS`

### security-reviewer

- Review changed trust boundaries for fail-open behavior, authorization bypass,
  data exposure, destructive actions, secret leakage, and abuse paths
- Return only security findings or concise `NO_SECURITY_IMPACT`

Blocking findings reopen scoped implementation and the affected review stages
within the existing retry limit. Each stage must consume the prior handoff,
avoid repeated work, and stop when its assigned evidence is complete.

## Conditional Experiment Escalation

`hypothesis-workflow` is available globally but is not a mandatory orchestration
stage. Activate it only after a failed meaningful attempt, unclear evidence,
competing hypotheses, a regression or unwanted side effect, a need for measured
comparison, a core runtime/model/agent governance change, or an explicit user
request.

Do not activate it for routine first-pass work, typos, formatting, predictable
maintenance, or a clear deterministic fix with sufficient verification. Do not
create experiment records before a trigger exists.

When activated, it reads prior experiments, changes one main solution variable
when practical, preserves test-integrity controls, and records a supported
decision. It reuses project changelog and evidence paths and does not alter,
replace, or add stages to the mandatory orchestration chain.

## Guardrails

Once orchestration is used:

- do not skip stages
- do not reorder stages
- do not add extra stages inside the mandatory chain
- do not move to closure until both review stages complete

## Protected Boundaries

No orchestrated stage may silently:

- edit user-global runtime files
- edit `variants/dolphin/home/AGENTS.md`
- edit `variants/dolphin/home/config.toml`
- weaken destructive-operation approval rules
- weaken auth/security policy
- change model/runtime defaults

High-risk findings must be surfaced before further edits.

## Runtime Settings

Default runtime settings live in `variants/dolphin/home/config.toml`.
