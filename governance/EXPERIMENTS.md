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

## EXP-20260806-010 - Portable Codex Subagent Restoration Prompt

Date: 2026-08-06
Status: ACCEPTED

Problem:
The current Codex runtime has a verified token-conscious 12-agent matrix, but
there is no installed CMA prompt for restoring that matrix without embedding a
specific user's absolute home path or re-generating the full agent bodies.

Evidence:
The managed Codex variant and active runtime contain eight default agent TOMLs
plus four conditional Sol variants, all at medium reasoning. The portable
installer rewrites a selected runtime home but does not currently install a
`prompts/` tree or prefer an active `CODEX_HOME` when no explicit target is
provided.

Hypothesis:
A concise restoration prompt derived from the authoritative agent TOMLs,
installed through a dynamically resolved runtime home, will make recovery
portable while preserving the current model quality and reducing repeated
discovery, generated output, and reasoning-token pressure.

Solution Attempt:
Add a Codex-only restoration prompt, teach the shared variant installer to
manage optional prompt trees and prefer an explicit target, then `CODEX_HOME`,
then the selected variant's current-user default. Preserve no-overwrite and
symlink protections. Validate source before narrowly synchronizing only the
prompt into the active Codex home.

Test:
Add RED contracts for the prompt's exact live TOML-derived inventory, portable
runtime resolution, real installer output, no-overwrite preservation, and
prompt-directory symlink rejection. Then run focused, related, and complete
regressions, shell syntax and diff checks, active source-target hashes, and
independent code and security reviews.

Success Criteria:
- No fixed username or `/Users/.../.codex` path appears in the prompt.
- Exactly eight default roles and four conditional Sol variants retain their
  current friendly identities, models, medium reasoning, and sandboxes.
- The mandatory chain remains unchanged and no high-reasoning role is added.
- Installer resolution is explicit target, active `CODEX_HOME`, then the
  selected current-user default.
- Existing prompt files are preserved without force and prompt-directory
  symlink escapes fail before outside mutation.
- Source tests pass before a narrow, hash-verified active prompt sync.
- Config, auth, agent TOMLs, registries, skills, other providers, commit, push,
  and deployment remain unchanged.

Result:
The initial five-test RED run produced four failures and one missing-file
error for the absent prompt, missing installer transport, ignored
`CODEX_HOME`, and missing prompt-directory preflight. The first implementation
then passed the focused 5/5 checks, related suites at 17/17, 21/21, and 11/11,
and the complete 111/111 regression suite. Shell syntax and diff checks passed.

The approved narrow activation installed only the new prompt into the resolved
active Codex home. Its SHA-256 matched the managed source and the protected
runtime surface hash remained unchanged. Independent code review then found
that the symlink test did not yet prove fail-before-write behavior. A second
meaningful RED test reproduced policy overwrite before the symlink failure.
Adding `prompts` to the pre-write managed-directory validation made that test
and the focused 5/5 checks pass while preserving both target and outside
sentinels.

After remediation, the installer suite passed 17/17 and the complete suite
passed 111/111. Shell syntax and diff checks passed. Code re-review and security
review both passed with no remaining blocking finding; security review
confirmed fail-before-write path containment, no-overwrite behavior, quoted
runtime resolution, and no credential, auth, dependency, external-service, or
destructive-operation change.

Decision:
ACCEPT

Notes:
The user approved Codex source, tests, records, and narrow active prompt
synchronization. Claude adaptation is planning-only after Codex closure.

## EXP-20260806-011 - Portable Claude Subagent Restoration Prompt

Date: 2026-08-06
Status: ACCEPTED

Problem:
The portable Claude CMA variant has the verified 12-agent Sonnet/Opus matrix
but lacks an installed recovery prompt that derives the current Markdown/YAML
definitions without embedding a machine-specific user path or duplicating full
agent bodies.

Evidence:
The Claude source contains eight canonical agents and four conditional Opus
variants, all at medium effort. The shared installer now transports optional
prompt trees safely, but the Claude package has no prompt to install and its
exact manifest remains 34 files.

Hypothesis:
A Claude-native restoration prompt derived from authoritative frontmatter and
installed only into an explicitly selected isolated runtime will provide
portable recovery with bounded token use while preserving models, effort,
tools, permissions, orchestration, and active native Claude isolation.

Solution Attempt:
Add one Claude prompt and document it. Reuse the existing provider-neutral
installer prompt transport without changing installer behavior unless RED
evidence requires it. Validate source and an isolated installation before
narrowly synchronizing the prompt to the current user's isolated CMA Claude
runtime, never the active native Claude home.

Test:
Add RED contracts for the 35-file manifest, actual frontmatter-derived role
rows, target-resolution order, token/model rules, exact chain, explicit-runtime
installation, no-overwrite preservation, and provider-neutral symlink
preflight. Run focused Claude and installer suites, complete regressions,
syntax/diff checks, isolated source-target hashes, and independent reviews.

Success Criteria:
- The prompt contains no fixed username or machine-specific absolute path.
- Exactly 12 roles preserve their actual identity, model, medium effort, tools,
  and permission mode, including four conditional Opus replacements.
- Target resolution is explicit target, non-empty `CLAUDE_CONFIG_DIR`, then
  the current user's `${HOME}/.claude`.
- No Codex agent format, Codex model identifier, `-sol` role, unsupported token
  field, extra chain stage, or broad escalation is introduced.
- The installer copies the prompt to an explicit isolated runtime, preserves
  existing prompts without force, and rejects prompt symlinks before writes.
- Source validation precedes a narrow hash-verified sync to the isolated CMA
  Claude runtime; `${HOME}/.claude` remains unchanged.
- Settings, credentials, native Claude, SDK, dependencies, commit, push, and
  deployment remain unchanged.

Result:
The initial source RED produced one manifest failure and one missing-file error:
the package had 34 files and no Claude restoration prompt. The installer RED
kept the Codex, no-overwrite, and symlink cases green while the Claude explicit
install subcase failed because no source or installed prompt existed.

After adding only the Claude-native prompt and README entry, the focused source
checks passed 2/2 and provider-neutral installer checks passed 3/3. The Claude
suite passed 17/17, installer suite 17/17, orchestration suite 11/11, and the
complete suite 112/112. Shell syntax and diff checks passed. No shared installer
implementation change was required.

The isolated CMA Claude runtime did not previously exist, so broad installation
was avoided. Only its `prompts/` directory and the approved prompt were created.
The source and isolated prompt SHA-256 values match, the isolated runtime
contains no other file, and the native `${HOME}/.claude` prompt path remains
absent.

Code review found a high-severity cross-runtime delegation risk: an explicit
target could differ from the active `CLAUDE_CONFIG_DIR` while Sam remained
scoped to the active runtime. After explicit user approval, a meaningful RED
contract required fail-closed target equality, isolated-process continuation,
and governor use only after the effective config directory equals the resolved
target. The corrected contract passed and the prior isolated prompt was saved
in a hash-verified recoverable backup before narrow replacement.

After remediation, the Claude suite passed 17/17, installer suite 17/17, and
complete suite 112/112; shell syntax and diff checks passed. Code re-review and
security review both passed. The updated source and isolated prompt SHA-256 is
`b6e1b926d4f47e8bd5d886eb450378792f4d12fbe05e4fa6ec326978334e17e8`,
and native Claude state remains unchanged.

Decision:
ACCEPT

Notes:
The user approved source, tests, records, and isolated CMA Claude prompt
synchronization only.

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
