# Runtime Skill Scope Audit

**Date:** 2026-07-14 02:18 +03  
**Mode:** Read-only audit followed by user-approved cleanup.

## Scope

All skill files packaged under `variants/*/home/skills/`, their skill registry
entries, tracked-file state, and related agent definitions were checked for
project-specific content that does not belong in the generic runtime template.

## Commands

```text
git status --short
git ls-files 'variants/*/home/skills/**'
find variants -type d -path '*/skills/*'
rg -n -i 'formproxy|crypto|signalbot|signal bot|turnstile|tenant|smtp|...'
git log --follow -- <skill paths>
```

The worktree was clean at audit start. The tracked runtime contains seven
Codex skills and two Dolphin skills.

## Findings

### F-01 — FormProxy skill bundle

**Classification:** Remove from the generic runtime template.  
**Confidence:** Confirmed.

Tracked files:

- `variants/codex/home/skills/formproxy-implementation-planner/SKILL.md`
- `variants/codex/home/skills/formproxy-security-review/SKILL.md`
- `variants/codex/home/skills/formproxy-verification-loop/SKILL.md`

Evidence:

- Every skill names FormProxy directly in its frontmatter and heading.
- The planner requires FormProxy-specific `docs/PRD.md` and
  `docs/TEST_PLAN.md` contracts.
- The security reviewer mandates FormProxy domain controls including
  Cloudflare Turnstile, tenant isolation, submission ordering, and SMTP.
- The three skills are registered as globally active in
  `variants/codex/home/registry/SKILLS_INDEX.md` lines 16-18.
- Git history shows they entered the portable template in commit `cea9dba` and
  moved into the current variant layout in `e3addbc`; they are not baseline
  runtime governance skills.

Required removal scope:

1. Remove the three tracked skill directories from the Codex variant.
2. Remove their three active rows from the Codex `SKILLS_INDEX.md`.
3. Remove the local empty FormProxy directories under
   `variants/dolphin/home/skills/`; Git does not track them, but direct installs
   from this working copy can still copy empty directories.

### F-02 — Crypto strategy discovery skill

**Classification:** Remove from the generic runtime template or package as an
explicit optional/domain bundle.  
**Confidence:** High.

Tracked files:

- `variants/codex/home/skills/crypto-strategy-discovery/SKILL.md`
- `variants/codex/home/skills/crypto-strategy-discovery/agents/openai.yaml`

Evidence:

- The complete workflow is limited to crypto markets, signal bots, backtests,
  realized trade data, exchange accounts, and trading strategy evaluation.
- It is useful reusable content, but it is a domain skill rather than a generic
  Codex runtime/governance dependency.
- It is registered globally in
  `variants/codex/home/registry/SKILLS_INDEX.md` line 13.
- Git history shows the same portable-template origin as the FormProxy skills.

Required removal scope for a strictly generic runtime:

1. Remove the tracked `crypto-strategy-discovery` directory from the Codex
   variant.
2. Remove its active row from the Codex `SKILLS_INDEX.md`.
3. Remove the local empty directory under
   `variants/dolphin/home/skills/crypto-strategy-discovery/`.

If this personal domain skill must remain distributable, it should be moved to
an optional bundle that is not installed by the default runtime installer.

## Retained Skills

| Skill | Decision | Reason |
|---|---|---|
| `orchestration-gate` | Keep | Generic runtime governance and required by the project contract. |
| `tdd-workflow` | Keep | Generic implementation workflow, required in every variant. |

`tdd-workflow` contains `/api/markets` and `NextRequest` snippets as isolated
testing examples. They do not reference a named project, repository path,
project document, or project-specific operational contract. They are therefore
not classified as project leakage and the skill must not be removed.

## Result

Four domain/project-specific skills are outside a strictly generic runtime
surface: three confirmed FormProxy skills and one crypto strategy skill. The
corresponding four Codex registry entries must be removed with them. Four
untracked empty directory remnants under the Dolphin skill tree should also be
deleted during the approved cleanup. No other project-specific skill, tracked
skill file, or agent-role content was detected.

## Applied Cleanup

After user approval, the four identified Codex skill directories and their
four active registry rows were removed. The corresponding empty Dolphin
directory remnants were also removed. The Codex registry audit log records the
change.

Verification:

- `quick_validate.py` passed for `orchestration-gate` and `tdd-workflow` in
  both variants.
- Clean temporary installs of both variants contained only
  `orchestration-gate` and `tdd-workflow` under `skills/`.
- No FormProxy or crypto strategy reference was found in either temporary
  runtime installation.
- The complete Python test suite passed: 4 tests, 0 failures.
- `git diff --check` passed.
