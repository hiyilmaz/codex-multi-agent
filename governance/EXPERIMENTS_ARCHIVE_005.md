# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260801-001 - Local CMA Core And Lazy Runtime

Date: 2026-08-01
Status: ACCEPTED

Problem:
The local CMA runtime loads a broad global policy surface for every task, while
friendly agent naming and conditional model escalation are only partially or
non-operationally represented. This increases token cost and leaves the active
routing behavior weaker than the approved plan.

Evidence:
The approved model matrix is present in the managed Codex variant and active
local global agent files, but Core/Lazy modules do not exist, the global policy
still contains the full detailed guidance, `display_name` is not part of the
documented standalone custom-agent schema, and escalation rules exist only in
planning documents.

Hypothesis:
A compact Core CMA policy plus trigger-loaded registry modules, supported
friendly identities, and reliable static high-risk routing will reduce
default context while preserving the mandatory chain, approval boundaries,
truthful reporting, and test integrity.

Solution Attempt:
Add managed Core/Lazy registry modules, reduce the Codex global policy to the
non-negotiable core and module router, remove unsupported agent metadata, and
encode conditional model/reasoning routing in orchestration policy. Validate
managed source before synchronizing only the approved files into
`/Users/iyilmaz/.codex`.

Test:
Add failing contract tests for module packaging, compact policy routing,
supported agent metadata, the approved model matrix, escalation triggers,
portable installation, and mandatory-chain integrity. Then run focused and
full suites, validate source-to-active equality, and perform bounded default
and escalated runtime probes where the client exposes selected model metadata.

Success Criteria:
- The global Codex policy contains the complete non-negotiable core and a
  compact trigger-to-module index.
- Eight managed modules are packaged and installed by the portable Codex
  installer.
- `display_name` is absent from standalone agent TOML files while friendly
  identities remain in instructions and registry documentation.
- The approved model matrix remains exact and no mandatory role uses Luna.
- Routing defines explicit default and static high-risk variants without
  skipping or reordering the mandatory chain.
- Source tests pass before active runtime synchronization.
- Managed and active local global owned files are checksum-equivalent after a
  fresh targeted backup.
- Pilot evidence separates token/latency observations from quality results.

Result:
The initial RED suite ran five tests and produced 21 failures for missing lazy
modules, an oversized 483-line policy, unsupported metadata, absent escalation,
and incomplete portable packaging. Later RED revisions caught an invalid chain
rendering, missing memory routing, unreliable spawn override assumptions, and
ambiguous read-only precedence.

The final focused suite passed 9 tests and the full suite passed 46 tests in
8.785 seconds. The global policy is now 201 lines, 1,118 words, and 8,443 bytes;
this reduces lines by 58.4 percent, words by 52.4 percent, and bytes by 48.4
percent. Eight lazy modules and fourteen agent TOMLs are packaged and active.
The fourteen TOMLs comprise the approved eight defaults plus six Sol/high
routing variants. Unsupported `display_name` metadata is absent.

Managed and active owned files are byte-equivalent, except the active
append-only audit log intentionally preserves additional local history. The
targeted rollback manifest passed SHA-256 validation. Fresh Terra/medium and
Sol/high sessions completed, and the final routing probe preserved the exact
four-role chain, approvals, memory routing, and security escalation.

Decision:
ACCEPT

Notes:
Scope is limited to this repository and `/Users/iyilmaz/.codex`. Remote hosts,
Hermes profiles, other projects, Dolphin, config, auth, secrets, and plugin
state are excluded.
No subagents were spawned during implementation. Static role selection and
fresh noninteractive sessions were used for bounded runtime validation.

## EXP-20260728-001 - Truthful Success Reporting

Date: 2026-07-28
Status: ACCEPTED

Problem:
The runtime rejects false-positive tests, but its general outcome reporting does
not define a shared status-to-success contract. An agent could therefore report
an unexecuted or unverified task as successful.

Evidence:
The global runtime policies require honesty, and the TDD and reviewer contracts
reject hardcoded success, skipped tests, and swallowed errors. They do not yet
define `passed`, `failed`, `unverified`, and `not_executed` or constrain
`success=true` to verified execution evidence.

Hypothesis:
A short global reporting rule, enforced by source and portable-install contract
tests, will prevent unsupported success claims without changing normal
conversation or adding a mandatory output format.

Solution Attempt:
Add the same minimal outcome-reporting contract to the Codex global template,
the Codex runtime variant, and the Dolphin runtime variant. Keep existing
skills, agents, registries, dependencies, and orchestration behavior unchanged.

Test:
First add contract assertions that fail while the policy is absent. Then verify
the three source policies, Codex mirror equality, portable Codex and Dolphin
installations, the full regression suite, and the active runtime copy and
rollback backup.

Success Criteria:
- Only `passed` may use `success=true`.
- `passed` requires execution, inspected real output, satisfied criteria, no
  remaining critical failure, and concrete evidence.
- `failed`, `unverified`, and `not_executed` always use `success=false`.
- The rule applies only to explicit task, operation, or test outcome reporting;
  it does not impose JSON or status fields on ordinary conversation.
- Both portable runtime variants contain the validated contract.
- The full test suite passes before the active runtime is changed.
- The active runtime update has a verified backup and checksum rollback path.

Result:
The initial RED run executed 10 focused tests and failed five assertions because
the contract was absent. The first GREEN attempt still failed five assertions
because one semantic marker crossed a Markdown line break; whitespace
normalization fixed that test defect without removing any required marker.
The final focused suite passed 10 tests in 1.375 seconds and the full suite
passed 37 tests in 7.716 seconds. Codex mirror equality, portable Codex and
Dolphin installation, and `git diff --check` passed. Independent code review
returned `PASS`, and security review returned `NO_SECURITY_IMPACT`.

The active `~/.codex/AGENTS.md` was backed up before replacement. The backup
matched the prior SHA-256
`34d846dc2db9c3d9f817da01bb4c199914ec243ff972220b0af07458340954ad`;
the active file then matched the validated source SHA-256
`882fc5dc6c62c59085a9da24ba279797e467d7301dcde9119cb1a16b2317cfe3`
with mode `0644`.

Decision:
ACCEPT

Notes:
The user approved repository implementation and a verified, reversible update
of the active local Codex policy. Commit, push, remote deployment, dependency,
API, schema, skill, agent, and registry changes are outside scope.

## EXP-20260727-002 - Event-Driven Record Archiving

Date: 2026-07-27
Status: ACCEPTED

Problem:
Deferred findings, experiments, and changelog files grow without bound, but
checking or compacting them at every task closure would add recurring latency
and cost.

Evidence:
The accepted design review found that record files need bounded active context
without losing history. It also found that a five-date changelog window is too
small, while keeping fifty full date sections would likely exceed the runtime's
file-size guidance.

Hypothesis:
An event-driven `record-archive` skill with deterministic thresholds, dry-run
checks, atomic fail-closed writes, and format-specific retention rules will
bound active context without adding work to unrelated task closures.

Solution Attempt:
Add one reusable skill and script for Deferred Findings, experiments, and
changelog records. Trigger checks only when a finding becomes completed, an
experiment becomes terminal, or a new changelog date is created. Keep five
recent completed findings, five recent terminal experiments, and twenty full
changelog dates plus a thirty-date archive index.

Test:
Run contract tests against temporary repositories for below-threshold no-ops,
threshold rotation, preservation, duplicate and malformed-input rejection,
dirty-file protection, idempotence, portable installation, and runtime policy
activation.

Success Criteria:
- No event-independent or every-task archive check is introduced.
- Deferred Findings and experiments rotate at ten eligible records and retain
  five eligible records in the active file.
- Changelog rotation starts at thirty detailed dates or five hundred lines,
  retains twenty detailed dates, and exposes up to thirty archive links.
- Pending findings and non-terminal experiments always remain active.
- No record is lost, duplicated, or moved to the wrong section.
- `check` is non-mutating; `apply` is atomic, fail-closed, and idempotent.
- Codex, Dolphin, and the active local runtime expose the same validated skill.

Result:
The initial RED run failed on all thirteen missing behavior and packaging
surfaces. After implementation and two real-format compatibility revisions,
the focused suite passed 16 tests and the full project suite passed 35 tests.
Measured statement coverage for the bundled script is 87%. Codex, Dolphin, and
the active local skill passed `quick_validate.py`, compiled successfully, and
were checksum-equivalent. A read-only check against `yedekparcasor.com`
reported Deferred Findings and Changelog below threshold and Experiments ready
for rotation without changing that project. Dirty files, malformed formats,
duplicates, unsupported headings, and broken symlinks failed closed.

Decision:
ACCEPT

Notes:
This experiment changes only record-retention automation. It does not alter the
mandatory orchestration chain, agent reasoning defaults, or task approval
rules.

## EXP-20260727-001 - Conditional Hypothesis Workflow

Date: 2026-07-27
Status: ACCEPTED

Problem:
The runtime has evidence, retry, TDD, and review controls, but it does not yet
provide the conditional experiment workflow tracked by ORCH-005. Making the
workflow mandatory for every task would add duplicate records and latency.

Evidence:
`docs/ORCHESTRATION_IMPROVEMENT_TASKS.md` keeps ORCH-005 pending and limits
experiment escalation to failed attempts, unclear evidence, competing
hypotheses, regressions, or measured comparisons.

Hypothesis:
A concise global trigger combined with a reusable `hypothesis-workflow` skill
will add traceable experiments only when difficulty or uncertainty justifies
the extra process, without changing routine task flow or the mandatory agent
chain.

Solution Attempt:
Package the conditional skill for Codex and Dolphin, register it globally,
link it from runtime policy, preserve existing evidence and changelog paths,
and explicitly prohibit proactive experiment-file creation for routine work.

Test:
Run focused contract tests, the complete unit suite, skill validation, and
temporary Codex and Dolphin installations. Verify the active local Codex
runtime after synchronization.

Success Criteria:
- Routine first-pass work does not activate the experiment workflow.
- Defined escalation triggers activate prior-record review and a dated ID.
- Project `AGENTS.md` does not need to declare the skill.
- Existing `CHANGELOG_PATH` and `EVIDENCE_PATH` remain authoritative.
- The mandatory agent chain and `medium` reasoning defaults remain unchanged.
- Codex and Dolphin temporary installs contain the validated skill.
- Tests reject unconditional activation and missing test-integrity guardrails.

Result:
The corrected RED run failed on all missing behavior surfaces: skill files,
global policy, registry links, and portable installation. After implementation,
the focused suite passed 7 tests and the full suite passed 19 tests. Both
packaged skills and the active global skill passed `quick_validate.py`. Codex
and Dolphin temporary installs contained identical skill contracts.
`~/.codex/AGENTS.md`, the active skill, and active registry policy were
checksum-equivalent to their source templates after targeted synchronization.
The existing active audit history remained intact.

Decision:
ACCEPT

Notes:
This experiment changes one main behavior: conditional activation of a
traceable hypothesis cycle. It does not alter approval, scope, destructive
operation, retry, orchestration, or security boundaries. The prior active
policy and registry files are recoverable from
`~/.codex/archive/hypothesis-workflow-20260727_004001/`.

## EXP-20260803-001 - Independent Opt-In GLM Evidence Validator

Date: 2026-08-03
Status: ACCEPTED

Problem:
Evidence validation is useful for selected projects, but embedding it in CMA
policy, templates, or the default completion path would change every project.

Evidence:
The rejected first attempt coupled validation to CMA runtime templates and
failed review on MCP initialization, portable paths, hook preservation, and
missing tests. The approved scope requires an independent installation with no
automatic project activation.

Hypothesis:
A standalone ACP client installed under `~/.codex/evidence-validator`, combined
with project-local opt-in configuration and hooks, can validate changed evidence
without changing CMA instructions, evidence creation rules, global hooks, or
inactive projects.

Solution Attempt:
Implement and test an independent validator, project enable/disable/status
commands, hash-based session evidence detection, strict GLM result parsing, and
project-local hook merging. Install it globally but activate only a temporary
pilot project.

Test:
Run unit and integration tests against temporary projects and a fake ACP agent,
then run a real GLM smoke test using the existing `glm-acp-agent` setup. Verify
that CMA files, the active global hook, and real project files remain unchanged.

Success Criteria:
- No CMA policy, template, installer, or evidence-creation instruction changes.
- No real project is activated automatically.
- Enable and disable preserve unrelated project hooks and are idempotent.
- Only session-created or session-modified evidence is sent for validation.
- Only schema-valid `PASS` permits completion; every uncertain path is
  `UNVERIFIED`.
- The existing global notification hook remains byte-identical.
- Focused tests, regression tests, real GLM smoke validation, code review, and
  security review complete without blocking findings.

Result:
The independent validator was installed under `~/.codex/evidence-validator`
without changing global CMA instructions, Codex configuration, or the existing
global notification hook. The final focused suite passed 24/24 with no skipped
tests. A temporary project completed real pinned GLM ACP manual validation with
`PASS`, then its changed evidence completed the real Stop hook with `{}`. The
temporary project was disabled and moved to Trash. Final independent code and
security reviews both returned PASS with no blocking findings.

Decision:
ACCEPT

Notes:
The global installation makes the validator available only. Project activation,
commit, and push remain outside this task.

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
