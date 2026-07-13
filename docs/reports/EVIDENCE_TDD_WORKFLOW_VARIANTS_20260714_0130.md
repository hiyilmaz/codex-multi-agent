# Evidence: TDD Workflow Runtime Variants

## Summary

Imported the existing Codex-native ECC `tdd-workflow` skill into both portable
runtime variants and preserved it as a mandatory project skill.

## Upstream Source

- Repository: `/Users/iyilmaz/Codex-ECC`
- Repository commit: `4e66b2882da9afb9747468b08a253ca2f09c85f3`
- Skill path: `.agents/skills/tdd-workflow/`
- License: MIT

The legacy `skills/tdd-workflow` copy was not used because it requires Git
checkpoint commits, which conflicts with this project's no-auto-commit policy.

## Compatibility Normalization

The canonical Codex skill failed current validation because its frontmatter
contained the unsupported field `origin: ECC`. The imported copies replace
that field with `license: MIT`. The workflow body is unchanged, and
`agents/openai.yaml` is byte-identical to upstream.

```text
upstream SKILL.md sha256:
63249998befbdbbf2f7d2f089c9cd7a9912f26ddc8fdf04ab1248c82614b43ac

codex and dolphin normalized SKILL.md sha256:
bd9352a67bb6a137f46317f13df05af00491cfa4f9184cbf2b6961bc8c75f22a

upstream and variant openai.yaml sha256:
ac132cb2dc93fa89181f8abe4067930ab215a440894be46fc5d0ebde7ee6185b
```

## Validation

Validate both source skill folders:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  variants/codex/home/skills/tdd-workflow
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  variants/dolphin/home/skills/tdd-workflow
```

Observed:

```text
Skill is valid!
Skill is valid!
PASS source skill validation and variant parity
```

Install both variants into an isolated temporary home and validate discovery:

```bash
HOME="$TEST_HOME" bin/codex-user-install --variant codex
HOME="$TEST_HOME" bin/codex-user-install --variant dolphin
```

Observed:

```text
Variant installed: codex
Variant installed: dolphin
PASS installed runtime discovery matrix
```

Verified in both installed runtime homes:

- `skills/tdd-workflow/SKILL.md` exists.
- `skills/tdd-workflow/agents/openai.yaml` exists.
- `SKILLS_INDEX.md` declares `tdd-workflow` active.
- Installed skill validation passes.

Initialize an isolated project and verify the baseline contract:

```bash
printf 'y\n' | HOME="$TEST_HOME" bin/codex-project-init "$PROJECT"
rg -n 'orchestration-gate|tdd-workflow|ORCHESTRATION_MODE' \
  "$PROJECT/AGENTS.md"
```

Observed:

```text
29:  - orchestration-gate
30:  - tdd-workflow
38:ORCHESTRATION_MODE: ask-approval
PASS generated project contract and upgrade compatibility
```

Remove `tdd-workflow` from an isolated project and verify upgrade recovery:

```bash
HOME="$TEST_HOME" bin/codex-project-upgrade --dry-run "$PROJECT"
```

Observed:

```text
+  - tdd-workflow
Dry run only. No files changed.
PASS upgrade adds missing tdd-workflow in dry-run without mutation
```

Final static checks:

```bash
bash -n bin/codex-user-install bin/codex-setup bin/codex-project-init \
  bin/codex-project-upgrade variants/dolphin/bin/dolphin
cmp -s PROJECT_CONFIG_PROMPT.md \
  .codex/prompts/fill-project-configuration.md
git diff --check
```

Observed:

```text
PASS syntax, prompt sync, and whitespace checks
```
