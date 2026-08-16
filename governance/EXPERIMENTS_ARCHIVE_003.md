# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

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

## EXP-20260809-003 - CMA-ARK Adapter Process Boundary

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The first Phase 3 design review found that the adapter contract mixes a direct
ARK Python-import boundary with ARK process-exit passthrough semantics, omits an
exact run/error response schema, and claims tool-identity drift detection while
the canonical plan leaves tool identity unverified.

Evidence:
The mandatory code review returned three HIGH findings and one MEDIUM finding.
It identified the conflicting direct-import and `ark_exit_code` statements,
missing result/error types and examples, a null selected-tool digest despite
TOCTOU claims, and non-canonical digest placeholders.

Hypothesis:
Using the fixed repository-owned ARK CLI as the adapter's only ARK boundary,
defining exact plan/run/error response examples, and requiring a resolved tool
content/stat identity before a runnable plan will make exit origin, result
normalization, and drift limits deterministic without duplicating ARK routing.

Solution Attempt:
Revise only the Phase 3 design contract. Bind the adapter to the absolute
`ARK/bin/ark` launcher and config, define normalized result items and nullable
error correlation fields, preserve the actual ARK subprocess exit separately
from tool result exits, require a SHA-256/stat identity for runnable tools, use
valid canonical digest examples, and state the residual post-check/pre-exec race.

Test:
Run a RED validator against the current contradictory design, then parse and
validate all revised JSON examples, field types, digest encodings, exit origins,
result cardinality, tool-identity requirements, and cross-document status. Run
the monorepo contract and independent code/security review.

Success Criteria:
- The design chooses exactly one ARK integration boundary.
- Plan, successful run, and malformed-request responses have deterministic
  exact schemas and origin-aware exit fields.
- A runnable plan cannot use an unverified or null selected-tool identity.
- Canonical examples use valid encodings and only `explore` has a concurrency key.
- TOCTOU guarantees are limited to observable pre-execution revalidation.
- Existing ARK functional files and monorepo contracts remain unchanged.

Result:
The CLI-only boundary, exact request/plan/run/error schemas, canonical plan
digest, tool and target identity binding, failed-run execution semantics, and
honest truncation limits passed machine-readable validators. The monorepo
contract passed 9/9 and diff/whitespace checks passed. The user-approved bounded
continuation defined the complete POSIX/macOS ARK process range, signal-derived
negative exits, wrapped tool-signal relation, and origin-aware overlap with
adapter-reserved codes. Final code review and security review returned PASS.

Decision:
ACCEPT

Notes:
This experiment changes documentation only. Adapter implementation, activation,
global configuration, dependencies, MCP, cplt, commit, and push remain outside scope.
Revision after the first re-review: define `plan_sha256` over one exact canonical
`plan` object shared by plan/run rather than either wire request; bind target
device/inode identity; treat every spawned ARK run as execution even on failure;
remove truncation booleans unavailable through the CLI contract; and define the
exact normalized ARK plan and step schemas.
Final revision after the second re-review: include adapter version, ARK schema,
config/source digests, and selected-tool realpath inside the hashed plan binding
rather than only in unhashed response provenance.
User-approved bounded continuation: define the full observable ARK process-exit
domain, distinguish normal and signal termination, preserve the original tool
exit from valid ARK JSON, and make overlapping adapter-reserved codes
unambiguous through nullable `ark_exit_code`.
Security review retained non-blocking activation gates: approval JSON is not
authentication; interpreter path and recursive source-manifest algorithms need
pinning before activation; direct bounded output may expose repository secrets;
the post-check/pre-exec race remains; and Graphify serialization depends on a
tested CMA coordinator.

## EXP-20260808-002 - Task Transition Gate Synchronization

Date: 2026-08-08
Status: ACCEPTED

Problem:
The active Codex global policy already stops at distinct task boundaries, but
the portable Codex, Dolphin, Claude, and OpenCode policy sources do not all
carry the same rule. A newly installed or refreshed runtime can therefore
resume automatic task progression or interpret approval inconsistently.

Evidence:
`~/.codex/AGENTS.md` contains the complete Task Transition Gate, while
`GLOBAL_AGENTS_TEMPLATE.md` and the four portable variant policies do not share
that complete block. Active Dolphin, OpenCode, and native Claude CMA policy
surfaces also lack it.

Hypothesis:
Adding one canonical semantic gate to every portable global policy and safely
synchronizing only the three stale active runtime policy files will make task
boundaries consistent without pausing the already approved steps inside one
bounded task or overwriting unrelated runtime state.

Solution Attempt:
Add the canonical gate after Scope Lock in all five source policies, document
the behavior, and update only stale active policies through targeted,
permission-preserving backups. Preserve the already-correct active Codex file
and the user-owned native Claude loader byte-for-byte.

Test:
Capture RED semantic policy, portable-install, and documentation tests; then
verify focused and complete regressions, exact source/install contracts,
targeted active-runtime parity, backup hashes, preserved modes, unchanged
Codex and Claude loader hashes, diff integrity, and independent code/security
review.

Success Criteria:
- Every portable policy enforces the six task-transition obligations.
- The rule distinguishes a next distinct task from steps inside the same
  explicitly approved bounded task.
- Portable installs for Codex, Dolphin, Claude, and OpenCode expose the gate.
- Active Codex and the Claude loader remain byte-identical to their pre-update
  state; every changed active policy has an exact recoverable backup.
- User documentation and changelog match verified behavior.
- All tests and independent reviews pass without weakened assertions.

Result:
The initial semantic, portable-install, and documentation run produced 13
expected RED subtest failures. The canonical gate was then added to all five
source policies and the four user guides. A code-review finding exposed that
the first negative fixture failed only because positive markers were absent;
the replacement fixture kept the complete valid policy and added a conflicting
every-step approval rule, reproduced the false pass, and now fails through an
explicit conflict check.

The focused suite passed 4/4 and the complete suite passed 145/145 without
skips; `git diff --check` passed. Portable installs for all four variants expose
the gate. Active Dolphin, OpenCode, and Claude CMA policies differ from their
verified pre-state backups only by the canonical block, retain modes `0644`,
`0644`, and `0600`, and have exact backups under the private `0700` recovery
directory. Active Codex and the user-owned Claude loader retained their
pre-update hashes and modes. Final independent code and security reviews
returned PASS.

Decision:
ACCEPT

Notes:
The user approved Plan A and the mandatory orchestration chain. Commit and push
remain outside scope.

## EXP-20260808-003 - Additive Multi-Variant Project Initialization

Date: 2026-08-08
Status: ACCEPTED

Problem:
`codex-project-init --variant opencode` was applied to an already initialized
project and reset shared project state. The command treats every variant
selection as an exclusive new/reset initialization, so the same data-loss risk
applies when adding Codex, Dolphin, Claude, or OpenCode to a project that
already uses another runtime.

Evidence:
The init conflict list always archives `AGENTS.md`, `.codex/config.toml`, the
shared prompt, and `.codex/template-state.json`, then copies a blank project
template. Manifest schema 1 stores one `variant`; OpenCode replaces the Codex
config entry instead of coexisting with it. The original project files remain
recoverable in the private init archive and their hashes were captured before
rollback.

Hypothesis:
If init distinguishes first/reset initialization from additive variant
activation, preserves shared files byte-for-byte, and records an ordered set of
active variants in a backward-compatible manifest migration, every supported
runtime can coexist without resetting project configuration or customized
variant files.

Solution Attempt:
Restore the exact pre-init project state, make existing-project init additive
by default, require an explicit reset flag for destructive reinitialization,
and evolve template state to represent multiple active variants plus the union
of their managed files. Preserve customized and unrelated files.

Test:
Capture RED tests that initialize each variant after another variant and assert
unchanged shared hashes, coexisting variant surfaces, manifest migration from
schema 1, explicit reset behavior, customized-file preservation, symlink
failure, and idempotency. Then run focused project-init/upgrade tests, the full
regression suite, live additive OpenCode init on this repository, diff
integrity, and security-oriented recovery checks.

Success Criteria:
- Adding any supported variant never replaces an existing `AGENTS.md` or
  removes another variant's project files.
- Codex, Dolphin, Claude, and OpenCode can all be represented as active in one
  project manifest.
- Schema 1 state migrates without losing file ownership or customization
  evidence.
- Destructive reset remains possible only through an explicit reset option and
  keeps a private recovery archive.
- The erroneous local init effects are fully reversed before the corrected
  additive OpenCode activation is applied.
- Relevant and complete tests pass without weakened assertions or skipped
  cases.

Result:
The erroneous local init was reversed first: `AGENTS.md`, Codex config, the
shared prompt, and schema-1 template state matched their captured pre-init
hashes, the generated OpenCode project file was removed, and the private reset
archive was moved into the external recovery backup. The valid global OpenCode
runtime installation was retained.

Meaningful RED tests reproduced blank `AGENTS.md` replacement, loss of other
variant state, customized OpenCode config overwrite, the single-variant
manifest limitation, absent explicit-reset behavior, incomplete standalone
schema-1 migration, and same-second reset archive reuse. The implementation now
uses additive existing-project init, ordered multi-variant schema 2 state,
backward-compatible schema-1 migration, explicit `--reset`, and unique private
init/upgrade archives.

Focused project-init/upgrade tests passed 33/33 and the complete regression
suite passed 152/152 without skips. Bash syntax, Python compilation, and diff
integrity passed. Live additive OpenCode init on this repository preserved the
exact `AGENTS.md`, `.codex/config.toml`, and shared-prompt hashes, produced
`variants: [codex, opencode]`, kept the OpenCode config, used a `0700` recovery
archive, and was idempotent on a second run. Security-oriented symlink,
customized-config, secret-redaction, explicit-reset, and recovery tests passed.

Decision:
ACCEPT

Notes:
The user approved a direct implementation without an orchestration chain.
Global OpenCode runtime installation is valid and remains in scope; only the
project-reset behavior is being rolled back and redesigned.

## EXP-20260808-004 - Fail-Closed Result Semantics

Date: 2026-08-08
Status: ROLLED_BACK

Problem:
The first ARK implementation passed its source tests but independent code review found configuration type gaps, zero-execution success paths, and optional documentation flags that did not affect routing.

Evidence:
`config.py` accepted boolean schema version `true`, leaked `TypeError` for malformed collection types including a nested Serena mode value, allowed runtime root `.`, and accepted malformed GitHub identities. `run --intent docs` returned exit code 0 despite `success=false`. An empty security profile returned `passed` with no steps. DeepWiki and Context7 enable flags produced identical plans. Security review later found ambient cplt credentials, sensitive scanner output emission, unbounded subprocesses, and a Graphify output symlink escape.

Hypothesis:
Enforcing one fail-closed invariant across parsing and routing—invalid input becomes `ConfigError`, and no executed or executable work can never be `passed`—will remove all four review findings without widening ARK's MVP.

Solution Attempt:
Add RED regression tests for malformed configuration types and identities, runtime-root containment, no-execution CLI exits, empty security profiles, explicit enabled documentation providers, credential-free cplt isolation, suppressed security findings, bounded subprocesses, and Graphify output containment; then make the smallest config/router/CLI changes required.

Test:
Run focused config, routing, and CLI tests before and after implementation, followed by the full suite, branch coverage, live CLI probes, and independent code review.

Success Criteria:
All new regression tests fail before the fix and pass afterward; invalid configuration exits 2 without traceback; every `run` path with zero steps exits nonzero; empty security cannot report success; docs flags and provider selection change the plan; full branch coverage remains at least 80%.

Result:
The regression cycles reproduced the configuration, result-semantics, credential exposure, sensitive-output, symlink, memory-bound, locale, process-group, and closed-pipe timeout findings before each scoped fix. The final suite passed 33/33 with 91% branch coverage. Reopened code review and security review both returned PASS with no blocking findings.

Decision:
ACCEPT

Notes:
The attempt remained limited to reviewer-identified config, router, runner, tests, and records. External tools and live MCP transports remain out of scope. Security review retained two non-blocking advisories: broader ambient environment exposure for non-cplt local tools and theoretical same-user symlink TOCTOU races.

Migration note: This record was originally ARK-local `EXP-20260808-001`; it was remapped because that ID already belongs to CMA's Provider-Neutral OpenCode Runtime Variant.

## EXP-20260809-001 - ARK Monorepo Test Discovery

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The documented root-relative ARK test command fails after monorepo adoption because CMA's root `tests` package shadows `ARK/tests` during unittest discovery.

Evidence:
Fresh coverage execution from the CMA root collected 28 ARK tests but produced one `_FailedTest`: `ARK/tests/test_cli.py` could not import `tests.test_config`. The same ARK suite previously passed 33/33 from the ARK working directory.

Hypothesis:
Declaring `ARK` as unittest's explicit top-level directory with `-t ARK` will preserve root-relative commands while resolving `tests.*` imports to `ARK/tests` instead of CMA's root test package.

Solution Attempt:
Require `-t ARK` in root-relative ARK discovery commands and leave ARK production code and tests byte-identical.

Test:
First add a failing monorepo contract assertion for `-t ARK`, then rerun the contract, the 33-test ARK suite, and fresh branch coverage from the CMA root.

Success Criteria:
All 33 ARK tests collect and pass from the CMA root, branch coverage remains at least 80%, no import or fixture error occurs, and the functional ARK hash manifest remains unchanged.

Result:
The contract first failed because neither authoritative command included `-t ARK`. With the explicit top-level directory, all 33 ARK tests passed from the CMA root with no import errors and fresh branch coverage reached 85%. The functional ARK hash manifest remained unchanged.

Decision:
ACCEPT

Notes:
This experiment changes only test invocation documentation and its monorepo contract; it does not authorize ARK runtime wiring or functional code changes.

## EXP-20260809-002 - ARK Monorepo CLI Config Resolution

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The documented root-relative `ARK/bin/ark` commands resolve the default `ark.json` against the CMA working directory instead of the ARK module directory.

Evidence:
Independent code review executed `ARK/bin/ark doctor --json` from the CMA root. It exited 2 with `cannot read configuration` for the nonexistent root `ark.json`, while the contract test checked only textual command prefixes.

Hypothesis:
Passing the existing module config explicitly as `--config ARK/ark.json` in every root-relative command will make the documented interface executable without changing the already-reviewed launcher or runtime behavior.

Solution Attempt:
Make the monorepo contract execute the documented doctor command, require the explicit config argument on every example, and update the README and integration plan commands only.

Test:
Capture a RED failure by executing the current documented command from the CMA root, then require exit 0 and valid successful JSON after the documentation change. Rerun ARK, contract, and complete CMA suites.

Success Criteria:
Every documented ARK command names `ARK/ark.json`; the documented doctor command exits 0 from the CMA root with `status=passed` and `success=true`; functional ARK hashes remain unchanged.

Result:
The executable contract first reproduced exit 2 and the missing root `ark.json`. After adding the explicit config argument, the documented doctor command exited 0 from the CMA root with `status=passed` and `success=true`; the contract passed 9/9, the ARK suite passed 33/33, and functional ARK hashes remained unchanged.

Decision:
ACCEPT

Notes:
Automatic CMA routing, launcher behavior changes, global activation, and external tool installation remain outside this experiment.
