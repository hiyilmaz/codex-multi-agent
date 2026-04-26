# OpenAI Codex Local Docs

Updated: 2026-04-26T22:07:20+00:00

This directory contains a local, updateable index of official OpenAI Codex
developer documentation.

Source root: https://developers.openai.com/codex

## Files

- `index.md` — topic index for the local page entries
- `sources.json` — machine-readable source metadata
- `pages/` — compact page entries with URL, headings, checksum, and snippet
- `snapshots/` — update run metadata

## Update

Run from the repository root:

```bash
scripts/update-openai-codex-docs
```

## Policy

The official OpenAI docs remain the source of truth. Local page entries are
compact indexes, not full copies.

Indexed pages: 119
