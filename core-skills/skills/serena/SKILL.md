---
name: serena
description: Use for symbols, definitions, references, and refactor radius; not for text, architecture, or structural AST search.
---

# Serena

## Governance Metadata

- Stable Skill ID: serena
- Display Name: Serena
- Capability Category: symbol-intelligence
- Core / Protected Status: core/protected
- Tool Dependency: required: serena
- Semantic Version: 1.0.0

## Purpose

Use Serena for symbols, definitions, references, and refactor radius as one primary evidence need.

## Use When

- A named symbol's definition, callers, references, or bounded usage set is required.
- A proposed refactor needs a symbol-level impact radius before changes.
- The user explicitly requests Serena for a symbol-intelligence evidence need.

## Do Not Use When

- Exact text, path, or filename lookup; use `rg` or direct read.
- Architecture, cross-file call/data flow, or component coupling; use Graphify.
- Structural AST pattern or syntax-shape search; use ast-grep.

## Preconditions

- Identify the symbol, language context, and bounded repository scope.
- Check that Serena is available and the repository is indexed or accessible.
- Confirm that the task requests read-only symbol evidence, not a refactor mutation.

## Workflow

1. Before the first symbol or reference query, resolve the task's absolute project root and call `get_current_config`. Use the active-project path from Serena's session instructions if the config reports only a name and the session has not switched projects. Treat a `No active project` error as missing context.
2. If the active path is missing or differs from the target, call `activate_project` with the task's absolute project root when the task authorizes activation. A first activation can create Serena project files. Get authorization for that side effect if the task has not already authorized it.
3. After activation, recheck the active project with `get_current_config`. If it reports only a name, require the activation result to confirm the exact absolute path and the config to confirm the same active project. If inspection or activation fails or the exact path still cannot be verified, report the reason and stop before querying symbols or references.
4. Resolve the smallest unambiguous symbol identity. Locate its definition and only the references needed for the question.
5. Bound and summarize the refactor radius when requested.
6. Stop when the symbol evidence and provenance requirements are satisfied.

## Stop Conditions

- Stop when the requested definition, references, or refactor radius is complete.
- Stop if the request resolves to text, architecture, or structural AST search.
- Stop as unavailable if Serena cannot provide the required symbol evidence.
- Stop before editing or refactoring code without separate authority.

## Output Contract

- Report the tool availability, symbol identity, definition location, bounded reference scope, and relevant locations.
- Report the verified active project path or the reason project verification failed.
- Distinguish confirmed symbol results from ambiguity and state limitations.
- Use truthful status and success fields.

## Safety / Authority Boundary

- Symbol discovery is read-only by default.
- This skill never authorizes installation, configuration, indexing that mutates project state, refactoring, code changes, or broader repository access.
- Do not expose secrets; minimize and redact sensitive evidence.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked symbol evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another core skill, or widen the evidence route.
