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

Setup preferences and status messages live under `registry/`.

Excluded:

- sessions
- logs
- caches
- memories
- hook state
- plugin caches
- machine-local project trust entries
