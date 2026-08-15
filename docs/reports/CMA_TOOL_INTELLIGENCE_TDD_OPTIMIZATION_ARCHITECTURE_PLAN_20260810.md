# CMA Tool Intelligence and TDD Optimization Architecture Plan

**Date:** 2026-08-10  
**Status:** Planning only  
**Scope:** CMA orchestration, discovery evidence reuse, lazy tool routing, and
review verification boundaries  
**Authority:** This document does not authorize implementation, installation,
runtime synchronization, tool activation, scanning, graph building, or
benchmark execution.
## 1. Architecture Recommendation

Adopt a lightweight, main-agent-owned Shared Evidence Packet before adding new
tools. The packet should preserve source identity, discovery claims, test
results, change identity, security decisions, and artifact ownership across the
mandatory chain:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

The main agent remains responsible for implementation after `tdd-guide` and
before `code-reviewer`. The chain, role order, correctness requirements, and
security independence remain unchanged.

The recommended target is **Option B-light**: a JSON-compatible task-local
manifest for non-trivial chains, with a message-only representation for small
tasks. It introduces no daemon, wrapper, project state directory, or second
runtime. Specialized tools should be integrated only after the evidence layer
has demonstrated measurable value.
## 2. Proposed Execution Flow

```text
Task input
  -> classify task and risk
  -> validate existing evidence and mark stale entries
  -> perform the minimum discovery needed for unresolved gaps
  -> create or update Shared Evidence Packet
  -> planner consumes evidence and defines scope/acceptance/gaps
  -> tdd-guide consumes planner contract and evidence, then defines RED
  -> main agent implements, invalidates stale evidence, and records RED/GREEN
  -> code-reviewer reuses current evidence and independently verifies claims
  -> security-reviewer performs targeted impact analysis and triggered checks
  -> main agent closes artifacts, validates cleanup, and reports status
```

The main agent is the sole canonical packet writer. Roles consume a packet
revision and return structured deltas; they do not mutate the canonical packet
directly. Evidence entries are append-only and content-addressed. Corrections
supersede prior entries instead of rewriting history.

Evidence should be created after initial task/risk classification and before
planner discovery. A trivial task may use the same structure inside the role
handoff without creating a file. After implementation, evidence tied to changed
source, scope, configuration, dependencies, or diff identity becomes stale.
## 3. Shared Evidence Packet Schema

Minimum JSON-compatible envelope:

```json
{
  "schema_version": "cma-evidence/v1",
  "packet_id": "uuid",
  "revision": 3,
  "parent_digest": "sha256-or-null",
  "packet_digest": "sha256",
  "task": {},
  "source": {},
  "evidence": [],
  "tests": {},
  "change": {},
  "security": {},
  "artifacts": {},
  "stage_state": {}
}
```

| Area | Minimum fields | Requirement |
| --- | --- | --- |
| Envelope | schema version, packet ID, revision, packet digest | REQUIRED |
| Envelope history | parent digest | CONDITIONAL after revision 1 |
| Task | task ID, scope, acceptance criteria, risk, prohibited actions | REQUIRED |
| Source | repository root identity, worktree fingerprint | REQUIRED |
| Source | VCS commit, affected paths, path hashes | CONDITIONAL |
| Source | timestamps | OPTIONAL; not a substitute for content identity |
| Evidence entry | ID, kind, one claim, source references, fingerprint, status, verification class | REQUIRED |
| Evidence entry | tool invocation reference | CONDITIONAL |
| Evidence entry | superseded entry ID | OPTIONAL |
| Tool invocation | tool, normalized request, cwd/scope, ordinal, result status, output digest | CONDITIONAL |
| Tool invocation | version, argv, ruleset/provider identity | CONDITIONAL when relevant |
| Tool invocation | bounded excerpt, timestamp | OPTIONAL |
| Tests | acceptance mapping, RED, GREEN, regression, implementation boundary | CONDITIONAL for mutations |
| Change | changed paths, diff digest, added/removed symbols | CONDITIONAL after mutation |
| Change | trust-boundary, dependency, config, and runtime change lists, including empty lists | REQUIRED after mutation |
| Security | impact class, rationale, scanner trigger decisions | REQUIRED for a completed chain |
| Security | scanner identity/version/ruleset, scope digest, findings | CONDITIONAL when a scanner runs |
| Artifacts | created artifacts, modified runtime state, temporary roots, cleanup status | REQUIRED, including empty lists |
| Stage state | stage, consumed evidence IDs, new IDs, invalidations, unresolved gaps | REQUIRED per handoff |

The packet must not contain full source files, full diffs, raw scanner logs,
graph databases, unrestricted test logs, secrets, credentials, or copied policy
bodies. It stores references, hashes, normalized queries, short bounded excerpts,
and outcome summaries.

## 4. Freshness and Invalidation Model

Freshness is identity-based, not time-based.

| Evidence class | Freshness identity | Invalidated when |
| --- | --- | --- |
| File read | canonical path plus content hash | that path's content or resolution changes |
| Symbol definition | tool/parser identity, file hash, symbol identity | defining file or parser semantics change |
| Symbol references | symbol identity plus complete scope manifest | any file in scope changes or scope changes |
| ast-grep result | tool version, pattern, language, scope manifest | pattern, tool, language, or any scoped file changes |
| Graphify positive edge | graph digest plus provenance file hashes | graph identity or a provenance file changes |
| Graphify absence/completeness/path claim | graph digest plus complete corpus identity | any corpus file or graph identity changes |
| Test result | exact command, environment identity, source/diff digest | source, test, relevant config, dependency, or environment changes |
| Code/security review | reviewed diff and trust-boundary manifest | diff or trust-boundary manifest changes |
| Opengrep/Betterleaks | tool/ruleset plus scanned scope digest | ruleset, tool, or scanned content changes |
| OSV-Scanner | tool/database identity plus manifest/lock hashes | lock/manifest or advisory database identity changes |
| External MCP/docs | provider, canonical reference/version, retrieval time | requested version changes or currency window expires |
| cplt execution | runtime/sandbox identity, argv/env, source digest | command, environment, sandbox, or source changes |

An unchanged source hash permits reuse of local deterministic evidence. It does
not prove that current external documentation, releases, or advisories remain
fresh. Unrelated file changes do not invalidate path-local evidence, but they do
invalidate claims whose recorded scope includes those files.

## 5. Discovery-Budget Model

Discovery is driven by unresolved evidence gaps rather than an arbitrary call
count:

```text
discovery entitlement = unresolved independent evidence gaps
                        x one primary provider per gap
```

Rules:

1. Consume current evidence first.
2. Use one primary provider for each unresolved claim.
3. Add a second provider only for a different evidence modality, a required
   source check, a contradiction, or independent verification.
4. Permit broad rediscovery only after explicit invalidation, source-identity
   mismatch, or contradictory evidence.
5. Stop when every acceptance/risk claim is supported, rejected, or honestly
   marked unverified.

| Task class | Normal discovery ceiling |
| --- | --- |
| Trivial | Tier 0, then a single Tier 1 lookup if needed |
| Local | Tier 0-1 within named or directly implicated files |
| Cross-file | Tier 0-1, then Serena or Graphify for a specific relationship gap |
| Structural | Tier 0-1, then ast-grep for a defined AST property |
| Security-sensitive | Base task tier plus only the security tool triggered by the changed boundary |
| External/current | Base task tier plus one authoritative external provider |
| High-risk execution | Base task tier plus an execution-safety decision; cplt is an orthogonal gate |

Security-sensitive, external/current, and high-risk execution are overlays, not
reasons to perform every lower or specialized tier.

## 6. Tool-Cost Tiers

| Tier | Providers | Activation trigger | Escalation and stop condition | Evidence and reuse | Side effects |
| --- | --- | --- | --- | --- | --- |
| 0 | Current packet | Current evidence covers the claim | Escalate only on stale/missing/contradictory evidence; stop when sufficient | Evidence IDs and source identities; highest reuse | None |
| 1 | Bounded direct read, `rg` | Exact text/path/local content | Escalate when semantic, structural, or cross-file identity is required | Path/hash/query/match evidence | Local reads/processes |
| 2 | Serena, ast-grep | Semantic symbol or AST-specific question | Escalate only when the question exceeds symbol/structure scope | Definitions/references or structural matches | Local server/process/index may initialize |
| 3 | Graphify | Genuine architecture, coupling, or cross-file path | Stop after the requested graph claim and source check | Graph/query/node/edge/provenance evidence | Graph/index activation; rebuild is separately gated |
| 4 | Opengrep, OSV-Scanner, Betterleaks | Specific security trigger | Run only the relevant scanner; stop at scoped result | Rules/database/scope/findings evidence | Local process, databases, possible artifacts |
| 5 | GitHub MCP, DeepWiki MCP, Context7 | Current or unavailable external knowledge | Use one suitable provider; stop after authoritative evidence | Provider/reference/version evidence | Network, startup, approval, remote disclosure |
| X | cplt | Untrusted or risky execution not adequately isolated otherwise | Use only if approved and available; otherwise do not execute when ordinary sandbox is insufficient | Runtime/command/environment/result evidence | Isolated execution and task artifacts |

Tier X is not the final discovery tier. It is an execution boundary that can be
combined with a justified discovery tier.

## 7. Escalation Decision Tree

```text
Classify task, source, risk, and currency need
  |
  +-- Current packet covers claim and identity is fresh? -> Tier 0; consume
  |
  +-- Exact text, filename/path, or known local file? -> Tier 1
  |
  +-- Semantic definition, references, or refactor radius? -> Serena
  |
  +-- Syntax/AST property? -> ast-grep
  |
  +-- Cross-file architecture, coupling, call/data path? -> Graphify
  |      `-> source-check material positive claims
  |
  +-- Security trigger? -> one relevant scanner
  |
  +-- Current/remote/version-specific evidence? -> one suitable external provider
  |
  `-- Risky execution? -> cplt if approved/available and ordinary sandbox is insufficient
```

The default is one discovery provider per evidence gap. Two providers are
justified only when they establish different properties, for example:

- Graphify relationship plus source verification;
- Serena symbol identity plus ast-grep structural property;
- OSV advisory mapping plus local lockfile identity;
- scanner result plus manual reproduction of a material finding;
- remote advisory plus local affected-code evidence.

If a primary tool is unavailable, record the unavailable state. Use a narrower
faithful fallback when one exists; otherwise leave the claim unverified. Do not
install a tool, silently widen scope, or claim equivalence for a lexical
approximation. Escalation proceeds narrow-to-broad.

## 8. Stage Input and Output Contracts

### Planner

Input: user request and a validated packet revision.

Output:

- scope and exclusions;
- acceptance criteria;
- affected surface and risk class;
- consumed evidence IDs;
- unresolved evidence gaps;
- explicit tool-escalation requests;
- assumptions and a packet delta.

The planner should primarily consume evidence. New discovery is limited to a
missing planning-critical gap.

### TDD Guide

Input: planner contract, source/test evidence, and unresolved gaps.

Output:

- acceptance-to-test mapping;
- meaningful RED oracle;
- boundary, negative, and regression checks;
- evidence dependencies;
- stale or missing evidence IDs;
- packet delta.

It must not repeat current planner discovery merely to restate the plan.

### Main Implementation

Input: planner contract, TDD contract, and current packet.

Responsibilities:

- invalidate evidence affected by edits before relying on it;
- make scoped edits;
- capture RED, GREEN, and regression evidence;
- publish changed-path, diff, symbol, trust-boundary, dependency, config, and
  runtime manifests;
- update artifact ownership and cleanup state.

### Code Reviewer

Input: packet, reviewed diff identity, changed-surface manifest, and tests.

Output: consumed evidence IDs, `trusted_reuse`, `targeted_verify`, and
`independent_reproduce` arrays; review commands/results; findings; disposition;
and a packet delta. Default behavior is reuse plus targeted validation of the
actual diff, not full discovery replay.

### Security Reviewer

Input: changed trust-boundary/dependency/config/artifact manifests, code-review
evidence, scanner decisions, and current packet.

Output: security impact class, targeted and independent checks, scanner trigger
decisions, findings, residual risk, disposition, and a packet delta. Scanners
run only when a recorded trigger applies.

## 9. Reviewer Independence Model

| Class | Typical evidence | Required reviewer behavior |
| --- | --- | --- |
| TRUSTED-REUSE | Exact unchanged file hash; immutable command result with matching source identity; unchanged dependency/scope manifest | Consume without reproducing; validate identity/digest chain |
| TARGETED-VERIFY | Acceptance-to-test mapping; changed files; Graphify positive edge; reference overlap; scanner-clean scope; config/runtime changes | Recheck the precise claim/path against current state |
| INDEPENDENT-REPRODUCE | Auth/authz; secret handling; destructive/path containment; fail-open behavior; dependency applicability; high/critical finding; hardcoded or weakened tests; security-critical call path | Reproduce from current source and runtime evidence without trusting the originating conclusion |

A `NO_SECURITY_IMPACT` claim becomes independently reproducible when a trust
boundary, dependency, config, runtime, secret-bearing artifact, or execution
surface changed. The final diff and test identity are always verified at
closure.

## 10. Per-Tool Integration Contracts

| Tool | Activation contract | Evidence contract | Reuse/invalidation | Fallback |
| --- | --- | --- | --- | --- |
| Graphify | Genuine cross-file architecture, call/data flow, coupling | Graph source/digest, query, nodes/edges, provenance files, source-check | Reuse on matching graph/provenance identity; completeness claims invalidate on corpus change | Targeted source/`rg`; Serena for symbol-only questions |
| Serena | Semantic symbol definition, references, refactor radius | Tool/version, symbol identity, definition, reference scope and locations | Reuse while symbol files and complete scope manifest match | Targeted `rg`, explicitly lexical |
| ast-grep | Syntax/AST structural question or transformation design | Version, language, pattern, scope, matched locations | Reuse while pattern/tool/scope hashes match | `rg` only as a declared lexical approximation |
| Opengrep | Code change matches a defined SAST/security trigger | Version/ruleset, scope digest, findings and exit status | Invalidate on ruleset/tool/scoped source change | Targeted manual review; never invent a clean scan |
| OSV-Scanner | Dependency manifest/lock change or dependency-CVE question | Tool/database identity, manifest/lock hashes, advisory mapping | Invalidate on lock/manifest/database change | Ecosystem audit or authoritative advisory research |
| Betterleaks | Credential, config, logs, generated artifacts, or secret-bearing change | Version/rules, scope digest, redacted findings | Invalidate on rules/scoped content change | Focused safe pattern checks; no secret disclosure |
| GitHub MCP | Remote source, release, changelog, or advisory evidence | Repository/ref, request, returned source identity, retrieval time | Reuse for immutable refs; current claims expire | Local checkout or official GitHub source |
| DeepWiki MCP | Public-repository conceptual knowledge unavailable or insufficient locally | Repository identity, question, cited source references | Reuse only for matching repository/ref and non-current claims | Local source, then GitHub/authoritative source |
| Context7 | Version-specific API or library documentation | Package/version, request, cited documentation identity | Reuse for the exact version; current claims expire | Official primary documentation |
| cplt | Approved untrusted/risky execution where ordinary sandbox is insufficient | Runtime/version, sandbox policy, argv/env summary, source digest, result/artifacts | Invalidate on command/runtime/policy/source change | Ordinary sandbox only if demonstrably sufficient; otherwise do not execute |

## 11. Architecture Option Comparison

| Option | Enforcement | Savings potential | Complexity/maintenance | Security blast radius | Observability/CMA fit | Main failure modes |
| --- | --- | --- | --- | --- | --- | --- |
| A. Policy plus structured prose | Low-medium | Medium | Low | Low | Compatible but weakly machine-checkable | Drift, omission, unparsable handoffs |
| B. Small task-local manifest | Medium-high | High | Medium | Low-medium | Strong identities and auditability; compatible | Stale manifest, schema bloat, cleanup errors |
| C. Runtime helper/wrapper | High on covered paths | High | High | High | Strong telemetry but creates a new execution surface | Bypass paths, wrapper authority, compatibility defects |
| D. Larger intelligence runtime | Potentially highest | Uncertain/high | Very high | Very high | Central orchestration but poor current fit | Second runtime, lock-in, state and policy divergence |

Recommendation: target **B-light**, but validate the first behavior through an
Option A message envelope. Adopt a task-local file only after the envelope and
freshness rules demonstrate measurable benefit. Reconsider C or D only if
benchmark evidence shows that B cannot meet correctness or observability needs.

## 12. Evidence Lifecycle

- Small task: packet remains in conversation/handoff state.
- Multi-stage task: main agent may materialize it in a task-owned temporary
  directory with mode `0700` and packet mode `0600`.
- Ownership: one task UUID and one canonical writer; role deltas name their
  input revision and output evidence IDs.
- Updates: atomic revisions with parent and packet digests; no in-place history
  rewriting.
- Safety: reject symlink/hardlink ambiguity, avoid secrets and raw sensitive
  output, and redact bounded excerpts.
- Concurrency: unique task IDs and roots; no shared mutable packet.
- Cleanup: resolve and validate the exact owned root, delete only owned
  artifacts, verify absence, and record truthful cleanup status.
- Retention: delete temporary packets at closure. Durable promotion requires an
  explicit, sanitized project-record decision.
- Persistent indexes/graphs remain tool-owned; the packet references their
  identity and does not copy them into a new CMA state directory.

## 13. Benchmark Design

Compare the current baseline with one candidate at a time on frozen repository
snapshots. Use the same task prompt, model/reasoning configuration, sandbox,
approval state, and stage chain. Run sequentially. Determine repetition count
only after observing baseline variance; do not invent a fixed percentage target.

Representative existing candidates:

| Category | Candidate record |
| --- | --- |
| Trivial lookup | EXP-007 exact/filename/known-file probes |
| Bugfix | EXP-20260809-002 documented ARK CLI path fix |
| Small feature | EXP-20260805-001 |
| Refactor | EXP-20260727-002 |
| Cross-file architecture | EXP-20260806-007 |
| Security-sensitive | EXP-20260809-007 |
| Dependency-related | EXP-20260806-008 |

Collect total and per-role wall-clock time; input, cached-input, output, and
reasoning tokens; top-level tool calls; duplicate discovery; repeated
file/module reads; Graphify, scanner, and MCP invocations; retries; test status;
code-review findings; security-review findings; and final correctness.

A duplicate discovery operation is the same normalized tool/query/scope/source
identity repeated by a later stage without invalidation. Required independent
verification is tagged separately and is not counted as waste.

## 14. Correctness and Performance Acceptance Model

### Immutable correctness gates

- Preserve the exact mandatory chain and implementation position.
- Pass all applicable existing and focused tests.
- Require a meaningful RED for behavior-changing implementation.
- Do not weaken assertions, skip tests, hardcode success, or swallow failures.
- Do not accept stale evidence as current.
- Validate source, revision, and digest identity at every handoff.
- Preserve targeted and independent reviewer checks.
- Do not suppress security findings or substitute a clean scan for reasoning.
- Source-check material Graphify claims.
- Treat unavailable tools and missing evidence as unverified, never successful.
- Track artifact ownership and report cleanup truthfully.

### Benchmark-derived performance targets

Establish thresholds only after the baseline distribution is measured. The
candidate should reduce duplicate discovery, total input/context, wall-clock,
and unnecessary module/tool activation beyond observed noise, while not
increasing retries, escaped findings, or correctness failures. Packet creation
and validation overhead must not exceed the measured savings.

## 15. Migration Phases

| Phase | Scope and expected benefit | Dependency/risk | Rollback and acceptance |
| --- | --- | --- | --- |
| 0 | Define observability and baseline protocol | No tool dependency; metric ambiguity | Docs-only rollback; metrics classified before execution |
| 1 | Planner-to-TDD message envelope | Low risk; tests handoff reuse | Restore contracts; measurable RED/GREEN and chain preserved |
| 2 | Full-chain packet, freshness, artifact lifecycle | Phase 1; stale/state risk | Remove manifest path; digest/invalidation/cleanup tests pass |
| 3 | Tier 0/1 discovery budgets | Phase 2; under-discovery risk | Restore routing prose; correctness unchanged and duplicates fall |
| 4A | Serena contract pilot | Availability and semantic accuracy | Remove route; one representative task proves value |
| 4B | ast-grep contract pilot | Availability and pattern accuracy | Remove route; structural task proves value independently |
| 5 | Graphify boundary | Fresh graph identity and source checks | Remove route; architecture task benefits without trivial activation |
| 6A-6C | Opengrep, OSV, Betterleaks separately | Tool/rules/database availability | Remove each trigger independently; security gates preserved |
| 7A-7C | GitHub, DeepWiki, Context7 separately | Network, approval, external disclosure | Disable provider; authoritative-use case proves value |
| 8 | cplt pilot | Explicit approval and sandbox evidence | Disable pilot; isolation benefit proven without authority drift |

Each phase is a separate approval and acceptance boundary. A failed phase is
rolled back and does not automatically authorize the next phase.

## 16. First Implementation Candidate

**Candidate:** Planner-to-TDD Structured Evidence Envelope v0.

This is the smallest candidate because it installs no tool, creates no runtime
service, adds no persistent state, and changes only one existing handoff. Its
schema subset contains: version, task identity, source identity, acceptance
criteria, affected paths, evidence IDs/claims, unresolved gaps, and consumed
evidence IDs.

Meaningful RED must establish one of these observable failures on the clean
baseline:

1. the current planner/TDD contracts cannot emit and validate a parseable,
   identity-bound envelope; or
2. on a fixed representative bugfix with pre-supplied source evidence, TDD
   repeats a current discovery operation that the envelope should preserve.

If neither failure is reproducible, the candidate hypothesis is unsupported and
the attempt must stop without weakening the oracle.

GREEN requires a valid planner envelope, TDD validation of source/digest
identity, explicit consumption of evidence IDs, no repeat of current evidence,
targeted discovery only for a named gap, equal or stronger test design, measured
JSONL evidence, and the unchanged mandatory chain. Rollback restores exact
preimages, performs no active sync, and removes only verified task-owned
temporary artifacts.

## 17. Risks and Failure Modes

- Evidence laundering: a summary is trusted without validating its source.
- Stale evidence survives a source, scope, config, dependency, or diff change.
- The packet becomes larger than the context it replaces.
- Weak digest or mutable-history handling hides replacement.
- Reviewers rubber-stamp producer conclusions.
- Independent review expands into full rediscovery.
- Metrics reward fewer calls while correctness declines.
- Graphify completeness is trusted without corpus identity or source checks.
- Scanner-clean results are treated as proof of security.
- Secrets enter excerpts, logs, or retained packets.
- Tool fallback silently changes semantic claims.
- External providers disclose unnecessary repository/task data.
- Temporary artifacts have weak permissions, ambiguous ownership, or incomplete cleanup.
- Concurrent tasks overwrite shared state.
- Conversation compaction drops packet identity or invalidation state.
- Schema rigidity causes prose workarounds or a shadow router.
- cplt pilot expands runtime authority beyond its approved boundary.

## 18. Open Product Decisions

The following require product or explicit implementation-phase decisions:

1. Which task classes require a materialized packet rather than message-only
   handoff?
2. What repository/worktree identity is canonical in non-Git workspaces?
3. Which environment fields are required for reusable test evidence?
4. What freshness window applies to release, advisory, and documentation data?
5. Which security changes mandate each scanner?
6. Which claims require independent reproduction regardless of risk score?
7. What external repository data may be sent to MCP providers?
8. Which MCP/provider approvals may be remembered within a task?
9. What defines ordinary-sandbox insufficiency for cplt escalation?
10. Are remote immutable Git references adequate for durable external evidence?
11. What benchmark variance and regression policy determines acceptance?
12. How long, if at all, may sanitized packets be retained?
13. Who owns schema versioning and backward compatibility?
14. What happens when role output cannot conform to the envelope schema?

## 19. Files Likely Affected by the First Candidate

If separately approved, the first candidate is expected to be limited to:

- `variants/codex/home/registry/ORCHESTRATION.md`
- `variants/codex/home/agents/planner.toml`
- `variants/codex/home/agents/tdd-guide.toml`
- `tests/test_cma_lazy_runtime.py`
- `docs/CHANGELOG.md`

This list is a planning estimate, not mutation authority. Exact paths and
preimages must be revalidated at implementation start.

## 20. Explicitly Not Changed Yet

This planning task does not change production code, global or portable policy,
active configuration, skills, agents, modules, tests, runtime state, trust
entries, tool installations, MCP connections, scanner state, Graphify graphs,
or the mandatory orchestration chain. It does not run a benchmark, create an
experiment, activate cplt, or make the EXP-007 `bounded-reader` oracle the
optimization objective.
