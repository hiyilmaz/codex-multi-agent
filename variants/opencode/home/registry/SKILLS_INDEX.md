# Skill Index

**Status:** Active
**Runtime Surface:** `~/.config/opencode/skills/`

This index tracks reusable OpenCode skills that are active in the user-global
runtime surface.

## Active Skills

| Name | Path | Scope | Status |
|---|---|---|---|
| hypothesis-workflow | `~/.config/opencode/skills/hypothesis-workflow/SKILL.md` | Escalate difficult or uncertain improvements into traceable experiments. | active |
| orchestration-gate | `~/.config/opencode/skills/orchestration-gate/SKILL.md` | Decide whether a task should skip orchestration, ask for approval, or run the mandatory chain. | active |
| record-archive | `~/.config/opencode/skills/record-archive/SKILL.md` | Compact governance records at sparse lifecycle events without losing history. | active |
| tdd-workflow | `~/.config/opencode/skills/tdd-workflow/SKILL.md` | Enforce test-first implementation and coverage verification for features, bug fixes, and refactors. | active |
| opencode-docs | `~/.config/opencode/skills/opencode-docs/SKILL.md` | Consult only official OpenCode documentation. | active |

System skills under `~/.config/opencode/skills/.system/` are managed by OpenCode and are not
duplicated in this user registry.

## Missing Skill Policy

When a task needs a skill not listed here:

1. Check whether an existing active skill covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new skill.
3. The governor must check duplication, scope, conflicts, protected policy
   boundaries, and whether a task-local helper is enough.
4. If activated, the new skill must be added to this index and logged in
   `AUDIT_LOG.md`.

No skill may weaken `~/.config/opencode/AGENTS.md`, the mandatory orchestration chain,
approval rules, or security/destructive-operation rules.
