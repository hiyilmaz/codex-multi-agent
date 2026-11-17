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

1. Resolve the smallest unambiguous symbol identity.
2. Locate its definition and only the references needed for the question.
3. Bound and summarize the refactor radius when requested.
4. Stop when the symbol evidence and provenance requirements are satisfied.

## Stop Conditions

- Stop when the requested definition, references, or refactor radius is complete.
- Stop if the request resolves to text, architecture, or structural AST search.
- Stop as unavailable if Serena cannot provide the required symbol evidence.
- Stop before editing or refactoring code without separate authority.

## Output Contract

- Report the tool availability, symbol identity, definition location, bounded reference scope, and relevant locations.
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
