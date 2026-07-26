# Improvement Experiments

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
