# Evidence - DolphinVersion Assistant Behavior

## Task

Apply the assistant conduct guidance from the root global instruction template
to the isolated DolphinVersion runtime instructions.

## Source Files Reviewed

- `docs/CHANGELOG.md`
- `docs/reports/EVIDENCE_AGENTS_ASSISTANT_BEHAVIOR_20260610_1504.md`
- `GLOBAL_AGENTS_TEMPLATE.md`

## Files Changed

- `variants/dolphin/home/AGENTS.md`
- `variants/dolphin/docs/CHANGELOG.md`
- `variants/dolphin/docs/reports/EVIDENCE_DOLPHIN_ASSISTANT_BEHAVIOR_20260610_2253.md`

## Result

- Added `Assistant Conduct` guidance to `variants/dolphin/home/AGENTS.md`.
- Preserved DolphinVersion's neutral runtime language and local isolation rules.
- Added the `nao` approval-wait rule to the simple workflow section.

## Verification

```text
rg -n 'Assistant Conduct|uncertainty|Recommended / Default|literal `nao`|overrides simple-task' variants/dolphin/home/AGENTS.md
```

Matched the new assistant conduct section and the workflow override rule.

- Legacy tool-specific file names were checked and no path matches remained.
- Legacy tool-specific runtime names and endpoint values were checked and no
  content matches remained.

```text
git diff --check
```

No whitespace errors.
