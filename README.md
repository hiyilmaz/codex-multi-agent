# Codex Template V2

**Version:** 2.6
**Updated:** 2026-08-15

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
| `COMMAND_REFERENCE.md` | Consolidated runtime, project, and verification commands |
| `CODEX_CONFIG_EXAMPLE.toml` | Optional project `.codex/config.toml` example |
| `PROJECT_CONFIG_PROMPT.md` | Prompt copied into projects after init |
| `REGISTRY_MANAGEMENT.md` | User-global skill/agent registry model |
| `variants/` | Installable runtime variants and default variant config |
| `TURKCE_KURULUM_REHBERI.md` | Turkish quick setup guide |
| `docs/openai-codex/` | Local updateable index of official OpenAI Codex docs |
| `bin/` | User-global and project init helper scripts |

---

## Runtime Model

The active reusable runtime surface lives under `~/.codex/`. Project
`AGENTS.md` files declare what is active but do not store reusable bodies.

Reusable content locations:

- User-global rules: `~/.codex/rules`
- User-global skills: `~/.codex/skills`
- User-global agents: `~/.codex/agents`
- User-global registry: `~/.codex/registry`

Reusable bodies should not be copied into project `AGENTS.md`.

Project orchestration behavior is declared with:

```text
ORCHESTRATION_MODE: skip | ask-approval | run-chain
```

The default project template uses `ask-approval`. The `orchestration-gate`
skill decides whether a task should skip orchestration, ask for approval, or
run the mandatory chain. When that chain is disclosed in the approved main
plan, the initial approval covers its planned agents and non-destructive Low or
Medium risk work; destructive and High/Critical work remains separately gated.

Every runtime variant packages `tdd-workflow`. The `tdd-guide` agent defines
the focused test strategy, and the skill enforces the test-first
RED-GREEN-refactor workflow during implementation.

Every runtime variant also packages `hypothesis-workflow`. It remains inactive
for routine first-pass work and escalates only failed, unclear, competing,
regressing, measurement-dependent, or explicitly requested improvements into a
traceable experiment.

The mandatory chain uses bounded handoffs: each agent consumes prior evidence,
avoids repeated discovery, returns a concise result, and stops. Codex chain
agents default to `medium` reasoning. Passing tests alone do not prove
completion; review also checks acceptance criteria, observable behavior, and
test integrity.

### Main Plan Execution

CMA requests approval once for a disclosed main plan, then completes its
planned phases without task-boundary pauses. It reports material list updates,
auxiliary discoveries, recommended work, and a truthful terminal result.
That approval also covers disclosed non-destructive Low/Medium work and planned
orchestration. Destructive and High/Critical operations still require separate
approval.
Work discovered outside the approved plan stays on an auxiliary list and is
not executed unless it is required to continue. A required deviation is
reported and approved before the plan changes. Recommended work is reported
separately and is never added to the main plan automatically.

Installable runtime variants live under `variants/`:

- `variants/codex/home/` — Default Codex runtime template
- `variants/claude/home/` — Claude Agent native CLI runtime template
- `variants/opencode/home/` — OpenCode native CLI runtime template
- `variants/config.toml` — default variant selection

---

## Quick Start

Install or refresh the default Codex runtime:

```bash
bin/codex-user-install
```

Install a specific variant:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant claude
bin/codex-user-install --variant opencode
```

The installer rewrites installed template paths to the selected target
`--runtime-home`.

When the Codex target resolves exactly to `$HOME/.codex`, the installer then
runs `bin/codex-native-activate`. It additively enables the ten protected core
tools, makes Context7 required but lazy, keeps cplt explicit-only, and preserves
an existing Graphify installation. It enables only Serena, DeepWiki, GitHub,
and Context7 MCP entries; xcodebuildmcp remains disabled. Custom runtime homes
and custom runtime homes remain portable. Native Claude and OpenCode activation
projects the same ten skills into their official user skill locations.
Restart Codex or begin a new session after native activation.

Default targets:

- `codex` -> `$HOME/.codex`
- `claude` -> `$HOME/.claude`
- `opencode` -> `$HOME/.config/opencode`

Variant launchers are installed as:

```text
<runtime-home>/bin/llm-claude
<runtime-home>/bin/llm-opencode
```

OpenCode activation uses its official `~/.config/opencode/skills` location and
preserves unrelated configuration, identity state, and skills. It installs no
plugin, provider, credential, or MCP server without a separately verified
official schema. Validate with `opencode mcp list` and `opencode debug config`.

The user-global Codex surface also provides `claude-docs` and `opencode-docs`.
They are narrow official-documentation skills: Claude guidance uses only
`code.claude.com/docs` or `docs.anthropic.com`; OpenCode guidance uses only
`opencode.ai/docs`. The matching native runtime receives only its own vendor
skill, and unavailable official evidence is reported as unverified rather than
guessed.

## Global MCP Contract

All three supported runtimes use the same four user-global MCP identities:
`serena`, `deepwiki`, `github`, and `context7`. The parity helper first checks
the installed Codex, Claude Code, and OpenCode versions, then performs an
additive, backup-backed merge using only `GITHUB_PAT_TOKEN` and
`CONTEXT7_API_KEY` references; it never writes their values. OpenCode 1.18 uses
its legacy top-level `mcp.<name>` configuration shape. `xcodebuildmcp` remains
disabled and cplt is not an MCP server.

```bash
bin/cma-mcp-parity
codex mcp list
claude mcp list
opencode mcp list
```

The default Claude installation uses its native user-global directory. It
preserves existing `CLAUDE.md` content through a backed-up import overlay,
leaves existing `settings.json` unchanged, and rejects `--force`. Explicit
alternate `--runtime-home` targets remain available for isolated testing.
`llm-claude` sets `CLAUDE_CONFIG_DIR` to its installed runtime home and delegates
to an already installed native `claude` command; it does not install the Claude
Agent SDK or authenticate.

Native activation adds exactly one functional `@registry/CMA_GLOBAL.md` import
to `~/.claude/CLAUDE.md`. Before changing an existing instruction file, it saves
the original and its SHA-256 checksum under
`~/.claude/backups/cma-activation-<UTC timestamp>-<suffix>/`. Existing
CMA-managed files must match the packaged source; conflicts, unsafe symlinks,
incomplete sources, or copy failures stop the activation without leaving a
partial overlay. Any legacy isolated Claude runtime is not removed or modified.

Run the interactive setup:

```bash
bin/codex-setup
```

Without `--variant`, setup asks whether to install all catalog variants. Answer
yes to install every active variant without further selection questions; answer
no to choose each variant individually. `--variant <id>` keeps the explicit
single-variant flow.

Initialize a project or add runtime variants:

```bash
bin/codex-project-init /path/to/project
```

Without `--variant`, init asks whether to apply every active catalog variant;
declining asks each one individually. On a new project, init creates the shared
project instructions and all selected variant surfaces. On an existing project,
init is additive: it preserves
`AGENTS.md`, shared prompts, customized files, and every existing variant while
adding only the requested surface. Multiple runtime variants can coexist and
are recorded in `.codex/template-state.json`.

Codex uses `.codex/config.toml`; Claude adds `CLAUDE.md` and
`.claude/settings.json`; OpenCode adds `.opencode/opencode.json`. Use `--reset`
only for an intentional destructive reinitialization; it displays and privately
archives conflicting files before recreating the project structure.

After init, run the generated prompt:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

That prompt tells the AI to inspect the project and fill only the
`AGENTS.md` `Project Configuration` block. If required values are ambiguous, it
must ask the user before editing instead of writing placeholders.

Upgrade an already initialized project without resetting its `AGENTS.md`:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

Dry-run is the default. Upgrade preserves project-specific values and additions,
merges only missing baseline fields into `AGENTS.md`, updates unchanged
template-managed files, and leaves locally modified files untouched. Every
applied change is archived under
`.codex/archive/upgrade-YYYYMMDD_HHMMSS_microseconds/`.

## Local Codex Docs

Refresh the local OpenAI Codex documentation index:

```bash
scripts/update-openai-codex-docs
```

The index is stored under `docs/openai-codex/`.

---

# EOF
