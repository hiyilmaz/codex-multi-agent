# Codex Orchestration Registry

**Status:** Active
**Owner:** `~/.codex/AGENTS.md`

## Source Of Truth

`~/.codex/AGENTS.md` remains the source of truth for global policy.

Project `AGENTS.md` files may define narrower local deltas, but they must not
weaken global approval, scope, evidence, destructive-operation, or orchestration
rules.

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

## Stage Contracts

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

## Lightweight Orchestrator Protocol

The lightweight orchestrator protocol is a review-lens policy, not a competing
chain.

It may be used to decide whether extra subagent opinions are useful for a
specific risk, such as correctness, security, runtime/config, persistence,
strategy behavior, or project-rule compliance.

It must not create fixed extra stages. It must not bypass approvals required by
`AGENTS.md`.

## Skill/Agent Governor

The `skill-agent-governor` owns controlled self-improvement for reusable skills
and agents.

It may automatically:

- detect missing skill or agent coverage
- create task-local or global skill/agent candidates
- activate new skills or agents after completing its checks
- update registry indexes
- append audit log entries

It must not automatically:

- edit `~/.codex/AGENTS.md`
- edit `~/.codex/config.toml`
- change the mandatory orchestration chain
- weaken approval, security, destructive-operation, or scope rules
- delete or rewrite existing active skills or agents

Any change to the protected files or core policy above requires explicit user
approval.

## Reasoning Effort Policy

Default runtime settings live in `~/.codex/config.toml`.

The four mandatory Codex chain agents use `medium` reasoning by default. A
future increase must be justified by measured missed findings or a documented
quality regression; use the EXPERIMENT escalation workflow before changing the
baseline.

```text
low:
  - typos
  - simple command output
  - small formatting changes

medium:
  - small bugfixes
  - bounded file edits
  - simple debugging
  - mandatory orchestration chain agents

high:
  - architecture
  - multi-file implementation
  - security, auth, DB, API, persistence
  - strategy, signal, or financial logic
  - uncertain root cause analysis
  - registry or skill/agent governance
```

## YOLO Mode Boundary

YOLO mode may reduce interruptions for low-risk work, but it must never bypass
approval for destructive or high-risk changes.

Approval is always required for:

- `DROP`
- `DELETE *`
- `TRUNCATE`
- `rm -rf`
- `git reset --hard`
- `git push --force`
- adding dependencies
- changing API contracts
- DB schema changes
- auth/security code changes
