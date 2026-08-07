# Claude Code Runtime Variant

This directory is the portable template for a user-global Claude Code CMA
runtime. The default target is Claude Code's native `~/.claude` user scope.
Explicit alternate targets remain available for isolated tests through
`--runtime-home` and `CLAUDE_CONFIG_DIR`.

Install it with:

```bash
bin/codex-user-install --variant claude
```

For the default native target, the installer delegates to the transactional
`bin/claude-native-activate` helper. It keeps an existing `settings.json`
unchanged, stores an existing `CLAUDE.md` plus its SHA-256 checksum under
`~/.claude/backups/cma-activation-<UTC timestamp>-<suffix>/`, and appends exactly
one functional `@registry/CMA_GLOBAL.md` import. Native activation rejects
`--force`, differing CMA-managed files, unsafe symlinks, and incomplete source
manifests. Backup or copy failures roll back newly created overlay files. The
legacy isolated Claude runtime is outside the activation scope.

Included:

- complete Core CMA `CLAUDE.md` policy
- conservative `settings.json`
- eight canonical agents and four Opus escalation agents
- four complete reusable skills and the record archive helper
- eight lazy modules and six registry records
- a portable subagent restoration prompt under `prompts/`

Claude agent definitions use Markdown with YAML frontmatter. Routine planner,
test, exploration, and documentation roles use Sonnet; review, governance, and
explicit complex escalation roles use Opus. All roles use medium effort. Opus
variants replace one matching invocation and never add a mandatory chain stage.

`prompts/recreate-global-subagents.md` restores the verified 12-agent matrix
from authoritative Claude Code definitions. It resolves an explicit target
first, then an active `CLAUDE_CONFIG_DIR`, then the current user's native
default. It preserves medium-effort Sonnet/Opus routing and avoids duplicating
full agent bodies in the prompt or result.

The mandatory approved chain remains exactly:

`planner -> tdd-guide -> code-reviewer -> security-reviewer`

Project-level `CLAUDE.md` may import the shared project `AGENTS.md` declaration.
The global and project instruction surfaces therefore stay active together.

Excluded:

- credentials and API keys
- sessions, logs, histories, caches, and memories
- hooks and permission bypass settings
- Codex-only TOML agents and `skills/*/agents/openai.yaml`
- existing settings, credentials, sessions, native Claude installation, and
  SDK dependency; native activation changes only the backed-up instruction
  bridge and missing CMA-owned files
