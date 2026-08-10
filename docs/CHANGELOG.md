# Changelog

## 2026-08-10

- [ROLLBACK] EXP-20260810-001 moved the inactive ARK and CMA-ARK implementation, adapter, hook, evidence, and test surfaces into a private checksum-bound external recovery backup; the repository now retains only a non-executable planning proposal and historical audit records.

## 2026-08-09

- [CHANGED] Removed ARK's nested Git boundary and adopted it into the CMA monorepo.
- [DOCS] Consolidated ARK's ignore rules, instructions, changelog, experiment,
  and integration status under authoritative CMA records and policies.
- [TEST] Added a fail-closed ARK monorepo contract covering functional-file
  hashes, record preservation, experiment-ID uniqueness, and removed metadata.
- [FIX] EXP-20260809-001 made ARK unittest discovery monorepo-safe with explicit
  `-t ARK`; all 33 tests passed from the CMA root with 85% branch coverage.
- [FIX] EXP-20260809-002 made root-relative ARK CLI examples executable by
  requiring `--config ARK/ark.json` and verifying the documented doctor command.
- [DOCS] Made ARK coverage validation use an isolated temporary data file so
  root-level coverage state is not created by documented monorepo commands.
- [PILOT] Completed the isolated Phase 2 CMA–ARK read-only compatibility pilot:
  single-tool text and stale-graph routes passed, unavailable `ast-grep` stayed
  fail-closed, 9/9 contract and 33/33 ARK tests passed, and pre/post state was
  byte-identical; network activity, token usage, and tool provenance remain unverified.
- [DESIGN] EXP-20260809-003 approved the passive Phase 3 CMA–ARK adapter API:
  explicit activation, a three-intent allowlist, canonical plan-digest approval,
  bound provenance, deterministic POSIX/macOS exit origins, rollback, and future
  TDD gates; implementation was later separately approved while activation remains unapproved.
- [FEAT] Added the passive stdlib CMA–ARK v1 process adapter with a fixed
  repo-owned ARK boundary, three-intent allowlist, plan-digest approval handshake,
  bound executable provenance, fail-closed protocol normalization, and no activation.
- [TEST] Added RED-first unit, subprocess, real fixed-ARK black-box, and passive
  footprint contracts; 29 adapter tests passed with 82.81% branch coverage.
- [SECURITY] Revalidated fixed ARK resources and selected-tool PATH/content/stat
  identity immediately before execution; independent code and security reviews passed.
- [RECORDS] Rotated five older terminal experiments after the ARK migrations
  reached the deterministic archive threshold; post-check returned below threshold.
- [DESIGN] EXP-20260809-005 defined a repo-local, explicit-only CMA-ARK
  activation boundary with a plan-only text-search pilot, trusted host approval
  gate, isolated bootstrap, outer identity binding, atomic replay/rate control,
  sensitive-output controls, staged Graphify coordination, manifest-bound
  rollback, and no runtime activation.
- [FEAT] Added the inactive EXP-20260809-006 CMA-ARK skill candidate with
  explicit-only metadata, fixed isolated bootstrap, strict query framing, a
  bounded real passive-adapter plan boundary, digest-only query reporting, and
  no discovery or execution authority; future activation remains blocked on
  adapter launcher/interpreter and writable-PATH identity pinning.
- [SECURITY] EXP-20260809-007 pinned CMA-ARK launchers to isolated system Python,
  bound adapter/ARK/interpreter/target/tool identities, and hardened the
  disposable skill pilot against import injection, writable ancestors,
  concurrent state races, symlink and inode drift, and false commit status.
- [TEST] Passed 58/58 adapter and pilot tests with 80% pilot and 91% combined
  branch coverage, 33/33 ARK tests, 14/14 root ARK contracts, skill validation,
  and independent code and security reviews; no real activation occurred.
- [ROLLBACK] EXP-20260809-008 exercised governed repo-local CMA-ARK activation,
  direct plan-only verification, rollback, and fresh-host discovery, then
  removed the discovery surface after three host sessions produced no usable
  plan. Canonical activation operations and the unproven bootstrap revision
  were removed; global and repo-local activation remain absent.
- [FIX] Made disposable pilot rollback use its validated installer-recorded
  manifest so later candidate-source edits cannot strand an unchanged installed
  copy; installed file and directory drift still fails closed.
- [FEAT] EXP-20260809-009 added an inactive repo-local `UserPromptSubmit`
  transport candidate and descriptor-anchored disposable hook lifecycle pilot,
  replacing the failed model-driven skill stdin path without activating hook
  trust, canonical config, skill discovery, or tool execution.
- [SECURITY] Bounded encoded hook config before publication, preserved
  unrelated hook entries, rejected unsafe descriptor/path state, and made
  residual pre/post-commit cleanup failures report their actual mutation state;
  final code and security re-reviews passed.
- [TEST] Passed 18/18 focused hook tests with 85% branch coverage, 78/78 adapter
  tests, a real zero-execution hook-to-ARK plan, disposable CLI install/rollback,
  33/33 ARK tests, 5/5 CMA-ARK root contracts, and 166/166 root regressions.
- [FEAT] EXP-20260809-010 split the CMA-ARK hook pilot into a thin isolated CLI
  and private descriptor lifecycle, then added fixed no-target canonical hook
  install and rollback operations without reactivating the failed repo skill.
- [TEST] Added copied-layout canonical lifecycle, idempotency, rollback,
  reinstall, drift, module-identity, and truthful cleanup-state coverage;
  final 27/27 focused tests passed with 80.47% combined branch coverage,
  alongside 87/87 adapter, 33/33 ARK, and 166/166 root regressions.
- [SECURITY] Closed temp-unlink, descriptor-close, and outer-descriptor cleanup
  paths that could misreport residual or committed hook state; final code and
  security re-reviews passed.
- [ROLLBACK] Installed the canonical prompt hook, restored the exact original
  config during rehearsal, reinstalled and trusted only its displayed
  definition, then removed it after the first fresh-host trace returned a
  generic `rg` plan without required bound digests or explicit zero-execution
  evidence. The original config SHA-256 is restored; no hook or skill is active.
- [DESIGN] EXP-20260809-011 accepted a deterministic same-run CMA-ARK evidence
  contract with independent candidate and Codex lanes, semantic session/thread
  binding, exact fail-closed schemas, stable three-run comparison, and private
  cleanup; wrapper implementation and activation remain separately gated.
- [TEST] Passed 8/8 evidence-design, 6/6 plan-only hook candidate, and 3/3
  passive adapter contract tests; Draft 2020-12 negative validation and final
  independent code/security re-reviews passed without activating any hook.
- [FEAT] EXP-20260809-012 added a disposable deterministic host-evidence
  wrapper/harness with independent candidate and JSONL lanes, reviewed source
  manifest binding, private cleanup, and no canonical activation.
- [SECURITY] Unified the plan-only subprocess tree under one wrapper-owned
  process group, closed timeout/reap and semantic-failure escape paths, and
  passed 27/27 focused tests at 84% combined branch coverage plus 115/115
  adapter tests and final independent code/security reviews.

## 2026-08-08

- [FIX] EXP-20260808-003 made project init additive for Codex, Dolphin, Claude,
  and OpenCode, migrated template state to a multi-variant schema, preserved
  shared/customized project files, and restricted destructive reinitialization
  to explicit `--reset` with collision-safe private recovery archives.
- [POLICY] Added a global Task Transition Gate across the portable Codex,
  Dolphin, Claude, and OpenCode policies. Distinct completed tasks now require
  a short summary, the next task or an explicit statement that none is known,
  and fresh user approval before work continues; already approved steps inside
  the same bounded task remain uninterrupted. Synchronized only the stale
  active policy files through private, permission-preserving backups and passed
  145/145 regressions plus independent code and security review.
- [FEAT] Added a provider-neutral OpenCode CMA variant with an isolated
  `llm-opencode` launcher, eight Markdown agents, four workflow skills, lazy
  registry modules, and preservation-aware project init/upgrade support.
- [SECURITY] Isolated OpenCode config, data, cache, and state roots; rejected
  symlinked state paths; approval-gated governor writes; omitted sensitive
  project-config diffs; and protected init/upgrade archives with private modes.
- [TEST] Captured runtime, isolation, secret-redaction, preservation, and custom
  path RED states; passed 141/141 regressions plus live OpenCode 1.18.15 config,
  path, agent, skill, and single-plugin pilot checks; final code and security
  reviews passed.
- [CHANGED] Relocated the independent ARK repository under `Codex-Multi-Agent/ARK`.
- [ADDED] Created the independent ARK repository with a strict JSON configuration contract.
- [ADDED] Added narrowest-sufficient-tool planning for Graphify, rg, ast-grep, conditional OSV, Serena, GitHub MCP, Opengrep, Betterleaks, cplt, DeepWiki, and Context7.
- [ADDED] Added argv-only execution, fail-closed target containment, private cplt runtime roots, credential stripping, output redaction, and truthful result statuses.
- [TEST] Added RED-first unit and integration coverage for configuration, routing, execution, CLI behavior, injection resistance, and runtime isolation.
- [FIX] Enforced fail-closed configuration types, `.ark/runtime` containment, exact GitHub identities, nonzero no-execution exits, nonempty security evidence, and explicit docs providers (`EXP-20260808-004`).
- [FIX] Rejected non-string Serena mode values with a controlled configuration error (`EXP-20260808-004`).
- [SECURITY] Isolated cplt behind a minimal repo-local environment, suppressed sensitive scanner output, bounded subprocess duration/output while draining streams, terminated timed-out process groups, and rejected Graphify output symlink escapes (`EXP-20260808-004`).

## 2026-08-07

- [DOCS] Aligned CMA project guidance and the managed configuration prompt so
  active-skill declarations exclude disabled-plugin and inactive-registry
  entries, and refreshed the project instruction version to template 2.2.
- [INFRA] EXP-20260807-002 aligned the self-hosted CMA project with Codex
  template 2.2, created managed template state, and synchronized the selected
  active global policy, runtime README, and orchestration gate.
- [SECURITY] Preserved user configuration, setup preferences, status messages,
  audit history, stricter record/archive overrides, credentials, sessions, and
  unrelated runtime state through a verified five-file recovery backup and
  targeted updates only.
- [TEST] Verified project-template and active-runtime parity, preserved hashes,
  valid TOML/JSON, managed upgrade idempotency, 52/52 focused checks, 122/122
  complete regressions, and clean diff integrity.
- [DOCS] Synchronized the English and Turkish runtime guides, command reference,
  Claude variant README, and integration tracker with the completed native
  Claude activation, recovery backup, rollback, force-rejection, and legacy
  runtime preservation behavior.
- [FEAT] EXP-20260807-001 changed Claude's default user-global runtime from the
  isolated `.llm-runtimes/claude` path to native `${HOME}/.claude` with a
  preservation-first CMA policy import and dedicated activation helper.
- [SECURITY] Native activation rejects force, differing managed files,
  incomplete sources, unsafe or equivalent-path bypasses, and partial backup
  failures; new runtime paths use owner-only permissions regardless of umask.
- [MIGRATION] Activated the current user's native Claude CMA surface with a
  byte-identical policy backup while preserving existing settings, modes,
  unrelated user state, and the legacy isolated runtime.
- [TEST] Verified meaningful RED regressions, 10/10 activation checks, 17/17
  installer checks, 17/17 Claude runtime checks, 122/122 complete regressions,
  live source parity and idempotency, plus passing independent code and
  security reviews.

## 2026-08-06

- [FEAT] EXP-20260806-011 added a portable Claude Code subagent restoration
  prompt derived from the verified 12-agent Sonnet/Opus frontmatter matrix.
- [SECURITY] Fail-closed explicit-target restoration unless the effective
  `CLAUDE_CONFIG_DIR` equals the resolved target before delegation or writes.
- [TEST] Verified Claude and installer suites at 17/17 each, complete
  regressions at 112/112, isolated prompt hash parity, native Claude isolation,
  and passing independent code/security reviews.
- [FEAT] EXP-20260806-010 added a portable, token-conscious Codex subagent
  restoration prompt with dynamic runtime-home resolution and the verified
  12-role medium-only Terra/Sol matrix.
- [SECURITY] Extended installer fail-before-write symlink validation to the
  managed prompt directory and preserved existing prompts without force.
- [TEST] Verified meaningful restoration and partial-mutation RED cases,
  focused 5/5 checks, 17/17 installer tests, 21/21 runtime-contract tests,
  11/11 orchestration tests, 111/111 complete regressions, active prompt hash
  parity, and independent code/security review.
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
