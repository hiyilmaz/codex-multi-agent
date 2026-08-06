# Restore the Existing Global Claude Code Subagents

Restore this installation's existing personalized Claude Code subagents. This
is a recovery task, not a redesign or a request to invent new roles.

## Runtime Resolution

Resolve the target runtime in this order:

1. An explicit target supplied by the user or invoking command.
2. A non-empty active `CLAUDE_CONFIG_DIR`.
3. The current user's `${HOME}/.claude` directory.

Resolve and validate the target before writing. Never embed a username or copy
a path from another machine. Do not assign or replace `HOME`.

If an explicit target differs from the effective `CLAUDE_CONFIG_DIR`, stop without writing.
Continue only in a new isolated Claude Code process whose `CLAUDE_CONFIG_DIR` resolves to the target.
Apply the same equality check to the native fallback; when the environment is
unset, start the new process with the resolved target instead of delegating
from the current process.

## Authoritative Sources

Use the authoritative agent files from the current CMA package or its verified
runtime template. Compare inventory and frontmatter first, then use targeted
reads only for missing or divergent definitions. Copy verified definitions
instead of regenerating their full instruction bodies in the conversation.

If neither a trusted CMA source nor an equivalent verified runtime definition
is available, stop with `unverified`. Do not fabricate an agent body.

## Required Matrix

| Runtime role | Friendly identity | Model | Effort | Tools | Permission mode |
|---|---|---|---|---|---|
| `code-reviewer` | Cody | opus | medium | Read, Glob, Grep | plan |
| `docs-researcher` | Doc | sonnet | medium | Read, Glob, Grep, WebFetch, WebSearch | plan |
| `docs-researcher-opus` | Doc | opus | medium | Read, Glob, Grep, WebFetch, WebSearch | plan |
| `explorer` | Scout | sonnet | medium | Read, Glob, Grep | plan |
| `explorer-opus` | Scout | opus | medium | Read, Glob, Grep | plan |
| `planner` | Pete | sonnet | medium | Read, Glob, Grep | plan |
| `planner-opus` | Pete | opus | medium | Read, Glob, Grep | plan |
| `reviewer` | Simon | opus | medium | Read, Glob, Grep | plan |
| `security-reviewer` | Sec | opus | medium | Read, Glob, Grep | plan |
| `skill-agent-governor` | Sam | opus | medium | Read, Glob, Grep, Edit, Write | default |
| `tdd-guide` | Ted | sonnet | medium | Read, Glob, Grep | plan |
| `tdd-guide-opus` | Ted | opus | medium | Read, Glob, Grep | plan |

The four `-opus` roles are conditional replacements for their corresponding
Sonnet roles. They are not additional orchestration stages. Preserve exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

The main agent implements after `tdd-guide` and before `code-reviewer`.

## Token and Model Discipline

- Preserve `medium` effort for every restored role.
- Use Sonnet defaults for routine planning, test guidance, exploration, and
  documentation research.
- Select an Opus replacement only for its documented complexity trigger.
- Use inventory-first comparison, targeted reads, bounded handoffs, and
  delta-only repair with concise result reporting.
- Do not repeat discovery already supported by the handoff.
- Do not duplicate full agent bodies in reports or registry prose.
- Do not add unsupported token-budget frontmatter fields.
- Do not shorten or skip the mandatory review chain to save tokens.

## Safe Restoration

Use `skill-agent-governor` only after the effective `CLAUDE_CONFIG_DIR` equals the resolved target.
Preserve equivalent files.
Before replacing a divergent definition, create a targeted recoverable backup
and show the exact delta. Reject symlinked managed paths and any target outside
the resolved runtime home.

Restore only the required agent definitions and directly corresponding agent
index or audit entries. Do not change global policy, runtime settings,
authentication, credentials, approval rules, the mandatory chain, plugins,
project files, or unrelated agents. Do not commit, push, deploy, execute this
prompt against another runtime, or contact external services.

## Validation and Report

Parse every restored frontmatter block. Verify the exact 12-role inventory,
friendly identities, models, effort values, tools, permission modes, four
conditional variants, and unchanged chain. Confirm equivalent files were
preserved and every changed file remains inside the resolved runtime home.

Report only created, repaired, preserved, and backed-up files; validation
commands and results; unresolved conflicts; and the truthful final status.
Never report success without captured validation evidence.
