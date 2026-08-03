# Agent Index

**Status:** Active
**Runtime Surface:** `~/.codex/agents/`

This index tracks reusable Codex agents that are active in the user-global
runtime surface.

## Active Agents

| Role Key | Friendly Identity | Path | Scope | Status |
|---|---|---|---|---|
| planner | Pete | `~/.codex/agents/planner.toml` | Plans non-trivial scoped work before implementation. | active |
| tdd-guide | Ted | `~/.codex/agents/tdd-guide.toml` | Defines focused test strategy and regression coverage for scoped changes. | active |
| code-reviewer | Cody | `~/.codex/agents/code-reviewer.toml` | Reviews implementation for correctness, regressions, maintainability, and project-rule compliance. | active |
| security-reviewer | Sec | `~/.codex/agents/security-reviewer.toml` | Reviews scoped changes for security, auth, data safety, destructive operations, and abuse risks. | active |
| explorer | Scout | `~/.codex/agents/explorer.toml` | Read-only evidence gathering before implementation. | active |
| reviewer | Simon | `~/.codex/agents/reviewer.toml` | Correctness, security, and regression review. | active |
| docs-researcher | Doc | `~/.codex/agents/docs-researcher.toml` | Primary-doc verification for APIs, framework behavior, and release notes. | active |
| skill-agent-governor | Sam | `~/.codex/agents/skill-agent-governor.toml` | Controlled creation, activation, indexing, and auditing of reusable skills and agents. | active |

## Sol Routing Variants

The following static variants preserve the same friendly identity while
pinning `gpt-5.6-sol` / `medium`: `planner-sol`, `tdd-guide-sol`,
`explorer-sol`, and `docs-researcher-sol`. They replace one Terra invocation
when its documented model-quality trigger applies; they are not additional
chain stages. All custom subagents use `medium` reasoning.

Codex uses each TOML `name` as the runtime role identifier. Friendly identities
are instruction and registry aliases; they do not control client UI or spawned
thread labels.

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
