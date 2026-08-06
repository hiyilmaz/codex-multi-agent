# Claude Integration Task Plan

Date: 2026-08-06
Last Updated: 2026-08-06
Overall Status: **Tamamlandı**
Current Gate: Phase 5 complete; optional Gate C real API work remains gated

## Purpose

Track the approved preparation, implementation, verification, and optional
production work required to add Claude as a third runtime variant alongside
Codex and Dolphin.

The recommended delivery path is:

1. Add native Claude Code CLI compatibility.
2. Add a safe project-level `CLAUDE.md` bridge.
3. Verify parity without changing active user runtime state.
4. Evaluate the Claude Agent SDK only through a separately approved pilot.
5. Add production hosting controls only if the SDK will be operated as a
   service.

## Status Contract

Every tracked task and phase must use exactly one of these values:

- **Bekliyor**: Work has not started or is waiting for an approval/dependency.
- **İşlemde**: Work is actively being performed or verified.
- **Tamamlandı**: Acceptance criteria were executed and satisfied with
  reviewed evidence.

Status update rules:

1. Change a task to **İşlemde** before its implementation begins.
2. Change a task to **Tamamlandı** only after its stated verification passes.
3. Keep a blocked task as **Bekliyor** or **İşlemde** and describe the blocker
   in its Notes field; do not introduce another status value.
4. A phase becomes **Tamamlandı** only when every required task in that phase
   is **Tamamlandı** and its approval gate is satisfied.
5. Update `Last Updated`, the progress summary, and the decision log whenever
   any task status changes.
6. Test failures, missing evidence, or incomplete output must never be recorded
   as completion.

## Scope Boundaries

Phase 0 through Phase 4 and the local, offline Phase 5 SDK pilot are approved
and complete.

Excluded until separately approved:

- Using a real Anthropic API key or subscription credential.
- Making a real Claude API request.
- Installing or changing an active `~/.claude` or global Claude runtime.
- Changing remote machines or production services.
- Releasing or deploying changes.
- Commit and push were excluded from the implementation phases; Gate E is now
  approved for the reviewed repository changes.
- Weakening Codex or Dolphin behavior to simplify Claude compatibility.

## Progress Summary

| Phase | Description | Status |
|---|---|---|
| Plan | Persist and maintain this task tracker | **Tamamlandı** |
| Phase 0 | Experiment and baseline contract | **Tamamlandı** |
| Phase 1 | Provider-neutral variant contract | **Tamamlandı** |
| Phase 2 | Native Claude runtime variant | **Tamamlandı** |
| Phase 3 | Project bridge and safe upgrade | **Tamamlandı** |
| Phase 4 | Parity verification and documentation | **Tamamlandı** |
| Phase 5 | Optional Claude Agent SDK pilot | **Tamamlandı** |
| Phase 6 | Optional production hardening | **Bekliyor** |

## Plan Task

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| PLAN-001 | Save all phases and tasks in one durable tracker | **Tamamlandı** | This document exists and contains the required status contract. |

## Phase 0 - Experiment And Baseline Contract

Phase Status: **Tamamlandı**

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-000 | Obtain explicit approval for Phase 0 through Phase 4 | **Tamamlandı** | Approval excludes SDK dependencies, live activation, commit, push, and deployment. |
| CLD-001 | Create the Claude integration hypothesis experiment before implementation | **Tamamlandı** | `EXP-20260806-007` records the required workflow before production edits. |
| CLD-002 | Capture the current Codex and Dolphin variant baseline | **Tamamlandı** | Catalog/file inventory captured; pre-change suite passed 60/60. |
| CLD-003 | Inventory and preserve unrelated dirty work | **Tamamlandı** | Existing changelog, experiment, archive, hypothesis-test, and Graphify changes remain outside owned edits. |
| CLD-004 | Define RED tests and observable acceptance criteria | **Tamamlandı** | TDD Guide supplied isolated behavior and anti-cheat coverage. |
| CLD-005 | Define repository and temporary-install rollback procedures | **Tamamlandı** | Experiment record defines patch-only source rollback and disposable fixtures. |

Phase exit criteria:

- Experiment record exists in `PROPOSED` or `TESTING` state.
- Baseline and rollback sources are recorded.
- RED tests and prohibited shortcuts are agreed before production changes.

## Phase 1 - Provider-Neutral Variant Contract

Phase Status: **Tamamlandı**

Primary ownership:

- `variants/config.toml`
- `bin/codex-user-install`
- `bin/codex-setup`
- Installer and setup contract tests

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-100 | Define provider-aware policy and configuration metadata | **Tamamlandı** | Catalog declares provider policy, settings, and agent format metadata. |
| CLD-101 | Add failing tests for a third variant | **Tamamlandı** | Valid RED captured before production files were added. |
| CLD-102 | Refactor installer file selection without weakening preservation | **Tamamlandı** | Declared files install; existing files remain untouched without `--force`. |
| CLD-103 | Preserve optional launcher installation and path rewriting | **Tamamlandı** | Claude and Dolphin launchers remain executable and runtime-relative. |
| CLD-104 | Make setup variant selection display Claude | **Tamamlandı** | Catalog listing and explicit Claude setup are covered. |
| CLD-105 | Keep legacy CLI compatibility | **Tamamlandı** | `--codex-home` alias regression passes. |
| CLD-106 | Verify unknown and malformed variants fail closed | **Tamamlandı** | Unknown/incomplete metadata and managed symlinks fail before unsafe writes. |

Phase exit criteria:

- Installer logic no longer assumes every provider uses Codex filenames.
- Existing Codex and Dolphin install tests still pass unchanged.
- No dependency or active runtime change has occurred.

## Phase 2 - Native Claude Runtime Variant

Phase Status: **Tamamlandı**

Planned surface:

```text
variants/claude/
├── bin/claude
└── home/
    ├── CLAUDE.md
    ├── settings.json
    ├── agents/*.md
    ├── skills/*/SKILL.md
    └── registry/
```

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-200 | Register the `claude` runtime variant | **Tamamlandı** | Default home and `llm-claude` launcher are catalogued. |
| CLD-201 | Create a neutral Claude launcher | **Tamamlandı** | Stub proves isolated `CLAUDE_CONFIG_DIR`, argv forwarding, and exit propagation. |
| CLD-202 | Handle a missing native `claude` binary safely | **Tamamlandı** | Missing binary returns a clear message and exit 127. |
| CLD-203 | Create the user-level Core CMA `CLAUDE.md` | **Tamamlandı** | Scope, approval, truthful reporting, TDD, and exact chain are covered. |
| CLD-204 | Add safe Claude `settings.json` defaults | **Tamamlandı** | Minimal default permission mode; no bypass, hook, or credential data. |
| CLD-205 | Convert mandatory roles to Claude Markdown/YAML subagents | **Tamamlandı** | Four distinct Markdown/frontmatter roles are packaged. |
| CLD-206 | Package compatible skills without OpenAI-only metadata requirements | **Tamamlandı** | Four native skill directories install byte-for-byte in isolation. |
| CLD-207 | Exclude session, cache, memory, credentials, and hook state | **Tamamlandı** | Source artifact exclusion and safe settings tests pass. |

Phase exit criteria:

- A temporary Claude runtime installs without touching `~/.claude`.
- Launcher behavior is verified with a stub native binary.
- The exact mandatory chain remains `planner -> tdd-guide -> code-reviewer -> security-reviewer`.

## Phase 3 - Project Bridge And Safe Upgrade

Phase Status: **Tamamlandı**

Primary ownership:

- `PROJECT_AGENTS_TEMPLATE.md`
- Claude project template files
- `bin/codex-project-init`
- `bin/codex-project-upgrade`
- Template-state migration tests

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-300 | Define the project `CLAUDE.md` bridge | **Tamamlandı** | Managed template contains exactly `@AGENTS.md`. |
| CLD-301 | Add variant-specific project managed files | **Tamamlandı** | Claude init adds bridge/settings while base behavior remains green. |
| CLD-302 | Extend template-state schema safely | **Tamamlandı** | Schema v1 safely records variant-specific managed paths without a format bump. |
| CLD-303 | Preserve existing `CLAUDE.md` and `.claude/` content | **Tamamlandı** | Customized bridge and unrelated Claude content are preserved. |
| CLD-304 | Add Claude-aware init conflict reporting | **Tamamlandı** | Exact bridge/settings conflicts are listed and archived after confirmation. |
| CLD-305 | Add Claude-aware upgrade dry-run | **Tamamlandı** | Byte-level non-mutation test passes. |
| CLD-306 | Verify idempotent upgrade and rollback | **Tamamlandı** | Initialized state is unchanged on repeat; init recovery archive is verified. |

Phase exit criteria:

- New Claude projects load shared `AGENTS.md` policy through `CLAUDE.md`.
- Existing Claude project state is preserved.
- Init and upgrade remain approval-gated and recoverable.

## Phase 4 - Parity Verification And Documentation

Phase Status: **Tamamlandı**

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-400 | Replace hardcoded two-variant test loops where appropriate | **Tamamlandı** | Provider-neutral orchestration/install coverage includes all catalog variants. |
| CLD-401 | Keep Claude format assertions provider-specific | **Tamamlandı** | Markdown and TOML assertions remain separate. |
| CLD-402 | Add portable three-variant installation tests | **Tamamlandı** | All variants install into isolated temporary directories. |
| CLD-403 | Add launcher syntax, mode, and environment tests | **Tamamlandı** | Syntax, mode, config-dir, argv, exit, and missing-binary checks pass. |
| CLD-404 | Run the complete regression suite | **Tamamlandı** | Final full suite passed 88/88 after review hardening. |
| CLD-405 | Update user-facing runtime documentation | **Tamamlandı** | Four runtime guides describe Claude commands and excluded boundaries. |
| CLD-406 | Complete independent code review | **Tamamlandı** | Initial blockers were fixed with RED regressions; final re-review passed. |
| CLD-407 | Complete independent security review | **Tamamlandı** | Managed-parent symlink escape was fixed; final attack re-review passed. |
| CLD-408 | Record experiment decision and accepted changelog entry | **Tamamlandı** | `EXP-20260806-007` accepted and changelog updated after all checks passed. |

Phase exit criteria:

- Codex, Dolphin, and Claude portable contracts pass.
- Source and temporary-installed Claude artifacts match expected content.
- No active runtime, credential, commit, push, or deployment change occurred
  during phase verification.

## Phase 5 - Optional Claude Agent SDK Pilot

Phase Status: **Tamamlandı**
Approval Gate: Dependency and API contract approved; real API use remains gated

Proposed surface:

```text
adapters/claude-agent-sdk/
├── pyproject.toml
├── src/
│   ├── runner.py
│   ├── permissions.py
│   ├── sessions.py
│   └── result_mapper.py
└── tests/
```

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-500 | Obtain dependency and SDK API-contract approval | **Tamamlandı** | User explicitly requested continuation after the separate Gate B notice. |
| CLD-501 | Pin a supported Python SDK version | **Tamamlandı** | Exact `claude-agent-sdk==0.2.130`, Python `>=3.10,<4`, `uv.lock`, and frozen sync verified. |
| CLD-502 | Implement a bounded programmatic query adapter | **Tamamlandı** | Prompt, timeout, turn, budget, cancellation, cleanup, and no-retry contracts pass. Live SDK transport is default-denied. |
| CLD-503 | Map SDK results to truthful-success states | **Tamamlandı** | Only one terminal without any error signal passes; missing/duplicate/error results fail closed. |
| CLD-504 | Implement restrictive permission handling | **Tamamlandı** | Empty tools/settings/MCP, `dontAsk`, and defense-in-depth denylist verified. |
| CLD-505 | Add session resume and fork contracts | **Tamamlandı** | Canonical UUID, conflict, resume, and fork contracts pass without credentials. |
| CLD-506 | Track tokens, cost, and budget limits | **Tamamlandı** | Raw usage, normalized tokens, cost, API error, session, elapsed time, and configured ceilings remain observable. |
| CLD-507 | Obtain separate approval for an optional real API smoke test | **Bekliyor** | Non-blocking Gate C task; credential source, cost, prompt, and expected result require approval. |

Phase exit criteria:

- SDK adapter tests pass without exposing credentials.
- A real API call is optional and remains separately gated.
- Native Claude runtime remains usable without the SDK adapter.

Verification: 21/21 adapter tests, 92% adapter coverage, 88/88 root tests,
frozen lock/sync, compile and diff checks, code review, and security review
passed. The live SDK boundary returns `not_executed` until Gate C adds a
separately reviewed isolated executor.

## Phase 6 - Optional Production Hardening

Phase Status: **Bekliyor**
Approval Gate: Required only if the SDK will be hosted as a service

| ID | Task | Status | Verification / Notes |
|---|---|---|---|
| CLD-600 | Define the deployment threat model | **Bekliyor** | Identify tenants, untrusted inputs, data boundaries, and allowed tools. |
| CLD-601 | Add container or sandbox isolation | **Bekliyor** | Run non-root with resource, process, filesystem, and capability limits. |
| CLD-602 | Add secret-manager and credential-proxy integration | **Bekliyor** | Agent process must not receive reusable third-party credentials directly. |
| CLD-603 | Enforce outbound network policy | **Bekliyor** | Egress proxy, domain allowlist, and audit logs are verified. |
| CLD-604 | Isolate tenant configuration and workspaces | **Bekliyor** | Separate `cwd`, `CLAUDE_CONFIG_DIR`, memory, and filesystem access. |
| CLD-605 | Add durable session storage if required | **Bekliyor** | Resume survives host replacement without cross-tenant leakage. |
| CLD-606 | Add observability and resource budgets | **Bekliyor** | OpenTelemetry, subprocess health, token cost, and timeout alerts work. |
| CLD-607 | Complete production security and rollback review | **Bekliyor** | Production activation remains separately approved and reversible. |

## Approval Gates

| Gate | Required Decision | Status |
|---|---|---|
| GATE-A | Approve local Phase 0 through Phase 4 implementation | **Tamamlandı** |
| GATE-B | Approve Claude Agent SDK dependency and API contract | **Tamamlandı** |
| GATE-C | Approve credential use and real Claude API smoke test | **Bekliyor** |
| GATE-D | Approve active local/global Claude runtime activation | **Bekliyor** |
| GATE-E | Approve commit and push | **Tamamlandı** |
| GATE-F | Approve production deployment | **Bekliyor** |

## Definition Of Done

The native Claude integration is complete only when:

- Phase 0 through Phase 4 are **Tamamlandı**.
- All scoped RED tests were observed before implementation and later pass.
- Codex and Dolphin regression coverage remains green.
- Claude installs into a temporary runtime without touching active user state.
- Existing project Claude files are preserved during init and upgrade.
- Mandatory orchestration and truthful-success contracts remain intact.
- Code review and security review have no blocking findings.
- The experiment decision is supported by reviewed evidence.

The SDK and production phases are optional and do not block native Claude
runtime completion unless the user explicitly expands the objective.

## Rollback Contract

- Preserve the pre-change Git diff and unrelated dirty files.
- Use isolated temporary runtime homes for installation tests.
- Do not use `git reset --hard`, destructive cleanup, or force push.
- Archive only task-owned files before an approved migration.
- Restore a failed phase from its validated pre-change snapshot.
- After rollback, rerun the same scoped verification that detected the failure.
- Record the experiment decision as `ROLLBACK` when recovery is required.

## Decision Log

| Date | Decision | Result |
|---|---|---|
| 2026-08-06 | Save the Claude integration phases and tasks in one tracker | **Tamamlandı** |
| 2026-08-06 | Approve Phase 0 through Phase 4 implementation | **Tamamlandı** |
| 2026-08-06 | Approve four logical commits and one push to `main` | **Tamamlandı** |
