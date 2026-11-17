# CMA Records Module

## Load When

Load for changelog, evidence, Deferred Findings, experiments, archiving, task
closure after mutations, or explicitly requested record maintenance.

## Do Not Load When

Do not load for ordinary answer-only or read-only tasks with no record event.

## Rules

- Use the project `CHANGELOG_PATH` and `EVIDENCE_PATH`; never create a second
  changelog.
- Update the changelog after every completed mutation unless disabled locally.
- Record out-of-scope findings in `docs/DEFERRED_FINDINGS.md` without fixing
  them; keep Pending and Completed separate with timestamps.
- Activate `hypothesis-workflow` only for its defined triggers and record the
  experiment before the attempted solution.
- Use `record-archive` only on defined record events. Run `check` first and
  apply only when the threshold is reached and the task owns the changes.
- Archive complete records without loss, duplication, or summarization.
- Automatic evidence-report creation and automatic Evidence Validator use apply only when `EVIDENCE_MODE: enable`.
- Treat a missing field and `EVIDENCE_MODE: disable` as disabled.
- For any other explicit value, report invalid `EVIDENCE_MODE` and never enable evidence automation.
- An explicit user request to create or validate evidence remains applicable regardless of `EVIDENCE_MODE`.
- Keep evidence concise, reproducible, redacted, and tied to real commands,
  outputs, diffs, tests, and review findings.
- For every new or materially updated evidence report:
  - Include the exact heading `## Claims`.
  - Put exactly one bullet under it for each material claim.
  - Each bullet must state exactly one independently verifiable outcome.
  - Keep supporting proof outside the `## Claims` section.
  - Support each claim with one coherent verbatim proof excerpt outside the `## Claims` section that directly proves that outcome.
  - When splitting a compound claim, preserve every original acceptance outcome.
  - Do not replace an acceptance outcome with a weaker meta-claim that only says output or results were reported.
  - End the claims section at the next Markdown heading.
  - Apply this requirement prospectively; do not rewrite historical evidence reports solely to adopt it.
- When a new or materially updated evidence report records both an expected TDD RED result and a final verification result:
  - Include the exact heading `## Initial RED Evidence`.
  - Include the exact heading `## Final Verification Evidence`.
  - Treat Initial RED Evidence as historical pre-fix proof, not as the final status.
  - Support final-success claims only with proof from `## Final Verification Evidence`.
  - Require the same validation scope to be rerun after the fix and pass before reporting final success.
  - Use each temporal heading exactly once and keep Initial RED Evidence before Final Verification Evidence.
  - Treat temporal headings inside fenced or quoted evidence as proof text, not as report structure.
  - Do not require these temporal headings for one-phase or non-TDD evidence reports.
- Never auto-commit.
