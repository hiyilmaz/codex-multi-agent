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
- Keep evidence concise, reproducible, redacted, and tied to real commands,
  outputs, diffs, tests, and review findings.
- For every new or materially updated evidence report:
  - Include the exact heading `## Claims`.
  - Put exactly one bullet under it for each material claim.
  - Keep supporting proof outside the `## Claims` section.
  - End the claims section at the next Markdown heading.
  - Apply this requirement prospectively; do not rewrite historical evidence reports solely to adopt it.
- Never auto-commit.
