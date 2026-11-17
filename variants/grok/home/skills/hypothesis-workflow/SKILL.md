---
name: hypothesis-workflow
description: Use a traceable Problem to Hypothesis to Solution Attempt to Test to Result to Decision cycle only after a meaningful improvement has a failed attempt, unclear evidence, competing hypotheses, a regression or unwanted side effect, a need for measured comparison, a core runtime/model/agent governance change, or when the user explicitly requests an experiment. Do not use for routine first-pass work, typos, formatting, or a clear deterministic fix with sufficient verification.
---

# Conditional Hypothesis Workflow

Use this workflow as an escalation mechanism, not as the default task flow.
Preserve all active scope, approval, security, destructive-operation, retry,
orchestration, changelog, and evidence rules.

## Activation Gate

Activate when at least one condition is supported by concrete evidence:

- a meaningful solution attempt failed
- the result or evidence is unclear
- competing hypotheses need comparison
- a regression or unwanted side effect occurred
- a measured comparison is needed
- a core runtime, model, agent, skill, or orchestration-governance default will
  change
- the user explicitly requests an experiment or hypothesis cycle

Do not activate for:

- routine first-pass work
- a typo or formatting-only change
- a clear deterministic fix with sufficient verification
- predictable documentation or configuration maintenance
- a known procedure that succeeds without conflicting evidence

If no activation condition is met, continue the normal project workflow. Do not
create `governance/`, `governance/EXPERIMENTS.md`, or an experiment ID.

## Before An Attempt

1. Read `governance/EXPERIMENTS.md` when it exists.
2. Compare the proposed attempt with prior records using problem, hypothesis,
   solution mechanism, and evidence. Do not treat keyword similarity alone as
   proof that two attempts are the same.
3. If an equivalent attempt was accepted, do not reimplement it.
4. If an equivalent attempt failed, require a concrete new reason, changed
   condition, or new evidence before repeating it.
5. If the prior result needs more data, collect that data or revise the
   hypothesis.
6. Choose the next ID for the current local date:
   `EXP-YYYYMMDD-XXX`.
7. Create the experiment record before changing the proposed solution.

## Run The Cycle

Use one main solution variable at a time when practical:

```text
Problem -> Hypothesis -> Solution Attempt -> Test -> Result -> Decision
```

Keep the attempt no larger than required to test the hypothesis. Record scope
changes as a revision instead of silently expanding the experiment.

## Record Format

Append experiments to `governance/EXPERIMENTS.md`:

```text
## EXP-YYYYMMDD-XXX - Short Title

Date:
Status: PROPOSED | TESTING | ACCEPTED | REJECTED | REVISED | NEED_MORE_DATA | ROLLED_BACK

Problem:
What problem is being solved?

Evidence:
What indicates this is a real problem?

Hypothesis:
What change is expected to improve the result, and why?

Solution Attempt:
What one main change will be made?

Test:
How will observable behavior be checked?

Success Criteria:
What evidence will show that the solution worked?

Result:
What happened after testing?

Decision:
ACCEPT | REJECT | REVISE | NEED_MORE_DATA | ROLLBACK

Notes:
Important observations, side effects, or follow-up items.
```

`Status` describes lifecycle state. `Decision` records the conclusion. During
active testing, use `Status: TESTING` and `Decision: NEED_MORE_DATA`.

## Test Integrity

Define success criteria before implementation. Tests and observations must
demonstrate requested observable behavior and must fail against an absent or
dummy implementation.

Never:

- replace behavior with hardcoded success
- weaken assertions to obtain a pass
- skip or disable relevant tests
- add test-only production branches
- swallow errors and report success
- mock the target behavior instead of external dependencies

For code changes, use the active `tdd-workflow` and preserve independent review
of acceptance criteria, the implementation diff, negative paths, and side
effects. A passing test alone is not an `ACCEPT` decision.

## Decision Rules

- `ACCEPT`: success criteria are met with no unacceptable side effects.
- `REJECT`: the hypothesis is unsupported, ineffective, too risky, or
  unnecessarily complex.
- `REVISE`: the approach is partly useful but requires a changed hypothesis or
  solution attempt.
- `NEED_MORE_DATA`: evidence or testing is insufficient.
- `ROLLBACK`: regressions, instability, data risk, or unacceptable side effects
  require restoration of the prior safe state.

Do not mark an experiment accepted before verification. If rollback is needed,
follow active destructive-operation approval rules and document the observable
recovery result.

## Existing Project Records

- Keep detailed commands, outputs, diffs, and test logs under the project
  `EVIDENCE_PATH`.
- Add only accepted improvements to the existing project `CHANGELOG_PATH`, and
  include the experiment ID.
- Do not create `governance/CHANGELOG.md`; it would duplicate the authoritative
  project changelog.
- Do not add rejected, untested, or rolled-back attempts as completed
  improvements.

If the user explicitly authorizes a commit, preserve Conventional Commit format:

```text
type(scope): EXP-YYYYMMDD-XXX description
```

Never include unrelated changes in that commit.

## Report And Stop

Report the problem, hypothesis, attempt, test result, decision, updated records,
and next action concisely. Stop when the experiment has a supported decision or
when user input, new authority, or more data is required.
