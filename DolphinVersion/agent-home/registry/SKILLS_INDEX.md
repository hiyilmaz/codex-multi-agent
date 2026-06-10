# Skill Index

**Status:** Active
**Runtime Surface:** `DolphinVersion/agent-home/skills/`

This index tracks reusable skills that are active in the isolated
DolphinVersion runtime surface.

## Active Skills

| Name | Path | Scope | Status |
|---|---|---|---|
| _none_ | _n/a_ | No reusable skills are active by default in the isolated DolphinVersion runtime. | inactive |

Default user-global skills are not duplicated in this runtime.

## Missing Skill Policy

When a task needs a skill not listed here:

1. Check whether an existing active skill covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new skill.
3. The governor must check duplication, scope, conflicts, protected policy
   boundaries, and whether a task-local helper is enough.
4. If activated, the new skill must be added to this index and logged in
   `AUDIT_LOG.md`.

No skill may weaken DolphinVersion runtime instructions, the mandatory
orchestration chain, approval rules, or security/destructive-operation rules.
