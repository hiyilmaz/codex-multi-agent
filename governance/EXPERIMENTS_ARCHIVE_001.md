# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260817-009 - Blockmanpro Fix Commit Deployment

Date: 2026-08-17
Status: ACCEPTED

Problem:
Blockmanpro still reports the Go-installed scanners as missing after a Git pull
and runs the old repair semantics.

Evidence:
The server repository and installed UV package have identical source hashes,
but both are at main commit `85ca147` while the accepted codex-tools fix is at
descendant commit `b45ddc7` on `origin/agent/cma-project-defaults`. The real
scanner binaries exist under `/root/go/bin` with executable modes.

Hypothesis:
Fast-forwarding the clean server main branch to the accepted fix commit and
reinstalling the user-scoped UV package from that exact repository will make
the existing Go tools healthy without changing Codex config or credentials.

Solution Attempt:
Capture exact Git, package, config-hash, and permission pre-state; fast-forward
only to `b45ddc7`; take a private UV-tool backup; force-reinstall the package
from the repository; and run standalone install in MCP `verify-only` mode.

Test:
Compare repository and installed source hashes, execute the real scanner
version commands, compare config hash and metadata before and after, and require
JSON to distinguish `AUTH_REQUIRED` from genuine failures while continuing all
selected CLI tools.

Success Criteria:
- The server repository and installed package both identify the accepted fix.
- `osv-scanner` and `betterleaks` execute and report `HEALTHY` without profile edits.
- All selected CLI tools are healthy; credential-gated MCP tools remain typed `AUTH_REQUIRED` when unavailable.
- Codex config hash and credentials metadata remain unchanged in verify-only mode.
- Any incomplete selected tool keeps the overall exit status nonzero without a false success claim.

Result:
The clean server main branch fast-forwarded from `85ca147` to the accepted
`b45ddc7` fix, and the user-scoped UV package was rebuilt from that exact
repository after an owner-only backup. Repository and installed `cli.py`
hashes match. The real `osv-scanner` 2.5.0 and Betterleaks version commands
execute, and both `check` and non-interactive MCP `verify-only` install report
nine tools `HEALTHY`, two credential-gated MCP tools `AUTH_REQUIRED`, zero
generic failures, and exact config preservation. Install exits 1 as required
while selected credential-gated tools remain incomplete. Config hash, inode,
mode, and mtime plus credential-file metadata remained unchanged; the server
repository is clean at the expected commit. Independent code review found no
behavioral or deployment defect. Security review then found that manage-mode
rollback captured its pre-state before credential resolution, allowing a user
edit made during the prompt to be overwritten after a later verification
failure. A meaningful RED reproduced the overwrite. The revised implementation
now carries the updater's actual original bytes in its transaction result; the
new regression and all 72 package tests pass with 85 percent branch coverage,
and the 385-test repository suite remains green. Final re-reviews and live
deployment of this revision are pending. The first live manage-mode run then
repaired Context7 but exposed a second input-boundary defect: a stored GitHub
credential containing a control character reached subprocess environment
construction and produced a generic config failure. An isolated transaction
confirmed a `ValueError` cause without printing the value. New unit and E2E
RED tests require invalid environment, secure-store, and prompt values to be
rejected before subprocess use and reported as typed `AUTH_REQUIRED` in
non-interactive mode. Review then extended the same boundary to configured MCP
discovery and verification and rejected Unicode whitespace/control/format
bypasses by requiring printable ASCII token values. Meaningful CLI and unit
RED tests covered stored NUL, environment NUL, NEL, NBSP, line separator, and
bidi override inputs. The revised credential boundary passes all 75 package
tests with 85 percent branch coverage and the 385-test repository suite;
independent code and security re-reviews pass. Final live deployment remained
pending at that point. The final `65309d6` revision was then fast-forwarded to
the clean server repository and rebuilt into the user-scoped UV environment
from the exact source. Repository and installed credential-module hashes
match. A live normal non-interactive install reports ten functionally healthy
tools, zero generic failures, and only the corrupted stored GitHub value as typed
`AUTH_REQUIRED`; Context7 passes functional verification. The expected exit 1
truthfully reflects that one incomplete selected tool. Config hash, inode,
mode, and mtime and credential-file inode, mode, and mtime remained unchanged
during the final run. The real scanner version commands still pass, and the
server repository is clean at `65309d6`.

Decision:
ACCEPT

## EXP-20260817-008 - Transactional MCP Credentials

Date: 2026-08-17
Status: ACCEPTED

Problem:
Standalone MCP installation can persist a prompted credential before config
and functional verification succeed, and empty credentials become `FAILED`.

Evidence:
The blockmanpro run left a private credential file after GitHub failed, while
Context7 was reported as `FAILED` instead of `AUTH_REQUIRED`.

Hypothesis:
Deferring credential persistence until config and functional verification
succeed, with per-tool config rollback and typed outcomes, will prevent partial
state while allowing later independent tools to continue.

Solution Attempt:
Add a per-tool pending transaction that commits the prompted credential only
after verification and restores that tool's config pre-state on failure.

Test:
Capture RED for deferred persistence, exact rollback, typed `AUTH_REQUIRED`,
continued execution, idempotency, and secret-free output.

Success Criteria:
- Failed MCP setup leaves config bytes and credential storage unchanged.
- Successful setup commits config and prompted credential once.
- `AUTH_REQUIRED` remains distinct from `FAILED`; later tools still run.
- Secrets never appear in output, status details, config, or backups.

Result:
Prompted credentials now remain in memory until config and read-only functional
verification pass. Failed MCP setup restores only that tool's owned config
state, preserves earlier successful MCP changes, cleans the process credential
even when rollback is refused, and reports missing credentials as the typed
`AUTH_REQUIRED` outcome. Rollback verifies expected bytes and inode first, so
a concurrent user edit is preserved. Secret-bearing success, functional
failure, store failure, concurrent edit, empty prompt, later-tool continuation,
and idempotency regressions passed without exposing test secrets. Package tests
passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7 and
the full repository passed 385/385. Independent code and security re-reviews
passed.

Decision:
ACCEPT

## EXP-20260817-007 - Truthful Config Preservation

Date: 2026-08-17
Status: ACCEPTED

Problem:
`config_preserved` currently mirrors config validity rather than whether the
config bytes changed.

Evidence:
The blockmanpro output claimed existing settings were preserved even though a
new DeepWiki MCP table was present after standalone installation.

Hypothesis:
Comparing the exact config pre-state and post-state will make preservation
reporting independent from TOML validity and reject false success.

Solution Attempt:
Capture config bytes before lifecycle execution and pass their exact equality
to the summary renderer.

Test:
Require `preserved=true` for byte-identical and exact rollback cases, and
`preserved=false` for valid but changed config.

Success Criteria:
- Validity and preservation are independently reported.
- Whitespace or comment-only byte changes count as changed.
- A successful exact rollback reports preserved.

Result:
The lifecycle now compares exact config bytes captured before and after the
selected operation. Validity and preservation are reported independently:
the first managed DeepWiki write reports changed, an idempotent repeat reports
preserved, and an exact rollback reports preserved. Non-regular or unreadable
capture fails closed with structured evidence instead of crashing. Package
tests passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7
and the full repository passed 385/385. Independent code and security
re-reviews passed.

Decision:
ACCEPT

## EXP-20260817-006 - Installed Binary Rediscovery

Date: 2026-08-17
Status: ACCEPTED

Problem:
Go tools can install successfully into `GOBIN` or `GOPATH/bin` but be reported
as failed when that directory is absent from the invoking shell's `PATH`.

Evidence:
On blockmanpro both Go binaries existed under `/root/go/bin` and became healthy
when that directory was added only to the check process environment.

Hypothesis:
Resolving managed user bin directories inside the installer process will make
same-run verification accurate without editing shell profiles.

Solution Attempt:
Use a scoped effective environment for install, discovery, and verification,
including explicit `GOBIN` or the first `GOPATH/bin` plus the user-local bin.

Test:
Capture RED where a binary exists only outside the original PATH, then require
healthy discovery, nonzero-version failure handling, and no profile mutation.

Success Criteria:
- Successfully installed Go tools are healthy in the same lifecycle run.
- Missing or broken binaries remain missing or broken.
- Caller environment and shell profile files remain unchanged.

Result:
The installer now appends the user-local bin directory and active absolute
`GOBIN` or first `GOPATH/bin` to a process-only effective PATH while preserving
the caller's command precedence. It refreshes that environment after installing
Go as a missing dependency, so both preinstalled-Go and fresh-host scenarios
rediscover and verify `osv-scanner` in the same run. Relative Go paths are
ignored and no caller environment or shell profile is written. Package tests
passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7 and
the full repository passed 385/385. Independent code and security re-reviews
passed.

Decision:
ACCEPT

## EXP-20260817-005 - Turkish Dialogue And Simple Decisions

Date: 2026-08-17
Status: ACCEPTED

Problem:
Agents can answer the user in English, and `CRITICAL DECISION` blocks can be
too technical or difficult to choose between.

Evidence:
The user reported both behaviors directly and approved a bounded policy change.
The current policies say only `User dialogue: Turkish` and define English,
placeholder-heavy decision fields without an explicit simplicity contract.

Hypothesis:
An explicit always-Turkish user-dialogue rule plus a short Turkish six-line
decision template with two concrete options will make runtime communication
consistent and decisions easier to understand.

Solution Attempt:
Update the canonical Codex, Claude, and OpenCode policies and orchestration-gate
projections with one shared dialogue and decision-simplicity contract.

Test:
Add contract and portable-install tests before production edits. Require all
user-facing message classes to remain Turkish, reject language-switching and
verbose decision mutants, and preserve the six-line stop boundary.

Success Criteria:
- Every packaged runtime requires Turkish for all user-facing dialogue.
- The decision block uses short Turkish labels, exactly two options, and one
  short recommendation.
- Tests reject partial, English-only, and verbose replacement policies.
- Focused and full regressions pass without changing approval or safety scope.

Result:
The new contract failed against the old policies, then passed across all four
packaged runtime policies, all three orchestration-gate projections, and all
three portable installer variants. Focused orchestration, variant, Claude, and
OpenCode suites passed 80/80. The final full suite passed 382/382 in 93.173 seconds.
Active Codex, Claude, and OpenCode global policies match their packaged sources;
the active Codex and Claude orchestration gates also match their projections.

Decision:
ACCEPTED

Notes:
The user approved one bounded exception to append this record while the active
experiment file is over 800 lines. No other record maintenance is authorized.

## EXP-20260817-004 - Qualified Plugin Skill Disable Selectors

Date: 2026-08-17
Status: ACCEPTED

Problem:
The approved Vercel plugin disablement removed Vercel skills from a fresh
Codex prompt, but nine Build iOS Apps skills remained visible after unqualified
skill-name disable entries were added to the global configuration.

Evidence:
`codex debug prompt-input` returned all nine `build-ios-apps:*` qualified skill
names after the first configuration attempt, while no `vercel:*` skill remained.

Hypothesis:
Plugin-provided skills are matched by their model-visible qualified names, so
changing only the nine selectors from unqualified names to
`build-ios-apps:<skill>` will remove them without disabling unrelated skills or
changing the already-disabled XcodeBuildMCP server.

Solution Attempt:
Replace the nine unqualified `skills.config` names with their exact
`build-ios-apps:`-qualified names. Keep the Vercel plugin override and every
unrelated global configuration entry unchanged.

Test:
Run strict configuration validation, render a fresh model-visible prompt, and
search it for both `vercel:*` and `build-ios-apps:*` skill names.

Success Criteria:
- Strict configuration validation passes.
- A fresh prompt contains no Vercel skill names.
- A fresh prompt contains no Build iOS Apps skill names.
- Existing unrelated configuration and owner-only file mode remain unchanged.

Result:
Codex 0.147.0 strict configuration validation passed with 17 checks OK and no
warnings or failures. A fresh model-visible prompt contained zero `vercel:*`
skills and zero `build-ios-apps:*` skills. The global configuration retained
its owner-only `0600` mode, and the existing XcodeBuildMCP disable override
remained unchanged.

Decision:
ACCEPT

Notes:
The initial unqualified selectors were schema-valid but behaviorally
ineffective for plugin-qualified skills.

## EXP-20260817-003 - Evidence-First Objectivity Policy

Date: 2026-08-17
Status: ACCEPTED

Problem:
The core CMA policies require honesty and authoritative research, but they do
not explicitly require evidence-supported conclusions over user agreement,
credible counterevidence, source-independence checks, or a clear separation of
verified facts, source claims, inferences, and opinions.

Evidence:
The approved policy review found these behaviors absent from the canonical
Codex template and the Codex, Claude, and OpenCode projections. Applying an
unbounded research rule to every task would also create unnecessary sourcing
for routine coding, editing, translation, and operational work.

Hypothesis:
Adding one equivalent, evaluation-scoped Evidence-First Objectivity contract to
all three runtime policies will improve neutrality and uncertainty reporting
without forcing research for routine tasks.

Solution Attempt:
Add the approved eight-part semantic contract beneath Language And Conduct in
the canonical template and every native projection, then document its scope.
Do not add dependencies, automatic browsing, provider behavior, or mutate an
active user runtime.

Test:
Capture RED with positive and negative semantic contract tests, including a
diluted-policy mutant and an overbroad every-task research mutant. Then run
policy parity and portable-install tests, the full repository suite, static
checks, and independent code and security reviews.

Success Criteria:
- Codex template/projection parity remains byte-identical.
- Codex, Claude, and OpenCode carry all eight approved semantic requirements.
- Material decisions require genuinely independent evidence where available.
- Counterevidence, conflicts, uncertainty, and fact/claim/inference/opinion
  distinctions cannot be removed without failing tests.
- Routine tasks do not acquire a mandatory research requirement.
- No active user-global policy is modified by this repository-only change.

Result:
The canonical Codex template and Codex projection remain byte-identical at
policy version 2.6, while Claude and OpenCode carry the same eight semantic
requirements. Contract tests reject missing clauses, diluted objectivity,
repeated-reporting source inflation, blanket every-task research, unconditional
research, and explicit research mandates for routine work. Portable installs
for all three variants expose the contract. Focused policy/runtime checks
passed, the full repository suite passed 374/374, code review passed after two
false-positive mutants tightened the oracle, and security review reported
`NO_SECURITY_IMPACT` with no new browsing or execution authority.

Decision:
ACCEPT

Notes:
Existing native-policy preservation and merge-prompt behavior remains unchanged.

## EXP-20260817-002 - Controlled Instruction Merge Hardening

Date: 2026-08-17
Status: ACCEPTED

Problem:
The first controlled instruction-merge implementation can replace an existing
user prompt, treats path and document content as trusted AI instructions, and
uses check-then-open path operations that can be redirected by a concurrent
ancestor swap.

Evidence:
Independent security review reproduced replacement of a custom prompt and
identified unescaped prompt metadata, missing untrusted-document boundaries,
and pathname-based source and destination races. It also found that prompt
validation occurred after the confidential snapshot was persisted.

Hypothesis:
A descriptor-pinned, no-clobber publication helper with encoded metadata and an
explicit untrusted-data merge protocol will preserve user files, contain
snapshots, and prevent loaded instructions or path names from overriding the
diff-only contract.

Solution Attempt:
Harden the single instruction merge helper: preflight all outputs, refuse
existing non-CMA prompts, reuse only byte-identical generated prompts, pin file
and directory operations with directory descriptors and no-follow flags, and
encode prompt metadata while classifying both input documents as untrusted
data.

Test:
Add regressions for custom prompt preservation, newline/control metadata,
embedded hostile instructions, ancestor-swap resistance, and no partial
snapshot on an unsafe prompt destination. Run focused installer/init tests,
the full suite, static checks, and repeated independent code/security review.

Success Criteria:
- Existing user-owned prompt content is never overwritten.
- Generated metadata cannot create Markdown instructions or extra fields.
- Input documents are handled only as merge data, never executable commands.
- Concurrently swapped source/destination ancestors cannot redirect reads or writes.
- A failed preflight leaves no new confidential snapshot.
- All focused and full regression checks pass and both reviews approve.

Result:
The helper now pins every source and destination ancestor with directory file
descriptors and `O_NOFOLLOW`, publishes files atomically without replacement,
preserves differing prompt content through deterministic hash-suffixed names,
and validates the prompt destination before persisting confidential snapshots.
Prompt metadata is Base64URL-encoded, referenced documents are explicitly
untrusted/non-executable data, and runtime-rewritten candidates stay private.
Custom-prompt, unsafe-target, hostile-metadata/document, and concurrent
source/destination ancestor-swap regressions passed; the race suite passed
10/10 three consecutive times, the full repository suite passed 370/370, and
independent code and security re-reviews both passed.

Decision:
ACCEPT

Notes:
This experiment is limited to the approved instruction snapshot and merge-prompt flow.

## EXP-20260817-001 - Independent Codex Tools Integration

Date: 2026-08-17
Status: ACCEPTED

Problem:
The selected `codex-tools` installer is coupled to the ToolSmith benchmark
workspace, and its default install path attempts to reconfigure healthy
user-owned MCP entries. That prevents safe reuse as an independent CMA tool.

Evidence:
The P9 implementation passed its existing 41 tests and reported all 11 tools
healthy in read-only checks, but a real non-interactive install exited nonzero
after attempting to configure the healthy user-owned DeepWiki, GitHub, and
Context7 MCP entries. The Codex config remained unchanged.

Hypothesis:
Extracting the installer as a self-contained package, adding an MCP
`verify-only` ownership mode, and exposing it through an explicit CMA adapter
will preserve CMA ownership while supporting both standalone and optional
user-requested installation.

Solution Attempt:
Create `tools/codex-tool-installer` without ToolSmith runtime dependencies; add
portable CLI, ownership, path, release-integrity, and idempotency contracts;
add `bin/cma-tools`; and add an opt-in `--tools-mode` setup path. Do not mutate
the active user Codex home, credential stores, remote MCP services, or host
package managers during validation.

Test:
Capture meaningful RED for the new ownership and CMA adapter contracts, then
run focused tests, branch coverage, the full project suite, shell syntax,
packaging outside the repository, and independent code and security reviews.

Success Criteria:
- The package installs and runs independently of CMA and ToolSmith paths.
- CMA mode verifies MCP entries without writing config or credentials.
- Standalone mode changes only installer-marker-owned MCP entries and fails
  closed on user-owned collisions.
- JSON option placement is consistent and configuration paths fail closed on
  symlinks or non-regular targets.
- Downloaded releases use pinned HTTPS artifacts with verified checksums.
- Package branch coverage is at least 80 percent and all project tests pass.

Result:
The independent package preserved the original 41-test baseline and expanded
it to 56 passing tests with 80 percent branch coverage. Meaningful RED exposed
missing ownership modes, option parity, symlink handling, release integrity,
and adapter behavior. Code and security reviews then exposed four path and
lifecycle issues plus mutable upstream references and ambient executable
substitution; regression tests reproduced each blocking finding before the
fixes. Final code and security re-reviews passed. A real isolated `uv tool`
install, version/help execution, and uninstall succeeded outside the repo while
preserving an unrelated sentinel. The full CMA suite passed 355/355, shell
syntax and diff checks passed, and no active Codex config, credentials, remote
MCP service, sudo command, or host package manager was mutated.

Decision:
ACCEPT

Notes:
Real Ubuntu 24 installation remains a separate live validation on an exact
approved host. This experiment does not authorize writes to `~/.codex`.
DF-20260817-0000-001 records the non-blocking directory-swap hardening opportunity.

## EXP-20260816-001 - Multi-Runtime Registry Write Containment

Date: 2026-08-16
Status: ACCEPTED

Problem:
The multi-runtime setup flow writes status and preference files after a user
declines template installation, allowing a symlinked runtime `registry/`
directory to redirect those writes outside the selected runtime home.

Evidence:
Security review reproduced the redirected write with exit status zero.

Hypothesis:
Validating each selected runtime and its `registry/` directory as regular,
non-symlinked directories before any setup-owned file write will fail closed
and prevent writes outside the selected runtime home.

Solution Attempt:
Add a narrow runtime-registry validation helper and a regression test; retain
the existing installer, reset, and template overwrite behavior.

Test:
Run the regression against a symlinked `registry/`, then focused setup tests,
syntax checks, and the full regression suite.

Success Criteria:
- A redirected registry path exits nonzero without creating files outside the runtime.
- Normal selected runtimes still receive their status and preference files.
- Existing symlink and installer safety tests remain green.

Result:
The new regression failed before the fix by writing both files outside the
selected runtime through a symlinked registry. The first fix prevented that
write, but review found that its single system write could publish truncated
content. The revised writer loops until every byte is written before fsync and
atomic replacement, then preserves an existing regular file's mode. A later
review found the first mode fix overrode restrictive umasks for new files; the
final revision retains the caller umask for new files and preserves existing
modes. Tests assert complete content, preserved restrictive permissions, and a
new-file `077` umask result.

Decision:
ACCEPT

Notes:
This record covers only setup-owned registry writes after a declined template installation.

## EXP-20260815-003 - Autonomous Main Plan Execution

Date: 2026-08-15
Status: ACCEPTED

Problem:
The per-task approval gate creates unnecessary user pauses inside a disclosed
and approved multi-phase plan.

Hypothesis:
One initial main-plan approval can reduce interaction while preserving explicit
approval for destructive, High, and Critical operations.

Solution Attempt:
Project the same main-plan, auxiliary-task, recommended-task, and terminal
reporting policy to Codex, Claude, and OpenCode.

Test:
Require policy-contract, portable-install, and safety-regression tests.

Success Criteria:
Planned work proceeds without boundary approvals while safety approvals remain
mandatory and all variants expose equivalent behavior.

Evidence:
- The four canonical policies expose one equivalent Main Plan Execution
  contract, and the installed Codex, Claude, and official OpenCode policies
  byte-match their sources. The legacy OpenCode copy matches the changed
  approval sections while retaining its expected runtime-path substitution.
- Clause-removal and contradictory-policy mutants reject missing plan,
  deviation, recommendation, terminal-report, and destructive-safety terms.
- Focused suites passed 5/5, 25/25, and 11/11; the full suite passed 343/343.
- Code review passed after strengthening the public documentation contract;
  security review found no authority widening, backup issue, secret exposure,
  record loss, or duplicate archive entry.

Result:
Core policy 2.5 now uses one approved ordered plan for uninterrupted disclosed
work across Codex, Claude, and OpenCode. Required plan deviations and all
destructive, High, or Critical operations remain separately approval-gated.
Auxiliary and recommended work stay outside automatic main-plan execution, and
terminal reporting remains evidence-based. Active global policies were updated
with private rollback material and require a new runtime session to be loaded.

Decision:
ACCEPT

## EXP-20260815-002 - Official Native Claude and OpenCode Parity

Date: 2026-08-15
Status: ACCEPTED

Problem:
The approved CMA core-tool activation is currently Codex-only. Claude and
OpenCode have incomplete native projections, while the retired Dolphin source
variant remains selectable.

Hypothesis:
An additive, official-schema-only activation path can project the ten protected
skills and narrow vendor-documentation skills to the native Claude and OpenCode
locations without overwriting unmanaged configuration, credentials, or MCP
entries; removing Dolphin only from repository selection preserves its existing
installed runtime.

Solution Attempt:
Use the canonical Claude/OpenCode projections, vendor-native skill layouts, and
the installed stable CLIs' documented configuration surfaces. Add conflict-aware
native activation, remove Dolphin from the source catalog, and update the
corresponding installer, tests, and user documentation.

Test:
Require positive, idempotency, unmanaged-content preservation, conflicting
managed-content rejection, Dolphin rejection, syntax, focused, and full-suite
checks before active-runtime verification. Do not embed credentials, enable
xcodebuildmcp, execute cplt payloads, or delete the existing Dolphin runtime.

Decision:
ACCEPTED

Result:
The source catalog now exposes only Codex, Claude, and OpenCode; existing
Dolphin runtime data was not removed. Official native Claude and OpenCode skill
locations now contain the ten protected projections plus their own narrow
vendor-documentation skill. Existing conflicting Claude managed files were
replaced only after explicit per-file approval and saved in owner-only backup
directories. OpenCode activation rejects unsafe ancestors and managed-path
symlinks, rolls back created files on publication failure, preserves unrelated
configuration, and has no configured MCP server added by this change.

## EXP-20260815-001 - Global Codex Core Tool Activation

Date: 2026-08-15
Status: ACCEPTED

Problem:
The ten protected CMA repository-tool capabilities exist as canonical skills and
inactive native projections, but the active Codex runtime does not discover all
ten globally. Context7 is still classified as optional, and there is no bounded,
conflict-aware activation path that preserves customized global skills and MCP
configuration.

Evidence:
The protected registry marks Context7 optional, the Codex profile reports zero
projected instances and explicit-only inactive representation, and only Graphify
is present among the ten global CMA tool skills. Serena, DeepWiki, GitHub, and
Context7 MCP servers are enabled; xcodebuildmcp is disabled. Existing accepted
experiments explicitly stopped before active runtime synchronization.

Hypothesis:
Changing the canonical/projection contracts to required lazy routing and adding
one additive, atomic Codex activator will make the ten capabilities globally
discoverable while selecting only the narrowest provider, preserving customized
Graphify state, keeping cplt explicit, and avoiding latency/context fan-out.

Solution Attempt:
Use the existing ten canonical skills and Codex projections. Make Context7 a
required capability, enable conditional implicit invocation for the nine
non-cplt skills, keep cplt explicit-only, update the compact repository router,
and add a conflict-aware activator that stages writes, creates private backups,
preserves unrelated state, merges only owned MCP flags, and rolls back on any
failure. Synchronize only the approved active Codex runtime after temporary-home
tests and mandatory reviews.

Test:
Capture focused RED for the old optional/inactive state and missing activator.
Then validate exact skill IDs and policy split, single-provider routing,
Context7 required MCP semantics, Graphify preservation, conflict and symlink
refusal, private backup, rollback, idempotency, secret-safe output, no command
execution, xcodebuildmcp disabled state, focused coverage, full regression,
static checks, live global inventory, functional MCP calls, and fresh-session
routing probes.

Success Criteria:
- Exactly the ten protected skills are globally discoverable; nine are
  conditionally implicit and cplt remains explicit-only.
- Context7 is required but queried only for a bounded version-specific
  documentation need; one evidence gap never fans out across providers.
- Existing customized skills, unrelated global files, credentials, modes, and
  MCP/plugin settings remain unchanged.
- Activation is atomic, private-backup-backed, idempotent, and exactly
  rollbackable; differing or symlinked managed targets fail closed.
- xcodebuildmcp remains disabled and no cplt payload, scanner, or Graphify build
  runs during activation.
- Focused and full tests, code review, security review, and live verification
  pass without commit or push.

Result:
The bounded activator completed successfully against the active Codex runtime
and a second run was a no-op without creating another backup. Exactly ten
protected skill routes are globally discoverable: the preserved customized
legacy Graphify route plus nine official user-global projections. cplt remains
explicit-only; the other nine routes are conditionally implicit. Only the owned
MCP flags changed, Context7 is enabled and required, xcodebuildmcp remains
disabled, unrelated configuration is semantically unchanged, the router matches
the approved source, and the private backup uses a 0700 directory with 0600
files. Read-only live calls succeeded for Serena, DeepWiki, GitHub, and Context7.
A fresh ephemeral Codex session reported all ten skills and used only local `rg`
for the inventory request without MCP fan-out, scanner execution, cplt payloads,
or a Graphify build. Focused activation tests passed 19/19 with 80% branch
coverage; the full suite passed 328/328; code and security reviews passed.
The fresh inventory probe consumed 80,079 input tokens, of which 57,600 were
cached, so an actual total-token reduction versus a pre-activation baseline
remains unverified.

Decision:
ACCEPTED

Notes:
User approved the complete repository, global synchronization, restart/fresh
session verification, and mandatory orchestration scope with option A. This
record does not authorize credential changes, dependency upgrades, commit,
push, scanner-wide scans, cplt payload execution, or xcodebuildmcp activation.
Acceptance covers safe global availability and narrow lazy routing; it does not
claim a measured token-cost reduction.
