# Deferred Findings

## Pending

- ID: DF-20260818-0000-001
  Type: OPERATIONAL_HARDENING
  Discovered At: 2026-08-18
  Source Task: Blockmanpro codex-tools live repair
  Location: /root/.local/share/cma-rollbacks/codex-tools-pre-*
  Summary: Owner-only UV-tool rollback copies were created and their expected top-level contents were inspected, but a full recursive integrity manifest and isolated restore rehearsal were not performed against the live package environment.
  Recommended Fix: Add an isolated rollout harness that records a recursive manifest and rehearses restoration outside the active UV tool path before using the backup in a real rollback.

- ID: DF-20260817-0000-001
  Type: SECURITY_HARDENING
  Discovered At: 2026-08-17
  Source Task: Independent codex-tools CMA integration
  Location: tools/codex-tool-installer/src/codex_tool_installer/config.py
  Summary: Config transactions reject lexical symlink components, and rollback now rejects unexpected content or inode changes, but a concurrently replaceable ancestor or same-user change could still occur between validation and path-based backup/replace operations. Normal private native Codex homes limit exploitability; custom CMA homes are rejected.
  Recommended Fix: Anchor transaction reads, backups, replacement, and rollback to validated directory descriptors with no-follow/openat-style operations and inode identity checks.

## Completed

- ID: DF-20260716-0535-001
  Type: RISK
  Discovered At: 2026-07-16 05:35
  Fixed At: 2026-07-16 05:37
  Source Task: Update user-global custom subagent models to gpt-5.6-sol
  Location: variants/codex/home/agents/*.toml
  Summary: The portable Codex variant still pins eight custom agents to gpt-5.5.
  Fix Summary: Updated all eight Codex variant agent model overrides to gpt-5.6-sol and retained Dolphin-specific model settings.
  Evidence: Python 3.13 TOML validation and temporary Codex variant installation confirmed all eight packaged agents use gpt-5.6-sol.
