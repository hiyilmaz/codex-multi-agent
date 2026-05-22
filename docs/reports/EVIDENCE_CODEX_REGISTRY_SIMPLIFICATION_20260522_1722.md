# Evidence: Codex Registry Simplification

## Task

Simplify the Codex structure to `~/.codex + AGENTS.md`, remove the external
runtime layer from active resolution, add a user-global skill/agent registry,
and add automatic skill/agent governance.

## Commands

```bash
git status --short
rg -n "ECC|ECC_ROOT|Codex-ECC|everything-claude-code|codex-ecc" \
  /Users/iyilmaz/.codex/AGENTS.md \
  /Users/iyilmaz/.codex/config.toml \
  /Users/iyilmaz/.codex/registry \
  AGENTS.md GLOBAL_AGENTS_TEMPLATE.md PROJECT_AGENTS_TEMPLATE.md \
  README.md USAGE_GUIDE.md REGISTRY_MANAGEMENT.md \
  CODEX_CONFIG_EXAMPLE.toml PROJECT_CONFIG_PROMPT.md \
  docs/CHANGELOG.md bin scripts -S
bash -n bin/codex-project-init
python3 -c 'import pathlib,tomli; files=[pathlib.Path("/Users/iyilmaz/.codex/config.toml")]+list(pathlib.Path("/Users/iyilmaz/.codex/agents").glob("*.toml")); [tomli.loads(p.read_text()) for p in files]; print("parsed", len(files), "toml files")'
printf 'y\n' | bin/codex-project-init /private/tmp/codex-template-smoke-20260522
rg -n "ECC|ECC_ROOT|Codex-ECC|everything-claude-code|codex-ecc" /private/tmp/codex-template-smoke-20260522 -S
```

## Results

- `bash -n bin/codex-project-init` passed.
- TOML parse passed for `~/.codex/config.toml` and all user-global agent TOML
  files: `parsed 9 toml files`.
- Active docs/templates/scripts returned no external-layer references for the
  searched legacy terms.
- Smoke-generated project under `/private/tmp/codex-template-smoke-20260522`
  returned no legacy external-layer references.

## Files

- Updated user-global policy: `/Users/iyilmaz/.codex/AGENTS.md`
- Updated user-global config comments: `/Users/iyilmaz/.codex/config.toml`
- Added user-global registry: `/Users/iyilmaz/.codex/registry/`
- Added core orchestration agents and governor under `/Users/iyilmaz/.codex/agents/`
- Updated project templates and docs in this repository.

