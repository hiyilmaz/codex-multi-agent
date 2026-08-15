---
name: opengrep
description: Use conditionally for SAST and security-sensitive source behavior; not for dependency CVEs, secret-only exposure, or ordinary source discovery.
disable-model-invocation: true
user-invocable: true
---

# Opengrep

## Governance Metadata

- Stable Skill ID: opengrep
- Display Name: Opengrep
- Capability Category: static-application-security-testing
- Core / Protected Status: core/protected
- Tool Dependency: required: opengrep
- Semantic Version: 1.0.0

## Purpose

Use Opengrep conditionally for SAST and security-sensitive source behavior as one primary evidence need.

## Use When

- Source changes affect authentication, authorization, command execution, deserialization, input parsing, permission boundaries, or security-sensitive data handling.
- A bounded source-security question requires rule-based static analysis.
- The user explicitly requests Opengrep for a SAST evidence need.

## Do Not Use When

- Dependency or package vulnerability detection; use OSV-Scanner.
- Secret, credential, token, or key exposure; use Betterleaks.
- Ordinary source discovery, exact text lookup, architecture mapping, or every routine task.

## Preconditions

- Confirm a source-security evidence need and bound the target paths and rule set.
- Confirm Opengrep and the intended rules are already available.
- Obtain separate authority for network access, rule downloads, configuration changes, or broad scans.

## Workflow

1. State the security question, scope, and applicable rule source.
2. Run the smallest authorized read-only analysis against bounded source paths.
3. Triage findings against source context; do not treat a match as proof by itself.
4. Stop when sufficient source-security evidence and provenance are recorded.

## Stop Conditions

- Stop when the bounded SAST question has sufficient evidence.
- Stop if the need is dependency vulnerability or secret exposure detection.
- Stop before network access, rule download, configuration, code change, or broad scanning without authority.
- Stop as unavailable when Opengrep or the required rules are unavailable.

## Output Contract

- Report finding type, severity when available, location, short explanation, and remediation direction.
- Identify the analyzed scope and rule provenance, and distinguish confirmed findings from candidates.
- Omit or redact sensitive snippets and report truthful status and success fields.

## Safety / Authority Boundary

- Opengrep analysis is conditional, read-only, and bounded; it never runs by default on every task.
- This skill never authorizes installation, configuration, rule downloads, network access, code changes, or expansion to a broad repository scan.
- Do not expose secrets or unsafe sensitive source snippets; minimize and redact evidence.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked SAST evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another scanner, or widen the evidence route.
