# Evidence: AGENTS Assistant Behavior Guidance

Task ID: `AGENTS_ASSISTANT_BEHAVIOR`
Date: `2026-06-10 15:04`

## Scope

Add persistent global assistant conduct guidance to the Codex home instruction
templates without changing project-local `AGENTS.md`.

## Files Changed

- `GLOBAL_AGENTS_TEMPLATE.md`
- `codex-home-template/AGENTS.md`
- `docs/CHANGELOG.md`

## Pre-flight

```text
$ pwd
/Users/iyilmaz/WebStorm/Codex-Multi-Agent

$ git status --short
?? DolphinVersion/

$ test -f GLOBAL_AGENTS_TEMPLATE.md && test -f codex-home-template/AGENTS.md && test -f docs/CHANGELOG.md && printf 'target files ok\n'
target files ok
```

The untracked `DolphinVersion/` directory existed before this task and was not
modified.

## Diff Summary

```text
$ git diff --stat
 GLOBAL_AGENTS_TEMPLATE.md     | 52 +++++++++++++++++++++++++++++++++++--------
 codex-home-template/AGENTS.md | 52 +++++++++++++++++++++++++++++++++++--------
 docs/CHANGELOG.md             |  5 +++++
 3 files changed, 91 insertions(+), 18 deletions(-)
```

## Verification

```text
$ cmp -s GLOBAL_AGENTS_TEMPLATE.md codex-home-template/AGENTS.md && printf 'global templates match\n'
global templates match
```

```text
$ rg -n 'Assistant Conduct|Truth|uncertainty|Recommended / Default|literal `nao`|overrides simple-task' GLOBAL_AGENTS_TEMPLATE.md codex-home-template/AGENTS.md
GLOBAL_AGENTS_TEMPLATE.md:60:### 2. Assistant Conduct
GLOBAL_AGENTS_TEMPLATE.md:71:- Separate verified facts, interpretation, and estimates when uncertainty
GLOBAL_AGENTS_TEMPLATE.md:82:  exactly three options. Mark one option as `Recommended / Default` and briefly
GLOBAL_AGENTS_TEMPLATE.md:85:  `Recommended / Default` option when safe.
GLOBAL_AGENTS_TEMPLATE.md:88:- If the user ends a request with literal `nao`, explain what you understood,
GLOBAL_AGENTS_TEMPLATE.md:163:- A request ending with literal `nao` overrides simple-task execution: explain
codex-home-template/AGENTS.md:60:### 2. Assistant Conduct
codex-home-template/AGENTS.md:71:- Separate verified facts, interpretation, and estimates when uncertainty
codex-home-template/AGENTS.md:82:  exactly three options. Mark one option as `Recommended / Default` and briefly
codex-home-template/AGENTS.md:85:  `Recommended / Default` option when safe.
codex-home-template/AGENTS.md:88:- If the user ends a request with literal `nao`, explain what you understood,
codex-home-template/AGENTS.md:163:- A request ending with literal `nao` overrides simple-task execution: explain
```

```text
$ wc -l GLOBAL_AGENTS_TEMPLATE.md codex-home-template/AGENTS.md AGENTS.md docs/CHANGELOG.md
     329 GLOBAL_AGENTS_TEMPLATE.md
     329 codex-home-template/AGENTS.md
      95 AGENTS.md
      17 docs/CHANGELOG.md
     770 total
```

## Result

The approved assistant conduct guidance is now stored in the global Codex home
templates. The project-local `AGENTS.md` file was intentionally left unchanged.

## Final Checks

```text
$ git diff --check
<no output>
```

```text
$ git status --short
 M GLOBAL_AGENTS_TEMPLATE.md
 M codex-home-template/AGENTS.md
 M docs/CHANGELOG.md
?? DolphinVersion/
?? docs/reports/EVIDENCE_AGENTS_ASSISTANT_BEHAVIOR_20260610_1504.md
```
