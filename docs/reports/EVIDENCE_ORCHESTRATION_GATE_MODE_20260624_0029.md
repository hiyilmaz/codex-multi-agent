# Evidence: Orchestration Gate Mode

## Summary

Implemented project-level orchestration mode support and added the
`orchestration-gate` skill to runtime variants.

## Decision

Project configuration now uses:

```text
ORCHESTRATION_MODE: skip | ask-approval | run-chain
```

Default template value:

```text
ORCHESTRATION_MODE: ask-approval
```

The `orchestration-gate` skill decides whether to:

- skip orchestration
- ask for approval
- run the mandatory chain

The skill does not spawn subagents and does not bypass tool policy.
If active tool policy requires explicit approval before subagents are spawned,
`run-chain` falls back to approval-gated execution.

## Files Changed

- `AGENTS.md`
- `PROJECT_AGENTS_TEMPLATE.md`
- `PROJECT_CONFIG_PROMPT.md`
- `GLOBAL_AGENTS_TEMPLATE.md`
- `README.md`
- `USAGE_GUIDE.md`
- `TURKCE_KURULUM_REHBERI.md`
- `variants/codex/home/AGENTS.md`
- `variants/codex/home/README.md`
- `variants/codex/home/registry/AUDIT_LOG.md`
- `variants/codex/home/registry/ORCHESTRATION.md`
- `variants/codex/home/registry/SKILLS_INDEX.md`
- `variants/codex/home/skills/orchestration-gate/SKILL.md`
- `variants/codex/home/skills/orchestration-gate/agents/openai.yaml`
- `variants/dolphin/AGENTS.md`
- `variants/dolphin/docs/CHANGELOG.md`
- `variants/dolphin/home/AGENTS.md`
- `variants/dolphin/home/README.md`
- `variants/dolphin/home/registry/AUDIT_LOG.md`
- `variants/dolphin/home/registry/ORCHESTRATION.md`
- `variants/dolphin/home/registry/SKILLS_INDEX.md`
- `variants/dolphin/home/skills/orchestration-gate/SKILL.md`
- `variants/dolphin/home/skills/orchestration-gate/agents/openai.yaml`
- `docs/CHANGELOG.md`

## Verification Commands

```bash
rg -n "ORCHESTRATION_MODE|orchestration-gate" \
  AGENTS.md PROJECT_AGENTS_TEMPLATE.md PROJECT_CONFIG_PROMPT.md \
  GLOBAL_AGENTS_TEMPLATE.md README.md USAGE_GUIDE.md \
  TURKCE_KURULUM_REHBERI.md variants/codex/home variants/dolphin
```

Expected: project templates, runtime instructions, registries, README files,
and both variant skill directories reference the new mode and skill.

```bash
python3 /Users/iyilmaz/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  variants/codex/home/skills/orchestration-gate

python3 /Users/iyilmaz/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  variants/dolphin/home/skills/orchestration-gate
```

Expected: both skill folders validate successfully.

Observed:

```text
Skill is valid!
Skill is valid!
```

Temp install checks:

```bash
bin/codex-user-install --variant codex --runtime-home "$tmpdir/codex-home"
test -f "$tmpdir/codex-home/skills/orchestration-gate/SKILL.md"
rg -n "ORCHESTRATION_MODE|orchestration-gate" "$tmpdir/codex-home"

bin/codex-user-install --variant dolphin --runtime-home "$tmpdir/dolphin-home"
test -f "$tmpdir/dolphin-home/skills/orchestration-gate/SKILL.md"
rg -n "ORCHESTRATION_MODE|orchestration-gate" "$tmpdir/dolphin-home"
```

Observed: both temp runtime installs included
`skills/orchestration-gate/SKILL.md` and matching
`ORCHESTRATION_MODE` registry/runtime references.

Project init check:

```bash
printf 'y\n' | bin/codex-project-init "$tmpdir/project"
rg -n "ORCHESTRATION_MODE|orchestration-gate" "$tmpdir/project/AGENTS.md"
```

Observed:

```text
29:  - orchestration-gate
39:ORCHESTRATION_MODE: ask-approval
```

```bash
git diff --check
```

Expected: no whitespace errors.

Observed: no whitespace errors.
