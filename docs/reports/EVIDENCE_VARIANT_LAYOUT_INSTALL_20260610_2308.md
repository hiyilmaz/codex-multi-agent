# Evidence: Variant Layout and Installer Selection

Task ID: `VARIANT_LAYOUT_INSTALL`
Date: `2026-06-10 23:08`

## Scope

Move installable runtime templates under a shared `variants/` structure and
make installer commands select between `codex` and `dolphin` variants.

## Files and Directories

- Added `variants/config.toml` with `default_variant = "codex"`.
- Moved the default Codex home template to `variants/codex/home/`.
- Moved DolphinVersion files to `variants/dolphin/`.
- Updated `bin/codex-user-install` and `bin/codex-setup` for variant selection.
- Updated README, usage, Turkish setup, registry, changelog, and Dolphin docs.
- Left the root project `AGENTS.md` separate.

## Pre-flight

```text
$ pwd
/Users/iyilmaz/WebStorm/Codex-Multi-Agent

$ git status --short
 M DolphinVersion/agent-home/AGENTS.md
 M DolphinVersion/docs/CHANGELOG.md
?? DolphinVersion/docs/reports/EVIDENCE_DOLPHIN_ASSISTANT_BEHAVIOR_20260610_2253.md
```

Existing DolphinVersion changes were preserved and moved into the new
`variants/dolphin/` layout.

## Verification

```text
$ bash -n bin/codex-user-install bin/codex-setup bin/codex-project-init variants/dolphin/bin/dolphin
<no output>
```

```text
$ bin/codex-user-install --list-variants
codex	Default Codex	variants/codex/home
dolphin	DolphinVersion	variants/dolphin/home
```

```text
$ bin/codex-user-install --codex-home <tmp>
Variant installed: codex
Codex home installed at: <tmp>
default install ok
```

```text
$ bin/codex-user-install --variant codex --codex-home <tmp>
Variant installed: codex
Codex home installed at: <tmp>
codex install ok
```

```text
$ bin/codex-user-install --variant dolphin --codex-home <tmp>
Variant installed: dolphin
Codex home installed at: <tmp>
dolphin install ok
```

```text
$ printf '...' | bin/codex-setup --codex-home <tmp> --variant dolphin
Kurulum tamamlandı.
setup dolphin ok
```

```text
$ MODEL_API_BASE_URL=http://127.0.0.1:9 variants/dolphin/bin/dolphin
WARNING: model endpoint did not respond: http://127.0.0.1:9/models
export AGENT_HOME="variants/dolphin/home"
export MODEL_API_BASE_URL="http://127.0.0.1:9"
export MODEL_ID="cognitivecomputations_dolphin-mistral-24b-venice-edition"
```

```text
$ rg -n "codex-home-template|DolphinVersion/|agent-home|default-codex" README.md USAGE_GUIDE.md TURKCE_KURULUM_REHBERI.md REGISTRY_MANAGEMENT.md bin variants AGENTS_TEMPLATE.md docs/CHANGELOG.md || true
<no output>
```

## Result

The repository now has a single installable variant structure:

```text
variants/
  config.toml
  codex/home/
  dolphin/home/
  dolphin/bin/dolphin
  dolphin/docs/
```

The default install path is configured, and both direct and guided installers
can install the selected runtime variant.

## Final Checks

```text
$ python3 -c 'import pathlib,tomli; files=[pathlib.Path("variants/config.toml"), pathlib.Path("variants/codex/home/config.toml"), pathlib.Path("variants/dolphin/home/config.toml")]; [tomli.loads(p.read_text()) for p in files]; print("parsed", len(files), "toml files")'
parsed 3 toml files
```

```text
$ bin/codex-user-install --variant missing --codex-home <tmp>
FAILED: unknown variant: missing
Available variants:
codex	Default Codex	variants/codex/home
dolphin	DolphinVersion	variants/dolphin/home
```

```text
$ git diff --check
<no output>
```

```text
$ git diff -- AGENTS.md
<no output>
```

The root project `AGENTS.md` was intentionally left unchanged.
