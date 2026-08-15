# OpenCode Runtime Variant

This directory is the portable, provider-neutral CMA template for OpenCode.
Its default target is the isolated `~/.config/opencode` directory.

Install and launch it with:

```bash
bin/codex-user-install --variant opencode
~/.config/opencode/bin/llm-opencode
```

The launcher sets `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, and all XDG config,
data, cache, and state roots inside the isolated runtime before delegating to an
already installed native `opencode` binary. Symlinked state roots fail closed.
This prevents native global configuration and identity state from merging into
the CMA runtime. It does not install OpenCode, select a provider or model,
authenticate, or modify `~/.config/opencode`.

Included:

- Core CMA policy in `AGENTS.md`
- stable OpenCode configuration in `opencode.json`
- eight provider-neutral Markdown subagents
- four reusable workflow skills and the record archive helper
- eight lazy policy modules and registry records
- a portable subagent restoration prompt

The mandatory approved chain remains exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`
