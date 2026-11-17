---
name: betterleaks
description: Use conditionally for possible exposure of credentials, tokens, keys, secrets, or sensitive configuration; not for general SAST or dependency CVEs.
---

# Betterleaks

## Governance Metadata

- Stable Skill ID: betterleaks
- Display Name: Betterleaks
- Capability Category: secret-detection
- Core / Protected Status: core/protected
- Tool Dependency: required: betterleaks
- Semantic Version: 1.0.0

## Purpose

Use Betterleaks conditionally for secret exposure detection as one primary evidence need.

## Use When

- Credentials, tokens, keys, secrets, or sensitive configuration may be exposed.
- A bounded file, diff, or authorized history scope requires secret detection.
- The user explicitly requests Betterleaks for a secret-exposure evidence need.

## Do Not Use When

- General SAST or source security analysis; use Opengrep.
- Dependency or package vulnerability detection; use OSV-Scanner.
- Ordinary text search, configuration formatting, or every routine task.

## Preconditions

- Confirm the secret-exposure evidence need and bound the file, diff, or history scope.
- Confirm Betterleaks is available and redacted output is supported before analysis.
- Obtain separate authority for repository-history expansion, network validation, configuration changes, or broad scans.

## Workflow

1. State the secret-exposure question and smallest authorized scope.
2. Enable redacted output before running bounded read-only detection.
3. Triage the finding without copying, storing, or validating the matched value.
4. Stop when sufficient redacted evidence and provenance are recorded.

## Stop Conditions

- Stop when the bounded secret-exposure question has sufficient redacted evidence.
- Stop if redaction cannot be guaranteed or the need is general SAST or dependency vulnerability detection.
- Stop before history expansion, network validation, configuration, mutation, or broad scanning without authority.
- Stop as unavailable when Betterleaks is unavailable.

## Output Contract

- Report finding type, severity when available, location, short explanation, and remediation direction.
- Keep every finding redacted; Never report the matched secret value, full credential, token, or key.
- State scan scope and detector provenance without reproducing sensitive configuration, and report truthful status and success fields.

## Safety / Authority Boundary

- Betterleaks analysis is conditional, read-only, redacted, and bounded; it never runs by default on every task.
- This skill never authorizes installation, configuration, repository-history expansion, network validation, credential use, mutation, or a broad repository scan.
- Treat every match as sensitive; never expose, persist, echo, or transmit the matched value.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked secret-exposure evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another scanner, or widen the evidence route.
