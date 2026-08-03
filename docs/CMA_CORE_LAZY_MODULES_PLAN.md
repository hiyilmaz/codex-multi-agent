# CMA Core And Lazy Modules Plan

Date: 2026-08-01
Status: Implemented and verified
Scope: This repository and the active local global Codex directory at
`/Users/iyilmaz/.codex`

## Scope Boundary

Included:

- `/Users/iyilmaz/WebStorm/Codex-Multi-Agent`
- `/Users/iyilmaz/.codex`

Excluded:

- Remote servers and their `/root/.codex` directories.
- Hermes profiles and bridges.
- Other local projects, including `rfr.grisis.com`.
- The Dolphin variant, unless separately approved.

## Goal

Reduce the default local token load without weakening CMA safeguards against
false completion, weak tests, skipped review, unsafe changes, or unsupported
success claims.

## Verified Result

- The repository and active local global Codex ZIP backups exist and pass ZIP
  integrity checks.
- The approved eight-role model and reasoning matrix is identical in
  `variants/codex/home/agents/` and `/Users/iyilmaz/.codex/agents/`.
- The mandatory chain remains
  `planner -> tdd-guide -> code-reviewer -> security-reviewer`.
- No mandatory CMA role uses `gpt-5.6-luna`.
- The full repository test suite passes with the medium-only matrix.
- Core CMA was reduced from 483 to 201 lines while preserving mandatory safety,
  approval, truthful-success, test-integrity, and chain rules.
- Eight lazy modules are packaged and active in `/Users/iyilmaz/.codex`.
- Unsupported `display_name` fields are absent; friendly identities remain in
  instructions and registry documentation.
- Four static `*-sol` variants provide model-only escalation for Terra roles
  despite agent-file precedence over spawn configuration.
- All default and variant subagents use `medium` reasoning; no `*-high` agent
  files remain.

## Non-Negotiable Core

The lightweight core must always preserve:

- Scope lock.
- Turkish user dialogue and English implementation artifacts.
- Destructive and high-risk approval gates.
- Truthful success reporting.
- Test-integrity safeguards.
- Project `AGENTS.md` as a local delta only.
- `skip | ask-approval | run-chain` orchestration routing.
- The mandatory four-stage chain after orchestration approval.

## Active Lazy Modules

- `cma-orchestration`: chain rules, handoffs, and reviewer requirements.
- `cma-tdd`: RED/GREEN/refactor and test-strength requirements.
- `cma-security`: auth, secrets, destructive operations, and data safety.
- `cma-remote-admin`: SSH, wrappers, backups, and service checks. This remains
  a local reusable module even though remote hosts are outside this task.
- `cma-memory-routing`: memory lookup and citation rules.
- `cma-docs-research`: official-source lookup and citation rules.
- `cma-frontend`: browser, screenshot, and UI verification.
- `cma-records`: changelog, evidence, deferred findings, and archiving.

The default prompt should load only Core CMA plus a compact module index and
routing rules. Module bodies load only after a matching task trigger.

## Routing Matrix

| Task type | Default route | Required modules |
|---|---|---|
| Simple answer or short status | `skip` | None |
| Read-only audit or report | `skip` | Docs or memory only when needed |
| Small low-risk edit | Main agent | Records when required |
| Small tested bugfix | Main agent | TDD |
| Multi-file feature or refactor | `ask-approval` | Planning, TDD, records |
| API, DB, auth, security, runtime, or deployment | `ask-approval` | Planning, TDD, security, records |
| Explicit CMA, chain, or subagent request | `run-chain` after scope check | Full orchestration |

When uncertain, route to `ask-approval`.

## Shell Output Policy

Use file-list-first and targeted-read-second. Exclude generated or third-party
content by default:

- `.git`, `node_modules`, `vendor`, `dist`, `build`, `coverage`, and `cache`
- `*.map` and `*.min.js`
- `*.zip`, `*.tar`, and `*.gz`
- remote plugin catalogs unless explicitly requested

## Approved Model Matrix

| Agent role | Model | Reasoning | Escalation |
|---|---|---|---|
| `planner` | `gpt-5.6-terra` | `medium` | `planner-sol`, Sol/medium, for architecture or high-impact scope |
| `tdd-guide` | `gpt-5.6-terra` | `medium` | `tdd-guide-sol`, Sol/medium, for complex or safety-critical tests |
| `code-reviewer` | `gpt-5.6-sol` | `medium` | No variant |
| `security-reviewer` | `gpt-5.6-sol` | `medium` | No variant; never skip the stage |
| `explorer` | `gpt-5.6-terra` | `medium` | `explorer-sol`, Sol/medium, for complex incidents |
| `docs-researcher` | `gpt-5.6-terra` | `medium` | `docs-researcher-sol`, Sol/medium, for conflicting evidence |
| `reviewer` | `gpt-5.6-sol` | `medium` | No variant |
| `skill-agent-governor` | `gpt-5.6-sol` | `medium` | No variant |

## Implemented Sequence

1. Backed up the repository and active local Codex surface.
2. Added RED contract tests, then implemented Core/Lazy packaging and routing.
3. Removed unsupported naming metadata and preserved stable role keys.
4. Replaced high-reasoning variants with four Sol/medium role variants after
   review confirmed agent-file precedence and the token-reduction objective.
5. Mirrored only approved files into `/Users/iyilmaz/.codex`.
6. Verified focused/full tests, source-active parity, fresh-session routing,
   checksums, and rollback material.

## Rollback Sources

- Repository:
  `/Users/iyilmaz/CodexBackups/20260801T230058Z/Codex-Multi-Agent-repo-20260731T230058Z.zip`
- Active local global Codex:
  `/Users/iyilmaz/CodexBackups/20260801T230058Z/codex-home-global-nosocket-20260731T230345Z.zip`
- Targeted pre-activation snapshot:
  `/Users/iyilmaz/CodexBackups/20260801T235744Z-cma-core-lazy-active/`

Do not use the incomplete
`codex-home-global-20260731T230058Z.zip` archive.

## Official Sources

- OpenAI Codex subagents documentation:
  `https://developers.openai.com/codex/subagents`
- OpenAI Codex models documentation:
  `https://developers.openai.com/codex/models`
- OpenAI Codex configuration reference:
  `https://developers.openai.com/codex/config-reference`
