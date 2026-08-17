# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

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

## EXP-20260804-003 - Atomic Evidence Claim Contract

Date: 2026-08-04
Status: ACCEPTED

Problem:
CMA requires one material claim per bullet and direct proof outside Claims, but
does not explicitly prevent one bullet from combining independently verifiable
outcomes. Codex can therefore enter repeated EV validation cycles or weaken a
claim into a statement that output was reported.

Evidence:
An observed Codex/EV run repeatedly split test, review, gateway-health, and
admin-capability assertions before GLM could bind each claim to direct proof.
The final validation passed, but the repeated rewrites exposed missing atomic
claim semantics in CMA rather than a need to weaken EV.

Hypothesis:
If CMA requires one independently verifiable outcome per claim, one coherent
verbatim proof excerpt for that outcome, and semantic preservation during
splitting, future evidence will bind cleanly without narrowing acceptance
meaning or expanding EV.

Solution Attempt:
Add four prospective atomic-claim clauses to the existing Claims contract and
verify the managed and portable records modules. Do not rewrite historical
reports, alter EV, or synchronize the active global runtime.

Test:
Add source and portable-install contract tests before changing the records
module. Include negative checks showing that formatting-only wording and a
reporting-only downgrade do not satisfy the contract. Run focused and full CMA
regression suites, independent code and security reviews, and EV validation of
the new evidence report.

Success Criteria:
- Each claim bullet contains exactly one independently verifiable outcome.
- One coherent verbatim proof excerpt outside Claims directly proves it.
- Splitting preserves every original acceptance outcome.
- Outcome claims cannot be weakened into reporting-only meta-claims.
- Managed and portable records modules are byte-identical and satisfy the rule.
- No EV, active global runtime, historical evidence, dependency, commit, push,
  or deployment change occurs.

Result:
The targeted source and portable tests first failed 2/2 because the records
module lacked the independently verifiable outcome clause. After the four
prospective semantics were added, both targeted tests passed. The focused CMA
records suite passed 17/17, the complete CMA suite passed 55/55, and
`git diff --check` completed cleanly. Independent code and security reviews
both passed. EV first returned `UNVERIFIED` for negated review-proof prose;
after each PASS result was placed in its own direct proof sentence, the same
six atomic claims returned `PASS` with `success=true` and no diagnostics.

Decision:
ACCEPT

Notes:
This experiment is intentionally limited to the prospective CMA records
contract and its verification.
Detailed evidence is recorded in
`docs/reports/EVIDENCE_EXP-20260804-003_ATOMIC_CLAIM_CONTRACT_20260804.md`.

## EXP-20260805-001 - Optional Evidence Mode

Date: 2026-08-05
Status: ACCEPTED

Problem:
CMA projects declare an evidence path but have no explicit switch controlling
automatic evidence creation or validation. Evidence can therefore add cost and
friction to low-risk work even after EV hooks are disabled.

Evidence:
The user approved optional evidence with exactly `enable | disable`, selected
`disable` as the default, and requested the setting across all active CMA
projects under `/Users/iyilmaz/WebStorm`.

Hypothesis:
An explicit fail-closed project field with missing treated as disabled will
make evidence genuinely optional without weakening evidence quality when the
mode is enabled or when the user explicitly requests it.

Solution Attempt:
Add `EVIDENCE_MODE: disable` to the project template and active CMA project
configuration blocks. Gate only automatic evidence-report creation and
automatic EV use in the records module. Preserve explicit user requests and
all existing evidence quality rules.

Test:
Add RED tests for fresh-project defaults, configuration guidance, source and
portable records semantics, missing values, invalid values, and explicit user
requests. Run focused and full CMA suites, verify an explicit 17-project
manifest, and preserve excluded archives, backups, worktrees, and variants.

Success Criteria:
- Only literal `enable` activates automatic evidence creation and validation.
- Literal `disable` and a missing field keep automation disabled.
- Invalid explicit values are reported and never enable automation.
- Explicit user evidence requests remain applicable in either mode.
- Fresh projects and all 17 active CMA projects declare `disable` exactly once.
- Excluded copies and unrelated dirty changes remain untouched.
- Active global CMA runtime, dependencies, commits, pushes, and deployment
  remain unchanged.

Result:
The initial targeted run failed 3/3 because fresh projects omitted the field
and the source and portable records modules lacked the mode contract. After the
minimal framework change, the targeted tests passed 3/3, project-upgrade tests
passed 6/6, and CMA lazy-runtime tests passed 20/20. The explicit rollout
manifest verified exactly one `EVIDENCE_MODE: disable` declaration in each of
17 active CMA projects. The complete CMA suite passed 60/60 and
`git diff --check` completed cleanly. Code review passed. Security review
confirmed that the project declarations are staged but not yet enforced by the
active global runtime because its `CMA_RECORDS.md` lacks the new mode gate.
After separate option A approval, the previous active records module was backed
up at
`~/.codex/archive/cma-evidence-mode-20260805_135615/CMA_RECORDS.md` with SHA-256
`c3d4813491a493775db57f24b451e13c5b9168c5a15445113d1f33a72e9299ea`.
Only the four EVIDENCE_MODE clauses were added to the active module; its new
SHA-256 is
`e8d6a962ea74990028baedea10f183726484e8fe64ba5f4995bb1c1d1921c065`
and mode remains `0644`. Reopened code and security reviews both passed with
no blocking findings.

Decision:
ACCEPT

Notes:
Active global runtime synchronization was performed only after separate option
A approval. No evidence report was created because this project now declares
`EVIDENCE_MODE: disable` and the user did not explicitly request one.

## EXP-20260806-001 - Git Archive Executable Mode Verification

Date: 2026-08-06
Status: ACCEPTED

Problem:
The transferred CMA source archive passed SHA-256 verification, but the remote
installer-mode check expected exactly `755` and observed `775`, leaving the
source-integrity gate unresolved before installation.

Evidence:
The local and remote archive SHA-256 values are identical, the local and remote
installer content SHA-256 values are identical, the local working-tree mode is
`755`, and the extracted archive mode is `775` inside a root-owned mode-`700`
staging directory.

Hypothesis:
Git archive preserved an executable script with additional group execute/write
mode bits, while content and executable semantics remained intact. Verifying
the executable bits together with the root-only staging boundary is the correct
security and integrity criterion.

Solution Attempt:
Replace the overly strict exact-`755` staging assertion with checks that the
installer is a regular root-owned file, has at least one executable bit, and is
contained by a root-owned mode-`700` staging directory. Do not change archive
content or installed target permissions.

Test:
Re-run the revised mode assertion, verify local and remote installer hashes are
identical, and include a negative check proving a non-executable copied mode is
rejected.

Success Criteria:
- Local and remote installer content hashes match exactly.
- The extracted installer is a regular root-owned executable file.
- The staging directory remains `root:root` mode `700`.
- The same assertion rejects a non-executable mode.
- No real runtime or project installation occurs before this gate passes.

Result:
The revised positive check accepted the root-owned executable installer at
mode `775` inside the root-owned mode-`700` staging directory. Local and remote
installer SHA-256 values both equal
`627312caeaf016427267d4f67bda236113204818d970eec9dad14c4194526321`.
The same checker rejected an explicit mode-`600` non-executable copy. No real
runtime or project installation occurred during the test.

Decision:
ACCEPT

Notes:
This experiment is limited to the source-transfer mode assertion and does not
expand the approved remote-installation scope.

## EXP-20260806-002 - Sentinel Preservation Manifest Scope

Date: 2026-08-06
Status: ACCEPTED

Problem:
The isolated no-overwrite installation stopped because the before and after
manifest files differed even though every seeded sentinel retained its hash.

Evidence:
The diff contains only three newly installed, previously absent skill files:
`hypothesis-workflow`, `orchestration-gate`, and `record-archive`. All seven
seeded managed and unrelated sentinels have identical before/after SHA-256
values.

Hypothesis:
The first post-install `find` expression selected new files by shared basename,
so it compared the complete installed tree rather than the fixed sentinel set.
Comparing an explicit sentinel path list will prove preservation without
mistaking legitimate additions for overwrites.

Solution Attempt:
Re-run the preservation assertion over the seven exact pre-seeded paths and
separately require that a previously absent managed skill was installed. Keep
the installer command and isolated target unchanged.

Test:
Generate before and after hashes from the same explicit sentinel path list,
require byte-identical manifests, verify `Skipped existing:` output, and mutate
a copied manifest value to prove the equality check fails.

Success Criteria:
- The seven exact sentinel hashes remain unchanged.
- Existing managed files are reported as skipped.
- Missing managed files are installed.
- A deliberately altered expected hash is rejected.
- No real runtime or project installation occurs during the test.

Result:
The explicit seven-path sentinel check confirmed identical SHA-256 values for
all pre-existing managed and unrelated files. Installer output reported
existing managed paths as skipped, and previously absent skills were installed.
An altered expected hash was rejected. The isolated project conflict test also
preserved archived conflicts and the unrelated file, while the cancellation
test produced no project mutation.

Decision:
ACCEPT

Notes:
This experiment changes only the isolated-test manifest selection.

## EXP-20260806-004 - Bounded Fresh SSH Codex Install

Date: 2026-08-06
Status: ACCEPTED

Problem:
Codex remains missing after apt completed because the original PTY stdin was
consumed and later closed, preventing continuation in that session.

Evidence:
Node.js and npm are installed and verified through a fresh read-only SSH
connection, while `codex` is missing. Writing to the previous session failed
before command delivery.

Hypothesis:
A fresh non-PTY SSH invocation with the pinned npm command passed as the remote
command argument will avoid stdin consumers and complete only the missing Codex
installation.

Solution Attempt:
Run one bounded non-PTY SSH command that verifies the global prefix, installs
`@openai/codex@0.146.1`, and prints executable paths and versions. Do not invoke
apt or use a heredoc.

Test:
Require the SSH command to exit zero and then verify package identity and CLI
version through an independent fresh SSH call.

Success Criteria:
- Only the pinned npm package is added.
- `codex --version` reports `0.146.1`.
- The executable resolves from npm's actual global prefix.
- A separate verification command exits zero.
- No service or host restart occurs.

Result:
The fresh non-PTY command installed two npm packages and exited successfully.
The verified global prefix is `/usr/local`, the CLI resolves to
`/usr/local/bin/codex`, and `codex --version` reports `codex-cli 0.146.1`.
An independent SSH check confirmed `@openai/codex@0.146.1` under
`/usr/local/lib/node_modules` and reproduced the expected CLI version.

Decision:
ACCEPT

Notes:
This is the final retry for the missing Codex package action.

## EXP-20260801-003 - Root-Only Contextual Voice Notification

Date: 2026-08-01
Status: ACCEPTED

Problem:
The active global `Stop` hook always speaks the same message and does not
distinguish root Codex completion, failure, user-input waiting, or subagent
completion. Subagent turns therefore produce unwanted voice notifications.

Evidence:
`~/.codex/hooks.json` runs `notify_stop.sh` for every matching `Stop` event.
The script unconditionally calls macOS `say`. Official Codex hook guidance
defines separate `Stop` and `SubagentStop` events, but `Stop` itself has no
agent identifier. Existing subagent transcripts identify themselves through
`session_meta.payload.source.subagent`, while root transcripts use a non-
subagent source.

Hypothesis:
If the notification script reads the hook payload, suppresses transcripts
whose session metadata marks them as subagents, and classifies the final root
message into failure, waiting, or completion, voice notifications will occur
only for root Codex with an appropriate message.

Solution Attempt:
Change only the active notification script. Preserve the existing trusted Stop
hook definition and add a silent dry-run mode for deterministic tests without
playing audio.

Test:
Run RED synthetic hook payloads against the old implementation. After the
change, test root completion, root failure, root approval/question waiting,
direct `SubagentStop`, subagent transcript metadata, malformed input, shell
syntax, JSON hook output, and preservation of the hook/config definitions.

Success Criteria:
- Root completion selects `Kodex işlemi tamamladı.`
- Root failure selects `Kodex bir hatayla karşılaştı.`
- Root approval or question waiting selects `Kodex senden yanıt bekliyor.`
- Subagent events and subagent transcripts produce no voice message.
- Every invocation returns valid `{"continue":true}` hook JSON.
- Existing hook registration and trusted config state remain unchanged.

Result:
The RED inspection found all five expected capabilities absent. After the
change, eight silent dry-run cases passed: root completion, failure, approval
waiting, question waiting, direct `SubagentStop`, a real subagent transcript,
malformed payload, and a root payload without a final message. Every case
returned valid continuation JSON, shell syntax validation passed, and the
script retained executable mode.

The active `hooks.json` and `config.toml` remained byte-identical to their
backups, so hook registration and trusted state did not change. The previous
script and both supporting files are recoverable from the timestamped archive.

Decision:
ACCEPT

Notes:
The user approved message option A. No subagent was spawned and no audio was
played during validation; `CODEX_NOTIFY_TEST=1` exposed the selected message on
stderr while preserving the production hook JSON response.

## EXP-20260801-002 - Medium-Only Subagent Matrix

Date: 2026-08-01
Status: ACCEPTED

Problem:
The accepted CMA runtime uses six Sol/high routing variants and two additional
Sol/high default roles. Higher reasoning effort increases token use and latency,
which conflicts with the current objective of reducing subagent cost while
retaining model-quality routing.

Evidence:
The managed and active Codex surfaces contain fourteen agent TOMLs: eight
defaults plus six `*-high` variants. Eight of those files pin `high` reasoning.
Official Codex guidance describes `medium` as the balanced default for most
agents and recommends using the lowest effort that produces the needed result.

Hypothesis:
Using `medium` for every subagent, keeping Terra/medium defaults for support
roles, and retaining only four Sol/medium model-escalation variants will reduce
reasoning-token pressure without weakening the mandatory chain, review stages,
approval gates, or test-integrity controls.

Solution Attempt:
Replace four Terra-role `*-high` variants with `*-sol` variants at medium,
remove redundant code-reviewer and security-reviewer high variants, and change
reviewer plus skill-agent-governor to medium. Update only the directly tied
routing, registry, skill, test, and current planning surfaces before mirroring
validated files into `/Users/iyilmaz/.codex`.

Test:
Add RED contracts requiring exactly twelve managed agent files, medium effort
in every agent TOML, four named Sol variants, no `*-high` files or high routing,
the unchanged mandatory chain, and portable-install packaging. Run focused and
full suites, source-active parity checks, and a fresh-session routing probe.

Success Criteria:
- All managed and active subagent TOMLs use `medium` reasoning.
- Exactly eight defaults and four Sol/medium variants remain.
- No `*-high` agent or routing reference remains in active instructions.
- Code-reviewer and security-reviewer stay Sol/medium and retain their required
  review stages without redundant variants.
- The mandatory chain, approval boundaries, truthful success, and test
  integrity remain unchanged.
- Focused, full, portable-install, parity, and fresh-session checks pass.
- Historical experiment, evidence, changelog, and audit records remain intact.

Result:
The RED contract run executed 10 focused tests and failed seven assertions with
one missing-file error, confirming that six high variants and two high defaults
were still active. After implementation, the focused suite passed 10 tests and
the complete repository suite passed 47 tests.

Managed and active Codex surfaces each contain exactly 12 agent TOMLs: eight
defaults and four Sol/medium variants. Every agent pins `medium`; no `*-high`
file remains. Managed-to-active parity passed for all agent files and the owned
routing, index, lazy-module, and skill files. A fresh ephemeral read-only Codex
session independently reported 12 agents, `medium` as the only reasoning value,
zero high variants, the four expected Sol variants, the exact mandatory chain,
and the security no-impact contract.

Both pre-change ZIP archives passed integrity checks. No project-local high
agent override was found under `/Users/iyilmaz/WebStorm`, so project files did
not require this runtime-matrix change.

Decision:
ACCEPT

Notes:
The main Codex session reasoning setting, project-local documents, Dolphin,
remote hosts, auth, config, secrets, and plugin state are outside scope.
