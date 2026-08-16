# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260804-001 - CMA Evidence Claims Contract

Date: 2026-08-04
Status: ACCEPTED

Problem:
CMA evidence reports do not require an explicit claims section, while EV
requires `## Claims` or explicit `Claim:` declarations before it invokes GLM.
Consequently, valid CMA evidence can stop as `UNVERIFIED` before validation.

Evidence:
The active CMA records module requires concise, reproducible proof but defines
no claim syntax. Existing reports commonly use headings such as `Outcome`,
`Implemented`, `Test Evidence`, and `Fresh Evidence`, which EV intentionally
does not interpret as material claim declarations.

Hypothesis:
Requiring one material claim per bullet under an exact `## Claims` heading for
new or materially updated CMA evidence will make future reports EV-compatible
without weakening EV or rewriting historical reports.

Solution Attempt:
Add a prospective claim-format contract to the CMA records module, enforce it
in source and portable-install tests, and add EV integration fixtures that use
the unchanged production parser. After the first real pilot showed GLM quoting
claim declarations instead of supporting proof, strengthen only EV's validation
prompt to require proof outside `## Claims` that directly supports the same
claim; keep the parser and fail-closed checks unchanged.

Test:
Run a meaningful CMA RED test before changing the module, then run focused and
full CMA suites plus focused and full EV suites. Verify portable installation,
unchanged EV runtime code, dirty-worktree isolation, and independent code and
security reviews.

Success Criteria:
- CMA requires the exact `## Claims` heading for new evidence reports.
- Each material claim is one bullet and supporting proof stays outside the
  claims section.
- Historical reports are not rewritten solely for compatibility.
- A representative CMA report passes EV parsing with complete grounded claims.
- Missing coverage and prompt injection remain `UNVERIFIED`.
- No EV parser, schema, hook, dependency, or activation behavior changes; the
  prompt may only be strengthened to align GLM output with existing grounding.
- Active global CMA runtime remains unchanged pending separate approval.

Result:
The CMA contract test first failed in the source and portable installation at
the missing `## Claims` requirement. After implementation, the focused CMA
suite passed 12/12 and the full CMA suite passed 49/49. EV compatibility tests
passed against the production parser, including complete coverage, omitted
claims, and prompt injection.

The first real GLM pilot reached ACP but returned `UNVERIFIED` because GLM cited
claim declarations instead of proof. The revised prompt-only attempt retained
all parser checks and explicitly required proof outside `## Claims` supporting
the same claim. The repeated end-to-end temporary pilot then returned `PASS`.
The final EV suite passed 34/34. Independent code and security reviews both
returned PASS with no blocking findings.

Decision:
ACCEPT

Notes:
Option A was explicitly approved. Commit, push, real-project activation, and
active global runtime synchronization are outside this implementation step.
The first real pilot reached GLM but returned `UNVERIFIED` because two GLM
responses cited claim declarations as proof. A diagnostic response demonstrated
that the same document can produce valid proof excerpts, supporting a prompt-
alignment revision without weakening validation.
The source candidate was accepted before runtime activation. After explicit
option A approval, only the active records module was backed up and synchronized.
Its final SHA-256 matches the source candidate and its mode remains `0644`.

## EXP-20260804-002 - Temporal TDD Evidence Contract

Date: 2026-08-04
Status: ACCEPTED

Problem:
CMA requires explicit claims and grounded proof, but a TDD evidence report can
mix an expected pre-fix RED result with final verification. That structure is
technically truthful yet can make the final state temporally ambiguous.

Evidence:
The current records module does not distinguish initial RED proof from final
verification proof or state which section may support a final-success claim.

Hypothesis:
A conditional two-section rule for reports that contain both expected RED and
final outcomes will remove temporal ambiguity without adding Acceptance
Criteria IDs, mapping tables, or mandatory headings to one-phase reports.

Solution Attempt:
Require exact `## Initial RED Evidence` and `## Final Verification Evidence`
headings only when both phases are documented. Require final-success claims to
use final-section proof from the same validation scope rerun after the fix, and
identify initial RED as historical pre-fix evidence. Apply the rule
prospectively without rewriting historical reports.

Test:
Add source and portable-install contract tests before changing the records
module. Verify the conditional headings, final-proof restriction, unchanged
Claims contract, and absence of Acceptance Criteria schema expansion.

Success Criteria:
- Two-phase TDD evidence has explicit initial and final sections.
- Final-success claims depend only on final verification proof.
- Final success requires the same validation scope to pass after the fix.
- Initial RED is identified as expected historical evidence, not final status.
- One-phase and non-TDD reports do not require temporal headings.
- No Acceptance Criteria IDs or mapping tables are introduced.
- Active global CMA runtime remains unchanged pending separate approval.

Result:
The focused RED run failed two contract tests because the records module lacked
the conditional temporal rule. After the minimal policy change, the focused
suite passed 14/14 and the full CMA suite passed 52/52. Portable installation
was byte-identical to the managed records module. The source candidate was
accepted before active global synchronization.

Security review found that ordering and uniqueness were not part of the CMA
contract, allowing reversed or duplicate temporal headings to misrepresent the
final state. A new RED contract test failed until the module required each
heading exactly once with Initial RED before Final Verification. The focused
14/14 and full 52/52 suites passed again.

Reopened security review found that temporal headings embedded in fenced proof
could still be mistaken for report structure. The CMA contract RED failed until
it explicitly classified fenced or quoted headings as proof text. The focused
14/14 and full 52/52 suites passed again. Reopened code and security reviews
both passed with no blocking findings.

A final scoped RED failed the source and portable contract paths because the
policy did not explicitly require the same validation scope to be rerun after
the fix. One additional rule closed that gap; the focused 14/14 and full 52/52
suites passed again.

Decision:
ACCEPT

Notes:
Implementation, tests, and independent reviews passed.
Approved option A covers local implementation, tests, evidence, and review.
Active global runtime synchronization was initially outside that scope. After
separate explicit approval, the prior active module was copied to
`~/.codex/archive/cma-temporal-evidence-20260804_230500/CMA_RECORDS.md` and the
then-validated source was synchronized. At that time, source and active SHA-256 were both
`c3d4813491a493775db57f24b451e13c5b9168c5a15445113d1f33a72e9299ea`;
the active mode remains `0644`. The later same-scope hardening changed only the
managed source and tests; active runtime synchronization was not repeated.
Detailed evidence is recorded in
`docs/reports/EVIDENCE_EXP-20260804-002_TEMPORAL_TDD_EVIDENCE_CONTRACT_20260804.md`.
