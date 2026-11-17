---
name: graphify
description: Use for architecture, cross-file relationships, and call or data flow; not for text, path, single-file, symbol, or AST lookup.
---

# Graphify

## Governance Metadata

- Stable Skill ID: graphify
- Display Name: Graphify
- Capability Category: architecture-analysis
- Core / Protected Status: core/protected
- Tool Dependency: required: graphify
- Semantic Version: 1.0.0

## Purpose

Use Graphify for architecture, cross-file relationships, and call or data flow as one primary evidence need.

## Use When

- The question depends on relationships across multiple files or components.
- A call path, data path, dependency chain, or architectural boundary must be mapped.
- The user explicitly requests Graphify for an architecture evidence need.

## Do Not Use When

- Exact text or path lookup, filename lookup, or a single known-file read; use `rg` or direct read.
- Symbol definition, reference, or refactor-radius lookup; use Serena.
- Structural syntax or AST-pattern matching; use ast-grep.

## Preconditions

- Confirm the evidence need is architectural and the repository scope is bounded.
- Check that Graphify is available and that a usable graph exists.
- Obtain explicit authority before creating or updating a graph.

## Workflow

1. State the architecture question and bounded repository scope.
2. Query the smallest sufficient existing graph view.
3. Source-check material graph claims with direct repository reads.
4. Stop when the architecture question and provenance requirements are satisfied.

## Stop Conditions

- Stop when sufficient source-checked relationship evidence has been collected.
- Stop if the request resolves to text, path, symbol, or syntax-structure lookup.
- Stop as unavailable if Graphify or the required graph is unavailable.
- Stop before graph creation, update, or other mutation without explicit authority.

## Output Contract

- Report the architecture conclusion, relevant nodes and edges, repository locations, and query scope.
- Distinguish Graphify-derived candidates from claims confirmed by direct source reads.
- State limitations and use truthful status and success fields.

## Safety / Authority Boundary

- Existing-graph queries and source reads are read-only by default.
- This skill never authorizes installation, configuration, graph creation or update, code changes, network access, or broader repository access.
- Do not expose secrets; minimize and redact sensitive evidence.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked architecture evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another core skill, or widen the evidence route.
