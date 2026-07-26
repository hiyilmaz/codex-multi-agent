# Orchestration Improvement Tasks

**Status:** Core contract implemented; runtime timing benchmark pending.

## Pending

- [ ] ORCH-006 — Benchmark the updated workflow on representative small,
  medium, and high-risk tasks; compare elapsed time, token use, findings, and
  missed regressions before considering any reasoning increase.

## Completed

- [x] ORCH-001 — Set the four mandatory Codex chain agents to `medium`
  reasoning.
- [x] ORCH-002 — Preserve the sequential four-agent chain while requiring
  bounded handoffs, evidence reuse, and fast `PASS` or `NO_SECURITY_IMPACT`
  exits.
- [x] ORCH-003 — Define narrow input, output, no-repeat, and stop conditions for
  `planner`, `tdd-guide`, `code-reviewer`, and `security-reviewer`.
- [x] ORCH-004 — Add independent test-integrity and false-success checks
  without allowing reviewers to restart planning or broad discovery.
- [x] ORCH-005 — Add `hypothesis-workflow` as a conditional escalation only
  after a failed attempt, unclear evidence, competing hypotheses, regression,
  measured comparison, core governance change, or explicit user request.

## Role Defaults

| Role | Default | Scope |
|---|---|---|
| `planner` | Medium | Scope and acceptance handoff |
| `tdd-guide` | Medium | Acceptance-to-test mapping |
| `code-reviewer` | Medium | Diff and test-integrity review |
| `security-reviewer` | Medium | Changed trust boundaries or fast no-impact result |

Any future move to `high` requires evidence from ORCH-006 and the conditional
EXPERIMENT workflow.
