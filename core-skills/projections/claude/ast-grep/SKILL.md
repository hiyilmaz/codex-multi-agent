---
name: ast-grep
description: Use for structural AST search and syntax-aware matching; not for text, filenames, architecture, or ordinary symbol references.
disable-model-invocation: true
user-invocable: true
---

# ast-grep

## Governance Metadata

- Stable Skill ID: ast-grep
- Display Name: ast-grep
- Capability Category: structural-search
- Core / Protected Status: core/protected
- Tool Dependency: required: ast-grep
- Semantic Version: 1.0.0

## Purpose

Use ast-grep for structural AST search and syntax-aware matching as one primary evidence need.

## Use When

- The search depends on syntax shape rather than literal text.
- A language-aware structural pattern must match across bounded source files.
- The user explicitly requests ast-grep for a structural-search evidence need.

## Do Not Use When

- Filename, path, exact string, or plain-text lookup; use `rg` or direct read.
- Architecture, cross-file flow, or component relationships; use Graphify.
- Ordinary symbol definition, reference, or refactor-radius lookup; use Serena.

## Preconditions

- Identify the language, structural pattern or rule, and bounded search scope.
- Check that ast-grep and the required language parser are available.
- Confirm that the task requests search only, not rewrite or transformation.

## Workflow

1. Express the smallest syntax-aware pattern that represents the evidence need.
2. Run a bounded structural search without rewrite options.
3. Inspect representative matches and exclude false structural matches.
4. Stop when the pattern, scope, and match evidence satisfy the question.

## Stop Conditions

- Stop when sufficient validated structural matches have been collected.
- Stop if the request resolves to text, path, architecture, or ordinary symbol lookup.
- Stop as unavailable if ast-grep or the required parser is unavailable.
- Stop before any rewrite, fix, or code mutation without separate authority.

## Output Contract

- Report tool availability, language, pattern or rule, bounded scope, matched locations, and representative match evidence.
- State false-positive limitations and use truthful status and success fields.
- Do not present text matches as structural AST evidence.

## Safety / Authority Boundary

- Structural search is read-only by default; do not use rewrite or update modes.
- This skill never authorizes installation, configuration, code transformation, file changes, or broader repository access.
- Do not expose secrets; minimize and redact sensitive evidence.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked structural evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another core skill, or widen the evidence route.
