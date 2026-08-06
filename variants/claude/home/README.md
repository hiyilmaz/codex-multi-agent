# Claude Code Runtime Variant

This directory is the portable template for a user-global Claude Code CMA
runtime. The default native location is `~/.claude`; the launcher and tests use
`CLAUDE_CONFIG_DIR` so isolated runtimes do not mutate active local state.

Install it with:

```bash
bin/codex-user-install --variant claude
```

Included:

- complete Core CMA `CLAUDE.md` policy
- conservative `settings.json`
- eight canonical agents and four Opus escalation agents
- four complete reusable skills and the record archive helper
- eight lazy modules and six registry records

Claude agent definitions use Markdown with YAML frontmatter. Routine planner,
test, exploration, and documentation roles use Sonnet; review, governance, and
explicit complex escalation roles use Opus. All roles use medium effort. Opus
variants replace one matching invocation and never add a mandatory chain stage.

The mandatory approved chain remains exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

Project-level `CLAUDE.md` may import the shared project `AGENTS.md` declaration.
The global and project instruction surfaces therefore stay active together.

Excluded:

- credentials and API keys
- sessions, logs, histories, caches, and memories
- hooks and permission bypass settings
- Codex-only TOML agents and `skills/*/agents/openai.yaml`
- active `~/.claude` mutation, native Claude installation, and SDK dependency
