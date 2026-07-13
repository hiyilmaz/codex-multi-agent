# Codex Runtime Variant

This directory is the default portable template for the active user-global
Codex runtime surface.

Install it with:

```bash
bin/codex-user-install --variant codex
```

or to overwrite existing template-managed files:

```bash
bin/codex-user-install --variant codex --force
```

Included:

- `AGENTS.md`
- `config.toml`
- `agents/`
- `skills/`
- `registry/`

The template includes `orchestration-gate` for project-level
`ORCHESTRATION_MODE` decisions:

```text
skip | ask-approval | run-chain
```

It must not bypass active tool or approval policy.

The template also includes the ECC `tdd-workflow` skill for mandatory
test-first feature, bugfix, and refactor work. The `tdd-guide` agent defines
the focused test strategy; `tdd-workflow` enforces the RED-GREEN-refactor loop.

Setup preferences and status messages live under `registry/`.

Excluded:

- sessions
- logs
- caches
- memories
- hook state
- plugin caches
- machine-local project trust entries
