# Agent Index

**Status:** Active
**Runtime Surface:** `${CLAUDE_CONFIG_DIR}/agents/`

This index tracks reusable Claude Code agents that are active in the user-global
runtime surface.

## Active Agents

| Role Key | Friendly Identity | Path | Scope | Status |
|---|---|---|---|---|
| planner | Pete | `${CLAUDE_CONFIG_DIR}/agents/planner.md` | Plans non-trivial scoped work before implementation. | active |
| tdd-guide | Ted | `${CLAUDE_CONFIG_DIR}/agents/tdd-guide.md` | Defines focused test strategy and regression coverage for scoped changes. | active |
| code-reviewer | Cody | `${CLAUDE_CONFIG_DIR}/agents/code-reviewer.md` | Reviews implementation for correctness, regressions, maintainability, and project-rule compliance. | active |
| security-reviewer | Sec | `${CLAUDE_CONFIG_DIR}/agents/security-reviewer.md` | Reviews scoped changes for security, auth, data safety, destructive operations, and abuse risks. | active |
| explorer | Scout | `${CLAUDE_CONFIG_DIR}/agents/explorer.md` | Read-only evidence gathering before implementation. | active |
| reviewer | Simon | `${CLAUDE_CONFIG_DIR}/agents/reviewer.md` | Correctness, security, and regression review. | active |
| docs-researcher | Doc | `${CLAUDE_CONFIG_DIR}/agents/docs-researcher.md` | Primary-doc verification for APIs, framework behavior, and release notes. | active |
| skill-agent-governor | Sam | `${CLAUDE_CONFIG_DIR}/agents/skill-agent-governor.md` | Controlled creation, activation, indexing, and auditing of reusable skills and agents. | active |

## Opus Routing Variants

| Role Key | Friendly Identity | Path | Scope | Status |
|---|---|---|---|---|
| planner-opus | Pete | `${CLAUDE_CONFIG_DIR}/agents/planner-opus.md` | Complex architecture, unclear scope, or high-impact planning. | active |
| tdd-guide-opus | Ted | `${CLAUDE_CONFIG_DIR}/agents/tdd-guide-opus.md` | Complex or safety-critical test strategy. | active |
| explorer-opus | Scout | `${CLAUDE_CONFIG_DIR}/agents/explorer-opus.md` | Complex incidents or conflicting root-cause evidence. | active |
| docs-researcher-opus | Doc | `${CLAUDE_CONFIG_DIR}/agents/docs-researcher-opus.md` | Conflicting migration, security, API, or release documentation. | active |

These static variants preserve the same friendly identities while pinning
`opus` / `medium`. They replace one Sonnet invocation when its documented
model-quality trigger applies; they are not additional chain stages. All custom
subagents use `medium` effort.

Claude Code uses each frontmatter `name` as the runtime role identifier. Friendly identities
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

No agent may modify `${CLAUDE_CONFIG_DIR}/CLAUDE.md`, `${CLAUDE_CONFIG_DIR}/settings.json`, or the
mandatory orchestration chain without explicit user approval.
