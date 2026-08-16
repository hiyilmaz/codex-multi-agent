# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

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
