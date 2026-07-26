# Changelog

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
