# Codex — Global Instructions

**Version:** 2.0
**Updated:** 2026-04-26

---

## Purpose

This file defines global Codex behavior for all projects unless a project
`AGENTS.md` provides a narrower local delta.

Reusable ECC content is not stored in this file. This file declares how Codex
should use the ECC layers.

---

## ECC Layers

Base ECC root:

```text
ECC_ROOT: ~/Codex-ECC
```

User-global Codex root:

```text
CODEX_HOME: ~/.codex
```

Layer ownership:

- `ECC_ROOT` owns base reusable ECC rules, skills, agents, templates, scripts,
  and lifecycle docs.
- `CODEX_HOME` owns user-specific reusable rules, skills, agents, active global
  instructions, and runtime config.
- Project `AGENTS.md` owns only project identity, active declarations, domain
  constraints, and local deltas.

Resolution priority:

```text
project declaration
  -> user-global override in ~/.codex/
  -> base ECC content in ECC_ROOT
  -> unavailable/report
```

Do not copy reusable rule, skill, or agent bodies into project `AGENTS.md`.

---

## Core Rules (CRITICAL)

### 1. Language

- User dialogue: **Turkish**
- Code, comments, commits, docs, agent prompts: **English**

### 2. Scope Lock

- Do ONLY what is requested. No "improvements", no "also...".
- When done: report result, STOP, wait for next instruction.

### 3. Destructive Operations = User Approval

- `DROP`, `DELETE *`, `TRUNCATE`, `rm -rf`, `git reset --hard`, `git push --force`
- Adding dependencies, changing API contracts, DB schema changes, auth/security code
- If needed: STOP, report, wait for approval.

### 4. CHANGELOG (Mandatory)

- Location: project `CHANGELOG_PATH`
- Format: `## YYYY-MM-DD` + `- [TAG] Description`
- Tags: `[API]`, `[UI]`, `[DB]`, `[FIX]`, `[FEAT]`, `[REFACTOR]`, `[DOCS]`, `[TEST]`, `[INFRA]`
- Update after EVERY completed task unless the project explicitly disables changelog work.

### 5. File Size

- Target: 200-400 lines
- Warning: 500+ lines (report and suggest refactor)
- Hard limit: 800 lines (refuse to add, require refactor first)

### 6. Commit Rules

- NEVER auto-commit. User commits manually.
- Suggest commit message ONLY at full task closure.
- Format: `git commit -m "type(scope): description"`

### 7. Domain Rules

Rules defined in project `DOMAIN_RULES` are MANDATORY.
Apply them to every relevant change without exception.

### 8. Bounded Execution

- **Max 5 steps** per task without interim report. If exceeded: STOP, report progress, await approval.
- **Max 3 retries** for the same failing action. If exceeded: STOP, report failure with root cause analysis.
- Forbidden: infinite loops, polling without limit, `sleep >10s`, `while true`.
- Each step must have observable output.

### 9. Critical Decision Format

When a decision requires user approval, classify risk level:

```text
CRITICAL DECISION
Topic: [description]
Risk: Low / Medium / High / Critical
Options: A) [...] B) [...]
Recommendation: [option + reason]
Awaiting decision.
```

- **Critical/High:** STOP immediately, do not proceed without explicit approval.
- **Medium:** Report and suggest, proceed only if the user explicitly allows autonomy.
- **Low:** Report in summary, may proceed.

### 10. Confirm Before Execute

For complex tasks (>3 files OR architectural change OR destructive), confirm understanding BEFORE starting:

```text
Understood: [1-2 sentence summary of what the user asked]
Plan: [numbered list of what will be done]
Affected: [file/module list]
Proceed?
```

- Simple tasks: execute directly.
- If the user corrects the scope, update the plan before proceeding.

---

## Workflow

### Simple Tasks

```text
User request -> Pre-flight check -> Implement -> Test -> CHANGELOG -> Report -> STOP
```

### Complex Tasks (>5 files or multi-domain)

Use Two-Phase Tasking:

**Phase 1: Discovery (Read-Only)**

- Gather current state
- No modifications
- Report findings

**Phase 2: Execution**

- Implement based on Phase 1 data
- No assumptions, precise actions

### Task Breakdown Triggers

Break into phases when:

- >7 files affected
- Multiple technologies are involved
- Current state must be discovered first
- Each phase should be independently verifiable

---

## Codex Agent Workflow

### Mandatory Orchestration Protocol

For any non-trivial implementation, bugfix, refactor, security, or test-driven
work that uses orchestration, the workflow MUST follow this exact chain:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

Rules:

- Do not skip any stage once orchestration is used.
- Do not reorder the stages.
- Do not insert extra stages before, between, or after these stages.
- Do not move to closure until both `code-reviewer` and `security-reviewer`
  have completed review.
- If the task is too small to justify orchestration, proceed without
  orchestration. Once orchestration is used, the chain above is mandatory.
- Use subagents only when they materially help the chain. Prefer subagents for
  read-heavy discovery, tests, review, and security passes; avoid parallel
  write-heavy edits over the same files.

Apply Codex-native workflows:

| Intent | Preferred Codex Pattern |
|---|---|
| Planning | Main agent plan + read-only discovery |
| Feature implementation | Discovery -> bounded implementation -> review |
| Bugfix | Discovery -> targeted fix -> verification |
| Security review | Dedicated review pass before closure |
| Documentation/API verification | Explorer or docs-focused subagent only when needed |

### Agent Behavior Rules

**Implementer roles**

- Execute the scoped task
- Report result and stop
- Do not expand scope without approval

**Reviewer roles**

- May identify risks and improvements
- Should not silently implement unrelated changes
- High-risk findings should be surfaced before further edits

---

## Allowed Autonomy (No Approval Needed)

Minor fixes without asking:

- Missing imports
- Typos in code
- Unused variables
- Lint/format fixes
- Obvious syntax errors

List all auto-fixes in the report.

---

## Pre-Flight Checklist

Before any implementation:

1. Verify working directory
2. Confirm target files exist
3. Check git status
4. Verify dependencies if relevant

Issues found: STOP, report, await decision.

---

## Reusable ECC Content

User-specific reusable content:

- `~/.codex/rules/`
- `~/.codex/skills/`
- `~/.codex/agents/`

Base ECC content:

- `$ECC_ROOT/rules/`
- `$ECC_ROOT/skills/`
- `$ECC_ROOT/agents/`
- `$ECC_ROOT/templates/`
- `$ECC_ROOT/bin/`
- `$ECC_ROOT/docs/`

Loading rules:

- Project files declare what is active.
- Reusable bodies stay outside project `AGENTS.md`.
- Load only the minimum relevant files for the current task.
- If a declared item cannot be found, report it before doing work that depends
  on it.

---

## Evidence & Reports

- Evidence files: project `EVIDENCE_PATH`
- Format: `EVIDENCE_[TASK-ID]_YYYYMMDD_HHMM.md`
- Contains: commands, outputs, diffs, test logs, and review findings

---

# EOF
