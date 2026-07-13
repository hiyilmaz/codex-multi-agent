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

`ACTIVE_AGENT_ROLES` declares available roles only. It does not start agents by
itself.

`ORCHESTRATION_MODE` must not bypass higher-priority tool or approval policy.

## Stage Responsibilities

### planner

- Define scope
- Identify affected files
- Identify risks and approval boundaries
- Produce an implementation plan

### tdd-guide

- Define the lightest useful verification path
- Identify missing tests
- Tie tests to behavior and risk

### code-reviewer

- Review correctness
- Review regressions
- Review maintainability
- Check project-rule compliance

### security-reviewer

- Review auth, data safety, destructive operations, abuse vectors, dependency
  risks, and secret exposure

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
