# Changelog

## 2026-08-06

- [CHORE] Normalized shared registry file endings across Codex, Dolphin, and
  Claude while preserving byte-identical provider-neutral assets.
- [FEAT] EXP-20260806-009 expanded the portable Claude Code runtime to full
  Core CMA source parity with 12 native agents, four complete skills, eight
  lazy modules, six registry records, and an exact 34-file home manifest.
- [SECURITY] Hardened the shared Codex, Dolphin, and Claude record archive
  helper against managed-parent symlink escapes using `O_NOFOLLOW` directory
  descriptors and rollback registration before atomic writes.
- [TEST] Added semantic Claude parity, truthful audit-history, external path
  escape, and post-replace rollback regressions; verified 48/48 focused tests,
  106/106 complete regressions, and clean independent code/security re-reviews.
- [CHORE] Applied threshold-triggered terminal experiment compaction and
  verified the active and split archives return `BELOW_THRESHOLD` without
  losing experiment records.
- [SECURITY] Extended project containment preflight to every managed template
  parent for dry-run, apply, and initial-state operations.
- [SECURITY] Rejected symlinked or non-directory project runtime parents before
  init/upgrade confirmation or mutation to prevent path escape and partial reset.
- [FIX] Classified terminal-less Claude assistant errors as failed outcomes
  while retaining unverified status for genuinely missing terminal evidence.
- [FIX] Made experiment archiving support contiguous split archive indexes and
  append rotations to the latest validated part.
- [CHORE] Excluded local Graphify indexes and reports from version control.
- [FEAT] EXP-20260806-008 added an optional offline Claude Agent SDK adapter
  pinned to `claude-agent-sdk==0.2.130` with bounded requests, restrictive
  permissions, session contracts, truthful terminal mapping, and usage/cost
  observability.
- [SECURITY] Default-denied credential-backed SDK execution until a separately
  approved Gate C executor provides per-call authorization, isolated state,
  and a minimal child-process environment; fixed cancellation and terminal
  error-metadata fail-closed findings from independent reviews.
- [TEST] Verified 21/21 adapter tests at 92% coverage, frozen lock/sync, Python
  compilation, `git diff --check`, 88/88 root regressions, and independent code
  and security review without credentials or a real Claude request.
- [FEAT] EXP-20260806-007 added a provider-aware native Claude runtime,
  isolated `llm-claude` launcher, Markdown chain agents, safe settings, and an
  `@AGENTS.md` project bridge with preservation-aware init and upgrade support.
- [TEST] Verified 88/88 tests plus syntax, JSON, path-boundary, symlink,
  no-overwrite, launcher, project dry-run, code-review, and security-review
  checks without SDK, credential, active-runtime, commit, push, or deployment
  changes.
- [DOCS] Added a single status-tracked Claude integration task plan covering
  native runtime parity, project migration, optional Agent SDK work, security
  gates, verification, and rollback.
- [INFRA] Installed the approved Codex CMA runtime on `blockmanpro`, preserving
  existing `/root/.codex` state and initializing `/opt/blockman-platform-dev`
  as a multi-repository CMA workspace without deployment or service changes.
- [INFRA] Installed Ubuntu Node.js 18.19.1, npm 9.2.0, and pinned
  `@openai/codex@0.146.1`; authentication remains intentionally unconfigured.
- [TEST] Verified 60/60 local tests, archive integrity, isolated RED/GREEN,
  no-overwrite sentinels, project conflict archiving, exact managed files,
  configuration parsing, root-only artifacts, and Codex CLI startup.
- [FIX] EXP-20260806-001 through EXP-20260806-006 documented executable-mode,
  manifest-scope, SSH stdin-continuation, archive-regression, and scoped
  assertion findings with bounded resolutions.

## 2026-08-05

- [FEAT] EXP-20260805-001: Added fail-closed `EVIDENCE_MODE: enable | disable`
  semantics with missing values defaulting to disabled and explicit user
  requests remaining available.
- [INFRA] EXP-20260805-001: Set all 17 active CMA projects to
  `EVIDENCE_MODE: disable` and activated only the four approved mode clauses in
  the backed-up global records module.
- [TEST] EXP-20260805-001: Verified meaningful 3/3 RED, 60/60 full CMA tests,
  the 17-project manifest, exact global delta, and independent code and
  security reviews.

## 2026-08-04

- [FIX] EXP-20260804-003: Required one independently verifiable outcome and one
  coherent verbatim proof excerpt per evidence claim while prohibiting
  reporting-only semantic downgrades.
- [TEST] EXP-20260804-003: Recorded meaningful source and portable RED failures,
  then passed 17 focused tests, 55 full CMA tests, independent reviews, and EV
  validation of six atomic claims.
- [FIX] EXP-20260804-002: Added a conditional temporal TDD evidence contract
  with one ordered structural RED-to-final pair, final-only success proof, and
  a same-scope post-fix rerun requirement.
- [TEST] EXP-20260804-002: Verified source and portable contracts, fenced and
  quoted proof boundaries, 14 focused tests, and 52 full CMA tests.
- [INFRA] EXP-20260804-002: Backed up and synchronized the validated temporal
  records contract to the active global Codex runtime.
- [FIX] Standardized `ask-approval` final messages on the exact six-line CMA
  decision block so EV can defer only the current non-completion Stop.
- [DOCS] Diagnosed the EV Stop-hook false trigger on structured CMA decision
  waits and recorded the bounded remediation scope without changing runtime
  behavior.
- [FEAT] EXP-20260804-001: Added the prospective CMA `## Claims` evidence
  contract required for EV compatibility.
- [TEST] EXP-20260804-001: Added source, portable-install, and real EV/GLM
  compatibility coverage while preserving fail-closed validation.
- [INFRA] EXP-20260804-001: Backed up and synchronized the validated CMA records
  module to the active local Codex runtime.

## 2026-08-01

- [FIX] EXP-20260801-003: Made global Codex Stop notifications root-only and
  selected distinct spoken messages for completion, failure, and user waiting.
- [TEST] EXP-20260801-003: Verified eight silent hook scenarios, subagent
  suppression, malformed-input safety, executable mode, and config parity.
- [FIX] EXP-20260801-002: Standardized all Codex subagents on medium reasoning
  and replaced six high variants with four Sol/medium routing variants.
- [TEST] EXP-20260801-002: Verified 47 tests, source-active parity, ZIP
  integrity, no project-local high override, and fresh-session routing.
- [INFRA] EXP-20260801-001: Activated compact Core CMA and eight trigger-loaded
  modules in the managed and active local Codex runtime.
- [FIX] EXP-20260801-001: Removed unsupported `display_name` metadata and added
  six static Sol/high variants for reliable conditional escalation.
- [TEST] EXP-20260801-001: Added RED/GREEN contracts and verified the full
  suite, source-active parity, rollback checksums, and fresh-session routing.
- [DOCS] Restricted the CMA optimization plans to this repository and the local
  global Codex directory, and recorded completed, partial, and pending work.
- [INFRA] Applied the approved CMA subagent model matrix to Codex source and
  active global agents, keeping mandatory quality roles on Sol.
- [INFRA] Added friendly identity aliases for Codex subagents while preserving
  role-key runtime naming and orchestration chain compatibility.
- [DOCS] Added the CMA Core and Lazy Modules plan with subagent model and
  reasoning evaluation guidance.
- [DOCS] Added the CMA subagent model pilot implementation plan with file-level
  scope, dry-run checks, and rollback criteria.

## 2026-07-28

- [FEAT] EXP-20260728-001: Added a minimal truthful outcome-reporting contract
  to Codex and Dolphin runtime policies.
- [TEST] EXP-20260728-001: Added RED/GREEN source and portable-install checks
  for verified status-to-success mappings.
- [INFRA] EXP-20260728-001: Activated the validated Codex policy locally with a
  checksum-verified rollback backup.

## 2026-07-27

- [FEAT] EXP-20260727-002: Added event-driven `record-archive` automation for
  Deferred Findings, experiments, and changelog records.
- [FIX] EXP-20260727-002: Limited checks to sparse record transitions, retained
  twenty full changelog dates plus thirty archive links, and preserved complete
  history in archive files.
- [FIX] EXP-20260727-002: Added legacy experiment and headerless changelog
  compatibility with dirty-file, malformed-format, duplicate, and symlink
  fail-closed protection.
- [TEST] EXP-20260727-002: Added 16 archive contract tests, reached 87% script
  coverage, and validated Codex, Dolphin, active runtime, and current
  `yedekparcasor.com` record formats.
- [FEAT] EXP-20260727-001: Added the conditional `hypothesis-workflow` skill to
  Codex, Dolphin, and the active local global runtime.
- [FIX] EXP-20260727-001: Kept routine first-pass work outside the experiment
  flow and reused existing project changelog and evidence paths.
- [TEST] EXP-20260727-001: Added activation, non-activation, test-integrity,
  registry, and portable-install contract coverage.

## 2026-07-26

- [INFRA] Added full-project ZIP backups to Git ignore rules.
- [FIX] Preserved the mandatory four-stage orchestration chain while adding
  bounded handoffs, no-repeat rules, fast review exits, and false-completion
  controls.
- [INFRA] Changed the four mandatory Codex chain agents from `high` to `medium`
  reasoning and synchronized the validated contract to the active runtime.
- [TEST] Added orchestration contract coverage and verified 12 tests, 24 agent
  TOML files, and temporary Codex and Dolphin installations.
- [DOCS] Reviewed the mandatory orchestration chain, recorded current Codex and
  community evidence, and added a proposed latency-reduction task list without
  changing runtime or agent configuration.

## 2026-07-16

- [FIX] Updated all portable Codex custom subagent model overrides to
  `gpt-5.6-sol`, preventing forced runtime refreshes from restoring `gpt-5.5`.
- [TEST] Verified Codex and Dolphin agent models, a clean Codex variant install,
  and the complete project upgrade regression suite.
- [INFRA] Updated all active user-global custom subagent model overrides to
  `gpt-5.6-sol` and archived the previous definitions.
- [DOCS] Recorded the deferred risk that a future forced runtime refresh could
  restore older subagent model overrides from the Codex variant template.

## 2026-07-14

- [DOCS] Added a consolidated command reference for runtime installation,
  project initialization and upgrades, docs refresh, and verification.
- [FIX] Removed FormProxy-specific and crypto strategy skills from the generic
  Codex runtime package and active skill registry.
- [DOCS] Audited packaged runtime skills and identified FormProxy and crypto
  strategy content that should not ship in the generic runtime template.
- [FEAT] Added versioned project template state and hash-aware safe migrations
  for already initialized projects.
- [FIX] Preserved locally developed project prompts, configs, documentation,
  domain rules, and custom configuration values during template upgrades.
- [DOCS] Made project upgrade dry-run-first with explicit `--apply` execution
  and per-upgrade archives.
- [TEST] Added regression coverage for fresh, legacy, customized, and unchanged
  managed project upgrade scenarios.
- [FEAT] Packaged the existing MIT-licensed ECC `tdd-workflow` skill in the
  Codex and Dolphin runtime variants.
- [FIX] Updated project initialization and upgrade contracts to require both
  `orchestration-gate` and `tdd-workflow` while keeping `openai-docs`
  project-specific.
- [FIX] Prevented launcher-free runtime variants from exiting the user installer
  with a failure status after copying their files.
- [DOCS] Added ECC source and license attribution for the imported workflow.

## 2026-06-26

- [DOCS] Added deferred findings log behavior to global Codex instructions.

## 2026-06-24

- [FEAT] Added `codex-project-upgrade` to update initialized project
  `AGENTS.md` files without resetting them.
- [INFRA] Added project-level `ORCHESTRATION_MODE` and the
  `orchestration-gate` decision skill across runtime variants.

## 2026-06-11

- [FIX] Install Dolphin launcher into the selected runtime home as
  `llm-dolphin`.

## 2026-06-10

- [FIX] Rewrite installed variant template paths to the selected runtime home.
- [INFRA] Move installable runtime templates under `variants/` with `codex`
  and `dolphin` variant selection.
- [DOCS] Added global assistant conduct guidance to the Codex home instruction
  templates.

## 2026-05-22

- [FEAT] Added interactive setup with status-message defaults and YOLO-mode
  preference guarded by mandatory destructive-operation approvals.
- [DOCS] Added a Turkish setup guide covering fresh user-global installation
  and project-local initialization.
- [INFRA] Added the portable template installer for the user-global Codex
  runtime surface.
- [INFRA] Removed the external runtime layer from the active Codex model and
  documented the simplified `~/.codex` skill/agent registry structure.
