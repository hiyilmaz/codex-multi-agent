# Improvement Experiments

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
