# Fill Project Configuration Prompt

**Version:** 2.4
**Updated:** 2026-05-22

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
- Determine concrete `ACTIVE_RULE_SETS`, `ACTIVE_SKILLS`, and
  `ACTIVE_AGENT_ROLES` from the project stack and available user-global assets
  under `~/.codex`. If the choice is ambiguous, ask the user before editing.
- For non-trivial implementation, bugfix, refactor, security, or test-driven
  work, `ACTIVE_AGENT_ROLES` must include:
  `planner`, `tdd-guide`, `code-reviewer`, `security-reviewer`.
- For projects using the mandatory orchestration chain, `ACTIVE_SKILLS` must
  include `tdd-workflow`.
- For this Codex adapter project and OpenAI/Codex documentation work,
  `ACTIVE_SKILLS` must include `openai-docs`.
- Do not remove baseline skills or agent roles that are present in
  `PROJECT_AGENTS_TEMPLATE.md` unless the user explicitly confirms removal.
- `CHANGELOG_PATH` and `EVIDENCE_PATH` must be concrete paths. If they do not
  exist and no convention is documented, ask the user before editing.
- Do not add external runtime root fields; `~/.codex` is the reusable runtime
  surface.

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
ACTIVE_RULE_SETS:
ACTIVE_SKILLS:
ACTIVE_AGENT_ROLES:
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
