# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

## EXP-20260817-009 - Blockmanpro Fix Commit Deployment

Date: 2026-08-17
Status: TESTING

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
independent code and security re-reviews pass. Final live deployment remains
pending.

Decision:
NEED_MORE_DATA

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

## EXP-20260811-007 - Native TDD Simplification Evaluation

Date: 2026-08-11
Status: NEED_MORE_DATA

Problem:
EXP-20260811-006 showed that static fixtures and token proxies cannot prove
whether a smaller TDD contract preserves real native-agent output quality or
reduces actual runtime cost across Codex, Claude, and OpenCode.

Evidence:
The Phase 10 candidate was rolled back after independent review found its
quality and tool-use evidence self-declared. All three native CLIs are locally
available, but their raw traces must first prove comparable input/output token,
tool-call, repository-read/search, core-skill, wall-clock, and final-output
measurement. The user approved exactly one bounded line-limit exception for
EXP-20260811-007 in the already over-800-line experiment log. This exception
applies only to this record and does not authorize editing, reordering,
refactoring, archiving, cleaning, or maintaining existing experiment records.

Hypothesis:
Running one fixed baseline and one fixed temporary Phase 10 candidate through
the real native TDD-agent mechanism on four identical bounded tasks can provide
trustworthy cost and behavior evidence without permanently modifying TDD,
runtime configuration, permissions, orchestration, or core skills.

Solution Attempt:
Freeze exactly four task inputs and two prompt contracts before scored runs.
Use ephemeral or isolated invocation inputs only, execute baseline and
candidate natively for Codex, Claude, and OpenCode, retain raw redacted traces
outside active runtime configuration, and score actual final TDD contracts with
one fixed rubric. Do not tune prompts after seeing results or implement the
candidate even if it passes.

Test:
First run a non-scored bounded preflight for each native runtime. Continue to
the 24 scored runs only if every runtime exposes trustworthy actual input and
output tokens, tool calls, repository reads/searches, core-skill invocations,
wall-clock, and final output without persistent runtime/config mutation. Use
the same four inputs for baseline and candidate. Compare acceptance mapping,
meaningful RED, positive, negative, boundary, regression, anti-hardcode, and
missing-information behavior. Require candidate quality to be component-wise
no weaker, repository discovery to decrease, tool calls and input tokens not to
increase, and semantic alignment across all variants.

Success Criteria:
- Baseline and candidate execute as real native TDD agents in all three
  variants with attributable raw measurements.
- The fixed four task inputs and fixed prompt contracts do not change after the
  first scored result.
- Candidate quality is not weaker for any task, dimension, or variant.
- Repository discovery decreases; tool calls and input tokens decrease or stay
  equal; no core skill, scanner, or external knowledge route is invoked.
- Active TDD, runtime configuration, permissions, orchestration, and core-skill
  files remain unchanged.
- If any native trace cannot support trustworthy measurement, stop before
  scored comparison and report `UNVERIFIED` with `success=false`.

Result:
Preflight stopped before any native model evaluation or scored run. The
installed Codex CLI (`codex-cli 0.147.0`) exposes no named-agent selector for
`codex exec`, so a direct native `tdd-guide` run and agent-attributable token
and tool measurements could not be established. OpenCode (`1.18.16`) exposes
`--agent`, but its plugin-free active runtime reported `Agent tdd-guide not
found`; creating or activating a temporary runtime agent definition would
change the evaluation surface prohibited by this phase. Claude exposes native
agent and stream-event options, but all three variants are required, so no
Claude model call was made in isolation. Consequently there are no real
baseline/candidate token, tool, discovery, wall-clock, or quality measurements.
The evaluation is `UNVERIFIED` with `success=false`.

Decision:
NEED_MORE_DATA

Notes:
The line-limit exception is exclusive to EXP-20260811-007. Experiment-log
maintenance remains a separately approved task. This phase evaluates only and
does not authorize permanent candidate installation or later work.

## EXP-20260806-003 - PTY Package Install Stdin Continuation

Date: 2026-08-06
Status: REVISED

Problem:
The approved apt installation completed, but the SSH PTY session returned to a
shell prompt without executing the remaining pinned Codex npm installation and
version-verification commands from the submitted stdin stream.

Evidence:
A separate read-only SSH check confirms `nodejs` 18.19.1 and `npm` 9.2.0 are
installed, no apt or dpkg process remains, and `codex` is still missing. The
original PTY session remains open at a root shell prompt after `needrestart`.

Hypothesis:
The interactive apt/needrestart path consumed or interrupted the remaining
heredoc stdin. Sending the bounded remaining commands directly to the already
open PTY session will complete the approved package step without rerunning apt.

Solution Attempt:
Write only the exact pinned npm install and version/path verification commands
to the existing SSH session, followed by `exit`. Do not rerun apt, open another
package source, or restart services.

Test:
Require the existing session to exit zero, then use a fresh read-only SSH
connection to verify the installed package version, executable path, and
`codex --version` output.

Success Criteria:
- Apt is not invoked again.
- `@openai/codex@0.146.1` is installed through npm's verified global prefix.
- `codex --version` reports the pinned release.
- The original SSH session exits successfully.
- No service or host restart is performed.

Result:
The tool rejected the write with `stdin is closed for this session`; no npm
command was delivered and Codex remained uninstalled. The open-session
continuation mechanism is therefore unavailable even though the remote shell
had previously displayed a prompt.

Decision:
REVISE

Notes:
This experiment addresses only stdin continuation after the already completed
approved package transaction.
