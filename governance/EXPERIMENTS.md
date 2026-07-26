# Improvement Experiments

## EXP-20260727-002 - Event-Driven Record Archiving

Date: 2026-07-27
Status: ACCEPTED

Problem:
Deferred findings, experiments, and changelog files grow without bound, but
checking or compacting them at every task closure would add recurring latency
and cost.

Evidence:
The accepted design review found that record files need bounded active context
without losing history. It also found that a five-date changelog window is too
small, while keeping fifty full date sections would likely exceed the runtime's
file-size guidance.

Hypothesis:
An event-driven `record-archive` skill with deterministic thresholds, dry-run
checks, atomic fail-closed writes, and format-specific retention rules will
bound active context without adding work to unrelated task closures.

Solution Attempt:
Add one reusable skill and script for Deferred Findings, experiments, and
changelog records. Trigger checks only when a finding becomes completed, an
experiment becomes terminal, or a new changelog date is created. Keep five
recent completed findings, five recent terminal experiments, and twenty full
changelog dates plus a thirty-date archive index.

Test:
Run contract tests against temporary repositories for below-threshold no-ops,
threshold rotation, preservation, duplicate and malformed-input rejection,
dirty-file protection, idempotence, portable installation, and runtime policy
activation.

Success Criteria:
- No event-independent or every-task archive check is introduced.
- Deferred Findings and experiments rotate at ten eligible records and retain
  five eligible records in the active file.
- Changelog rotation starts at thirty detailed dates or five hundred lines,
  retains twenty detailed dates, and exposes up to thirty archive links.
- Pending findings and non-terminal experiments always remain active.
- No record is lost, duplicated, or moved to the wrong section.
- `check` is non-mutating; `apply` is atomic, fail-closed, and idempotent.
- Codex, Dolphin, and the active local runtime expose the same validated skill.

Result:
The initial RED run failed on all thirteen missing behavior and packaging
surfaces. After implementation and two real-format compatibility revisions,
the focused suite passed 16 tests and the full project suite passed 35 tests.
Measured statement coverage for the bundled script is 87%. Codex, Dolphin, and
the active local skill passed `quick_validate.py`, compiled successfully, and
were checksum-equivalent. A read-only check against `yedekparcasor.com`
reported Deferred Findings and Changelog below threshold and Experiments ready
for rotation without changing that project. Dirty files, malformed formats,
duplicates, unsupported headings, and broken symlinks failed closed.

Decision:
ACCEPT

Notes:
This experiment changes only record-retention automation. It does not alter the
mandatory orchestration chain, agent reasoning defaults, or task approval
rules.

## EXP-20260727-001 - Conditional Hypothesis Workflow

Date: 2026-07-27
Status: ACCEPTED

Problem:
The runtime has evidence, retry, TDD, and review controls, but it does not yet
provide the conditional experiment workflow tracked by ORCH-005. Making the
workflow mandatory for every task would add duplicate records and latency.

Evidence:
`docs/ORCHESTRATION_IMPROVEMENT_TASKS.md` keeps ORCH-005 pending and limits
experiment escalation to failed attempts, unclear evidence, competing
hypotheses, regressions, or measured comparisons.

Hypothesis:
A concise global trigger combined with a reusable `hypothesis-workflow` skill
will add traceable experiments only when difficulty or uncertainty justifies
the extra process, without changing routine task flow or the mandatory agent
chain.

Solution Attempt:
Package the conditional skill for Codex and Dolphin, register it globally,
link it from runtime policy, preserve existing evidence and changelog paths,
and explicitly prohibit proactive experiment-file creation for routine work.

Test:
Run focused contract tests, the complete unit suite, skill validation, and
temporary Codex and Dolphin installations. Verify the active local Codex
runtime after synchronization.

Success Criteria:
- Routine first-pass work does not activate the experiment workflow.
- Defined escalation triggers activate prior-record review and a dated ID.
- Project `AGENTS.md` does not need to declare the skill.
- Existing `CHANGELOG_PATH` and `EVIDENCE_PATH` remain authoritative.
- The mandatory agent chain and `medium` reasoning defaults remain unchanged.
- Codex and Dolphin temporary installs contain the validated skill.
- Tests reject unconditional activation and missing test-integrity guardrails.

Result:
The corrected RED run failed on all missing behavior surfaces: skill files,
global policy, registry links, and portable installation. After implementation,
the focused suite passed 7 tests and the full suite passed 19 tests. Both
packaged skills and the active global skill passed `quick_validate.py`. Codex
and Dolphin temporary installs contained identical skill contracts.
`~/.codex/AGENTS.md`, the active skill, and active registry policy were
checksum-equivalent to their source templates after targeted synchronization.
The existing active audit history remained intact.

Decision:
ACCEPT

Notes:
This experiment changes one main behavior: conditional activation of a
traceable hypothesis cycle. It does not alter approval, scope, destructive
operation, retry, orchestration, or security boundaries. The prior active
policy and registry files are recoverable from
`~/.codex/archive/hypothesis-workflow-20260727_004001/`.
