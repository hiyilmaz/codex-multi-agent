# Setup Preferences

**Status:** Template Default

## YOLO Mode

```text
YOLO_MODE: disabled
```

YOLO mode may allow lower-risk automation to proceed with fewer interruptions.

YOLO mode must not bypass approval for:

- `DROP`
- `DELETE *`
- `TRUNCATE`
- `rm -rf`
- `git reset --hard`
- `git push --force`
- adding dependencies
- changing API contracts
- DB schema changes
- auth/security code changes

If any of these are needed: stop, report, and wait for user approval.
