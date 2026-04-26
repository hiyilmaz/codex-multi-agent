# Codex ECC Management

**Version:** 2.1
**Updated:** 2026-04-27

---

## Purpose

ECC is the reusable Codex development system.

It owns base rules, skills, agents, templates, scripts, and lifecycle docs. Codex
global files activate that system, and project files declare project-specific
deltas.

---

## Directory Model

Base ECC:

```text
~/Codex-ECC/
  VERSION
  rules/
  skills/
  agents/
  templates/
  docs/
  bin/
```

User-global Codex:

```text
~/.codex/
  AGENTS.md
  config.toml
  rules/
  skills/
  agents/
```

Project:

```text
<project>/
  AGENTS.md
  .codex/config.toml
  .codex/prompts/fill-project-configuration.md
  .codex/archive/           # init backups
```

---

## Ownership

`ECC_ROOT` is the base/vendor layer. Keep it updateable and avoid direct local
edits unless maintaining ECC itself.

`~/.codex` is the user-global layer. Put reusable user-specific rules, skills,
and agents here.

Project `AGENTS.md` is the project delta. It should not store reusable bodies.

---

## Install

Recommended command:

```bash
bin/codex-ecc-install
```

Default behavior:

- create `~/Codex-ECC` if missing
- create `~/.codex` if missing
- install `~/.codex/AGENTS.md` from `GLOBAL_AGENTS_TEMPLATE.md` if missing
- install `~/.codex/config.toml` from `CODEX_CONFIG_EXAMPLE.toml` if missing
- create user-global `rules/`, `skills/`, and `agents/` directories
- never overwrite existing global files without explicit flags

For isolated testing or non-default installs:

```bash
bin/codex-ecc-install --ecc-root /tmp/codex-ecc --codex-home /tmp/codex-home
```

---

## Update

Recommended command:

```bash
bin/codex-ecc-update
```

Default behavior:

- update `ECC_ROOT` if it is a git repository
- report current global `~/.codex/AGENTS.md` and config status
- do not rewrite project files
- do not overwrite user-global custom rules, skills, or agents

---

## Resolution Priority

```text
project declaration
  -> user-global override in ~/.codex/
  -> base ECC content in ECC_ROOT
  -> unavailable/report
```

---

# EOF
