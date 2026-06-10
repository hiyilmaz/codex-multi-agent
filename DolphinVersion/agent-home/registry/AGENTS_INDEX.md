# Agent Index

**Status:** Active
**Runtime Surface:** `DolphinVersion/agent-home/agents/`

This index tracks reusable agents that are active in the isolated
DolphinVersion runtime surface.

## Active Agents

| Name | Path | Scope | Status |
|---|---|---|---|
| planner | `DolphinVersion/agent-home/agents/planner.toml` | Plans non-trivial scoped work before implementation. | active |
| tdd-guide | `DolphinVersion/agent-home/agents/tdd-guide.toml` | Defines focused test strategy and regression coverage for scoped changes. | active |
| code-reviewer | `DolphinVersion/agent-home/agents/code-reviewer.toml` | Reviews implementation for correctness, regressions, maintainability, and project-rule compliance. | active |
| security-reviewer | `DolphinVersion/agent-home/agents/security-reviewer.toml` | Reviews scoped changes for security, auth, data safety, destructive operations, and abuse risks. | active |
| explorer | `DolphinVersion/agent-home/agents/explorer.toml` | Read-only evidence gathering before implementation. | active |
| reviewer | `DolphinVersion/agent-home/agents/reviewer.toml` | Correctness, security, and regression review. | active |
| docs-researcher | `DolphinVersion/agent-home/agents/docs-researcher.toml` | Primary-doc verification for APIs, framework behavior, and release notes. | active |
| skill-agent-governor | `DolphinVersion/agent-home/agents/skill-agent-governor.toml` | Controlled creation, activation, indexing, and auditing of reusable skills and agents. | active |

## Missing Agent Policy

When a task needs an agent not listed here:

1. Check whether an existing active agent covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new agent.
3. The governor must check duplication, scope, conflicts, and protected policy
   boundaries.
4. If activated, the new agent must be added to this index and logged in
   `AUDIT_LOG.md`.

No agent may modify user-global runtime files or the DolphinVersion mandatory
orchestration chain without explicit user approval.
