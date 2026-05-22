# Agent Index

**Status:** Active
**Runtime Surface:** `~/.codex/agents/`

This index tracks reusable Codex agents that are active in the user-global
runtime surface.

## Active Agents

| Name | Path | Scope | Status |
|---|---|---|---|
| planner | `~/.codex/agents/planner.toml` | Plans non-trivial scoped work before implementation. | active |
| tdd-guide | `~/.codex/agents/tdd-guide.toml` | Defines focused test strategy and regression coverage for scoped changes. | active |
| code-reviewer | `~/.codex/agents/code-reviewer.toml` | Reviews implementation for correctness, regressions, maintainability, and project-rule compliance. | active |
| security-reviewer | `~/.codex/agents/security-reviewer.toml` | Reviews scoped changes for security, auth, data safety, destructive operations, and abuse risks. | active |
| explorer | `~/.codex/agents/explorer.toml` | Read-only evidence gathering before implementation. | active |
| reviewer | `~/.codex/agents/reviewer.toml` | Correctness, security, and regression review. | active |
| docs-researcher | `~/.codex/agents/docs-researcher.toml` | Primary-doc verification for APIs, framework behavior, and release notes. | active |
| skill-agent-governor | `~/.codex/agents/skill-agent-governor.toml` | Controlled creation, activation, indexing, and auditing of reusable skills and agents. | active |

## Missing Agent Policy

When a task needs an agent not listed here:

1. Check whether an existing active agent covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new agent.
3. The governor must check duplication, scope, conflicts, and protected policy
   boundaries.
4. If activated, the new agent must be added to this index and logged in
   `AUDIT_LOG.md`.

No agent may modify `~/.codex/AGENTS.md`, `~/.codex/config.toml`, or the
mandatory orchestration chain without explicit user approval.
