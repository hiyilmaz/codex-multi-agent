# Evidence: EXP-20260804-002 Temporal TDD Evidence Contract

Date: 2026-08-04 22:58 +03

## Claims

- CMA conditionally separates expected RED evidence from final verification without adding an Acceptance Criteria schema
- The managed and portable CMA records modules passed their temporal contract tests
- The active global CMA records module was backed up and synchronized after separate approval

## Initial RED Evidence

The first focused CMA run completed 14 tests with two failures because the
records module did not contain the conditional temporal policy. Security review
later identified missing uniqueness, ordering, and fenced-proof boundaries;
each new contract marker failed before its corresponding policy update.

These failures were expected pre-fix observations. They describe the missing
contract and do not represent the final test state.

## Final Verification Evidence

CMA conditionally separates expected RED evidence from final verification
without adding an Acceptance Criteria schema: the records module requires the
two exact temporal headings only for reports containing both phases. It
requires one ordered structural pair, treats fenced or quoted heading text as
proof, and restricts final-success claims to Final Verification proof. It does
not add an Acceptance Criteria heading, ID system, or mapping table.

The managed and portable CMA records modules passed their temporal contract
tests: the focused command completed 14 tests with `OK`, including a
byte-identical portable installation. The complete CMA command completed 52
tests with `OK`. Reopened code review and security review both passed.

The active global CMA records module was backed up and synchronized after
separate approval: the previous active file is preserved at
`/Users/iyilmaz/.codex/archive/cma-temporal-evidence-20260804_230500/CMA_RECORDS.md`
with SHA-256
`a381775d5e803d610a34b0b443a063baf029d9e3e4584703221cd353c4860028`.
The managed source and `/Users/iyilmaz/.codex/registry/modules/CMA_RECORDS.md`
are byte-identical with SHA-256
`c3d4813491a493775db57f24b451e13c5b9168c5a15445113d1f33a72e9299ea`;
the active mode remains `0644`.

No deployment was performed.
