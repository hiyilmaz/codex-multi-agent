# Grok Build Runtime Variant

This is the native CMA projection for Grok Build, using `~/.grok` by default.
An existing native `grok` executable is required to launch it.

```bash
bin/codex-user-install --variant grok
~/.grok/bin/llm-grok version
~/.grok/bin/llm-grok inspect --json
```

Native activation preserves existing configuration, credentials, instructions,
and unrelated assets. Conflicting CMA-owned assets and unsafe managed paths
fail before installation. New files use private permissions. Activation records
created files and hashes under `backups/cma-activation-*`; a failed write rolls
back only unchanged files created by that transaction. Existing instructions
receive a private snapshot and a path-only merge prompt rather than replacement.

Alternate `--runtime-home` installations use the portable installer. The
launcher selects its installed directory with `GROK_HOME`, forwards arguments
and exit status, and disables background updates. It does not install Grok,
authenticate, choose a model, or change the native executable.

`GROK_HOME` does not isolate vendor compatibility discovery. Grok may also read
Claude instructions, hooks, plugins, and shared `~/.agents/skills`. Inspect the
reported source paths when validating a deployment. Project configuration is
limited to MCP servers, plugins, and permissions; global model/UI settings
belong in the user configuration. This template enables no MCP servers.

Included: eight native Markdown agents, four workflow skills, ten existing
core skill instructions, lazy policy modules, registry records, and a recovery
prompt. Core skill instructions do not install or authenticate their tools.
Read-only roles specify native tool allowlists and `permissionMode: plan`;
`inspect` proves discovery, not enforcement or successful model execution.

The approved chain remains:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

Sources: [settings](https://docs.x.ai/build/settings),
[rules](https://docs.x.ai/build/features/project-rules),
[agent definitions](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-agent/README.md),
[skills and compatibility](https://docs.x.ai/build/features/skills-plugins-marketplaces).
