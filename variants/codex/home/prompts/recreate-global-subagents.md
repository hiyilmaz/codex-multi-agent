# Restore the Existing Global Codex Subagents

Restore this installation's existing personalized Codex subagents. This is a
recovery task, not a redesign or a request to invent new roles.

## Runtime Resolution

Resolve the target runtime in this order:

1. An explicit target supplied by the user or invoking command.
2. A non-empty active `CODEX_HOME`.
3. The current user's `${HOME}/.codex` directory.

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

| Runtime role | Friendly identity | Model | Reasoning | Sandbox |
|---|---|---|---|---|
| `planner` | Pete | gpt-5.6-terra | medium | read-only |
| `planner-sol` | Pete | gpt-5.6-sol | medium | read-only |
| `tdd-guide` | Ted | gpt-5.6-terra | medium | read-only |
| `tdd-guide-sol` | Ted | gpt-5.6-sol | medium | read-only |
| `code-reviewer` | Cody | gpt-5.6-sol | medium | read-only |
| `security-reviewer` | Sec | gpt-5.6-sol | medium | read-only |
| `explorer` | Scout | gpt-5.6-terra | medium | read-only |
| `explorer-sol` | Scout | gpt-5.6-sol | medium | read-only |
| `reviewer` | Simon | gpt-5.6-sol | medium | read-only |
| `docs-researcher` | Doc | gpt-5.6-terra | medium | read-only |
| `docs-researcher-sol` | Doc | gpt-5.6-sol | medium | read-only |
| `skill-agent-governor` | Sam | gpt-5.6-sol | medium | workspace-write |

The four `-sol` roles are conditional replacements for their corresponding
Terra roles. They are not additional orchestration stages. Preserve exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

The main agent implements after `tdd-guide` and before `code-reviewer`.

## Token and Model Discipline

- Preserve `medium` reasoning for every restored role.
- Use Terra defaults for routine planning, test guidance, exploration, and
  documentation research.
- Select a Sol replacement only for its documented complexity trigger.
- Use inventory-first comparison, targeted reads, bounded handoffs, delta-only
  repair, and concise result reporting.
- Do not repeat discovery already supported by the handoff.
- Do not duplicate full agent bodies in reports or registry prose.
- Do not add unsupported token-budget TOML fields.
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

Parse every restored TOML. Verify the exact 12-role inventory, friendly
identities, models, reasoning values, sandboxes, four conditional variants,
and unchanged chain. Confirm equivalent files were preserved and every changed
file remains inside the resolved runtime home.

Report only created, repaired, preserved, and backed-up files; validation
commands and results; unresolved conflicts; and the truthful final status.
Never report success without captured validation evidence.
