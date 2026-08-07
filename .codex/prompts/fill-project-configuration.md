# Fill Project Configuration Prompt

**Version:** 2.5
**Updated:** 2026-07-14

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
- Do not write uncertainty placeholders into `AGENTS.md`.
- Do not write uncertainty placeholders or literal strings such as "TODO",
  "Not configured", "None", "Not found", or bracket placeholders.
- If a required value cannot be determined confidently, stop and ask the user
  the smallest necessary question before editing `AGENTS.md`.
- Determine concrete `ACTIVE_RULE_SETS`, `ACTIVE_SKILLS`,
  `ACTIVE_AGENT_ROLES`, and `ORCHESTRATION_MODE` from the project stack and
  the selected runtime home and assets exposed by the current Codex session.
  Consider documented repository, user, admin, and system skill locations; do
  not mark a skill unavailable only because it is absent from
  `~/.codex/skills`. If the choice is ambiguous, ask the user before editing.
- For non-trivial implementation, bugfix, refactor, security, or test-driven
  work, `ACTIVE_AGENT_ROLES` must include:
  `planner`, `tdd-guide`, `code-reviewer`, `security-reviewer`.
- For projects using the mandatory orchestration chain, `ACTIVE_SKILLS` must
  include `orchestration-gate` and `tdd-workflow`.
- `ORCHESTRATION_MODE` must be one of `skip`, `ask-approval`, or `run-chain`.
  Use `ask-approval` unless the project or user explicitly requires another
  mode.
- `EVIDENCE_MODE` must be exactly `enable` or `disable`.
  Use `disable` when the field is missing or no explicit choice is provided.
  If an explicit value is invalid, report it and do not treat evidence automation as enabled.
- Add `openai-docs` only for OpenAI/Codex development or documentation work
  when that skill is available in the current session. Do not add it as a
  baseline skill for unrelated projects.
- Do not remove baseline skills or agent roles that are present in
  `PROJECT_AGENTS_TEMPLATE.md` unless the user explicitly confirms removal.
- Do not switch `ORCHESTRATION_MODE` to `skip` only because an optional skill
  is unavailable.
- `CHANGELOG_PATH` and `EVIDENCE_PATH` must be concrete paths. If they do not
  exist and no convention is documented, ask the user before editing.
- Do not add external runtime root fields; the selected runtime home is the
  reusable runtime surface.

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
EVIDENCE_MODE:
ACTIVE_RULE_SETS:
ACTIVE_SKILLS:
ACTIVE_AGENT_ROLES:
ORCHESTRATION_MODE:
DOMAIN_RULES:
```

Expected output:
- Updated `AGENTS.md`
- Short report listing which sources were used
- Questions asked before editing when required values were ambiguous
- Confirmation that no uncertainty placeholders remain in the
  `Project Configuration` block

Stop after this configuration task.

---

# EOF
