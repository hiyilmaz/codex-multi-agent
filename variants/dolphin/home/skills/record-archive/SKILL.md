---
name: record-archive
description: Check and compact growing project governance records without losing history. Use only when a Deferred Finding becomes Completed, an experiment becomes terminal, a new changelog date heading is created, or the user explicitly requests record archiving. Supports docs/DEFERRED_FINDINGS.md, governance/EXPERIMENTS.md, and docs/CHANGELOG.md with deterministic retention, validation, dry-run checks, and atomic writes. Do not invoke for unrelated task closures.
---

# Record Archive

Use this skill only at a supported record event. Do not run at every task
closure and do not add a cron job, daemon, or Git hook.

## Event Gate

Run a check only when:

- a finding becomes `Completed`
- an experiment becomes terminal: `ACCEPTED`, `REJECTED`, or `ROLLED_BACK`
- a new changelog date heading is created
- the user explicitly requests an archive check or compaction

Do not run for a new pending finding, an open experiment update, another entry
under an existing changelog date, or an unrelated task.

## Command

Use the bundled script from this skill directory:

```text
python3 scripts/record_archive.py check --root /path/to/project --record all
python3 scripts/record_archive.py apply --root /path/to/project --record TYPE
```

`TYPE` is `deferred-findings`, `experiments`, `changelog`, or `all`.

Always run `check` first. It is read-only. Run `apply` only when the result is
`ACTION_REQUIRED`. When Git reports a managed file as dirty, `apply` refuses by
default. Use `--allow-dirty` only after confirming that the current task owns
the exact managed-file changes and that the diff contains no unrelated edits.

## Retention

- Deferred Findings: evaluate after a completion event; at 10 Completed
  records, retain the first 5 Completed records plus every Pending record in
  the active file and move older Completed records to the archive.
- Experiments: evaluate after a terminal transition; at 10 terminal records,
  retain the 5 newest terminal records plus every open record in the active
  file and move older terminal records to the archive. Open statuses are
  `PROPOSED`, `TESTING`, `REVISED`, and `NEED_MORE_DATA`.
- Changelog: evaluate only after a new date heading. Rotate when the active
  file has at least 30 detailed date sections or at least 500 lines and more
  than 20 detailed dates. Retain 20 full dates, show links for the next 30
  archived dates, and keep all older full content in the archive.

Treat a date section as one unit. Never split entries from the same date.

## Safety Contract

The script must:

- reject malformed formats, duplicate IDs or dates, wrong-section records, and
  unsupported changelog headings
- preserve existing document order for Deferred Findings ties
- preserve every Pending finding and open experiment in the active file
- write the active and archive files as one rollback-capable transaction
- add direct links between active and archive files
- remain idempotent after successful compaction
- never report success after a validation or write failure

If a format is unsupported, report `UNSUPPORTED_FORMAT` and do not edit either
file. Do not weaken validation or manually delete records to make the command
pass.

## Closure

After `apply`, run `check` again and inspect the diff. Confirm unique IDs or
dates, correct sections, retained counts, direct links, and unchanged record
content. Record accepted project changes in the authoritative project
changelog; do not create a second changelog.
