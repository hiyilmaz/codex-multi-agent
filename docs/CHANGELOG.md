# Changelog

## 2026-06-24

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
