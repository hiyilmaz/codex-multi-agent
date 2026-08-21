# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

## EXP-20260821-001 - Context7 General Setup And Node 22 Preflight

Date: 2026-08-21
Status: ACCEPTED

Problem:
The CMA general setup does not run Context7's official multi-agent setup flow,
and mutating setup entry points do not fail closed when Node.js is older than
the required major version 22.

Evidence:
The current `bin/codex-setup` completes without invoking `npx ctx7 setup`, and
neither it nor `bin/codex-user-install` validates Node.js or `npx` before
runtime mutations. A real Context7 setup configured MCP, rules, and skills for
Claude Code, OpenCode, and Codex under the process user's global home.

Hypothesis:
An early Node.js 22 and `npx` preflight on mutating entry points, followed by an
explicit default-yes `npx ctx7 setup` step at the end of the general wizard,
will provide the requested multi-agent Context7 setup without leaking
credentials or reporting false completion.

Solution Attempt:
Add equivalent fail-closed runtime preflights to `codex-setup` and
`codex-user-install`, preserve read-only help and variant listing without the
preflight, and let the Context7 CLI exclusively own its interactive
authentication and global configuration flow.

Test:
Capture RED and GREEN with real setup scripts and hermetic fake `node` and
`npx` executables. Cover missing, malformed, too-old, boundary, and newer Node
versions; missing `npx`; exact unpinned Context7 argv; explicit skip; exact
failure propagation; secret-free argv/output; custom runtime HOME behavior;
focused regressions; shell syntax; diff checks; and the full repository suite.

Success Criteria:
- Node.js below 22, malformed versions, missing Node.js, and missing `npx` fail
  before runtime or network mutation.
- Node.js 22 and newer allow mutating setup flows to continue.
- Read-only help and variant listing remain available without Node.js or `npx`.
- The accepted Context7 step invokes exactly `npx ctx7 setup` once; an explicit
  rejection invokes nothing.
- Context7 failures preserve their exit status and suppress CMA completion.
- CMA never adds the Context7 API key or token value to argv or its own output.
- Focused and full regression suites pass without real network access.

Result:
The pre-change focused suite produced meaningful RED: Node.js below 22,
malformed versions, missing Node.js, and missing `npx` did not stop mutation;
`codex-setup --list-variants` was unavailable; no Context7 command or exit
propagation occurred; and the required documentation was absent. After the
implementation, the new focused suite passed 8/8, variant-install regressions
passed 31/31, codex-tools integration regressions passed 7/7, and shell syntax
validation passed. The first full regression passed 397/397. Code review then
found that a valid-looking Node version printed by a failing `node --version`
process was accepted because its exit status was swallowed. A dedicated RED
reproduced the false continuation. The revised preflight now treats that exit
status as terminal; the focused suite passes 9/9 and the full regression passes
398/398. Code re-review passed after the fix. Security review passed with no blocking
finding and retained the explicitly accepted risks of unpinned remote `npx`
execution, user-controlled `PATH` resolution, and no transactional rollback for
third-party partial writes. ShellCheck was unavailable; Bash syntax validation
passed instead. The record archive regression passed 19/19, the focused suite
remained 9/9, and the post-archive check reported every managed record below
its compaction threshold.

Decision:
ACCEPT

Notes:
The Context7 command remains interactive and unpinned by explicit user request.
It targets the process user's global agent locations even when CMA uses a
custom runtime home. CMA does not install Node.js or modify shell profiles.

## EXP-20260818-001 - Cross-Platform Atomic Rename

Date: 2026-08-18
Status: ACCEPTED

Problem:
The native Codex activator uses Darwin-only `renameatx_np`, so its fail-closed
atomic publication path is unavailable on Linux and blocks CMA activation.

Evidence:
On blockmanpro Ubuntu 24.04 x86_64, libc exposes `renameat2` but not
`renameatx_np`; the full repository suite ran 385 tests with 13 failures and
5 errors rooted in `atomic_rename_unavailable`.

Hypothesis:
Dispatching the existing exclusive-publish and atomic-exchange semantics to
Darwin `renameatx_np` or Linux `renameat2`, with platform-specific flags, will
restore Linux activation without weakening no-overwrite, descriptor anchoring,
rollback, or cleanup guarantees.

Solution Attempt:
Introduce an explicit semantic-to-platform syscall adapter: Darwin uses
`RENAME_EXCL=4` and `RENAME_SWAP=2`; Linux uses `RENAME_NOREPLACE=1` and
`RENAME_EXCHANGE=2`. Unsupported platforms, symbols, semantics, or kernel and
filesystem support remain fail-closed without a plain rename fallback.

Test:
Capture RED for Linux symbol and flag dispatch before implementation; then run
platform/errno/fallback unit tests, real-host atomic publish/no-overwrite tests,
the focused native-activation suite, Python compilation, whitespace checks,
and the full repository suite. Re-run the focused and full suites on
blockmanpro after separately approved deployment.

Success Criteria:
- Darwin and Linux select their correct libc symbol and exact flags.
- Both source and target remain anchored to the supplied directory FD.
- Existing targets are never overwritten and staging files are cleaned.
- Missing or unsupported atomic operations fail closed without fallback.
- Race, rollback, cleanup, and idempotency regressions remain green.
- The Ubuntu focused and 385-test full suites pass without skips.

Result:
The pre-change focused suite produced the required RED with exit 1: Linux
dispatch attempted no `renameat2` call and raised `atomic_rename_unavailable`;
unsupported syscall and semantic cases also failed. The platform adapter then
passed all 23 focused native-activation tests. Python compilation and
`git diff --check` passed, the full repository suite passed 389/389, and
focused branch coverage for the activator measured 82 percent. Darwin real-host
publication remained idempotent, preserved descriptor anchoring, rejected an
existing target, and left no hidden staging artifact. Commit `85e0412` was then
pushed to both the working branch and `main` and fast-forwarded into the clean
blockmanpro repository. On Ubuntu 24.04 x86_64, the real `renameat2` focused
suite passed 23/23 and the full repository suite passed 389/389, both with exit
0. Independent code and security reviews found no blocking issue.

Decision:
ACCEPT

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
