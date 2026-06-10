# Orchestration Registry

**Status:** Active
**Owner:** `DolphinVersion/agent-home/AGENTS.md`

---

`DolphinVersion/agent-home/AGENTS.md` remains the source of truth for this
isolated runtime policy.

## Mandatory Chain

For non-trivial implementation, bugfix, refactor, security, or test-driven work
that uses orchestration:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

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
- edit `DolphinVersion/agent-home/AGENTS.md`
- edit `DolphinVersion/agent-home/config.toml`
- weaken destructive-operation approval rules
- weaken auth/security policy
- change model/runtime defaults

High-risk findings must be surfaced before further edits.

## Runtime Settings

Default runtime settings live in `DolphinVersion/agent-home/config.toml`.
