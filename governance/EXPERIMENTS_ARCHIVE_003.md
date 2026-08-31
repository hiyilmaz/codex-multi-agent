# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260810-008 - Planner-to-TDD Structured Evidence Envelope v0

Date: 2026-08-10
Status: REJECTED

Problem:
The planner and tdd-guide contracts require bounded handoffs and discourage
repeated broad discovery, but they have no structured, identity-bound way for
the TDD guide to consume a planner source fact. The same current repository
fact can therefore be independently rediscovered between the two stages.

Evidence:
This experiment will first replay the real EXP-20260804-002 temporal-TDD
bugfix against the immutable pre-fix Git tree
`2f0f84e768504eddc6895cf27899ab46c64808de` at commit
`ff6592e171b3fb6827141f44aa5b45bad960797f`. Candidate mutation is forbidden
unless the unchanged planner and TDD contracts produce a complete behavioral
RED trace containing at least one non-verification duplicate canonical fact.

Hypothesis:
When planner supplies current, source-identity-bound discovery evidence in a
minimal Envelope v0, tdd-guide will consume that evidence and avoid repeating
the same discovery operation unless it identifies an explicit unresolved gap,
while producing an equal-or-stronger test contract.

Solution Attempt:
If and only if behavioral RED passes, define Envelope v0 in the portable Codex
orchestration registry, require the default planner to emit it, require the
default tdd-guide to validate and consume it, and add fail-closed contract tests.
Limit production/test scope to
`variants/codex/home/registry/ORCHESTRATION.md`,
`variants/codex/home/agents/planner.toml`,
`variants/codex/home/agents/tdd-guide.toml`, and
`tests/test_cma_lazy_runtime.py`. Do not synchronize active runtime files or
add storage, helpers, runtimes, tools, scanners, MCPs, or graph behavior.

Test:
Run fresh sequential planner and tdd-guide baseline sessions on a read-only
complete repository fixture using the approved natural prompt. Normalize exact
and evidence-equivalent discovery by canonical fact key, path, query/range, and
source identity. If meaningful RED passes, add static negative contract tests,
capture their failure, make the minimum candidate change, rerun static tests,
replay the identical live task, compare AC-TEMP-1 through AC-TEMP-7, run focused
and full regressions, then complete code and security review.

Success Criteria:
- Baseline planner-to-TDD duplicate discovery count is at least one and the TDD
  contract completes normally without source invalidation.
- Static candidate tests fail before implementation and reject plausible
  weakened, stale, conflicting, unresolved-gap, schema, and chain contracts.
- Candidate duplicate discovery count is zero; current sufficient evidence IDs
  are consumed and every new discovery is tied to a named unresolved gap.
- Envelope top-level fields are limited to the eight approved v0 fields and its
  measured transport cost does not exceed the duplicate evidence it replaces.
- AC-TEMP-1 through AC-TEMP-7 and positive, negative, boundary, regression,
  meaningful-RED, anti-hardcoding, and no-weakened-oracle protections remain.
- Focused and full tests, code review, and security review pass; active runtime,
  config, mandatory chain, and unrelated work remain unchanged.

Result:
Behavioral RED passed on the locked 325-node fixture with manifest
`7dd6c6e5817d6a5eccc740e63c79bb28d87a302784bc6987c71c4306fa3671b2`.
Planner completed with six tool calls and TDD completed with four; TDD
re-read the records contract, TDD module, installer, and existing test seams
already identified by planner, giving a conservative duplicate count of four.
The first focused invocation was a transport-only import error; the corrected
unchanged four-test command then produced meaningful static RED because the
orchestration registry lacked Envelope v0. After the minimum four-file
candidate, five focused contract/chain tests passed.

Live candidate planner emitted a parseable eight-field envelope, but expanded
the historical two-file task to six unrelated policy/test/changelog paths.
Candidate TDD reported consuming `E1` through `E4` and claimed no additional
discovery, while its complete JSONL trace contained one compound command that
re-hashed and re-ran `rg` against all four supplied evidence paths. Excluding
the hashes as identity checks still leaves four evidence-equivalent discovery
repetitions, so the required candidate duplicate count of zero was not met.
The candidate TDD contract also omitted the AC-TEMP-2 exact-once/ordering
obligation and the AC-TEMP-4 fenced/quoted-heading boundary.

Code review returned three HIGH blocking findings: failed primary behavioral
gate, empty/untyped source and evidence identity, and weakened-contract tests
that accepted duplicate/quoted headings and appended contradictory prose.
Security review confirmed fail-open evidence laundering, bypassable presence
tests, false provenance in `consumed_evidence_ids`, and an unverified path/
symlink containment exposure. No correction was attempted because the approved
stop conditions require rejection without a second solution attempt.

All four candidate production/test files were restored byte-for-byte with
their original `0644` modes. Post-rollback focused tests passed 26/26 and the
full suite passed 157/157. Active runtime files were not synchronized.

Decision:
REJECT

Notes:
The hypothesis is unsupported by this v0 policy-only envelope: the observed
duplicate was not removed, the audit claim contradicted the trace, and the
minimal schema/tests did not safely bind trusted evidence. The changelog is
unchanged because the candidate was rejected. Exact preimages, runtime hashes,
fixture, traces, and temporary validation artifacts were task-owned under a
private `0700` root and were removed after rollback verification. No later
optimization phase is authorized by this experiment.

## EXP-20260810-007 - Direct Local Lookup Fast Path

Date: 2026-08-10
Status: REJECTED

Problem:
The main Graphify/router task has four rejected independent attempts. Natural
exact lookups still activate the broad repository-tools router and Graphify,
while a prescriptive command prompt can mask that routing behavior.

Evidence:
EXP-20260810-005 reproduced a module read and Graphify false positive with a
natural lookup prompt. EXP-20260810-006 was rejected before publication because
its command-prescriptive baseline already passed and could not distinguish the
candidate. This is the fifth and final permitted attempt.

Hypothesis:
An explicit pre-router fast path directing exact repository text, filename, and
path lookups to local `rg`, combined with an advanced-only router row and a
positive-only Graphify description, will make natural simple lookups lightweight
without breaking advanced routing or explicit Graphify behavior.

Solution Attempt:
Add one literal fast-path rule before the lazy-router table; narrow its
repository-tools row in the template, portable Codex policy, and active global
policy; change only Graphify frontmatter description. Preserve module and skill
bodies. No sixth attempt is permitted.

Test:
Require static RED and a completed natural live behavioral RED before publishing
production changes. Then run focused static GREEN and six fresh sequential
trace-validated probes: exact text, filename, known file, generic content,
literal help, and a real two-file architecture graph. Finish with regressions,
parity, independent reviews, permission hardening, and exact cleanup.

Success Criteria:
- Baseline natural exact lookup returns the correct match and shows a module or
  Graphify false-positive; otherwise publish nothing and reject.
- GREEN exact and filename probes use only contained successful `rg` commands,
  return exact results, and show no module or Graphify activity.
- Known/generic probes use only bounded contained `rg`/`sed` readers and show no
  module or Graphify activity.
- Help returns the captured Usage block byte-for-byte with zero task commands.
- Architecture loads the exact module and skill, executes real Graphify on two
  Python sources, and creates a fresh source-verified `EXTRACTED` calls edge
  without semantic, subagent, network, or fabricated evidence.
- Literal fast path precedes the router; advanced triggers remain; all three
  policies are byte-identical; module/body/config/other variants retain preimages.
- Focused/full tests, reviews, permissions, and task-owned cleanup pass. Any
  completed violation rejects and rolls back without retry.

Result:
Both required RED gates passed. The natural baseline returned the correct exact
match but first read the complete Graphify skill and repository-tools module and
announced Graphify routing. After publishing the candidate, the focused 26-test
suite passed; fresh exact-text and filename probes used only contained `rg`, and
the known-file probe used one bounded `sed`, all with correct outputs and no
module or Graphify activity. The generic-content probe returned the correct
value but executed two composed shell commands containing `rg`, `sed`, `ls`, and
`wc`, violating the immutable bounded-reader and no-shell-composition criteria.
No retry was permitted after completed task activity. Remaining help and
architecture probes were not run. All candidate policy, metadata, and test
changes were restored to their verified preimages.

Decision:
REJECT

Notes:
One retry is allowed only for an incomplete zero-activity transport failure.
Authorized scope excludes installs, module-body/config-schema changes, network,
MCP/scanners, repository-root graph construction, commit, push, deployment, and
archive mutation. Acceptance criteria will not be weakened.
This was failed independent attempt 5 of 5. Per the user-defined ceiling, no
sixth attempt or further candidate change will be started.
Independent code review passed the rejection, trace evidence, and exact rollback.
Security review confirmed no changed trust-boundary residue or task-created graph
artifact and identified four subagent session logs for `0600` hardening before
removing only the verified task-owned temporary root.
The terminal archive check returned `ACTION_REQUIRED` (`active=5`, `archive=41`,
`moved=7`); no archive mutation was applied because it is outside this task.

## EXP-20260810-006 - Repository Router Trigger Boundary

Date: 2026-08-10
Status: REJECTED

Problem:
The main Graphify trigger-narrowing task remains incomplete after three
independent attempts. EXP-20260810-005 proved that a narrow Graphify description
prevents the false-positive skill load, but the broad repository-tools router
still reads `CMA_REPO_TOOLS.md` before an exact lookup and violates the strict
`rg`-only contract.

Evidence:
The first EXP-20260810-005 GREEN exact-text trace completed a `sed` read of the
repository-tools module before its successful `rg` command. The active,
portable, and template policies all use a router trigger beginning with
`Repository text/path`, so exact lookups necessarily activate that module.

Hypothesis:
Removing exact text/path and generic repository-content vocabulary from the
router trigger, while publishing a positive-only Graphify description, will
keep simple lookups on their prescribed local readers and preserve explicit
Graphify plus architecture and advanced repository-tool routing.

Solution Attempt:
Replace the single repository-tools router row in the template, portable Codex
policy, and active global policy; change only Graphify's frontmatter description.
Keep the repository-tools module body, config, other variants, and Graphify body
unchanged. This is independent solution attempt 4 of at most 5.

Test:
Capture static and fresh live exact-lookup RED evidence before publication.
Then run fresh sequential exact-text, filename, known-file, generic-content,
literal help, and two-file architecture probes. Validate raw JSONL lifecycle,
exact commands and bounded paths, positive Graphify execution provenance, a
source-verified EXTRACTED calls edge, parity, regressions, reviews, and cleanup.

Success Criteria:
- Exact text and filename probes each run exactly the prescribed successful
  `rg` command, with no policy/module or Graphify activity.
- Known-file and generic-content probes run only their prescribed bounded local
  reader, with no policy/module or Graphify activity or out-of-corpus access.
- Literal `/graphify --help` returns the captured Usage block byte-for-byte and
  runs no task command.
- The architecture probe reads the repository-tools module and Graphify skill,
  executes the real local Graphify build on exactly two Python files, and
  produces a source-verified `EXTRACTED` `calls` edge from
  `consumer.render_label` to `provider.canonical_label`, without semantic,
  subagent, network, or fabricated evidence.
- The narrowed row retains architecture, structural AST, symbol, dependency,
  security, and public-source triggers; template, portable, and active policies
  are byte-identical.
- The repository-tools module, config/trust state, Graphify body, other variants,
  and unrelated work retain their preimages; focused/full tests, independent
  reviews, permissions, and exact task-owned cleanup pass.
- A retry is allowed only after an incomplete lifecycle with zero observable
  task activity. Any completed violation rejects this attempt without retry.

Result:
The static contract produced meaningful RED because neither the narrow router
row nor the positive-only Graphify description was present. However, the
required fresh live pre-change exact-text probe already passed the immutable
oracle: it executed exactly the prescribed `rg` command, returned the exact
normalized line, and showed no repository-tools module or Graphify activity.
The prescriptive prompt therefore bypassed the behavior this attempt intended
to distinguish. No policy or Graphify production change was published, and the
test-only contract edit was restored.

Decision:
REJECT

Notes:
The user authorized autonomous continuation through at most five independent
attempts. This attempt authorizes the bounded active policy and metadata changes
plus exact rollback, but not dependency installation, module-body/config-schema
changes, network/MCP/scanner use, repository-root graph construction, commit,
push, deployment, or archive mutation. Acceptance criteria will not be weakened.
This is failed independent attempt 4 of 5. The final attempt must use a
non-prescriptive natural lookup prompt whose baseline reproduces the unwanted
activation, while retaining strict trace-based command and provenance checks.
Independent code review passed the rejection and rollback evidence. Security
review confirmed all policy, skill, module, test, config, and trust preimages;
four task-created subagent session logs were identified for `0600` hardening
before exact temporary-root cleanup.

## EXP-20260810-005 - Graphify Activation Boundary

Date: 2026-08-10
Status: REJECTED

Problem:
Graphify's broad frontmatter description still activates for simple repository
content work, while EXP-20260810-004 could not be accepted because it coupled
the activation boundary to an over-broad `rg`-only command-purity criterion.

Evidence:
EXP-20260810-003 observed a full Graphify skill load before an exact lookup.
EXP-20260810-004 showed that a narrower description prevents Graphify false
positives, but also showed that mandatory policy bootstrap and bounded known-file
reading can legitimately use `sed` without making Graphify the selected tool.

Hypothesis:
A Graphify description limited to architecture, cross-file, data-flow,
call-path, coupling, relationship, and explicit `/graphify` requests will remove
simple-task false positives while preserving real help and architecture flows.

Solution Attempt:
Change only the active Graphify frontmatter description. Keep its body, global
policy, repository-tools module, config schema, and portable CMA assets
unchanged.

Test:
Capture same-scope static and live exact-lookup RED evidence, then validate six
fresh sequential sessions: exact text, filename, one known file, generic project
content, literal `/graphify --help`, and a two-file code-only architecture
fixture. Validate raw JSONL lifecycle, commands, outputs, graph edges, source
behavior, permissions, config/trust parity, and cleanup.

Success Criteria:
- Exact text and filename probes use successful `rg` and show no Graphify load,
  invocation, announcement, or artifact.
- Known-file and generic-content probes use only bounded `rg`/`sed` readers and
  show no Graphify activity.
- Literal help returns the current Usage block byte-for-byte with zero task
  commands.
- The architecture probe uses exactly two Python files, performs no semantic
  extraction or subagent work, and produces a source-verified EXTRACTED `calls`
  edge from `consumer.render_label` to `provider.canonical_label`.
- At most one transport-only retry is allowed only after a zero-activity
  incomplete lifecycle; retries after task activity are forbidden.
- Global policy, repository-tools module, config, trust entries, Graphify body,
  source fixtures, and unrelated dirty work remain byte-identical; tests,
  independent reviews, permissions, and exact task-owned cleanup pass.

Result:
The static pre-change assertion and fresh exact-text probe both produced
meaningful RED evidence. After publishing the candidate description, the first
fresh exact-text probe returned the correct normalized match and did not load
Graphify, but its trace first read `CMA_REPO_TOOLS.md` with `sed` before running
`rg`. This violated the immutable exact-lookup requirement that every task
command be `rg`. Because the attempt contained completed task commands and a
final answer, the transport-only retry rule prohibited a retry. The active
Graphify skill was restored byte-for-byte from its verified preimage.

Decision:
REJECT

Notes:
Approval includes exact incidental trust-entry cleanup, session/log permission
hardening, and deletion of only the validated task-owned temporary root. It does
not include dependency installation, policy/router/config-schema edits, graph
building in the CMA repository root, commit, push, or deployment.
The failure is outside the permitted Graphify-description-only scope: the
repository-tool policy bootstrap itself caused the extra reader. The remaining
five GREEN probes were not run after this fail-closed rejection.
Independent code review also found that the disposable validator's unexecuted
architecture branch could accept a fabricated graph without positive Graphify
provenance, and that its known-file/generic path checks did not reject every
absolute out-of-corpus read. These gaps reinforce rejection; no result from
those branches was used as acceptance evidence.
The focused lazy-runtime suite passed 26 tests and the full suite passed 157
tests after rollback. Security review confirmed active skill/config parity and
safe containment; four task-created subagent session logs were hardened from
`0644` to `0600`, then the verified task-owned temporary root was deleted and
its absence confirmed. The terminal record archive check returned
`ACTION_REQUIRED`; no archive mutation was applied because it would exceed this
experiment's approved scope.

## EXP-20260810-004 - Narrow Graphify Skill Activation

Date: 2026-08-10
Status: REJECTED

Problem:
Graphify's broad skill description activates for exact repository text and path
lookups that the repository-tool router assigns to `rg`, adding unnecessary
skill loading and commands.

Evidence:
EXP-20260810-003 rejected the routing pilot after a fresh exact-text task loaded
the complete Graphify skill through four shell commands before running `rg`.

Hypothesis:
Replacing only the active Graphify frontmatter description with explicit
architecture and relationship triggers plus explicit `rg` exclusions will keep
exact lookups on `rg` while preserving literal `/graphify` and architecture
activation.

Solution Attempt:
Change only the active Graphify skill description. Keep the skill body, active
repository-tool router, global policy, configuration, and portable CMA assets
unchanged.

Test:
Capture a pre-change static and fresh-session RED, then run static metadata
checks and bounded sequential fresh-session probes for exact lookup, filename
lookup, single-file reading, generic project content, `/graphify --help`, and a
cross-file dependency question. Validate the JSONL traces rather than trusting
final prose.

Success Criteria:
- Four simple repository-content probes use only `rg` and never load or invoke
  Graphify.
- `/graphify --help` returns the unchanged Usage section without task commands.
- A cross-file dependency prompt produces real Graphify activation evidence.
- The Graphify body, router, global policy, configuration, and unrelated dirty
  work remain byte-identical.
- Focused CMA lazy-router regression tests and diff checks pass.

Result:
The metadata assertion changed from RED to GREEN without altering the Graphify
skill body. Fresh exact-text, filename, and generic project-content runs no
longer activated Graphify; literal help and cross-file dependency runs still
activated it. However, the defined success criteria were not met: the exact
run loaded the repository-tools module with `sed` before `rg`, the generic
README run used `sed`, and the single-known-file run stalled after lifecycle
start and was terminated without retry. The architecture probe also added one
temporary trust entry for its disposable corpus; that exact entry was removed
and the active config hash returned to its pre-test value. The active Graphify
description and changelog entry were rolled back after code review.

Decision:
REJECT

Notes:
No installation, graph build in this repository, MCP connection, config change,
commit, push, or deployment is authorized by this experiment.
The global policy, repository-tools module, config, and Graphify skill returned
to their pre-attempt hashes. Code review identified unmet acceptance criteria as
a HIGH blocker. A narrower acceptance contract or a broader router-policy change
would be a separate approved task.

## EXP-20260810-003 - Repository Router Usage Measurement

Date: 2026-08-10
Status: REJECTED

Problem:
The active policy-only router has not been observed in a fresh Codex task, so
its routing behavior, latency, and token use remain unverified.

Evidence:
EXP-20260810-002 verified activation but explicitly deferred tool use and cost
evaluation. A strict router-disabled baseline would require prohibited policy
or authentication changes.

Hypothesis:
One exact-text lookup will select only `rg`, while one simple control will use
no tools; two ephemeral JSONL runs can measure their elapsed time and tokens
without changing repository or active runtime state.

Solution Attempt:
Run exactly two sequential `codex exec --ephemeral --json` tasks in a read-only
sandbox: one fixed exact-text lookup and one fixed no-tool control.

Test:
Validate synthetic failure fixtures before live execution, then require exact
JSONL lifecycle and usage events, an allowlisted successful `rg` command for
the routed task, zero tools for the control, distinct thread IDs, and pre/post
state parity.

Success Criteria:
- Both original runs exit zero with exactly one valid usage event.
- The routed run uses only the narrowest approved local command and returns the
  exact expected path.
- The control returns the exact sentinel with zero tool events.
- Repository, active policy/config, and session inventories remain unchanged.
- Results report observed time and tokens without claiming causal speedup or
  actual account billing.

Result:
The synthetic validator produced meaningful RED before implementation and then
passed 7/7 fixtures. The first and only live routed run exited at the Codex
transport level with one valid usage event, but the pilot failed closed before
the control run. Instead of selecting only `rg`, the fresh session announced
Graphify, read all 699 lines of the Graphify skill using four shell commands,
then ran an `rg` pipeline and emitted two agent messages. Observed usage was
163,172 input tokens, including 132,864 cached input tokens, plus 839 output
tokens and 294 reasoning output tokens. The exact path result was correct, but
the route violated the narrowest-tool and minimal-command criteria. The control
run was not executed and no retry occurred. Active policy/module parity and
repository status were checked afterward; the only repository change is this
experiment record. Exact monotonic latency and full pre/post inventory parity
are unverified because validation stopped before the runner persisted them.

Decision:
REJECT

Notes:
No retry, installation, MCP connection, scan, graph build, policy change,
commit, or push occurred. The ephemeral thread identifier is absent from the
persisted session tree. The failure indicates a routing conflict: the broad
Graphify skill trigger overrides the compact exact-text route and adds material
context cost. Independent code and security reviews returned PASS. The exact
task-owned private harness and raw JSONL directory was removed after review.
Any correction is a separate task and approval gate.

## EXP-20260810-002 - Active Repository Tool Router Pilot

Date: 2026-08-10
Status: ACCEPTED

Problem:
The approved repository-tool router exists only in the managed Codex source.
The active local `~/.codex` runtime cannot be evaluated until its policy and
module are synchronized, but activation must preserve the current runtime and
provide a verified rollback point.

Evidence:
The active policy differs from the approved template by exactly the missing
router row, and the active `CMA_REPO_TOOLS.md` module is absent. The active
runtime contains 7.8 GB of recoverable files plus one live IPC socket. A live
copy cannot be an atomic point-in-time snapshot, and macOS `ditto` intentionally
excludes sockets and pipes.

Hypothesis:
A private, verified backup of all recoverable active runtime state followed by
preimage-bound atomic publication of only the module and router row will enable
a reversible usage pilot without widening runtime authority.

Solution Attempt:
Create a unique external `0700` backup with source-before, payload, and
source-after manifests, explicitly classify volatile and excluded special
entries, validate stable parity, and write the completion marker last. Direct
`ditto` was rejected after a socket error/FIFO hang; `rsync` and `bsdtar`
attempts were then rejected for macOS metadata drift. The final method builds a
simplified BOM containing only recoverable paths and applies BOM-filtered
`ditto`, preventing special-file access while preserving required metadata.
Then publish the module and policy atomically, with the policy as the activation
point and fixture-proven rollback on partial failure.

Test:
Capture active RED drift, run disposable backup/corruption/unique-name and
partial-sync rollback fixtures, validate the real backup and active source
parity, run focused and full CMA tests, and complete independent code and
security reviews.

Success Criteria:
- The experiment record predates the first backup attempt.
- A private external backup contains every recoverable stable entry with
  verified content and metadata parity.
- Live sockets, pipes, and changing files are truthfully classified rather than
  reported as stable backup parity.
- Active policy and module match their approved repository sources exactly.
- No unrelated active surface, tool installation, tool execution, fresh-session
  claim, commit, or push occurs.
- Rollback fixtures, focused/full tests, and independent reviews pass.

Result:
The approved planner and TDD stages completed. Active RED was captured. The
first disposable backup fixture rejected direct `ditto`; subsequent real
`rsync` and `bsdtar` staging attempts were rejected for xattr/creation-metadata
drift and preserved without completion markers. A BOM-filtered `ditto` fixture
preserved content, symlink target, mode, xattr, and ACL while excluding
socket/FIFO objects; corruption and destination collision were also rejected.
The atomic sync fixture passed wrong-preimage, symlink, both partial-publication
rollback, target-drift rejection, and positive postimage checks. The private
recoverable backup completed with an explicit special-file and system-metadata
boundary. Active policy and module hashes now match their approved repository
sources. The hardened fixture passed both partial-publication rollback cases and
target-drift rejection. Focused 26-test and full 157-test suites passed, and
independent code and security reviews returned PASS. No repository tool or
fresh Codex session was executed; runtime usefulness and cost remain a separate
usage evaluation.

Decision:
ACCEPT

Notes:
The user approved a live recoverable backup and accepted explicit exclusion of
ephemeral socket/FIFO objects. A complete runtime restore remains separately
gated and requires quiescence.

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
