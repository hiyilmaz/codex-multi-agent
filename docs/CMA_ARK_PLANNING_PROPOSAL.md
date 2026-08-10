# CMA-ARK Planning Proposal

Status: PROPOSED — planning only

## Problem And Intended Value

CMA needs a small, optional way to select the narrowest sufficient repository
tool without lengthening the normal task path. ARK is retained only as a concept
for lazy CLI routing of existing tools. No implementation is approved.

## Explicit Non-Goals

- No adapter, hook, skill, installer, evidence wrapper, daemon, or second runtime.
- No automatic tool installation, MCP ownership, credential handling, or sandbox.
- No global Codex changes and no repo-local activation or discovery surface.
- No implementation, dependency addition, commit, push, or deployment.

## Questions Requiring Validation

- Can direct `rg`, Graphify, and `ast-grep` usage cover the normal discovery path
  without a custom router?
- Is a small explicit CLI materially better than a documented decision table?
- Which security scanners are already available and useful on real projects?
- Can optional MCP providers remain entirely outside the default CMA context?
- What measurable maintenance or token reduction would justify implementation?

## Future Approval Gates

Each stage requires a separate plan and explicit approval:

1. Read-only tool availability and overlap assessment.
2. Minimal architecture decision: documentation-only router or explicit CLI.
3. Any implementation and its focused tests.
4. Any adapter boundary.
5. Any hook or skill candidate.
6. Any host-evidence mechanism.
7. Any activation, global runtime change, or deployment.

Failure at one stage does not authorize a wider replacement. The default
recommendation is documentation-only routing until measured evidence proves a
small CLI is necessary.

## Historical Rollback Scope

The following implementation experiments remain in the audit ledgers with
current status `ROLLED_BACK`:

- `EXP-20260808-004`
- `EXP-20260809-001`
- `EXP-20260809-002`
- `EXP-20260809-003`
- `EXP-20260809-004`
- `EXP-20260809-005`
- `EXP-20260809-006`
- `EXP-20260809-007`
- `EXP-20260809-008`
- `EXP-20260809-009`
- `EXP-20260809-010`
- `EXP-20260809-011`
- `EXP-20260809-012`

Their former source, tests, and generated artifacts are recoverable from a
private checksum-bound external recovery backup. That backup is inert and is
not an installation source without a separate restore approval and validation.

## Authority Boundary

This proposal grants no runtime or tool-execution authority. It is not an
implementation plan approval, activation record, trust decision, or permission
to modify global or project runtime configuration.
