# Evidence: Deferred Findings Global AGENTS Behavior

## Summary

Added global deferred findings behavior so agents can record out-of-scope
issues without expanding the active task scope.

## Decision

Deferred findings are stored in:

```text
docs/DEFERRED_FINDINGS.md
```

The document is created only when a deferred finding is actually found.

## Behavior Added

- Keep the requested task as the only active work.
- Record out-of-scope bugs, risks, cleanup needs, missing tests, outdated docs,
  and follow-up improvements as deferred records.
- Do not investigate deferred findings beyond the minimum needed to describe
  them accurately.
- Do not implement deferred items unless the user explicitly approves them in a
  new task.
- Keep `Pending` and `Completed` items separate.
- Record discovery and fix times in `YYYY-MM-DD HH:MM` format.

## Files Updated

- `GLOBAL_AGENTS_TEMPLATE.md`
- `variants/codex/home/AGENTS.md`
- `/Users/iyilmaz/.codex/AGENTS.md`
- `docs/CHANGELOG.md`

## Verification Commands

```bash
rg -n "Deferred Findings Log|docs/DEFERRED_FINDINGS.md|Discovered At|Fixed At" \
  GLOBAL_AGENTS_TEMPLATE.md variants/codex/home/AGENTS.md /Users/iyilmaz/.codex/AGENTS.md
```

Expected: all three AGENTS files include the deferred findings policy.

Observed:

```text
GLOBAL_AGENTS_TEMPLATE.md:97:### 4. Deferred Findings Log
variants/codex/home/AGENTS.md:97:### 4. Deferred Findings Log
/Users/iyilmaz/.codex/AGENTS.md:97:### 4. Deferred Findings Log
GLOBAL_AGENTS_TEMPLATE.md:106:docs/DEFERRED_FINDINGS.md
variants/codex/home/AGENTS.md:106:docs/DEFERRED_FINDINGS.md
/Users/iyilmaz/.codex/AGENTS.md:106:docs/DEFERRED_FINDINGS.md
```

Heading order was verified as:

```text
3. Scope Lock
4. Deferred Findings Log
5. Destructive Operations
6. CHANGELOG
7. File Size
8. Commit Rules
9. Domain Rules
10. Bounded Execution
11. Critical Decision Format
12. Confirm Before Execute
```

```bash
git diff --check
```

Expected: no whitespace errors.

Observed: no whitespace errors.
