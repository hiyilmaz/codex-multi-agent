# CMA Subagent Model Pilot Implementation Plan

Date: 2026-08-01
Status: Implemented and verified
Scope: This repository and `/Users/iyilmaz/.codex` only

## Guardrails

- Preserve `planner -> tdd-guide -> code-reviewer -> security-reviewer`.
- Never weaken truthful-success, test-integrity, approval, or destructive
  operation rules.
- Do not edit `/Users/iyilmaz/.codex/config.toml`, `auth.json`, secrets, plugin
  state, remote hosts, other projects, or the Dolphin variant.
- Patch managed source first, validate it, then mirror only approved files into
  the active local global Codex directory.
- Preserve unrelated dirty work and do not auto-commit.

## Verified Implemented Matrix

The following values are present and identical in the managed Codex variant
and active local global agents:

| Role key | Friendly identity | Model | Reasoning |
|---|---|---|---|
| `planner` | Pete | `gpt-5.6-terra` | `medium` |
| `tdd-guide` | Ted | `gpt-5.6-terra` | `medium` |
| `code-reviewer` | Cody | `gpt-5.6-sol` | `medium` |
| `security-reviewer` | Sec | `gpt-5.6-sol` | `medium` |
| `explorer` | Scout | `gpt-5.6-terra` | `medium` |
| `docs-researcher` | Doc | `gpt-5.6-terra` | `medium` |
| `reviewer` | Simon | `gpt-5.6-sol` | `medium` |
| `skill-agent-governor` | Sam | `gpt-5.6-sol` | `medium` |

No mandatory CMA role uses `gpt-5.6-luna`.

## Naming Correction Applied

Official standalone custom-agent files require `name`, `description`, and
`developer_instructions`. Codex uses `name` as the agent identifier.
`display_name` is not part of the documented standalone custom-agent schema.

Therefore:

- Keep role keys in `name` for orchestration compatibility.
- Keep Pete, Ted, Cody, Sec, Doc, Scout, Sam, and Simon as friendly identities
  in `developer_instructions` and registry documentation.
- Unsupported `display_name` fields were removed from managed and active agent
  files.
- Do not claim that friendly identities control the client UI or spawned
  thread labels.

## Medium-Only Conditional Routing Applied

Official precedence makes agent-file values override parent or spawn model
configuration. The implementation therefore uses these static variants:

- `planner-sol`: Sol/medium for architecture, unclear scope, high-impact runtime, or
  security-sensitive work.
- `tdd-guide-sol`: Sol/medium for complex test architecture, safety-critical
  behavior, weak-test detection, or hardcoded-success traps.
- `explorer-sol`: Sol/medium for unclear incidents, complex root causes, or
  conflicting evidence.
- `docs-researcher-sol`: Sol/medium for conflicting migration, security, API, or
  release-note evidence.

`code-reviewer`, `security-reviewer`, `reviewer`, and
`skill-agent-governor` already use Sol/medium and therefore have no separate
variant. The security stage always runs and returns `NO_SECURITY_IMPACT` when
appropriate. No subagent uses high reasoning.

## Implemented Files

Managed source:

- `variants/codex/home/agents/*.toml` for defaults, Sol/medium variants, and
  unsupported-field cleanup.
- `variants/codex/home/registry/AGENTS_INDEX.md` for naming semantics.
- `variants/codex/home/registry/ORCHESTRATION.md` for escalation routing.
- `variants/codex/home/skills/orchestration-gate/SKILL.md` for trigger rules.
- `tests/test_cma_lazy_runtime.py` for negative, routing, packaging, and matrix
  checks.
- `docs/CHANGELOG.md` after verified implementation.

Active local global runtime:

- `/Users/iyilmaz/.codex/agents/*.toml`
- `/Users/iyilmaz/.codex/registry/AGENTS_INDEX.md`
- `/Users/iyilmaz/.codex/registry/ORCHESTRATION.md`
- `/Users/iyilmaz/.codex/skills/orchestration-gate/SKILL.md`

## Validation Result

1. A checksum-verified targeted active-runtime backup was created.
2. RED tests exposed stale high variants and routing; the final focused suite
   validates the 12-file medium-only matrix.
3. The complete repository suite passes after the medium-only revision.
4. Managed and active owned files are checksum-equivalent, except the active
   append-only audit log intentionally preserves older local history.
5. Fresh-session routing confirms default Terra/medium and Sol/medium roles.
6. A final routing probe preserved the exact chain, approval behavior, lazy
   module selection, and mandatory security route.
7. Actual subagent spawning was not performed because this execution did not
   separately authorize spawning; static TOML selection is directly testable.

## Acceptance Criteria

- The mandatory chain and all approval/test-integrity rules remain unchanged.
- The implemented matrix remains exact in source and active local global
  files.
- Friendly identities are documented honestly without unsupported TOML fields.
- Default and Sol role files pin the expected model and medium reasoning effort,
  and routing selects the corresponding static role key.
- No required security-review stage is skipped.
- The full test suite passes without weakened or skipped assertions.
- Token and latency results are recorded separately from quality results.
- Rollback is possible from verified archives and file hashes.

## Rollback

- Repository ZIP:
  `/Users/iyilmaz/CodexBackups/20260801T230058Z/Codex-Multi-Agent-repo-20260731T230058Z.zip`
- Active local global Codex ZIP:
  `/Users/iyilmaz/CodexBackups/20260801T230058Z/codex-home-global-nosocket-20260731T230345Z.zip`

Restore only files owned by the failed attempt and only after explicit user
approval. Re-run focused and full tests after restoration.

## Approval Boundary

The approved local implementation is complete. Any future matrix, chain,
remote, config, auth, plugin, or excluded-project change requires a new scope
and approval.
