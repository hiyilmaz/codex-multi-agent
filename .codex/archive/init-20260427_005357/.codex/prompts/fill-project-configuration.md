# Fill Project Configuration Prompt

**Version:** 2.1
**Updated:** 2026-04-27

---

## Prompt

You are configuring this repository for Codex.

Task:
Fill only the `## Project Configuration` block in `AGENTS.md`.

Rules:
- Do not rewrite any other section of `AGENTS.md`.
- Do not change global Codex rules.
- Do not copy reusable rule, skill, or agent bodies into `AGENTS.md`.
- Inspect the repository before editing.
- Prefer durable project facts from existing docs and files.
- If a value cannot be determined confidently, leave a clear placeholder and
  report it.

Read these sources when present:
- `README.md`
- `docs/PRD.md`
- `docs/PROJECT_BRIEF.md`
- `docs/TEST_PLAN.md`
- `docs/CHANGELOG.md`
- package or dependency manifests
- existing app config files
- existing archived Codex files under `.codex/archive/`

Fill these fields:

```text
PROJECT_NAME:
PROJECT_SUMMARY:
STACK_BACKEND:
STACK_FRONTEND:
CHANGELOG_PATH:
EVIDENCE_PATH:
ECC_ROOT:
ACTIVE_RULE_SETS:
ACTIVE_SKILLS:
ACTIVE_AGENT_ROLES:
DOMAIN_RULES:
```

Expected output:
- Updated `AGENTS.md`
- Short report listing which sources were used
- Warnings for unknown or inferred fields

Stop after this configuration task.

---

# EOF
