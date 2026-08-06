# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

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

## EXP-20260806-005 - Archived Bootstrap Experiment Contract

Date: 2026-08-06
Status: ACCEPTED

Problem:
After the required experiment compaction, the full suite failed because the
hypothesis-workflow bootstrap test searches only the active experiment file for
an accepted record that was correctly moved to the indexed archive.

Evidence:
The archive check is healthy, `EXP-20260727-001` exists in
`governance/EXPERIMENTS_ARCHIVE_001.md`, and the only failing assertion expects
that ID in `governance/EXPERIMENTS.md`.

Hypothesis:
If the test reads the active experiment record plus the archive index and its
declared parts, it will preserve the accepted-result contract across supported
record compaction without weakening any content assertion.

Solution Attempt:
Update only the bootstrap experiment test to assemble the supported active and
indexed archive text before applying the existing ID, status, decision, and
approval-boundary assertions.

Test:
Run the focused hypothesis-workflow suite, the complete 60-test suite,
`record_archive.py check --record all`, and `git diff --check`.

Success Criteria:
- The focused and complete suites pass.
- The test still requires the exact bootstrap ID, accepted status, decision,
  and approval-boundary text.
- Archive parts are discovered through the stable index rather than a glob.
- Missing or unindexed records still fail the test.
- Record archive validation remains below threshold and healthy.

Result:
The test now reads the active record, the stable archive index, and only the
archive parts declared by that index before applying the unchanged bootstrap
ID, status, decision, and approval-boundary assertions. The focused suite
passed 7/7, the complete suite passed 60/60, `git diff --check` passed, and the
record archive check reported every record below threshold.

Decision:
ACCEPT

Notes:
This regression fix is limited to test compatibility with the supported record
archive layout created by the current task.

## EXP-20260806-006 - Bootstrap Record Scoped Assertions

Date: 2026-08-06
Status: ACCEPTED

Problem:
Code review found that the archive-compatible bootstrap experiment test checks
generic accepted status and decision strings across all concatenated records,
so another accepted experiment can mask a rejected target bootstrap record.

Evidence:
The test locates `EXP-20260727-001` in the indexed archive but applies the
`Status: ACCEPTED`, `Decision: ACCEPT`, and approval-boundary assertions to the
complete aggregate text rather than the target record block.

Hypothesis:
Extracting the exact `EXP-20260727-001` block by heading boundaries and applying
every semantic assertion only to that block will reject a mutated target record
even when other accepted records remain present.

Solution Attempt:
Change only the bootstrap contract test to require one exact target block and
scope all target assertions to it. Preserve index-driven archive discovery.

Test:
First run a mutation probe demonstrating the current aggregate assertion stays
green when the target status and decision are changed. Then apply the scoped
block assertion, repeat the mutation probe expecting rejection, and run the
focused and complete suites.

Success Criteria:
- The pre-fix mutation probe demonstrates the false positive.
- The post-fix assertion rejects mutated target status or decision values.
- The real focused suite passes 7/7 and the complete suite passes 60/60.
- Archive discovery remains limited to parts declared by the stable index.
- The code-reviewer blocking finding is resolved on re-review.

Result:
The pre-fix mutation probe reproduced the false positive: changing the target
record to rejected still satisfied the aggregate assertions. The updated test
extracts exactly one target record by heading boundaries and scopes every
semantic assertion to that block. The post-fix mutation was correctly rejected,
the focused suite passed 7/7, the complete suite passed 60/60, and
`git diff --check` passed.

Decision:
ACCEPT

Notes:
This experiment reopens only the test-integrity scope identified by code review.

## EXP-20260806-007 - Provider-Aware Claude Runtime Integration

Date: 2026-08-06
Status: ACCEPTED

Problem:
The portable CMA runtime catalog and installers support Codex and Dolphin, but
their file contracts assume Codex-native `AGENTS.md`, `config.toml`, and TOML
agents. Those assumptions cannot safely install or initialize Claude's native
`CLAUDE.md`, `settings.json`, and Markdown subagent surfaces.

Evidence:
The pre-change catalog contains only `codex` and `dolphin`; the installer
unconditionally reads `AGENTS.md` and `config.toml`; project init and upgrade do
not manage a Claude bridge. The complete pre-change suite passed 60/60, and the
dirty-worktree inventory was captured before implementation.

Hypothesis:
If provider-specific policy, settings, agent format, and launcher metadata are
declared in the variant catalog, a native Claude variant and project bridge can
be added without weakening Codex/Dolphin behavior or overwriting local files.

Solution Attempt:
Add RED contracts first, then implement catalog-driven installation, a native
Claude launcher using `CLAUDE_CONFIG_DIR`, minimal safe settings, four distinct
Markdown chain agents, compatible skills, and an `@AGENTS.md` project bridge
with preservation-aware init and upgrade behavior.

Test:
Run the focused RED/GREEN suites, the complete unittest suite, shell and Python
syntax checks, JSON parsing, isolated temporary-home installs and launcher
stubs, `git diff --check`, and independent code and security reviews.

Success Criteria:
- RED failures prove the missing Claude and provider-aware behaviors.
- All catalog variants install only their declared policy and settings files.
- Claude launcher forwards arguments and exit status without exposing secrets.
- Existing and customized project Claude files are preserved or archived only
  after explicit init confirmation.
- Codex and Dolphin regressions remain green and the mandatory chain stays
  exactly `planner -> tdd-guide -> code-reviewer -> security-reviewer`.
- No SDK dependency, real credential, network call, active runtime mutation,
  commit, push, release, deployment, skipped test, or weakened assertion occurs.

Rollback:
Before a commit, remove only files introduced by this experiment and reverse
only its narrow tracked hunks with `apply_patch`; do not use destructive Git
commands. Temporary install fixtures are disposable and never target active
runtime homes. Project init recovery uses its timestamped archive.

Result:
The valid RED cycle demonstrated the absent third variant, provider metadata,
Claude runtime files, launcher behavior, and project bridge before production
implementation. The provider-aware installer, native Claude runtime, project
bridge, preservation-aware upgrade behavior, and four user guides were then
implemented without dependencies or active runtime writes.

The first code review found launcher-name traversal, launcher-mode mutation,
and project `.claude` parent-symlink defects. Direct RED regressions reproduced
all three before fail-closed fixes; code re-review passed. Security review then
reproduced a managed-directory symlink escape in the installer. A final RED
attack test proved the outside write, and the fix added managed-tree preflight
plus per-target ancestor checks. Code and security re-reviews both passed.

The final complete suite passed 88/88. Shell and Python syntax checks, both
Claude settings JSON parses, catalog listing, and `git diff --check` passed.
No test was skipped or weakened. No SDK dependency, credential, real Claude
call, active runtime mutation, commit, push, release, or deployment occurred.

Decision:
ACCEPT

Notes:
User approval covers local Phases 0 through 4 only. Agent SDK work, credentials,
live activation, commit, push, and deployment remain separately gated.

## EXP-20260806-008 - Bounded Claude Agent SDK Adapter Pilot

Date: 2026-08-06
Status: ACCEPTED

Problem:
The native Claude runtime is complete, but the project has no bounded
programmatic adapter for the Claude Agent SDK. Direct SDK use could mistake
tool approval for isolation, report incomplete streams as success, leak local
settings into a session, or duplicate cost through retries.

Evidence:
Phase 5 remains pending in the task tracker. Current official SDK documentation
defines `query()` as an async iterator, exposes restrictive option fields and
terminal `ResultMessage` metadata, and explicitly states that `allowed_tools`
auto-approves tools rather than restricting the available toolset.

Hypothesis:
An isolated Python adapter pinned to `claude-agent-sdk==0.2.130`, with empty
tool and setting sources, bounded requests, explicit session validation, no
automatic retry, and fail-closed terminal mapping can provide an offline-
testable programmatic contract without credentials or a real API call.

Solution Attempt:
Add RED tests first, then implement a small adapter under
`adapters/claude-agent-sdk/` with an exact dependency lock, injected query
boundary, restrictive options, timeout/cancellation cleanup, truthful result
mapping, and cost/token/session observability.

Test:
Run frozen dependency resolution, adapter unit tests with SDK-shaped local
messages and injected async iterators, the complete root regression suite,
syntax and diff checks, and independent code and security reviews.

Success Criteria:
- Exact SDK pin and lockfile install reproducibly with Python 3.10+.
- Tests prove query invocation, request bounds, session modes, permissions,
  cleanup, no retry, timeout, cancellation, and truthful terminal mapping.
- Only one verified non-error terminal result can report `success=True`.
- Missing cost or token values remain unknown rather than becoming zero.
- No credential, real API call, active runtime mutation, commit, push,
  deployment, skipped test, weakened assertion, or hidden retry occurs.

Rollback:
Remove only the new adapter directory and reverse only the tracker, experiment,
and changelog hunks owned by this phase. Do not use destructive Git commands or
modify the completed native Claude runtime.

Result:
Meaningful RED runs rejected permissive options, hardcoded success, lost
terminal metadata, missing query invocation, swallowed cancellation during
stream cleanup, error-bearing terminal success, and an accidentally live SDK
default. The completed adapter pins `claude-agent-sdk==0.2.130`, disables
built-in tools and settings sources, validates request and session bounds,
performs no retry, closes streams, preserves external cancellation, and maps
incomplete or error-bearing terminal evidence fail-closed.

The final adapter suite passed 21/21 with 92% combined line/branch coverage.
Frozen lock validation and synchronization, Python compilation, `git diff
--check`, and the complete 88/88 root regression suite passed. Code review
found and verified fixes for cancellation and explicit terminal error metadata.
Security review found and verified a default-deny fix preventing accidental
credential-backed SDK execution. No credential was inspected, no real Claude
call was made, and no active runtime, commit, push, or deployment change
occurred.

Decision:
ACCEPT

Notes:
The user approved Gate B by asking implementation to continue after the native
phase. Gate C must add a separate per-call authorization capability, isolated
workspace and Claude configuration, and a minimal allowlisted child-process
environment. Gates C through F remain pending.
