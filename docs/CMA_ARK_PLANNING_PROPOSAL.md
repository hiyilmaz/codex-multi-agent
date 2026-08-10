# CMA Repository Tool Router Plan

Status: PROPOSED — planning only
Decision: Option A approved — policy-only lazy routing

## Problem And Intended Value

CMA needs a small way to select the narrowest sufficient repository tool
without adding another runtime. ARK remains only historical context; the
approved direction is a compact policy module that routes existing tools.

## Approved Minimal Shape

A future implementation is limited to these repository source changes:

1. Add `variants/codex/home/registry/modules/CMA_REPO_TOOLS.md`.
2. Add one lazy-router row to `variants/codex/home/AGENTS.md`.
3. Record the completed mutation in the existing changelog.

The module will contain only this decision table:

| Need | Tool |
|---|---|
| Exact text or path | `rg` |
| Architecture or cross-file dependency | Graphify |
| Structural AST pattern | `ast-grep` |
| Symbol references or refactor radius | Serena, explicit and lazy |
| Dependency vulnerability | OSV-Scanner |
| SAST or secret scan | Opengrep or Betterleaks, security-triggered |
| GitHub source, release, or advisory | GitHub MCP, gated read-only |
| Public-repo or versioned-doc fallback | DeepWiki or Context7, explicit |

Mandatory routing rules:

- Use the narrowest sufficient tool.
- Do not query multiple discovery tools for the same question.
- Stop discovery when sufficient evidence exists.
- Keep MCP providers and scanners outside the default task path.
- Report unavailable tools; never silently widen the route.

## Fast Execution Plan

1. Read-only: verify which listed tools are available; install nothing.
2. RED: prove the Codex variant has no repository-tool module or router row.
3. Add only the module and router row listed above.
4. Validate the reference, Markdown structure, existing CMA tests, and diff.
5. Stop. Active `~/.codex` synchronization requires separate approval.

## Acceptance Criteria

- No executable, dependency, adapter, hook, skill, daemon, or state directory.
- No default MCP connection, scanner run, graph build, or network request.
- Normal tasks remain unchanged unless a listed trigger applies.
- Repository implementation changes stay within two CMA source files; the
  changelog is the only additional record mutation.
- Codex-only repository scope; other variants remain unchanged unless separately
  approved.

## Explicit Non-Goals

- No ARK repository or CLI.
- No adapter, hook, installer, evidence wrapper, sandbox, or second runtime.
- No automatic tool installation, MCP ownership, or credential handling.
- No active global Codex change, commit, push, deployment, or activation.

## Questions Requiring Validation

- Which tools are currently available without installation?
- Do direct routing rules cover real tasks without a wrapper?
- Does measured use justify adding any future tool or transport?

## Future Approval Gates

1. Implement the two repository source changes and focused validation.
2. Synchronize the verified module to active `~/.codex`.
3. Install or configure any unavailable tool.

Failure at one gate grants no authority for the next. A CLI may be reconsidered
only after measured failures show that policy-only routing is insufficient.

## Historical Rollback Scope

The prior implementation remains rolled back under `EXP-20260808-004` and
`EXP-20260809-001`, `EXP-20260809-002`, `EXP-20260809-003`,
`EXP-20260809-004`, `EXP-20260809-005`, `EXP-20260809-006`,
`EXP-20260809-007`, `EXP-20260809-008`, `EXP-20260809-009`,
`EXP-20260809-010`, `EXP-20260809-011`, and `EXP-20260809-012`.

Former source and tests remain recoverable from the private checksum-bound external recovery backup. The backup is inert and is not an installation source.

## Authority Boundary

This plan grants no runtime or tool-execution authority. It does not approve
implementation, installation, active synchronization, commit, or push.
