# Evidence: Project Upgrade For Orchestration Mode

## Summary

Added `bin/codex-project-upgrade` so already initialized project directories can
receive the current orchestration baseline without rerunning reset-style project
init.

## Behavior

The upgrade command:

- requires an existing `<project>/AGENTS.md`
- edits only the `## Project Configuration` fenced text block
- adds `orchestration-gate` to `ACTIVE_SKILLS` when missing
- adds `ORCHESTRATION_MODE: ask-approval` when missing
- archives the previous `AGENTS.md` under
  `<project>/.codex/archive/upgrade-YYYYMMDD_HHMMSS/`
- supports `--dry-run`

## Verification

Commands to run:

```bash
bash -n bin/codex-project-upgrade
```

Observed: command completed without syntax errors.

```bash
tmpdir=$(mktemp -d)
mkdir -p "$tmpdir/project"
cp PROJECT_AGENTS_TEMPLATE.md "$tmpdir/project/AGENTS.md"
perl -0pi -e 's/\n  - orchestration-gate//; s/\nORCHESTRATION_MODE: ask-approval\n//;' "$tmpdir/project/AGENTS.md"
bin/codex-project-upgrade --dry-run "$tmpdir/project"
printf 'y\n' | bin/codex-project-upgrade "$tmpdir/project"
rg -n "orchestration-gate|ORCHESTRATION_MODE" "$tmpdir/project/AGENTS.md"
find "$tmpdir/project/.codex/archive" -type f -name AGENTS.md
rm -rf "$tmpdir"
```

Expected:

- dry run prints a diff and does not write
- confirmed run updates `AGENTS.md`
- archive contains the previous `AGENTS.md`

Observed:

```text
dry_run_preserved=yes
29:  - orchestration-gate
39:ORCHESTRATION_MODE: ask-approval
<project>/.codex/archive/upgrade-20260624_003645/AGENTS.md
Already up to date: <project>/AGENTS.md
```

Missing `AGENTS.md` check:

```bash
tmpdir=$(mktemp -d)
mkdir -p "$tmpdir/project"
bin/codex-project-upgrade "$tmpdir/project"
rm -rf "$tmpdir"
```

Observed:

```text
FAILED: missing project AGENTS.md: <project>/AGENTS.md
Run codex-project-init first if this project has not been initialized.
```

```bash
git diff --check
```

Expected: no whitespace errors.
