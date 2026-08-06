# Claude Code Orchestration Registry

**Status:** Active
**Owner:** `${CLAUDE_CONFIG_DIR}/CLAUDE.md`

## Source Of Truth

`${CLAUDE_CONFIG_DIR}/CLAUDE.md` remains the source of truth for global policy.

Project `CLAUDE.md` files may define narrower local deltas, but they must not
weaken global approval, scope, evidence, destructive-operation, or orchestration
rules.

## Mandatory Chain

Project `CLAUDE.md` files may declare:

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

Implementation is not a chain stage. The main agent implements between the TDD
and review stages, but any reported chain string must contain only the four
named roles in the exact order above.

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

- edit `${CLAUDE_CONFIG_DIR}/CLAUDE.md`
- edit `${CLAUDE_CONFIG_DIR}/settings.json`
- change the mandatory orchestration chain
- weaken approval, security, destructive-operation, or scope rules
- delete or rewrite existing active skills or agents

Any change to the protected files or core policy above requires explicit user
approval.

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
decision. It reuses project `CHANGELOG_PATH` and `EVIDENCE_PATH` and does not
alter, replace, or add stages to the mandatory orchestration chain.

## Model And Effort Routing

Agent Markdown frontmatter files define the default matrix. Static `*-opus`
agent definitions make model escalation explicit and reviewable; all custom
subagents use `medium` effort. Selecting an Opus variant changes only the model for that
role invocation; it does not alter the mandatory chain, approval state,
sandbox, or persistent defaults.

| Role | Default | Opus variant and trigger |
|---|---|---|
| `planner` | `sonnet` / `medium` | `planner-opus`, `opus` / `medium`, for architecture, unclear scope, high-impact runtime, or security-sensitive planning |
| `tdd-guide` | `sonnet` / `medium` | `tdd-guide-opus`, `opus` / `medium`, for complex test architecture, safety-critical behavior, weak-test detection, or hardcoded-success traps |
| `code-reviewer` | `opus` / `medium` | No variant; keep the configured default |
| `security-reviewer` | `opus` / `medium` | No variant; keep the configured default |
| `explorer` | `sonnet` / `medium` | `explorer-opus`, `opus` / `medium`, for complex incidents, unclear root causes, or conflicting evidence |
| `docs-researcher` | `sonnet` / `medium` | `docs-researcher-opus`, `opus` / `medium`, for conflicting migration, security, API, or release-note evidence |
| `reviewer` | `opus` / `medium` | Keep the configured default |
| `skill-agent-governor` | `opus` / `medium` | Keep the configured default |

The security-reviewer stage always runs in an approved chain. When no trust
boundary changed, it returns `NO_SECURITY_IMPACT` with a concise evidence
summary.

The Opus variants are routing aliases, not extra mandatory stages. Render the
canonical four-role chain even when one invocation uses an Opus variant.

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
