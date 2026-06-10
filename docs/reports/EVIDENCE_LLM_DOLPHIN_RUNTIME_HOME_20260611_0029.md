# Evidence: LLM Dolphin Runtime Home

Task ID: `LLM_DOLPHIN_RUNTIME_HOME`
Date: `2026-06-11 00:29`

## Scope

Move Dolphin launcher installation away from repository-local paths and install
it into the selected runtime home as `bin/llm-dolphin`.

## Changes

- `variants/config.toml`
  - `codex` default home remains `~/.codex`.
  - `dolphin` default home is `~/.llm-runtimes/dolphin`.
  - Dolphin launcher name is `llm-dolphin`.
- `bin/codex-user-install`
  - Supports `--runtime-home` while preserving `--codex-home` as an alias.
  - Installs variant launchers under `<runtime-home>/bin/`.
  - Rewrites installed launcher paths to `<runtime-home>/bin/llm-dolphin`.
- `bin/codex-setup`
  - Uses variant default runtime homes from `variants/config.toml`.
- Docs updated to use runtime-home language.

## Verification

```text
$ bash -n bin/codex-user-install bin/codex-setup variants/dolphin/bin/dolphin
syntax ok
```

```text
$ HOME=<tmp-home> bin/codex-user-install --variant dolphin
Variant installed: dolphin
Runtime home installed at: <tmp-home>/.llm-runtimes/dolphin

$ test -f <tmp-home>/.llm-runtimes/dolphin/bin/llm-dolphin
$ rg -n 'agent_home|launcher' <tmp-home>/.llm-runtimes/dolphin/config.toml
3:agent_home = "<tmp-home>/.llm-runtimes/dolphin"
6:launcher = "<tmp-home>/.llm-runtimes/dolphin/bin/llm-dolphin"
```

```text
$ HOME=<tmp-home> bin/codex-user-install --variant codex
Variant installed: codex
Runtime home installed at: <tmp-home>/.codex
codex default runtime ok
```

```text
$ bin/codex-user-install --variant dolphin --runtime-home <tmp-runtime>
Variant installed: dolphin
Runtime home installed at: <tmp-runtime>

$ MODEL_API_BASE_URL=http://127.0.0.1:9 <tmp-runtime>/bin/llm-dolphin
export AGENT_HOME="<tmp-runtime>"
export MODEL_API_BASE_URL="http://127.0.0.1:9"
export MODEL_ID="cognitivecomputations_dolphin-mistral-24b-venice-edition"
```

```text
$ HOME=<tmp-home> bin/codex-setup --variant dolphin
Runtime home dizini [~/.llm-runtimes/dolphin]
Kurulum tamamlandı.
setup dolphin runtime ok
```

## Result

Dolphin runtime installs are no longer tied to a repository-local launcher path.
The installed launcher is portable within the selected runtime home. The Codex
variant still defaults to `$HOME/.codex`.
