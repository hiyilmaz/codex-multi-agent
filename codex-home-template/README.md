# Codex Home Template

This directory is a portable template for the active user-global Codex runtime
surface.

Install it with:

```bash
bin/codex-user-install
```

or to overwrite existing template-managed files:

```bash
bin/codex-user-install --force
```

Included:

- `AGENTS.md`
- `config.toml`
- `agents/`
- `skills/`
- `registry/`

Excluded:

- sessions
- logs
- caches
- memories
- hook state
- plugin caches
- machine-local project trust entries

