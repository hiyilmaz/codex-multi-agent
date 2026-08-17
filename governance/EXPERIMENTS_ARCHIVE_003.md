# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260810-001 - Selective CMA-ARK Rollback

Date: 2026-08-10
Status: ROLLED_BACK

Problem:
The CMA-ARK work expanded a simple lazy-tool integration into a large inactive
adapter, hook, lifecycle, and host-evidence stack. The implementation adds
substantial maintenance and review cost while no CMA-ARK hook, skill, or managed
runtime path is active.

Evidence:
The ARK and CMA-ARK implementation surfaces are entirely untracked at the
current Git HEAD, while tracked changelog and experiment ledgers contain mixed
ARK and unrelated CMA changes. The approved assessment found roughly 7,500
lines in the CMA-ARK integration layer versus roughly 1,400 lines in ARK, with
115 adapter tests but no active integration surface.

Hypothesis:
A selective, recoverable rollback can return ARK to one planning-only proposal
without losing audit history or changing unrelated dirty CMA work. Moving the
implementation to a private checksum-bound external backup and applying exact
preimage transforms to mixed tracked files should be safer than a repository
reset or broad patch reversal.

Solution Attempt:
Create an external private rollback manifest and RED-first acceptance checker,
move only approved ARK/CMA-ARK implementation artifacts into its payload, remove
only the four ARK ignore rules, transition the thirteen historical ARK
experiment statuses to `ROLLED_BACK`, add one truthful changelog entry, and
retain exactly one non-executable planning proposal.

Test:
Require meaningful RED before mutation, exact source-to-backup hash and metadata
parity, planning-only repository surface, deterministic tracked-file postimages,
anti-hardcoded-success mutation probes, full remaining root regressions,
read-only record checks, diff integrity, and independent code and security
reviews.

Success Criteria:
- Every approved implementation artifact is absent from the repository and
  recoverable from a private verified external backup.
- Exactly one CMA-ARK planning proposal remains and grants no implementation,
  runtime, activation, tool-execution, commit, or push authority.
- All thirteen historical ARK experiment records occur once and have current
  status `ROLLED_BACK` without rewriting their historical evidence or decisions.
- All unrelated tracked and non-ignored untracked CMA state remains
  byte-identical; generated ignored files are outside this rollback claim.
- RED, GREEN, mutation probes, remaining regressions, record validation, and
  independent reviews pass.

Result:
The approved ARK and CMA-ARK implementation surfaces were moved to a private
checksum-bound recovery backup, leaving one non-executable planning proposal.
Meaningful RED, final acceptance, all nine mutation probes, 152 remaining root
regressions under Python 3.10, record checks, diff integrity, and independent
code and security reviews passed. An initial Python 3.9 run failed on existing
Python 3.10 union-type syntax and was not counted as success.

Decision:
ROLLBACK

Notes:
The user explicitly approved the selective rollback and mandatory orchestration
chain. Commit, push, backup deletion, global runtime changes, and any future ARK
implementation or activation remain outside scope.

## EXP-20260809-012 - Disposable CMA-ARK Host Evidence Wrapper

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-011 accepted a deterministic same-run evidence contract, but no
test-only wrapper or disposable host harness implements it. The accepted design
therefore cannot yet prove that real hook/candidate evidence and a paired Codex
JSONL lane are bound, non-compensating, private, and truthfully cleaned up.

Evidence:
The inactive hook candidate can already produce a real plan-only artifact, and
its focused tests prove zero routed-tool execution. The repository has no host
evidence wrapper or harness, canonical `UserPromptSubmit` activation remains
absent, and the accepted schema has not yet been exercised by a same-child
disposable boundary.

Hypothesis:
A fixed isolated wrapper plus a three-pair disposable host harness can implement
the accepted contract without widening runtime authority. Executing the real
candidate/coordinator path inside each fake-host child and independently
validating exact artifacts, JSONL, identity, hashes, cleanup, and final status
will reject missing, altered, dirty, or hardcoded evidence.

Solution Attempt:
Add separate bounded wrapper, contract-validation, and harness modules plus a
disposable fake Codex host fixture and RED-first tests. Keep the canonical hook,
candidate, coordinator, adapter, ARK, trust configuration, dependencies, and
routed-tool authority unchanged. If truthful missing-artifact failure cannot be
represented by the accepted schema, stop before implementation and request a
narrow contract correction instead of fabricating evidence.

Test:
Capture meaningful RED from absent wrapper/harness behavior. Then run focused
positive, negative, boundary, cleanup, same-child binding, hardcoded-success,
three-run stability, and branch-coverage checks followed by relevant hook,
adapter, ARK, root-governance, code-review, and security-review regressions.

Success Criteria:
- Every disposable pair invokes the real wrapper and real inactive candidate
  exactly once while executing no routed tool.
- Candidate and Codex lanes are independently required and bound to the same
  run, session/thread identity, fixed query, prompt, reviewed files, and hashes.
- Three fresh pairs pass without retry or replacement and share one normalized
  candidate hash.
- Private artifacts are exact, bounded, mode-safe, hashed before deletion, and
  absent after successful cleanup; cleanup failure cannot report success.
- Missing hook execution, dirty JSONL, identity/hash drift, timeout, stderr,
  nonzero exit, malformed input, or hardcoded success fails closed.
- Focused branch coverage is at least 80%, relevant regressions pass, and
  independent code and security reviews have no blocking findings.
- No canonical activation, trust action, real Codex session, global change,
  dependency, routed-tool execution, commit, or push occurs.

Result:
Planner and TDD review independently confirmed a blocking contract gap before
implementation began. When the hook does not run, the accepted
contract correctly leaves both pass-only candidate artifacts absent. A valid
assessment cannot then provide their required raw hashes or normalized candidate
hash, while `final_result` still requires `assessment_sha256`. Hashing a sentinel
or fabricating passing-shaped failure artifacts would violate the contract.
The minimum truthful correction retains the field but permits
`assessment_sha256=null` only in a failed or unverified final result when no
valid assessment could be constructed; a passing final still requires a
lowercase 64-character assessment hash. The user approved that correction; its
meaningful RED failed 1/9 on the old schema and the corrected design passed 9/9.

The wrapper/harness RED then failed because the three implementation modules
were absent. The first implementation slice passes 5/5 contract tests and 2/2
real wrapper-to-candidate tests. The disposable harness passes 5/6 tests, but
three clean real candidate runs produce different normalized hashes even though
their query hashes are identical. Source inspection confirms that
`plan_sha256` covers the coordinator-generated UUID request ID, so it is
intentionally different on every invocation. The accepted empty volatile-field
allowlist is therefore incompatible with the real candidate. Excluding
`plan_sha256` only from cross-run normalization, while retaining and validating
every raw per-run plan hash, is the narrowest feasible correction; changing the
real coordinator request identity would exceed this test-only scope. The user
approved that correction. The resulting focused suite reached 19/19 with 84%,
81%, and 84% branch coverage for wrapper, contract, and harness sources.

The approved containment correction gives the candidate one wrapper-owned
process group and makes the candidate, coordinator, adapter, and plan-only ARK
boundary inherit it. Timeout and semantic-failure paths now terminate the full
group and reap direct children. A checked-in reviewed manifest binds the exact
hook-definition bytes plus wrapper, candidate, coordinator, contract, and
schema hashes before contract import; ownership, permission, path, type, and
bytes-only drift checks fail closed.

Final verification passed 27/27 focused host-evidence tests with 84% combined
branch coverage (wrapper 89%, contract 81%, harness 84%), 115/115 adapter tests,
and the previously completed 55/55 relevant root contracts. Independent code
and security re-reviews returned PASS with no blocking findings. Canonical hook
activation, trust, real Codex sessions, global changes, dependencies, routed
tool execution, commit, and push did not occur.

Decision:
ACCEPTED

Notes:
This experiment owns only the test-only wrapper/harness implementation and its
focused tests and records. Real activation and three fresh Codex sessions remain
separate approval gates.

## EXP-20260809-011 - Deterministic CMA-ARK Host Evidence Contract

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-010 correctly rolled back canonical hook activation after the
first fresh Codex session omitted bound plan fields from its final response and
JSONL trace. Later diagnosis established that the acceptance gate conflated
hook `additionalContext`, which is model context, with deterministic final or
JSONL evidence.

Evidence:
The inactive hook candidate directly returns the exact target, query and plan
digests, `success=true`, and `execution_performed=false` in the documented
`UserPromptSubmit` envelope. Official OpenAI documentation defines that output
as extra developer context, defines `codex exec --json` as an emitted event
stream, and recommends `--output-schema` for stable final-response fields; it
does not define the model response as canonical hook evidence.

Hypothesis:
A same-run two-lane acceptance contract will provide deterministic evidence
without widening runtime authority: a test-only external wrapper will be the
actual hook command, validate the candidate/coordinator plan artifact, and bind
it to its paired ephemeral read-only Codex JSONL behavior. Neither lane may
rescue a failure in the other, and model output will remain non-authoritative.

Solution Attempt:
Define same-host identity binding, a machine-readable schema bundle for the
external evidence artifacts and final result, three-run stability, private
temporary lifecycle, independent gating, failure rules, and future TDD contract
in the CMA-ARK design. Keep production hook/coordinator code, canonical
activation, trust, App Server, dependencies, and routed-tool behavior unchanged.

Test:
Capture meaningful RED failures from new documentation-contract tests before
updating the design. Then run the focused design test, relevant adapter and root
regressions, `git diff --check`, independent code review, and security review.

Success Criteria:
- Canonical candidate evidence and Codex behavioral events are separate,
  independently required lanes bound to the same host run and reviewed hook.
- Four private temporary artifacts have exact schemas, hashes, normalization,
  cleanup, and fail-closed assessment rules.
- Three candidate runs and three Codex runs are required; no later run can
  replace a failed required run.
- Final model text and `--output-schema` output are presentation only and never
  authenticate plan identity, digest binding, or zero execution.
- App Server remains deferred and production hook/coordinator code, activation,
  trust, dependencies, and routed-tool authority remain unchanged.
- New tests fail against the pre-change design, then focused and relevant
  regressions pass with no blocking code or security review findings.

Result:
The documentation contract produced the required meaningful RED: the existing
two tests passed while all four initial evidence-contract tests failed on
absent design requirements. The first bounded design then passed 6/6 focused
tests after a whitespace-only harness correction for Markdown wrapping. Code
review exposed missing same-host identity binding, narrative-only artifact
schemas, and phrase-only test weakness. The remediated contract added a parsed
machine-readable schema test; code re-review passed. Security review then found
that contradictory success/lane/cleanup states remained schema-valid and that
embedding a fresh run ID in the candidate query made the three-run stability
rule unsatisfiable. The remediated contract uses conditional result variants, a
single post-comparison session/thread identity, and a fixed candidate query with
the run ID outside it. The current focused suite passes 8/8, alongside 6/6
plan-only hook candidate tests and 3/3 passive CMA-ARK contract tests. Direct
Draft 2020-12 validation accepts the coherent assessment and rejects both a
failed-lane passing assessment and failed-cleanup passing final result.
`git diff --check` also passes. Independent code and security re-reviews passed
with both security blockers closed. No wrapper, fresh Codex session, hook
activation, trust change, routed tool, dependency, commit, or push occurred.
Final governance regressions passed 11/11 orchestration, 7/7 hypothesis, and
19/19 record-archive tests. The terminal-record check reported every managed
record below its archive threshold, so no archive apply was required.

Decision:
ACCEPT

Notes:
This experiment is documentation and test-contract scope only. Wrapper
implementation and real three-session validation require a distinct approval.

## EXP-20260809-010 - Canonical CMA-ARK Hook Activation

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-009 proved a deterministic plan-only `UserPromptSubmit` transport
and a descriptor-anchored disposable lifecycle, but the canonical CMA repository
still has no active prompt hook. The existing pilot intentionally rejects the
canonical root, so the approved activation cannot be installed or rolled back
through the reviewed lifecycle.

Evidence:
The canonical `.codex/hooks.json` contains only empty `SessionStart` and `Stop`
events, `.codex/cma-ark-user-prompt.py` is absent, and the pilot accepts only
`install|rollback --target` against a marked disposable repository. Codex CLI
0.147.0 reports stable hook support. Official OpenAI documentation requires
review and trust of the exact non-managed hook definition through `/hooks` and
records trust against its current hash.

Hypothesis:
Fixed no-target `repo-install` and `repo-rollback` operations, built on the
existing descriptor-relative lifecycle and separated from the bounded CLI,
will permit exact canonical activation and recovery without reactivating the
failed repo skill or granting execution authority. A user-reviewed exact hook
definition should then produce deterministic fresh-session plans with
`execution_performed=false` and no routed tool execution.

Solution Attempt:
Split the lifecycle primitives into one adjacent private module, keep the pilot
as a thin isolated CLI/router, and add fixed canonical operations that derive
only their own repository root. Prove the lifecycle first in copied layouts,
then rehearse canonical install and rollback, reinstall exact bytes, use the
supported `/hooks` trust flow without bypass, and run three fresh plan-only
sessions.

Test:
Capture RED evidence for the absent repo operations. Verify copied-layout
install, idempotency, exact preservation, rollback, reinstall, path and content
drift refusal, atomic failure reporting, hostile environment isolation, and
anti-hardcoded-success behavior. Run focused branch coverage, adapter, ARK,
and root regressions before canonical rehearsal. Verify the exact live hook in
three fresh Codex sessions after trust.

Success Criteria:
- Repo operations derive one fixed canonical root and reject all caller targets.
- Disposable operations retain their marker and canonical-refusal behavior.
- Install and rollback mutate only the exact owned hook entry and script,
  preserve unrelated config, and truthfully report committed cleanup failures.
- The installed script is byte-identical to the reviewed candidate and mode
  `0600`; no skill activation, global skill, dependency, MCP/cplt, or Graphify
  execution is added.
- Exact trust uses the supported `/hooks` review only; no trust bypass, manual
  trust-state edit, or unrelated hook approval occurs.
- Three fresh sessions return usable matching CMA-ARK plans with
  `execution_performed=false`, no routed tool execution, retry, or fallback.
- Focused branch coverage is at least 80%, relevant regressions pass, and code
  plus security review have no blocking findings.

Result:
The missing canonical operations produced the expected initial RED: all three
copied-layout tests failed because the existing parser rejected `repo-install`
with exit 2. The bounded implementation then passed 23/23 focused tests with
80.70% combined CLI/lifecycle branch coverage, 83/83 adapter tests, 33/33 ARK
tests, and 166/166 root regressions. Code and security review both passed after
three false-state cleanup paths were found and closed. The real canonical
lifecycle installed, restored the original config SHA-256 exactly on rollback,
and reinstalled the byte-identical mode-`0600` hook with no lock/temp residue.
Exact trust was then granted only to the displayed project hook through
`/hooks`; no broad trust or bypass was used. The first fresh ephemeral
read-only Codex session exited 0 and returned a five-step generic `rg` plan with
no tool calls, but its JSONL trace omitted the required target/query/plan
digests, `success=true`, and literal `execution_performed=false` fields. It was
therefore not a usable bound CMA-ARK plan. The remaining two sessions were not
executed. The governed rollback removed the hook entry and script, restored the
original config SHA-256
`49ebbad6f600dbb37355f63e80bde9457a77023891a6bbca4157dee381abd071`,
and left no lock/temp or skill surface.

Decision:
ROLLBACK

Notes:
The hook lifecycle implementation remains as a tested inactive recovery tool,
but canonical activation is rejected by the fresh-host acceptance gate. The
Codex-owned exact-definition trust record is inert after config removal and was
not manually edited. Commit, push, deployment, global skill changes, routed
tool execution, and the remaining two fresh sessions did not occur.

## EXP-20260809-009 - Deterministic CMA-ARK Hook Transport

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The rolled-back repo-local skill activation depended on a model-generated
subprocess call carrying request JSON on stdin. Three fresh Codex sessions
discovered the skill, but none produced a usable host plan; the final attempt
omitted stdin and failed closed with `invalid_request`.

Evidence:
EXP-20260809-008 records the three failed host attempts and governed rollback.
The active Codex CLI reports stable hook support, and the official
`UserPromptSubmit` contract supplies the user prompt to a repo-local command
hook as JSON on stdin. The repository already contains one tracked private
`.codex/hooks.json` with no active prompt hook.

Hypothesis:
A repo-local `UserPromptSubmit` hook that recognizes only the existing literal
`$cma-ark <query>` grammar can translate the host event into the coordinator's
compact JSON request exactly once without placing the raw query in argv or new
persistent state. Descriptor-anchored install and rollback in a disposable
copy can bound config/script mutations without claiming protection from a
malicious process running as the same user.

Solution Attempt:
Build an inactive hook candidate and a separate disposable-only hook pilot.
The handler validates the exact host event, invokes the existing plan-only
coordinator through fixed literal argv and stdin, and emits only bounded
sanitized hook context. The pilot uses Python 3.9 `dir_fd`, `O_NOFOLLOW`,
relative atomic operations, and exact owned-content checks to add or remove one
hook entry and script in a disposable repository. It does not activate the
canonical repository.

Test:
Capture meaningful RED failures for missing hook transport and descriptor
operations. Then verify exact invocation grammar, input boundaries, one
coordinator delivery, query non-disclosure, hostile environment isolation,
protocol failure handling, config preservation, idempotency, drift refusal,
path-swap rejection, atomic cleanup, and anti-hardcoded-success behavior.

Success Criteria:
- Only an exact whole-prompt `$cma-ark <query>` event reaches the coordinator.
- The raw query appears only in the coordinator stdin inherited from the host
  prompt and never in argv, hook output, environment, or new files/state.
- A valid request invokes the coordinator once and returns plan-only evidence
  with `execution_performed=false`; invalid or contradictory evidence fails
  closed without fallback or retry.
- Disposable install and rollback preserve unrelated hooks, are idempotent,
  refuse drift/symlinks/path replacement, and truthfully report committed
  cleanup failures.
- Focused branch coverage is at least 80%, relevant regressions pass, and an
  always-success dummy fails the acceptance tests.
- No canonical hook trust/activation, skill activation, global config,
  dependency, MCP, cplt, Graphify, tool execution, commit, push, or deployment
  occurs.

Result:
The initial existence tests failed as expected because neither hook candidate
nor hook pilot existed. The completed handler accepted only the exact literal
invocation, delivered the compact coordinator request through stdin once,
rejected malformed and hardcoded-success responses, and returned digest-only
plan context. A real handler-to-coordinator-to-adapter-to-ARK black-box plan
returned `success=true`, `execution_performed=false`, and selected `rg` without
executing it. The disposable CLI installed and rolled back its exact hook entry
and script while restoring unrelated hook configuration.

Independent code review found and closed one swallowed combined
publish/cleanup failure; the final branch reports
`not_applied_cleanup_failed` when a residual staged script remains. Independent
security review found and closed compact-to-pretty JSON size expansion that
could strand an unreadable active config; encoded size is now rejected before
publication and staged state is removed. Final focused tests passed 18/18 with
85% combined branch coverage, the complete adapter suite passed 78/78, CMA-ARK
root contracts passed 5/5, ARK passed 33/33, and the broader root suite passed
166/166. Code and security re-reviews both returned PASS. The canonical hook
config, hook trust, repo/global skill discovery, dependencies, and execution
authority remained unchanged.

Decision:
ACCEPT. Retain the inactive hook candidate and descriptor-anchored disposable
pilot as the verified replacement transport design. Keep canonical hook trust
and activation as a distinct future task requiring explicit approval.

Notes:
Codex hook trust remains a separate user-controlled activation gate. This
experiment proved the candidate and disposable lifecycle only; it did not
silently trust or activate a repository hook.

## EXP-20260809-008 - Repo-Local CMA-ARK Plan Activation

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The reviewed CMA-ARK skill remains outside Codex discovery, so the repository
cannot use its explicit-only, plan-only routing boundary. The disposable pilot
correctly refuses the canonical repository and therefore cannot safely express
the separately approved real activation.

Evidence:
EXP-20260809-007 accepted the hardened launcher, identity binding, and atomic
disposable install/rollback pilot while reserving real repo-local activation
for a separate explicit approval. That approval is now present, and the real
`.agents/skills/cma-ark` path is absent.

Hypothesis:
Adding fixed `repo-install` and `repo-rollback` operations that derive the
canonical source root internally, while leaving disposable target validation
unchanged, will permit a bounded repo-local activation without adding global or
execution authority.

Solution Attempt:
Reuse the existing exact manifest, private state, exclusive operation lock,
atomic publication, identity-bound idempotency, drift-refusing rollback, and
truthful committed-failure reporting. The new operations accept no target
argument and can act only on the pilot's canonical repository root.

Test:
Capture copied-layout RED evidence for the missing operations, then verify
exact install, idempotency, rollback, drift refusal, pre-commit cleanup, and
target-argument rejection. After GREEN regressions, execute the approved real
install, verify plan-only zero-execution behavior, rehearse rollback, reinstall,
and leave only the repo-local explicit skill active.

Success Criteria:
- Disposable operations continue rejecting the canonical repository.
- Repo operations derive one fixed target and accept no `--target` input.
- The installed surface equals the reviewed three-file candidate byte-for-byte
  and retains `allow_implicit_invocation: false`.
- Installed-path planning returns `execution_performed=false` and never invokes
  routed `rg` or adapter `run` behavior.
- Rollback removes only unchanged installer-owned state and final reinstall is
  exact.
- No global skill, dependency, MCP/cplt, Graphify, commit, push, or deployment
  change occurs.

Result:
Copied-layout repo operations passed exact install, idempotency, rollback,
reinstall, drift refusal, target rejection, and pre-publication cleanup tests.
The real lifecycle installed, verified a direct `success=true` plan with
`execution_performed=false`, rolled back cleanly, and reinstalled exact files.
Three fresh Codex sessions discovered the repo skill and never executed routed
search, but none returned a usable plan: two failed under the macOS
`/usr/bin/python3` shim, and the revised pinned-interpreter attempt omitted the
required JSON stdin and returned fail-closed `invalid_request`. The governed
installer then removed the repo-local discovery surface and state.

Decision:
ROLLBACK. Remove the canonical repo operations and the unproven bootstrap
revision, preserve only the inactive EXP-20260809-007 candidate, and require a
separately approved deterministic host input and descriptor-safe installation
design before another activation attempt.

Notes:
Fresh Codex discovery loaded the repo-local skill, but both read-only and
workspace-write host sessions returned fail-closed `process_failed` because the
outer `/usr/bin/python3` developer-tool shim attempted a denied temporary cache
write. The attempt was revised to invoke the coordinator through its already
identity-pinned root-owned real interpreter binary; adapter and ARK child
boundaries remained unchanged. That revision also failed host validation and
was removed with the activation-only repo operations.

## EXP-20260809-007 - CMA-ARK Activation Identity Hardening

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The inactive CMA-ARK candidate can invoke a passive adapter launcher that
selects a user-owned Homebrew Python interpreter and resolves shell/runtime
commands through writable PATH segments. A forged or replaced child boundary
could therefore return a self-consistent plan before future repo activation.
The activation design also lacks an executable disposable install/rollback
pilot.

Evidence:
The final security review for EXP-20260809-006 accepted the inactive candidate
but retained adapter entrypoint/symlink identity, child interpreter, and
writable-PATH resolution as blocking gates for any `.agents/skills/cma-ark/`
activation. Live inspection confirmed the adapter prefers the user-owned
`/opt/homebrew/bin/python3` symlink from a group-writable directory.

Hypothesis:
Fixing both launchers to root-owned `/usr/bin/python3`, making the runtime
Python 3.9 compatible, independently binding and revalidating every child
identity, and proving manifest-owned install/rollback only in a disposable
repository will close the activation blockers without activating the skill or
adding dependencies.

Solution Attempt:
Use isolated literal launchers, a system-first fixed PATH, complete
launcher/source/interpreter/tool identity verification before and immediately
before spawn, and a repo-owned pilot that refuses the canonical CMA root and
publishes or removes only an exact three-file candidate manifest in a
disposable repository.

Test:
Capture RED failures for launcher selection, Python 3.9 compatibility,
identity drift and symlink substitution, missing disposable pilot, atomic
publication, idempotency, and drift-safe rollback. Then require real
black-box planning with zero tool execution, at least 80 percent branch
coverage, relevant adapter/ARK/CMA regressions, and independent code and
security review.

Success Criteria:
- Root-owned fixed interpreters and system-first command resolution replace
  ambient Homebrew/local launcher selection.
- Every adapter, ARK, interpreter, target, and selected-tool identity mismatch
  fails before adapter execution or before success reporting.
- Disposable install publishes exactly the candidate manifest and rollback
  removes only unchanged installer-owned files.
- The canonical CMA repository never gains `.agents/skills/cma-ark`.
- No global runtime, dependency, execution capability, commit, or push change
  occurs.

Result:
RED tests reproduced ambient Python import injection, writable activation
ancestors, concurrent installer-state races, file and directory identity drift,
and false `not_applied` results after committed install/rollback mutations. The
fixed implementation passed 58/58 adapter and disposable-pilot tests with 80%
pilot branch coverage and 91% combined branch coverage. ARK passed 33/33 tests,
the root ARK contracts passed 14/14, the candidate skill validator passed, and
independent code and security reviews ended with no blocking findings. The
canonical repository remained unactivated.

Decision:
ACCEPT. Keep the hardened launcher, runtime identity binding, and disposable
install/rollback pilot as inactive repository-owned infrastructure. Any real
`.agents/skills/cma-ark` activation remains a separate explicit approval and
validation task.

## EXP-20260809-006 - Inactive CMA-ARK Plan Skill Candidate

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The accepted CMA-ARK activation design has no reviewable Codex skill candidate.
Creating a discovered skill now would grant premature runtime authority, while
leaving only prose cannot prove explicit-only metadata, plan-only behavior, or
the fixed adapter boundary.

Evidence:
`EXP-20260809-005` accepted a non-discovered candidate as the next separately
approved task. Governor preflight found no duplicate CMA-ARK skill but corrected
the candidate layout so the directory and skill name both remain `cma-ark`.

Hypothesis:
A three-file candidate under
`adapters/cma-ark/skill-candidate/cma-ark/`, initialized with the official skill
creator and restricted to strict `text-search` planning, can provide a
reviewable workflow without activation or execution authority.

Solution Attempt:
Create only `SKILL.md`, explicit-only `agents/openai.yaml`, and a stdlib
plan coordinator. The coordinator accepts one bounded query object, verifies a
fixed isolated Python bootstrap, calls only the passive adapter's `plan`
operation for the canonical CMA root, validates the complete response, and
returns normalized zero-execution evidence.

Test:
Capture meaningful RED failures for the absent candidate, then verify exact
skill metadata, input bounds, bootstrap ordering, fixed process arguments,
correlated adapter protocol, forged-success rejection, real fixed-adapter
black-box planning, sentinel zero execution, at least 80 percent branch
coverage, and all relevant regressions.

Success Criteria:
- The candidate exists only in the non-discovered name-matched source path.
- Implicit invocation, `run`, approval/state, other intents, and tool execution
  remain unavailable.
- Invalid bootstrap, input, process, or adapter evidence fails closed before
  any wider action.
- The real black-box plan reports `execution_performed=false` while sentinel
  tools remain untouched.
- No activation, registry, audit, global, dependency, commit, or push change is
  made.

Result:
The candidate was initialized through the official skill creator and retained
exactly three non-discovered files. Meaningful RED tests first exposed the
missing candidate behavior, incomplete provenance type validation, post-hoc
subprocess buffering, an ineffective zero-tool sentinel, boolean/integer JSON
type confusion, and raw-query disclosure. The scoped fixes added exact
correlation types, bounded streaming, a disposable-repository sentinel that is
selected but never executed, and digest-only query reporting.

The final focused suite passed 11/11 with 89 percent branch coverage. The
complete adapter suite passed 40/40, ARK passed 33/33, scoped CMA governance
regressions passed, the official skill validator passed, and `git diff
--check` passed. Independent code and security re-reviews returned PASS. The
candidate remains absent from both repository discovery locations and made no
global, registry, dependency, commit, push, or deployment change.

Decision:
ACCEPT

Notes:
This acceptance covers only the inactive source candidate. Future
`.agents/skills/cma-ark/` activation remains blocked until the adapter
entrypoint and symlink identity, child interpreter, and writable-PATH command
resolution are pinned and independently verified. Activation requires a new
task and explicit approval.

## EXP-20260809-005 - Explicit CMA-ARK Activation Boundary

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The passive CMA-ARK adapter is implemented, but activation ownership, Codex
skill scope, authenticated approval, capability rollout, sensitive output,
Graphify coordination, and rollback are not yet defined as one executable
governance contract.

Evidence:
The adapter and integration documents explicitly leave activation pending. The
active user-global skill index has no CMA-ARK entry, no repository activation
surface exists, and the final Phase 3 security review retained these items as
activation gates.

Hypothesis:
A repo-local, non-discovered skill candidate with explicit-only invocation and
a plan-only, text-search-first pilot can define the narrowest activation
boundary without granting execution authority or creating a second router.

Solution Attempt:
Define the activation architecture, trust boundaries, staged capabilities,
future test contract, governor checks, and rollback order in documentation.
Do not create the candidate, activate a skill, change user-global state, or
implement the coordinator in this experiment.

Test:
Start with a failing documentation contract, then require the completed design
to encode explicit invocation, repo-only scope, outer identity binding,
single-use approval, output handling, Graphify serialization, rollback, and
out-of-scope boundaries. Run relevant CMA and ARK regressions plus independent
code and security review.

Success Criteria:
- The initial pilot is limited to explicit `text-search` against exactly the
  canonical CMA root.
- Implicit invocation, direct run, approval reuse, retry, fallback, and global
  promotion remain prohibited.
- `structure` and `explore` have separate evidence gates.
- Repo skill discovery remains plan-only until trusted host/user-role approval,
  isolated Python bootstrap, and atomic replay/rate controls are proven.
- The design does not create an active skill or mutate user-global state.
- Rollback and future activation tests are deterministic and fail closed.

Result:
The documentation contract first failed because the activation design was
absent. After the initial design passed 2/2 focused checks, code review found a
HIGH target-scope widening and later two installation containment/idempotency
findings. Security review found authenticated-approval, Python bootstrap,
atomic replay/rate, rollback ownership, and adversarial-output gaps. Each
affected contract was reopened with a meaningful failing assertion, narrowed,
and reverified. The final design limits repo activation to a plan-only,
canonical-root text-search pilot; execution remains fail-closed until trusted
host attestation and all named runtime gates are implemented. Final code and
security re-reviews returned PASS.

Decision:
ACCEPT

Notes:
This experiment defines architecture and future acceptance gates only. It does
not create the candidate, install a discovered skill, implement the
coordinator, authorize execution, or mutate user-global state.

## EXP-20260809-004 - Passive CMA-ARK Adapter Implementation

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The approved CMA-ARK process-boundary design is not executable. CMA has no
passive adapter that validates the v1 contract, binds an ARK plan to explicit
approval evidence, or normalizes ARK subprocess results without duplicating
routing.

Evidence:
`docs/CMA_ARK_ADAPTER_DESIGN.md` is accepted, while `adapters/cma-ark/` does not
exist. The integration plan therefore still reports implementation pending.

Hypothesis:
A standard-library-only, one-request-per-process adapter using the fixed
repository-owned `ARK/bin/ark` boundary can enforce the approved request,
binding, approval, protocol, and exit contracts while leaving ARK as the sole
router and remaining inactive by default.

Solution Attempt:
Add the passive adapter and RED-first unit, subprocess-integration, and
black-box tests under `adapters/cma-ark/`. Do not modify functional ARK sources,
activate a skill or registry entry, add dependencies, or implement the excluded
CMA Graphify coordinator.

Test:
Capture meaningful RED failures before production files exist. Then verify
exact request framing, fixed paths, plan/run binding, drift rejection, ARK
protocol and exit normalization, bounded subprocess behavior, passive state,
at least 80 percent adapter branch coverage, the unchanged ARK manifest, ARK
tests, and relevant CMA governance regressions.

Success Criteria:
- Only the three approved read-only intents can reach ARK.
- Planning performs no tool execution; denied runs perform no ARK run; an
  approved unchanged plan executes exactly once.
- Request, response, provenance, digest, status, and exit contracts fail closed.
- Fixed launcher, config, source, target, tool, and graph identities are bound
  and revalidated without request-controlled execution settings.
- The adapter remains passive and stateless; activation and caller-side
  Graphify serialization remain explicitly pending.
- Adapter branch coverage is at least 80 percent and all scoped regressions pass.

Result:
The initial RED suite failed because the adapter package and launcher were
absent. The completed stdlib adapter then passed 29 focused unit, subprocess,
protocol, drift, and real fixed-ARK black-box tests with 82.81 percent branch
coverage. The root passive contract passed 3/3, the unchanged ARK manifest
passed 9/9, ARK passed 33/33, and orchestration, hypothesis, and record
regressions passed 11/11, 7/7, and 19/19. Review fixes added symlink-free fixed
resource revalidation, a bounded ARK JSON envelope large enough for both
maximum tool streams, truthful unsupported-version status, and selected-tool
PATH re-resolution before run. Final code and security reviews returned PASS.

Decision:
ACCEPT

Notes:
Approval JSON is propagated evidence, not authentication. The documented
post-check/pre-exec race and direct-response repository-output exposure remain
residual activation risks rather than claims solved by this implementation.
Activation still requires authenticated approval and target authorization,
interpreter identity binding, sensitive-response handling, replay/rate control,
tested Graphify serialization, and acceptance of the documented final
check-to-exec race. Graphify runtime behavior remains unverified because its
executable is unavailable on the adapter's fixed PATH in this environment.
