# Evidence: Dolphin Install Path Rewrite

Task ID: `DOLPHIN_INSTALL_PATH_REWRITE`
Date: `2026-06-10 23:19`

## Scope

Fix variant installation so installed Dolphin runtime files point to the
selected target home instead of the source template path.

## Files Changed

- `bin/codex-user-install`
- `README.md`
- `USAGE_GUIDE.md`
- `TURKCE_KURULUM_REHBERI.md`
- `docs/CHANGELOG.md`

## Intended Behavior

- Default install target remains `$HOME/.codex`.
- `--codex-home <path>` installs into the selected target path.
- Installed files are rewritten only when they are actually copied or
  overwritten.
- Source templates under `variants/` are not rewritten.

## Verification Commands

```text
bash -n bin/codex-user-install bin/codex-setup variants/dolphin/bin/dolphin
```

```text
tmp=$(mktemp -d)
bin/codex-user-install --variant dolphin --codex-home "$tmp"
rg -n 'variants/dolphin/home' "$tmp" || true
rg -n "agent_home = \"$tmp\"" "$tmp/config.toml"
rg -n "launcher = \".*/variants/dolphin/bin/dolphin\"" "$tmp/config.toml"
```

```text
tmp_home=$(mktemp -d)
HOME="$tmp_home" bin/codex-user-install --variant codex
test -f "$tmp_home/.codex/AGENTS.md"
```

## Result

Installed Dolphin runtime files now resolve to the selected target home. The
default Codex installation target remains `$HOME/.codex`.

## Observed Results

```text
$ bash -n bin/codex-user-install bin/codex-setup variants/dolphin/bin/dolphin
bash syntax ok
```

```text
$ tmp="$(mktemp -d)"; bin/codex-user-install --variant dolphin --codex-home "$tmp"
Variant installed: dolphin
Codex home installed at: <tmp>

$ rg -n 'variants/dolphin/home' "$tmp" || true
<no output>

$ rg -n "agent_home = \"$tmp\"|launcher = \".*/variants/dolphin/bin/dolphin\"" "$tmp/config.toml"
3:agent_home = "<tmp>"
6:launcher = "<repo>/variants/dolphin/bin/dolphin"
dolphin rewrite install ok
```

```text
$ tmp_home="$(mktemp -d)"; HOME="$tmp_home" bin/codex-user-install --variant codex
Variant installed: codex
Codex home installed at: <tmp_home>/.codex
codex default home ok
```

```text
$ tmp="$(mktemp -d)"; printf 'keep-me variants/dolphin/home\n' > "$tmp/AGENTS.md"; bin/codex-user-install --variant dolphin --codex-home "$tmp"
Skipped existing: <tmp>/AGENTS.md
skip protection ok
```

```text
$ tmp="$(mktemp -d)"; printf 'keep-me variants/dolphin/home\n' > "$tmp/AGENTS.md"; bin/codex-user-install --variant dolphin --codex-home "$tmp" --force
1:# DolphinVersion Runtime Instructions
20:AGENT_HOME: <tmp>
force rewrite ok
```
