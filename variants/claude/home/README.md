# Claude Agent CMA Runtime

This directory is a portable Claude Code configuration source. Install it with
`bin/codex-user-install --variant claude`; launch it through `llm-claude`.

The launcher sets `CLAUDE_CONFIG_DIR` to the isolated installed runtime home and
then delegates to an existing native `claude` executable. This template stores
no credentials, sessions, hooks, cache, or machine-local state.

The runtime uses Claude-native surfaces:

- `CLAUDE.md` for Core CMA policy
- `settings.json` for conservative permission defaults
- `agents/*.md` for the four mandatory chain roles
- `skills/*/SKILL.md` for reusable workflows

The Claude Agent SDK is not installed or required by this native variant.
