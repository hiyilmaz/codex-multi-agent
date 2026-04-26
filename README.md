# Codex Template V2

**Version:** 2.3
**Updated:** 2026-04-27

---

## Purpose

This is a Codex-native project instruction template for new or existing
repositories.

It is self-contained and does not depend on another agent runtime.

---

## Files

| File | Purpose |
|---|---|
| `GLOBAL_AGENTS_TEMPLATE.md` | Copy to `~/.codex/AGENTS.md` |
| `PROJECT_AGENTS_TEMPLATE.md` | Copy to a project as `AGENTS.md` |
| `USAGE_GUIDE.md` | How to apply the template to new or existing projects |
| `CODEX_CONFIG_EXAMPLE.toml` | Optional project `.codex/config.toml` example |
| `PROJECT_CONFIG_PROMPT.md` | Prompt copied into projects after init |
| `ECC_MANAGEMENT.md` | Global ECC install/update model |
| `docs/openai-codex/` | Local updateable index of official OpenAI Codex docs |
| `bin/` | Init and ECC management helper scripts |

---

## ECC Model

Base ECC content lives under `ECC_ROOT`. User-specific reusable overrides live
under `~/.codex/`. Project `AGENTS.md` declares what is active but does not
store reusable bodies.

Reusable content locations:

- Base ECC: `$ECC_ROOT/rules`, `$ECC_ROOT/skills`, `$ECC_ROOT/agents`
- User-global: `~/.codex/rules`, `~/.codex/skills`, `~/.codex/agents`

Reusable bodies should not be copied into project `AGENTS.md`.

---

## Quick Start

Install/update the global ECC surface first:

```bash
bin/codex-ecc-install
```

Then initialize a project:

```bash
bin/codex-project-init /path/to/project
```

The init command asks for confirmation, archives existing project-local Codex
files, resets the project Codex structure, and creates a fresh project
`AGENTS.md`.

After init, run the generated prompt:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

That prompt tells the AI to inspect the project and fill only the
`AGENTS.md` `Project Configuration` block. If required values are ambiguous, it
must ask the user before editing instead of writing placeholders.

## Local Codex Docs

Refresh the local OpenAI Codex documentation index:

```bash
scripts/update-openai-codex-docs
```

The index is stored under `docs/openai-codex/`.

---

# EOF
