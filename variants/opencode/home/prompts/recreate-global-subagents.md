# Restore the Existing Global OpenCode Subagents

Restore this installation's existing personalized OpenCode subagents. This is a
recovery task, not a redesign or a request to invent new roles.

## Runtime Resolution

Resolve the target runtime in this order:

1. An explicit target supplied by the user or invoking command.
2. A non-empty active `OPENCODE_CONFIG_DIR`.
3. The current user's `${HOME}/.llm-runtimes/opencode` directory.

Resolve and validate the target before writing. Never embed a username or copy
a path from another machine. Do not assign or replace `HOME`.

## Authoritative Sources

Use the authoritative agent files from the current CMA package or its verified
runtime template. Compare inventory and metadata first, then read only missing
or divergent definitions. Copy verified definitions instead of regenerating
their full instruction bodies in the conversation.

If neither a trusted CMA source nor an equivalent verified runtime definition
is available, stop with `unverified`. Do not fabricate an agent body.

## Required Matrix

Restore exactly these provider-neutral Markdown roles: `planner`, `tdd-guide`,
`code-reviewer`, `security-reviewer`, `explorer`, `docs-researcher`, `reviewer`,
and `skill-agent-governor`. Do not add provider/model aliases or model fields.
Preserve exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

The main agent implements after `tdd-guide` and before `code-reviewer`.

## Context And Provider Discipline

- Use inventory-first comparison, targeted reads, bounded handoffs, delta-only
  repair, and concise result reporting.
- Do not repeat discovery already supported by the handoff.
- Do not duplicate full agent bodies in reports or registry prose.
- Do not add provider, model, or unsupported token-budget fields.
- Do not shorten or skip the mandatory review chain to save tokens.

## Safe Restoration

Use `skill-agent-governor` when it is available. Preserve equivalent files.
Before replacing a divergent definition, create a targeted recoverable backup
and show the exact delta. Reject symlinked managed paths and any target outside
the resolved runtime home.

Restore only the required agent definitions and directly corresponding agent
index or audit entries. Do not change global policy, runtime configuration,
authentication, secrets, approval rules, the mandatory chain, plugins, project
files, or unrelated agents. Do not commit, push, deploy, or contact external
services.

## Validation and Report

Parse every restored Markdown frontmatter block. Verify the exact eight-role
inventory, provider neutrality, permissions, and unchanged chain. Confirm
equivalent files were preserved and every changed
file remains inside the resolved runtime home.

Report only created, repaired, preserved, and backed-up files; validation
commands and results; unresolved conflicts; and the truthful final status.
Never report success without captured validation evidence.
