# Agent Index

**Status:** Active
**Runtime Surface:** `~/.config/opencode/agents/`

This index tracks reusable OpenCode agents that are active in the user-global
runtime surface.

## Active Agents

| Role Key | Friendly Identity | Path | Scope | Status |
|---|---|---|---|---|
| planner | Pete | `~/.config/opencode/agents/planner.md` | Plans non-trivial scoped work before implementation. | active |
| tdd-guide | Ted | `~/.config/opencode/agents/tdd-guide.md` | Defines focused test strategy and regression coverage for scoped changes. | active |
| code-reviewer | Cody | `~/.config/opencode/agents/code-reviewer.md` | Reviews implementation for correctness, regressions, maintainability, and project-rule compliance. | active |
| security-reviewer | Sec | `~/.config/opencode/agents/security-reviewer.md` | Reviews scoped changes for security, auth, data safety, destructive operations, and abuse risks. | active |
| explorer | Scout | `~/.config/opencode/agents/explorer.md` | Read-only evidence gathering before implementation. | active |
| reviewer | Simon | `~/.config/opencode/agents/reviewer.md` | Correctness, security, and regression review. | active |
| docs-researcher | Doc | `~/.config/opencode/agents/docs-researcher.md` | Primary-doc verification for APIs, framework behavior, and release notes. | active |
| skill-agent-governor | Sam | `~/.config/opencode/agents/skill-agent-governor.md` | Controlled creation, activation, indexing, and auditing of reusable skills and agents. | active |

## Provider-Neutral Routing

OpenCode uses each Markdown filename as the runtime role identifier. Agent
definitions do not pin a provider, model, or reasoning effort; they inherit the
active session configuration. Friendly identities are registry aliases only.

## Missing Agent Policy

When a task needs an agent not listed here:

1. Check whether an existing active agent covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new agent.
3. The governor must check duplication, scope, conflicts, and protected policy
   boundaries.
4. If activated, the new agent must be added to this index and logged in
   `AUDIT_LOG.md`.

No agent may modify `~/.config/opencode/AGENTS.md`,
`~/.config/opencode/opencode.json`, or the
mandatory orchestration chain without explicit user approval.
