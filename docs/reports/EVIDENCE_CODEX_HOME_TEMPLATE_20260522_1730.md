# Evidence: Codex Home Template

## Task

Add a portable `~/.codex` template to the project so the user-global Codex
runtime surface can be installed quickly on another machine.

## Commands

```bash
find codex-home-template -maxdepth 3 -type f | sort
bash -n bin/codex-user-install
python3 -c 'import pathlib,tomli; files=[pathlib.Path("codex-home-template/config.toml")]+list(pathlib.Path("codex-home-template/agents").glob("*.toml")); [tomli.loads(p.read_text()) for p in files]; print("parsed", len(files), "template toml files")'
rg -n "<absolute-user-path>|sessions|cache|logs|hooks.state|trusted_hash|projects\." codex-home-template -S
bin/codex-user-install --codex-home /private/tmp/codex-home-install-test-20260522
```

## Results

- `bash -n bin/codex-user-install` passed.
- Template config plus agent TOML files parsed successfully:
  `parsed 9 template toml files`.
- Install smoke test passed into
  `/private/tmp/codex-home-install-test-20260522`.
- The template intentionally excludes runtime sessions, logs, caches, hook
  state, project trust entries, and machine-local paths.

## Included Template Surface

- `codex-home-template/AGENTS.md`
- `codex-home-template/config.toml`
- `codex-home-template/agents/`
- `codex-home-template/skills/`
- `codex-home-template/registry/`
