# Evidence: EV Stop Hook Decision-Wait Debug

Date: 2026-08-04 03:56 +03
Scope: Read-only diagnosis of the CMA and EV control flow. No hook, validator,
runtime, or project activation behavior was changed.

## Claims

- Codex invokes the generic Stop event at a turn boundary, and Stop has no matcher that distinguishes task completion from waiting for a user decision
- The recorded incident turn ended with a structured CMA decision request and the literal text Awaiting decision
- The current EV Stop hook does not inspect the last assistant message before starting evidence discovery and validation
- A non-PASS EV result on the first Stop asks Codex to continue, while a repeated Stop terminates with manual intervention
- Existing EV coverage tests repeated-failure loop protection but does not test a CMA decision-wait turn
- The incident is caused by a missing decision-wait or completion-intent gate in EV rather than by the CMA approval requirement itself

## Problem

The command was:

```text
Evidence Validator uyarilarini/hatalarini duzelt.
```

CMA correctly classified the requested bugfix as non-trivial work in
`ask-approval` mode. Codex therefore returned a `CRITICAL DECISION` block and
stopped the turn with:

```text
Recommendation: A ...
Awaiting decision.
```

The project-level EV `Stop` hook was then eligible to run even though Codex was
waiting for the user's authorization rather than reporting task completion.

## Hypothesis

EV treats every root `Stop` event as a completion attempt. Because it does not
classify the turn's intent, it can validate or block an approval request just as
it would a completion response.

## Inspection And Proof

### Official Stop contract

The locally refreshed official Codex manual states:

- `matcher` is not currently used for `Stop`.
- Stop input includes `stop_hook_active` and `last_assistant_message`.
- `decision: "block"` tells Codex to continue and creates a new continuation
  prompt using the hook reason as a new user prompt.
- `continue: false` takes precedence over continuation decisions.

Source inspected:
`/var/folders/pk/_pp6g16d2bn8txcjf79z9cx00000gn/T/openai-docs-cache/codex-manual.md`,
lines 21805-21837.

This means hook configuration alone cannot filter completion turns. Any such
filter must be implemented inside the hook or through an explicit task-state
contract.

### Recorded incident flow

Session:

```text
/Users/iyilmaz/.codex/sessions/2026/08/04/
rollout-2026-08-04T02-26-10-019fc9f2-f4db-79b3-ba57-a78873069454.jsonl
```

Relevant records:

```text
line 717  user command: Evidence Validator uyarilarini/hatalarini duzelt.
line 720  Codex announces orchestration-gate inspection without mutation.
line 730  final assistant response: Decision: ask-approval ... Awaiting decision.
line 731  the same response is stored as the assistant final message.
```

The session proves that the assistant was waiting for a user decision. The
user-observed Stop/EV activation is consistent with the documented generic Stop
lifecycle and the current hook implementation.

### Current EV Stop hook

Inspected file:

```text
/Users/iyilmaz/WebStorm/evidence-validator/hooks/stop.mjs
```

Observed control flow:

```text
line 15      skips only subagent-like inputs carrying agent_id or agent_type
line 16      resolves the project and discovers changed evidence immediately
lines 17-21 blocks on operationally unverified discovery
lines 23-28 validates candidates and blocks the first non-PASS result
lines 10-12 first failure -> decision:block; repeated failure -> continue:false
```

The hook never reads `last_assistant_message`. It therefore has no branch for a
CMA decision block ending in `Awaiting decision.` and cannot distinguish that
state from a completion attempt.

### Existing test boundary

`/Users/iyilmaz/WebStorm/evidence-validator/tests/validator.test.mjs`, lines
280-300, verifies that a repeated Stop failure returns `continue: false` and
requires manual intervention. No test references `last_assistant_message`,
`Awaiting decision`, or a decision-wait bypass.

No live GLM validation was run for this diagnosis. Static source inspection,
the recorded session, and the official Stop contract were sufficient to locate
the control-flow defect.

## Result

Status: `failed`

The current integration incorrectly conflates these two states:

```text
assistant waits for user authorization -> Stop -> EV runs
assistant reports task completion       -> Stop -> EV runs
```

Only the second state is an EV completion-gate target. The first state must
remain an ordinary user approval boundary.

Loop protection is present but does not solve the trigger problem. The first
EV failure can inject a continuation prompt; the repeated path can stop with
manual intervention. Both outcomes interfere with the intended decision wait.

## Decision And Recommended Fix Scope

The CMA approval rule should remain unchanged. EV should self-filter the
structured CMA waiting state before evidence discovery or GLM invocation.

Minimum safe behavior to implement in a separate approved bugfix:

1. Inspect `last_assistant_message` before calling `changedCandidates`.
2. Recognize a complete CMA `CRITICAL DECISION` response that ends with the
   exact `Awaiting decision.` marker.
3. Return `{}` for that waiting state so control returns to the user.
4. Keep current fail-closed behavior for actual completion attempts.
5. Add tests proving that decision waits skip EV, while completion and repeated
   failure paths retain their current enforcement.

A broad natural-language classifier is not recommended. The existing exact CMA
decision marker provides a narrower and testable contract. Clarification waits
outside that structured contract should be evaluated separately rather than
silently exempted.

## Non-Actions

- No EV source or test file was changed.
- No CMA policy or orchestration mode was changed.
- No project EV activation state was changed.
- No GLM request was sent.
- No commit, push, or deployment was performed.
