---
name: osv-scanner
description: Use conditionally for dependency and package vulnerability detection when manifests, lockfiles, SBOMs, or dependency status matter; not for source SAST or secret detection.
---

# OSV-Scanner

## Governance Metadata

- Stable Skill ID: osv-scanner
- Display Name: OSV-Scanner
- Capability Category: dependency-vulnerability-analysis
- Core / Protected Status: core/protected
- Tool Dependency: required: osv-scanner
- Semantic Version: 1.0.0

## Purpose

Use OSV-Scanner conditionally for dependency and package vulnerability detection as one primary evidence need.

## Use When

- Dependencies, manifests, lockfiles, or SBOMs change.
- Package vulnerability status or a dependency CVE is relevant to the task.
- The user explicitly requests OSV-Scanner for dependency vulnerability evidence.

## Do Not Use When

- Source-code SAST or security-sensitive source behavior; use Opengrep.
- Secret, credential, token, or key exposure; use Betterleaks.
- Ordinary source discovery, dependency formatting, or every routine task.

## Preconditions

- Confirm the dependency evidence need and bound the manifest, lockfile, SBOM, or package scope.
- Confirm OSV-Scanner and required local package metadata are already available.
- Obtain separate authority for network access, database updates, package-manager execution, or dependency changes.

## Workflow

1. State the package-vulnerability question and bounded dependency inputs.
2. Run the smallest authorized detection-only analysis.
3. Correlate reported vulnerabilities with the resolved package identity and version.
4. Stop when sufficient dependency-vulnerability evidence and provenance are recorded.

## Stop Conditions

- Stop when the bounded dependency question has sufficient evidence.
- Stop if the need is source SAST or secret exposure detection.
- Stop before fix mode, package-manager execution, network access, database update, or dependency mutation without authority.
- Stop as unavailable when OSV-Scanner or required package metadata is unavailable.

## Output Contract

- Report finding type, severity when available, location, short explanation, and remediation direction.
- Include affected package, resolved version, advisory identifier, input scope, and distinguish vulnerabilities found from execution failure.
- Avoid sensitive configuration values and report truthful status and success fields.

## Safety / Authority Boundary

- OSV-Scanner analysis is conditional, detection-only, and bounded; it never runs by default on every task.
- This skill never authorizes installation, configuration, database updates, network access, fix mode, package-manager execution, or dependency changes.
- Do not expose credentials or sensitive package-source configuration; minimize and redact evidence.

## Tool Unavailable Behavior

- Report `availability=unavailable`, `status=unverified`, `success=false`, and `action=stop`.
- Name the blocked dependency-vulnerability evidence need and stop the dependent workflow.
- Never install, configure, activate, emulate, substitute another scanner, or widen the evidence route.
