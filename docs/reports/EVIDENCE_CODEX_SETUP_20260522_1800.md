# Evidence: Codex Interactive Setup

## Task

Add an interactive setup flow, sanitize local user/path references from docs,
and add default status messages plus a YOLO-mode preference with mandatory
approval boundaries.

## Commands

```bash
bash -n bin/codex-setup bin/codex-user-install bin/codex-project-init
python3 -c 'import pathlib,tomli; files=[pathlib.Path("codex-home-template/config.toml")]+list(pathlib.Path("codex-home-template/agents").glob("*.toml")); [tomli.loads(p.read_text()) for p in files]; print("parsed", len(files), "template toml files")'
printf '\ny\ny\ny\n\n\n\n\nn\n' | bin/codex-setup --codex-home /private/tmp/codex-setup-test-20260522b
rg -n "<local-user-name>|<local-host-name>|<local-workspace-root>" . --hidden -g '!docs/openai-codex/**' -g '!.git/**'
```

## Results

- Shell syntax checks passed.
- Template TOML files parsed successfully.
- Interactive setup smoke test passed against a temporary Codex home.
- The temporary setup wrote `YOLO_MODE: enabled` while preserving the mandatory
  approval boundary for destructive and high-risk changes.
- User-specific local name search returned no matches in checked project files.
