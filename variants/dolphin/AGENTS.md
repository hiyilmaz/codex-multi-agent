# DolphinVersion Project Instructions

**Version:** 1.1
**Updated:** 2026-06-10

---

## Project Configuration

```text
PROJECT_NAME:        DolphinVersion
PROJECT_SUMMARY:     Isolated agent runtime variant for cognitivecomputations_dolphin-mistral-24b-venice-edition through a remote LM-compatible endpoint.

STACK_BACKEND:       Bash environment wrapper / TOML model settings / Markdown instructions
STACK_FRONTEND:      Documentation only

CHANGELOG_PATH:      variants/dolphin/docs/CHANGELOG.md
EVIDENCE_PATH:       variants/dolphin/docs/reports/

ACTIVE_RULE_SETS:
  - shell: scripting, safety
  - markdown: documentation
  - toml: configuration

ACTIVE_SKILLS:
  - orchestration-gate

ACTIVE_AGENT_ROLES:
  - planner
  - tdd-guide
  - code-reviewer
  - security-reviewer

ORCHESTRATION_MODE: ask-approval

DOMAIN_RULES:
  - Keep all Dolphin runtime state under variants/dolphin/.
  - Do not depend on a repository-local launcher after installation.
  - Do not modify the repository root runtime files while working on this variant unless the user explicitly asks.
  - The launcher must only prepare environment variables; it must not start an agent CLI.
  - Use AGENT_HOME for the local runtime root.
  - Use MODEL_API_BASE_URL for the remote LM-compatible API endpoint.
  - Use MODEL_ID for the selected model identifier.
```

---

## Runtime Boundary

This project uses a local agent home:

```text
AGENT_HOME: variants/dolphin/home
```

Prepare the shell environment with:

```bash
source ~/.llm-runtimes/dolphin/bin/llm-dolphin
```

The launcher is intentionally neutral. It exports environment variables and
does not start the final agent tool.

---

# EOF
