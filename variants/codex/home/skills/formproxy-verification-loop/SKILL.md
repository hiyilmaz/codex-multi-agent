---
name: "formproxy-verification-loop"
description: "Run the lightest sufficient verification for FormProxy changes and report evidence clearly."
origin: "global"
---

# FormProxy Verification Loop

Use this skill after meaningful code or config changes.

## Goals

- Verify with the lightest sufficient checks first
- Do not claim success without evidence
- Prefer targeted checks before full suites

## Workflow

1. Identify what changed: config, docs, backend, frontend, tests
2. Choose the smallest proving check first
3. Escalate only if that check passes or is insufficient
4. Record what was verified and what was not verified

## Preferred Order

1. File existence and config sanity
2. Focused lint/type/test command for changed area
3. Broader integration or E2E checks only if relevant

## Reporting

- State exactly what command or inspection was used
- State whether the result is proof, partial proof, or not verifiable
- Call out any remaining risk or unverified path
