# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260807-001 - Native Claude Global CMA Activation

Date: 2026-08-07
Status: ACCEPTED

Problem:
The Claude variant defaults to `${HOME}/.llm-runtimes/claude`, so the portable
CMA package is isolated from Claude Code's native user-global `${HOME}/.claude`
surface and is not available to normal Claude sessions.

Evidence:
The variant catalog and launcher select the isolated runtime. The current
user's native `${HOME}/.claude` already contains `CLAUDE.md`, `settings.json`,
skills, and runtime state, while the isolated CMA directory contains only the
restoration prompt. Official Claude Code documentation defines
`${HOME}/.claude` as user scope and `CLAUDE_CONFIG_DIR` as an override.

Hypothesis:
A dedicated native activation overlay can make CMA available to normal Claude
Code sessions while preserving existing instructions, settings, credentials,
history, plugins, and unrelated files. A separate managed policy plus one
idempotent import avoids replacing the existing global `CLAUDE.md`.

Solution Attempt:
Change the Claude default home to `${HOME}/.claude`. Delegate only native-home
installs to a transactional activation helper that validates all source and
target paths before writes, preserves existing settings byte-for-byte, backs
up and appends one `@registry/CMA_GLOBAL.md` import to existing instructions,
installs missing CMA-owned files, rejects conflicts, and rolls back partial
activation. Keep explicit non-native installs portable and leave the legacy
isolated directory unchanged.

Test:
Add RED contracts for native default resolution, complete preservation-aware
activation, idempotency, functional import detection, conflict and symlink
rejection, rollback after copy failure, and incomplete source rejection. Run
focused Claude activation, installer, runtime, and complete regression suites,
shell syntax, JSON, diff, source-target parity, live native state preservation,
and independent code and security reviews.

Success Criteria:
- Default Claude installation resolves to `${HOME}/.claude`; explicit alternate
  runtime homes continue to use portable isolated installation behavior.
- Existing `CLAUDE.md` content and mode are preserved with exactly one
  functional CMA import and a byte-identical recoverable backup.
- Existing `settings.json` bytes and mode never change.
- Missing CMA agents, skills, registry, prompt, README, and launcher files are
  installed; differing CMA-owned files fail before mutation.
- Symlink, unsafe-type, incomplete-source, backup, and late-copy failures do
  not leave partial activation or touch unrelated native Claude state.
- Repeated activation is byte- and path-idempotent.
- The legacy `${HOME}/.llm-runtimes/claude` tree remains unchanged.
- Focused and complete tests, syntax, diff, live hashes, and independent code
  and security reviews pass before acceptance.

Result:
The initial native-activation contract produced seven intended failures: the
catalog still selected the isolated home, no preserved import or backup was
created, force and differing managed files did not fail closed, incomplete
sources reported success, and a symlinked native home could be followed.

The first implementation passed 8/8 focused checks, both related suites at
17/17, and the then-complete 120/120 suite. Live activation created a
byte-identical policy backup, preserved existing policy and settings modes,
preserved the settings and legacy-runtime hashes, installed the complete CMA
surface with source parity, and remained idempotent on a second run.

Independent code review then found an equivalent-path force bypass and two
partial-backup cleanup gaps. New RED cases reproduced trailing, dot, and
symlink-alias bypasses plus partial copy and post-move hash failures. Canonical
native routing, non-native root-symlink rejection, atomic backup writes, and
explicit incomplete-backup tracking resolved them. The durable plan was also
updated to reflect the approved activation.

Security review found insecure first-install permissions under an open umask.
The new regression reproduced `0777` directories and a `0666` instruction
bridge. Applying `umask 077` before creation made new directories `0700`, new
files `0600`, and the launcher `0700` without changing existing file modes.
Task-created live directory trees were narrowed from `0755` to `0700`.

Final activation checks passed 10/10, installer and Claude runtime suites each
passed 17/17, and the complete suite passed 122/122. Bash syntax and diff
checks passed; ShellCheck was unavailable. Final code review and security
review both passed with no blocking findings. No credentials, sessions,
plugins, authenticated Claude request, legacy deletion, commit, push, or
deployment were involved.

Decision:
ACCEPT

Notes:
The user explicitly approved active native Claude CMA activation with a
preservation-first merge. Credential use, authenticated Claude requests,
legacy deletion, commit, push, and deployment remain outside scope.

## EXP-20260807-002 - CMA Self-Hosted Codex Runtime Alignment

Date: 2026-08-07
Status: ACCEPTED

Problem:
The CMA repository uses its own project instructions and user-global Codex
runtime, but the project remains a legacy-safe bootstrap without
`.codex/template-state.json`. Its project config and configuration prompt are
older than the current templates, while selected active `${HOME}/.codex` CMA
policy files differ from the current Codex variant.

Evidence:
The read-only project upgrade reports `State: legacy-safe bootstrap`, preserves
both legacy managed files, and would create template state. Direct comparison
shows the active global policy, runtime README, and orchestration gate are
older than their packaged sources. Other differing global files contain user
preferences, runtime audit history, or stricter record/archive behavior and
must not be overwritten as ordinary template drift.

Hypothesis:
A preservation-first, targeted alignment can make the CMA repository use the
current project templates and selected current Codex policy surfaces without
weakening stronger active overrides or changing user configuration, secrets,
sessions, audit history, or unrelated runtime state.

Solution Attempt:
Back up every file that will change. Align the project config and generated
configuration prompt with their current templates, then create managed Codex
template state. Synchronize only the active global policy, runtime README, and
orchestration gate that are demonstrably older than source. Preserve
`config.toml`, setup preferences, status messages, audit history, record
contracts, archive implementation, credentials, sessions, and extra files.

Test:
Verify pre-change backups and hashes, project-template byte parity, valid TOML
and JSON, managed-state ownership, a clean second project upgrade dry-run,
source parity for the three approved global files, unchanged hashes for every
explicitly preserved global file, focused upgrade/orchestration tests, the
complete regression suite, and final Git diff integrity.

Success Criteria:
- Project config and configuration prompt match the current templates.
- `.codex/template-state.json` records variant `codex`, schema version 1,
  current template version, and matching managed hashes.
- A second project upgrade dry-run reports managed `UNCHANGED` state.
- The approved active global policy, README, and orchestration gate match their
  packaged sources byte-for-byte.
- Global config, preferences, status messages, audit history, record contracts,
  archive implementation, and unrelated runtime files remain byte-identical.
- Every changed pre-update file has a recoverable hash-recorded backup.
- Focused and complete regressions pass without weakened assertions or skipped
  checks.

Result:
The legacy baseline reproduced the expected drift: both project-managed files
differed from their templates, template state was absent, and the selected
global policy files differed from source. A restricted backup captured all
five changed pre-update files with verified SHA-256 manifests under
`/Users/iyilmaz/CodexBackups/cma-self-update-20260807T100340Z-qg3IdP/`.

The project config and configuration prompt now match their templates
byte-for-byte. Template state records schema version 1, template version 2.2,
variant `codex`, merge ownership for `AGENTS.md`, and managed hashes for both
project template files. A second upgrade dry-run reports managed state with
`UNCHANGED` for every path.

The active global policy, runtime README, and orchestration gate match their
packaged sources. Hash verification confirms the global config, audit log,
setup preferences, status messages, stricter records module, record archive
skill, modular archive scripts, and unrelated runtime state were preserved.

Project upgrade, orchestration, and lazy-runtime focused suites passed 52/52;
the complete regression suite passed 122/122. Backup manifests, TOML and JSON
parsing, source parity, preserved hashes, idempotency, and `git diff --check`
passed. The first TOML validation command selected Python 3.10 without
`tomllib`; rerunning the same parse with the installed Python 3.13 completed
successfully and did not require a product change.

Decision:
ACCEPT

Notes:
The user selected the full safe update and retained the prior instruction to
work without the orchestration chain. Commit and push are not authorized.

## EXP-20260808-001 - Provider-Neutral OpenCode Runtime Variant

Date: 2026-08-08
Status: ACCEPTED

Problem:
The CMA runtime catalog supports Codex, Dolphin, and Claude, but it has no
OpenCode-native package. Reusing a Codex or Claude runtime would expose the
wrong settings and agent formats, while writing directly into the active
`~/.config/opencode` tree could overwrite provider, model, permission, plugin,
or user-preference state.

Evidence:
The catalog lists three variants and the installer has no OpenCode entry. The
installed OpenCode 1.18.15 runtime uses JSON/JSONC configuration, Markdown
agents, lazy skills, `OPENCODE_CONFIG`, and `OPENCODE_CONFIG_DIR`. The Browser
Renderer pilot also resolves its Graphify plugin twice because its explicit
path is interpreted relative to `.opencode` while the same plugin is
auto-discovered from `.opencode/plugins`.

Hypothesis:
An isolated provider-neutral runtime under
`${HOME}/.llm-runtimes/opencode`, launched through `llm-opencode`, can expose
the Core CMA policy, Markdown agents, skills, registry, and prompts without
changing the native OpenCode configuration or hardcoding a provider/model. A
variant-aware project template can preserve unrelated `.opencode` content and
remove the pilot's redundant explicit plugin path without weakening existing
Codex, Dolphin, or Claude behavior.

Solution Attempt:
Add an `opencode` catalog entry, stable-schema runtime config, neutral launcher,
Markdown CMA agents, portable skills and registry, provider-aware project
init/upgrade ownership, regression tests, and user documentation. Validate the
source in temporary runtime homes before the approved Browser Renderer pilot;
do not install or activate the variant in the native global runtime.

Test:
Capture meaningful RED failures for the missing catalog, runtime package,
launcher, agent contracts, and project preservation behavior. Then run focused
OpenCode, installer, project-upgrade, and Claude regression suites; the complete
unittest suite; JSON and Bash validation; source/install parity; prohibited
provider/V2 scans; Browser Renderer OpenCode discovery checks; diff integrity;
and independent code and security reviews.

Success Criteria:
- `opencode` installs to an explicit or isolated runtime with an executable
  launcher and no writes under native `~/.config/opencode`.
- Runtime policy and agents preserve truthful reporting and the exact
  `planner -> tdd-guide -> code-reviewer -> security-reviewer` chain.
- Runtime configuration contains no model, provider, credential, plugin, or
  beta V2 settings and validates against the stable OpenCode schema surface.
- Project init and upgrade preserve unrelated `.opencode` files, customized
  managed files, modes, symlink protections, and dry-run behavior.
- Browser Renderer loads Graphify exactly once through automatic discovery
  after removing only the redundant explicit path.
- All focused and complete tests pass without skips, weakened assertions,
  hardcoded success, or regressions in existing variants.

Result:
The initial RED suite exposed the missing catalog, package, launcher,
init/upgrade ownership, and documentation behavior. A later live check showed
that `OPENCODE_CONFIG*` alone still merged native provider/model configuration;
the launcher therefore also isolates config, data, cache, and state through
symlink-protected XDG roots. Independent review then found and drove fixes for
sensitive OpenCode config diffs, private init/upgrade archives, governor write
approval, per-root symlink coverage, and custom runtime path rewriting.

The final complete regression suite passed 141/141 without skips. Bash syntax,
Python compile, JSON parsing, prohibited provider/model/agent scans, manifest
parity, and diff integrity passed. The installed OpenCode 1.18.15 runtime
reported no selected model or providers, eight provider-neutral CMA agents,
approval-gated governor writes, and config/data/cache/state paths entirely
inside `${HOME}/.llm-runtimes/opencode/runtime-state`. The Browser Renderer
pilot resolved Graphify exactly once from `.opencode/plugins/graphify.js` after
removing only the redundant explicit plugin entry. Final independent code and
security reviews returned PASS.

Decision:
ACCEPT

Notes:
The user approved implementation, isolated runtime installation, and the
Browser Renderer pilot. Native `~/.config/opencode`, provider/model/auth state,
dependencies, commits, pushes, and deployments were not changed. Expected low
residual risk remains: the native `opencode` executable is resolved from the
user's `PATH`, and existing project-local plugins execute with user authority.

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

## EXP-20260804-001 - CMA Evidence Claims Contract

Date: 2026-08-04
Status: ACCEPTED

Problem:
CMA evidence reports do not require an explicit claims section, while EV
requires `## Claims` or explicit `Claim:` declarations before it invokes GLM.
Consequently, valid CMA evidence can stop as `UNVERIFIED` before validation.

Evidence:
The active CMA records module requires concise, reproducible proof but defines
no claim syntax. Existing reports commonly use headings such as `Outcome`,
`Implemented`, `Test Evidence`, and `Fresh Evidence`, which EV intentionally
does not interpret as material claim declarations.

Hypothesis:
Requiring one material claim per bullet under an exact `## Claims` heading for
new or materially updated CMA evidence will make future reports EV-compatible
without weakening EV or rewriting historical reports.

Solution Attempt:
Add a prospective claim-format contract to the CMA records module, enforce it
in source and portable-install tests, and add EV integration fixtures that use
the unchanged production parser. After the first real pilot showed GLM quoting
claim declarations instead of supporting proof, strengthen only EV's validation
prompt to require proof outside `## Claims` that directly supports the same
claim; keep the parser and fail-closed checks unchanged.

Test:
Run a meaningful CMA RED test before changing the module, then run focused and
full CMA suites plus focused and full EV suites. Verify portable installation,
unchanged EV runtime code, dirty-worktree isolation, and independent code and
security reviews.

Success Criteria:
- CMA requires the exact `## Claims` heading for new evidence reports.
- Each material claim is one bullet and supporting proof stays outside the
  claims section.
- Historical reports are not rewritten solely for compatibility.
- A representative CMA report passes EV parsing with complete grounded claims.
- Missing coverage and prompt injection remain `UNVERIFIED`.
- No EV parser, schema, hook, dependency, or activation behavior changes; the
  prompt may only be strengthened to align GLM output with existing grounding.
- Active global CMA runtime remains unchanged pending separate approval.

Result:
The CMA contract test first failed in the source and portable installation at
the missing `## Claims` requirement. After implementation, the focused CMA
suite passed 12/12 and the full CMA suite passed 49/49. EV compatibility tests
passed against the production parser, including complete coverage, omitted
claims, and prompt injection.

The first real GLM pilot reached ACP but returned `UNVERIFIED` because GLM cited
claim declarations instead of proof. The revised prompt-only attempt retained
all parser checks and explicitly required proof outside `## Claims` supporting
the same claim. The repeated end-to-end temporary pilot then returned `PASS`.
The final EV suite passed 34/34. Independent code and security reviews both
returned PASS with no blocking findings.

Decision:
ACCEPT

Notes:
Option A was explicitly approved. Commit, push, real-project activation, and
active global runtime synchronization are outside this implementation step.
The first real pilot reached GLM but returned `UNVERIFIED` because two GLM
responses cited claim declarations as proof. A diagnostic response demonstrated
that the same document can produce valid proof excerpts, supporting a prompt-
alignment revision without weakening validation.
The source candidate was accepted before runtime activation. After explicit
option A approval, only the active records module was backed up and synchronized.
Its final SHA-256 matches the source candidate and its mode remains `0644`.

## EXP-20260804-002 - Temporal TDD Evidence Contract

Date: 2026-08-04
Status: ACCEPTED

Problem:
CMA requires explicit claims and grounded proof, but a TDD evidence report can
mix an expected pre-fix RED result with final verification. That structure is
technically truthful yet can make the final state temporally ambiguous.

Evidence:
The current records module does not distinguish initial RED proof from final
verification proof or state which section may support a final-success claim.

Hypothesis:
A conditional two-section rule for reports that contain both expected RED and
final outcomes will remove temporal ambiguity without adding Acceptance
Criteria IDs, mapping tables, or mandatory headings to one-phase reports.

Solution Attempt:
Require exact `## Initial RED Evidence` and `## Final Verification Evidence`
headings only when both phases are documented. Require final-success claims to
use final-section proof from the same validation scope rerun after the fix, and
identify initial RED as historical pre-fix evidence. Apply the rule
prospectively without rewriting historical reports.

Test:
Add source and portable-install contract tests before changing the records
module. Verify the conditional headings, final-proof restriction, unchanged
Claims contract, and absence of Acceptance Criteria schema expansion.

Success Criteria:
- Two-phase TDD evidence has explicit initial and final sections.
- Final-success claims depend only on final verification proof.
- Final success requires the same validation scope to pass after the fix.
- Initial RED is identified as expected historical evidence, not final status.
- One-phase and non-TDD reports do not require temporal headings.
- No Acceptance Criteria IDs or mapping tables are introduced.
- Active global CMA runtime remains unchanged pending separate approval.

Result:
The focused RED run failed two contract tests because the records module lacked
the conditional temporal rule. After the minimal policy change, the focused
suite passed 14/14 and the full CMA suite passed 52/52. Portable installation
was byte-identical to the managed records module. The source candidate was
accepted before active global synchronization.

Security review found that ordering and uniqueness were not part of the CMA
contract, allowing reversed or duplicate temporal headings to misrepresent the
final state. A new RED contract test failed until the module required each
heading exactly once with Initial RED before Final Verification. The focused
14/14 and full 52/52 suites passed again.

Reopened security review found that temporal headings embedded in fenced proof
could still be mistaken for report structure. The CMA contract RED failed until
it explicitly classified fenced or quoted headings as proof text. The focused
14/14 and full 52/52 suites passed again. Reopened code and security reviews
both passed with no blocking findings.

A final scoped RED failed the source and portable contract paths because the
policy did not explicitly require the same validation scope to be rerun after
the fix. One additional rule closed that gap; the focused 14/14 and full 52/52
suites passed again.

Decision:
ACCEPT

Notes:
Implementation, tests, and independent reviews passed.
Approved option A covers local implementation, tests, evidence, and review.
Active global runtime synchronization was initially outside that scope. After
separate explicit approval, the prior active module was copied to
`~/.codex/archive/cma-temporal-evidence-20260804_230500/CMA_RECORDS.md` and the
then-validated source was synchronized. At that time, source and active SHA-256 were both
`c3d4813491a493775db57f24b451e13c5b9168c5a15445113d1f33a72e9299ea`;
the active mode remains `0644`. The later same-scope hardening changed only the
managed source and tests; active runtime synchronization was not repeated.
Detailed evidence is recorded in
`docs/reports/EVIDENCE_EXP-20260804-002_TEMPORAL_TDD_EVIDENCE_CONTRACT_20260804.md`.
