# Evidence: Safe Project Upgrade

## Summary

Added versioned, hash-aware project template migrations that preserve local
project instructions, prompts, configs, domain rules, and documentation.

## Safety Contract

- Upgrade defaults to dry-run and performs no writes.
- Applying an upgrade requires `--apply` and confirmation unless `--force` is
  explicitly provided.
- `--force` skips confirmation only; it does not overwrite customized files.
- `AGENTS.md` uses an additive field-level merge inside `Project Configuration`.
- Existing project values, custom list entries, domain rules, and all content
  outside the managed block are preserved.
- Template-managed prompt/config files are updated only when their current hash
  matches the recorded installed-template hash.
- Legacy or locally modified files are preserved, shown as a non-applied
  local/template comparison, and marked project-owned after approval.
- Every changed existing file is copied to a timestamped upgrade archive before
  replacement.
- Repeated upgrades are idempotent.

## Template State

New project initialization creates:

```text
.codex/template-state.json
```

The state records:

- schema version
- project template version
- selected runtime variant
- per-file ownership mode
- installed-template hashes for managed files

The state is stored separately from `.codex/config.toml` so it does not add
custom metadata to Codex's reserved runtime configuration schema.

## CLI

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
bin/codex-project-upgrade --apply --force /path/to/project
```

Running without a mode is equivalent to `--dry-run`.

## Fixture Verification

Fresh initialized project:

```text
State: managed
AGENTS.md: UNCHANGED
.codex/config.toml: UNCHANGED
.codex/prompts/fill-project-configuration.md: UNCHANGED
.codex/template-state.json: UNCHANGED
PASS fresh manifest and idempotent dry-run
```

Legacy project with local prompt/config changes:

```text
State: legacy-safe bootstrap
AGENTS.md: MERGE
.codex/config.toml: PRESERVE_LEGACY
.codex/prompts/fill-project-configuration.md: PRESERVE_LEGACY
.codex/template-state.json: CREATE
PASS legacy additive migration preserves local files
```

Customized managed prompt:

```text
.codex/prompts/fill-project-configuration.md: PRESERVE_CUSTOMIZED
.codex/template-state.json: UPDATE
PASS customized managed file is preserved and reclassified
```

Unchanged managed prompt with an older recorded template:

```text
.codex/prompts/fill-project-configuration.md: UPDATE
PASS unchanged managed file receives template update
```

Apply, archive, permissions, and idempotence:

```text
PASS default dry-run is non-mutating
PASS apply archives changes and preserves permissions
PASS repeated upgrade is idempotent
PASS invalid orchestration mode stops upgrade
PASS CLI argument validation
PASS syntax and diff checks
```

## Automated Regression Test

Command:

```bash
python3 -m unittest discover -s tests -p 'test_project_upgrade.py' -v
```

Observed:

```text
test_customized_managed_file_is_preserved ... ok
test_fresh_project_records_state_and_is_idempotent ... ok
test_legacy_project_preserves_local_files ... ok
test_unchanged_managed_file_receives_update_and_is_archived ... ok

Ran 4 tests
OK
```

## Static Verification

```bash
python3 -c "compile(open('bin/codex-project-upgrade').read(), \
  'bin/codex-project-upgrade', 'exec')"
bash -n bin/codex-project-init bin/codex-setup bin/codex-user-install
git diff --check
```

Observed: all checks passed.
