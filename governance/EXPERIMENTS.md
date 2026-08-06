# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

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

## EXP-20260806-009 - Full Claude CMA Source Parity

Date: 2026-08-06
Status: ACCEPTED

Problem:
The packaged Claude runtime exposes the mandatory four-role chain and four
skills, but it does not yet carry the complete Codex Core CMA policy, canonical
role catalog, escalation roles, lazy modules, registry records, or archive
helper. Existing tests prove only the reduced Claude contract and can pass
while these semantic parity gaps remain.

Evidence:
The pre-change Claude source contains 14 home files, four agent definitions,
four abbreviated skills, and three registry files. The Codex source contains
38 home files, including 12 agents, four complete skills, eight lazy modules,
six registry records, and the record archive script. Four Codex-only
`skills/*/agents/openai.yaml` files are not portable Claude artifacts.

Hypothesis:
If provider-neutral CMA assets are copied byte-for-byte and provider-specific
surfaces are translated to documented Claude Markdown/YAML, model, permission,
and configuration conventions, Claude can reach full semantic CMA parity
without copying Codex-only runtime metadata or activating a local Claude home.

Solution Attempt:
First add semantic parity tests that reject the reduced package. Then package
the 34-file Claude-native manifest: the complete Core policy, 12 agents, four
skills and archive helper, eight lazy modules, six registry records, safe
settings, and updated runtime documentation. Preserve the mandatory chain
exactly and map complex Codex escalation roles to explicit Claude Opus roles.

Test:
Run a focused RED test before production edits. After implementation, verify
the exact manifest, agent frontmatter and model matrix, policy/router semantics,
byte-identical provider-neutral assets, adapted registry consistency, archive
helper behavior and executable mode, isolated installation, prohibited artifact
absence, complete regression suite, diff checks, and independent code and
security reviews.

Success Criteria:
- The RED run fails for observable missing policy, role, module, registry, and
  archive-helper behaviors rather than counts alone.
- The Claude home contains exactly the approved 34-file native manifest.
- Eight canonical roles and four `-opus` escalation roles use valid Claude
  frontmatter, medium effort, least-authority tools, and documented models.
- Core policy sections, all eight lazy routes, skills, modules, and registry
  indexes are semantically consistent with Codex CMA.
- No `openai.yaml`, `*-sol` role, Codex model ID, Codex-only TOML agent field,
  credential, hook, or permission bypass is packaged.
- Focused and complete suites pass without skipped or weakened tests, followed
  by clean code and security reviews.

Rollback:
Reverse only files and tracker records owned by this experiment with
`apply_patch`. Do not modify active `~/.claude`, use destructive Git commands,
or disturb unrelated repository work.

Result:
The initial semantic RED run produced seven failures and ten missing-file
errors, proving the reduced 14-file Claude package did not satisfy the 34-file
contract despite the old focused suites passing. The completed package now
contains the full Core policy, 12 native agents, four complete skills, the
record archive helper, eight lazy modules, six registry records, and safe
settings. Source and isolated-install manifests match byte-for-byte, while
Codex-only model, TOML, `*-sol`, and OpenAI skill metadata remain excluded.

Code review rejected mechanically backdated Claude audit history. A dedicated
RED regression exposed all seven false date headings; the audit log now records
only evidenced 2026-08-06 Claude changes and code re-review passed.

Security review then reproduced `docs` and `governance` parent-symlink escapes
in the shared archive helper. After explicit user approval, the canonical
Codex, Dolphin, and Claude scripts were hardened with `O_NOFOLLOW` directory
descriptors for managed reads, atomic replacement, and rollback deletion. A
second RED regression exposed a post-replace `fsync` rollback gap; registering
paths before writes restored transaction rollback. Code and security re-reviews
both passed.

Final focused security/parity verification passed 48/48 and the complete root
suite passed 106/106. JSON parsing, executable modes, exact 34-file manifest,
three-provider script byte parity, prohibited-pattern search, Python source
compilation, and `git diff --check` passed. No credential, real API call,
active runtime mutation, dependency addition, commit, push, or deployment
occurred.

Decision:
ACCEPT

Notes:
User approval covers repository source parity and offline verification only.
Local/global Claude activation, credentials, real API use, commit, push, and
deployment remain outside this experiment. The user separately approved the
shared archive-helper security remediation required to close review.
