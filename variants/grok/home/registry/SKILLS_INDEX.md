# Skill Index

**Status:** Active
**Runtime Surface:** `~/.grok/skills/`

This index tracks reusable Grok skills that are active in the user-global
runtime surface.

## Active Skills

| Name | Path | Scope | Status |
|---|---|---|---|
| hypothesis-workflow | `~/.grok/skills/hypothesis-workflow/SKILL.md` | Escalate difficult or uncertain improvements into traceable experiments. | active |
| orchestration-gate | `~/.grok/skills/orchestration-gate/SKILL.md` | Decide whether a task should skip orchestration, ask for approval, or run the mandatory chain. | active |
| record-archive | `~/.grok/skills/record-archive/SKILL.md` | Compact governance records at sparse lifecycle events without losing history. | active |
| tdd-workflow | `~/.grok/skills/tdd-workflow/SKILL.md` | Enforce test-first implementation and coverage verification for features, bug fixes, and refactors. | active |
| ast-grep | `~/.grok/skills/ast-grep/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| betterleaks | `~/.grok/skills/betterleaks/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| context7 | `~/.grok/skills/context7/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| cplt | `~/.grok/skills/cplt/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| deepwiki | `~/.grok/skills/deepwiki/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| github | `~/.grok/skills/github/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| graphify | `~/.grok/skills/graphify/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| opengrep | `~/.grok/skills/opengrep/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| osv-scanner | `~/.grok/skills/osv-scanner/SKILL.md` | Approved core skill projection; requires its documented tool. | active |
| serena | `~/.grok/skills/serena/SKILL.md` | Approved core skill projection; requires its documented tool. | active |

Grok may also discover shared and vendor compatibility skills. This projection
does not modify those locations or provision their external tool dependencies.

## Missing Skill Policy

When a task needs a skill not listed here:

1. Check whether an existing active skill covers the need.
2. If not, let `skill-agent-governor` define the narrowest useful new skill.
3. The governor must check duplication, scope, conflicts, protected policy
   boundaries, and whether a task-local helper is enough.
4. If activated, the new skill must be added to this index and logged in
   `AUDIT_LOG.md`.

No skill may weaken `~/.grok/AGENTS.md`, the mandatory orchestration chain,
approval rules, or security/destructive-operation rules.
