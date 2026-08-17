# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260815-003 - Autonomous Main Plan Execution

Date: 2026-08-15
Status: ACCEPTED

Problem:
The per-task approval gate creates unnecessary user pauses inside a disclosed
and approved multi-phase plan.

Hypothesis:
One initial main-plan approval can reduce interaction while preserving explicit
approval for destructive, High, and Critical operations.

Solution Attempt:
Project the same main-plan, auxiliary-task, recommended-task, and terminal
reporting policy to Codex, Claude, and OpenCode.

Test:
Require policy-contract, portable-install, and safety-regression tests.

Success Criteria:
Planned work proceeds without boundary approvals while safety approvals remain
mandatory and all variants expose equivalent behavior.

Evidence:
- The four canonical policies expose one equivalent Main Plan Execution
  contract, and the installed Codex, Claude, and official OpenCode policies
  byte-match their sources. The legacy OpenCode copy matches the changed
  approval sections while retaining its expected runtime-path substitution.
- Clause-removal and contradictory-policy mutants reject missing plan,
  deviation, recommendation, terminal-report, and destructive-safety terms.
- Focused suites passed 5/5, 25/25, and 11/11; the full suite passed 343/343.
- Code review passed after strengthening the public documentation contract;
  security review found no authority widening, backup issue, secret exposure,
  record loss, or duplicate archive entry.

Result:
Core policy 2.5 now uses one approved ordered plan for uninterrupted disclosed
work across Codex, Claude, and OpenCode. Required plan deviations and all
destructive, High, or Critical operations remain separately approval-gated.
Auxiliary and recommended work stay outside automatic main-plan execution, and
terminal reporting remains evidence-based. Active global policies were updated
with private rollback material and require a new runtime session to be loaded.

Decision:
ACCEPT

## EXP-20260815-002 - Official Native Claude and OpenCode Parity

Date: 2026-08-15
Status: ACCEPTED

Problem:
The approved CMA core-tool activation is currently Codex-only. Claude and
OpenCode have incomplete native projections, while the retired Dolphin source
variant remains selectable.

Hypothesis:
An additive, official-schema-only activation path can project the ten protected
skills and narrow vendor-documentation skills to the native Claude and OpenCode
locations without overwriting unmanaged configuration, credentials, or MCP
entries; removing Dolphin only from repository selection preserves its existing
installed runtime.

Solution Attempt:
Use the canonical Claude/OpenCode projections, vendor-native skill layouts, and
the installed stable CLIs' documented configuration surfaces. Add conflict-aware
native activation, remove Dolphin from the source catalog, and update the
corresponding installer, tests, and user documentation.

Test:
Require positive, idempotency, unmanaged-content preservation, conflicting
managed-content rejection, Dolphin rejection, syntax, focused, and full-suite
checks before active-runtime verification. Do not embed credentials, enable
xcodebuildmcp, execute cplt payloads, or delete the existing Dolphin runtime.

Decision:
ACCEPTED

Result:
The source catalog now exposes only Codex, Claude, and OpenCode; existing
Dolphin runtime data was not removed. Official native Claude and OpenCode skill
locations now contain the ten protected projections plus their own narrow
vendor-documentation skill. Existing conflicting Claude managed files were
replaced only after explicit per-file approval and saved in owner-only backup
directories. OpenCode activation rejects unsafe ancestors and managed-path
symlinks, rolls back created files on publication failure, preserves unrelated
configuration, and has no configured MCP server added by this change.

## EXP-20260815-001 - Global Codex Core Tool Activation

Date: 2026-08-15
Status: ACCEPTED

Problem:
The ten protected CMA repository-tool capabilities exist as canonical skills and
inactive native projections, but the active Codex runtime does not discover all
ten globally. Context7 is still classified as optional, and there is no bounded,
conflict-aware activation path that preserves customized global skills and MCP
configuration.

Evidence:
The protected registry marks Context7 optional, the Codex profile reports zero
projected instances and explicit-only inactive representation, and only Graphify
is present among the ten global CMA tool skills. Serena, DeepWiki, GitHub, and
Context7 MCP servers are enabled; xcodebuildmcp is disabled. Existing accepted
experiments explicitly stopped before active runtime synchronization.

Hypothesis:
Changing the canonical/projection contracts to required lazy routing and adding
one additive, atomic Codex activator will make the ten capabilities globally
discoverable while selecting only the narrowest provider, preserving customized
Graphify state, keeping cplt explicit, and avoiding latency/context fan-out.

Solution Attempt:
Use the existing ten canonical skills and Codex projections. Make Context7 a
required capability, enable conditional implicit invocation for the nine
non-cplt skills, keep cplt explicit-only, update the compact repository router,
and add a conflict-aware activator that stages writes, creates private backups,
preserves unrelated state, merges only owned MCP flags, and rolls back on any
failure. Synchronize only the approved active Codex runtime after temporary-home
tests and mandatory reviews.

Test:
Capture focused RED for the old optional/inactive state and missing activator.
Then validate exact skill IDs and policy split, single-provider routing,
Context7 required MCP semantics, Graphify preservation, conflict and symlink
refusal, private backup, rollback, idempotency, secret-safe output, no command
execution, xcodebuildmcp disabled state, focused coverage, full regression,
static checks, live global inventory, functional MCP calls, and fresh-session
routing probes.

Success Criteria:
- Exactly the ten protected skills are globally discoverable; nine are
  conditionally implicit and cplt remains explicit-only.
- Context7 is required but queried only for a bounded version-specific
  documentation need; one evidence gap never fans out across providers.
- Existing customized skills, unrelated global files, credentials, modes, and
  MCP/plugin settings remain unchanged.
- Activation is atomic, private-backup-backed, idempotent, and exactly
  rollbackable; differing or symlinked managed targets fail closed.
- xcodebuildmcp remains disabled and no cplt payload, scanner, or Graphify build
  runs during activation.
- Focused and full tests, code review, security review, and live verification
  pass without commit or push.

Result:
The bounded activator completed successfully against the active Codex runtime
and a second run was a no-op without creating another backup. Exactly ten
protected skill routes are globally discoverable: the preserved customized
legacy Graphify route plus nine official user-global projections. cplt remains
explicit-only; the other nine routes are conditionally implicit. Only the owned
MCP flags changed, Context7 is enabled and required, xcodebuildmcp remains
disabled, unrelated configuration is semantically unchanged, the router matches
the approved source, and the private backup uses a 0700 directory with 0600
files. Read-only live calls succeeded for Serena, DeepWiki, GitHub, and Context7.
A fresh ephemeral Codex session reported all ten skills and used only local `rg`
for the inventory request without MCP fan-out, scanner execution, cplt payloads,
or a Graphify build. Focused activation tests passed 19/19 with 80% branch
coverage; the full suite passed 328/328; code and security reviews passed.
The fresh inventory probe consumed 80,079 input tokens, of which 57,600 were
cached, so an actual total-token reduction versus a pre-activation baseline
remains unverified.

Decision:
ACCEPTED

Notes:
User approved the complete repository, global synchronization, restart/fresh
session verification, and mandatory orchestration scope with option A. This
record does not authorize credential changes, dependency upgrades, commit,
push, scanner-wide scans, cplt payload execution, or xcodebuildmcp activation.
Acceptance covers safe global availability and narrow lazy routing; it does not
claim a measured token-cost reduction.

## EXP-20260811-006 - TDD Responsibility Simplification

Date: 2026-08-11
Status: ROLLED_BACK

Problem:
The three CMA variants carry a large general-purpose TDD workflow that mixes
test reasoning with framework examples, repository exploration, tool choice,
and broad testing infrastructure guidance. This increases TDD context and can
duplicate discovery already completed before the tdd-guide stage.

Evidence:
Each Codex, Claude, and OpenCode candidate TDD skill is currently 428 lines and
1,369 words. The user requires a measured before/after comparison while
preserving test quality and the mandatory orchestration chain. The user
approved exactly one bounded line-limit exception for EXP-20260811-006 in the
already over-800-line experiment log. This exception applies only to this
record and does not authorize editing, reordering, refactoring, archiving,
cleaning, or maintaining existing experiment records.

Hypothesis:
A short semantic TDD contract that accepts a bounded planner handoff and owns
only acceptance mapping, meaningful RED, sufficient case selection, observable
oracles, regressions, and anti-hardcode checks will reduce TDD input and
discovery work without weakening test quality or changing orchestration.

Solution Attempt:
Replace the three native candidate TDD skill bodies with small semantically
equivalent instructions, narrow the native tdd-guide contracts and CMA TDD
modules where required, and add focused representative-task validation. Do not
change core skills, repository-tool routing, active runtime configuration,
permissions, providers, installation, or the mandatory chain.

Test:
Capture meaningful RED against the current broad contract. Validate complete
acceptance mapping, positive/negative/boundary/regression selection, meaningful
RED, observable oracles, dummy/hardcoded-success rejection, missing-input
reporting, no broad discovery or core-tool selection, three-variant semantic
parity, and unchanged chain behavior. Compare a frozen representative task set
before and after for instruction input size, allowed tool calls, repository
discovery operations, and output-quality score; run focused and full tests plus
independent code and security review.

Success Criteria:
- TDD owns test reasoning only and receives bounded discovered facts from the
  planner/main handoff.
- Repository discovery, architecture analysis, tool selection, core tools,
  installation/configuration, scanners, and provider activation are excluded.
- Every representative task preserves complete acceptance mapping, meaningful
  RED, sufficient cases, observable oracles, regressions, and anti-hardcode
  strength.
- Candidate TDD input size does not increase; permitted tool calls do not
  increase; broad discovery operations decrease to zero by contract.
- Codex, Claude, and OpenCode remain semantically aligned in native formats.
- The mandatory chain and implementation position remain unchanged.
- Focused/full tests and independent code/security reviews pass, with active
  runtime files unchanged.

Result:
Meaningful RED exposed the current broad TDD ownership. The candidate reduced
each skill from 428 to 97 lines and removed Claude discovery tools while its
focused tests and 317-test full suite passed. Independent code review found
that the representative output-quality comparison remained self-declared:
static fixtures were not outputs produced by the candidate native TDD agents,
and keyword-based contradiction checks remained bypassable. Proving candidate
behavior would require a separately authorized live/native runtime evaluation,
which Phase 10 explicitly excludes. The candidate instruction, metadata,
agent, module, prompt, runtime-test, fixture, and focused-test changes were
therefore restored to their exact Phase 10 preimages. Active runtime files were
never changed.

Decision:
ROLLBACK

Notes:
The line-limit exception is exclusive to EXP-20260811-006. Experiment-log
maintenance remains a separately approved task. Active runtime synchronization,
tool installation, provider activation, core-skill edits, and later phases are
outside Phase 10.
The design may be reconsidered only with a separately approved, bounded native
evaluation that produces real before/after outputs and tool-call traces.

## EXP-20260811-005 - cplt Isolated Execution Core Skill

Date: 2026-08-11
Status: ACCEPTED

Problem:
CMA protects discovery, security, and external-knowledge capabilities, but its
registered cplt isolated-execution capability has no narrow canonical skill,
inactive native projections, or independent contract preventing risky commands
from escaping to an ordinary host shell when isolation is unavailable.

Evidence:
The canonical registry already defines cplt as a required, protected
`isolated-execution` capability. Existing CMA routing denies execution authority
but has no distinct cplt selection boundary. The user approved exactly one
bounded line-limit exception for EXP-20260811-005 in the already over-800-line
experiment log. This exception applies only to this record and does not
authorize editing, reordering, refactoring, archiving, cleaning, or maintaining
existing experiment records.

Hypothesis:
One short instruction-only cplt skill with an explicit execution-isolation
decision gate, evidence-based containment claims, fail-closed absence, and
strict negative routes can preserve semantic parity across inactive Codex,
Claude, and OpenCode candidates without installing, configuring, activating,
or executing cplt.

Solution Attempt:
Add one canonical cplt definition, three native inactive candidate projections,
one compact routing row per variant, and a bounded read-only validator with
independent trigger, authority, unavailable-tool, isolation-evidence, parity,
and runtime-isolation tests. Do not change the standard, registry, profiles,
TDD, active runtime, permissions, other skills, or later phases.

Test:
Capture meaningful RED for the absent Phase 9 production surfaces and missing
route. Validate explicit and natural positive triggers; safe-command,
repository-discovery, scanner, mention-only, missing-authority, and
ordinary-sandbox-sufficient negatives; fail-closed absence; no host fallback;
evidence-based isolation reporting; native metadata; semantic parity; bounded
no-follow parsing; truthful status; and exact active-runtime isolation. Never
execute cplt or a dangerous payload. Run focused branch coverage, applicable
and full regressions, code review, and security review.

Success Criteria:
- The canonical skill contains every required standard field and matches the
  protected cplt registry entry.
- cplt is selected only after the required command is chosen and stronger
  isolation is justified; it never replaces discovery, scanners, or external
  knowledge.
- Missing cplt, authority, or verifiable isolation stops unavailable and
  unverified with `success=false`, without host-shell fallback.
- Isolation success distinguishes requested, available, and verified controls
  and is never inferred from configuration presence or exit code alone.
- Native candidates preserve semantic parity without implicit activation,
  runtime writes, permission changes, installation, configuration, or cplt
  execution.
- Focused coverage, full tests, independent code/security reviews, and exact
  active-runtime manifest comparison pass.

Result:
Meaningful RED exposed exactly seven absent production surfaces and the missing
route in all three variants. Independent review then exposed natural-language
authority bypasses and weak self-declared isolation evidence. The final router
does not infer authority from prompt text: strict orchestration state provides
authority, command-selection, and ordinary-sandbox sufficiency, while prompt
text only classifies risk and isolation need. The isolation schema is explicitly
not execution proof and requires bounded runtime, policy, digest, path, control,
and result evidence. Final validation passed 16/16 focused tests with 81%
validator branch coverage, 152/152 core-skill regressions, 55/55 runtime
regressions, and 309/309 full tests. Independent code and security reviews
passed, active-runtime and canonical authority manifests remained unchanged,
and cplt or a risky payload was never executed.

Decision:
ACCEPTED

Notes:
The line-limit exception is exclusive to EXP-20260811-005. Experiment-log
maintenance remains a separate approved task. cplt activation, configuration,
permissions, TDD simplification, and later phases are not authorized.

## EXP-20260811-004 - External Knowledge Core Skills

Date: 2026-08-11
Status: ACCEPTED

Problem:
CMA has protected local-intelligence and conditional security skills, but its
three external evidence needs still lack narrow, inactive skill contracts and
independent validation: authoritative remote GitHub facts, conceptual public
repository knowledge, and version-specific library documentation.

Evidence:
The canonical registry already assigns GitHub MCP to remote source knowledge,
DeepWiki MCP to public-repository knowledge, and optional Context7 to
version-specific documentation. Current repository routing combines DeepWiki
and Context7 and does not fully encode local-first authority or untrusted
external-content handling. Official provider documentation confirms distinct
evidence models and shows that retrieved content and tool results require
source validation rather than instruction authority. The user approved exactly
one bounded line-limit exception for EXP-20260811-004 in the already over-800-
line experiment log. This exception applies only to this record and does not
authorize editing, reordering, refactoring, archiving, cleaning, or maintaining
existing records.

Hypothesis:
Three short instruction-only skills with local-first routing, exact positive and
negative boundaries, untrusted-content handling, fail-closed tool absence, and
one-provider-by-default behavior can preserve semantic parity across inactive
Codex, Claude, and OpenCode candidates without installing, configuring,
authenticating, activating, or invoking an external provider.

Solution Attempt:
Add canonical GitHub, DeepWiki, and Context7 definitions; native inactive
candidate projections; three compact routing rows; and a bounded read-only
validator with independent trigger, parity, authority, injection-resistance,
and runtime-isolation tests. Do not change the registry, profiles, TDD, active
runtime, credentials, MCP/plugin configuration, cplt, or later phases.

Test:
Capture meaningful RED for the absent Phase 8 production surfaces. Validate
explicit and natural positive triggers, negative and local-first routes,
genuine overlap priority, fail-closed tool absence, external/local authority,
prompt-injection resistance, source provenance, optional Context7 semantics,
native metadata, normalized semantic parity, bounded no-follow inputs, compact
routing, truthful status, and active runtime isolation. Run focused coverage,
applicable and full regressions, code review, and security review without
connecting to or executing an external provider.

Success Criteria:
- Each canonical skill contains every required standard field and matches its
  protected registry entry, including Context7's optional capability status.
- Local evidence wins when sufficient; remote repository facts, public-repo
  concepts, and version-specific docs route to exactly one primary external
  skill by default.
- Retrieved content is identified as external untrusted evidence, cannot
  override CMA/repository authority, and cannot authorize commands or mutation.
- Required or optional provider absence stops unavailable and unverified with
  `success=false`, without provider substitution or widened scope.
- Native candidates preserve semantic parity without implicit activation,
  runtime writes, authentication, installation, configuration, plugin, or MCP
  changes.
- Focused coverage, full tests, independent code/security reviews, and exact
  active-runtime manifest comparison pass.

Result:
Meaningful RED exposed the missing Phase 8 surfaces, and a code-review RED
later exposed mixed local/external routing that selected an explicit provider
before sufficient local evidence. The corrected local-first router and three
provider-conflict regressions passed. Final validation passed 14/14 focused
tests with 84% validator branch coverage, 136/136 core-skill regressions,
55/55 runtime regressions, and 293/293 full tests. Each skill passed its direct
validator contract. Independent code and security reviews passed, the exact
active-runtime manifest remained unchanged, and no provider, MCP, plugin,
credential, installer, configuration, or network operation was invoked.

Decision:
ACCEPTED

Notes:
The line-limit exception is exclusive to EXP-20260811-004. Experiment-log
maintenance remains a separate task. Provider activation, credentials, cplt,
Phase 9, and TDD simplification are not authorized.

## EXP-20260811-003 - Conditional Security Core Skills

Date: 2026-08-11
Status: ACCEPTED

Problem:
CMA has protected local-intelligence core skills, but its three distinct
security evidence needs still lack narrow, inactive skill contracts and
independent validation: source SAST, dependency vulnerabilities, and secret
exposure.

Evidence:
The canonical registry already assigns Opengrep to SAST, OSV-Scanner to
dependency vulnerability analysis, and Betterleaks to secret detection. The
current repository router combines some security routes, while no canonical or
native skill projections exist for these three scanners. Official tool sources
confirm distinct evidence models: rule-driven source findings, extracted
package vulnerability matching, and redaction-capable secret detection. The
user approved exactly one bounded line-limit exception for EXP-20260811-003 in
the already over-800-line experiment log. This exception applies only to this
record and does not authorize editing, reordering, refactoring, archiving,
cleaning, or maintaining existing records.

Hypothesis:
Three short instruction-only skills with conditional triggers, exact negative
boundaries, fail-closed tool absence, and secret-safe output contracts can
preserve semantic parity across inactive Codex, Claude, and OpenCode candidates
without installing, configuring, activating, or running scanners.

Solution Attempt:
Add canonical Opengrep, OSV-Scanner, and Betterleaks definitions; native inactive
candidate projections; three compact routing rows; and a bounded read-only
validator with independent trigger, parity, authority, redaction, and runtime
isolation tests. Do not change the registry, profiles, TDD, active runtime, or
scanner configuration.

Test:
Capture meaningful RED for exactly 17 absent Phase 7 surfaces. Validate explicit
and natural positive triggers, negative and overlap routes, fail-closed tool
absence, Betterleaks redaction, output contracts, registry metadata, native
metadata, normalized semantic parity, bounded no-follow inputs, compact routing,
truthful status, and active runtime isolation. Run focused coverage, applicable
and full regressions, code review, and security review without executing a
scanner.

Success Criteria:
- Each canonical skill contains every required standard field and matches its
  protected registry entry.
- Source security, dependency CVE, and secret exposure route to exactly one
  primary scanner by default; scanners remain conditional.
- Required-tool absence stops unavailable and unverified with `success=false`,
  without scanner substitution or widened scope.
- Security outputs require finding type, optional supplied severity, location,
  short explanation, and remediation direction; Betterleaks never exposes a
  matched secret value.
- Native candidates preserve semantic parity without implicit activation,
  runtime writes, tool installation, configuration, plugin, or MCP changes.
- Focused coverage, full tests, independent code/security reviews, and exact
  active-runtime manifest comparison pass.

Result:
Meaningful RED failed only for the expected 17 absent Phase 7 production
surfaces. The three instruction-only skills and inactive native projections
were then added without installing, configuring, activating, or executing a
scanner. Independent validation now rejects semantic drift, incomplete
negative sets, fake overlap labels, unsafe unavailable-tool behavior, raw
secret output, native activation widening, routing drift, symlinks, deep JSON,
and malformed bounded input types. Final validation passed 40/40 focused tests
with 85% validator branch coverage and 279/279 full tests. Direct per-skill CLI
validation returned exact truthful passed payloads, code and security reviews
passed after their findings were closed, and the active Codex, Claude, and
OpenCode skill/config manifest remained byte-identical to its pre-task baseline.

Decision:
ACCEPTED. Phase 7 establishes Opengrep for conditional source SAST,
OSV-Scanner for conditional dependency vulnerability evidence, and Betterleaks
for conditional redacted secret detection. Each evidence need has one primary
scanner by default, all unavailable-tool paths stop fail-closed, and no active
runtime or scanner state was changed.

Notes:
The line-limit exception is exclusive to EXP-20260811-003. Experiment-log
maintenance remains a separate task. Scanner execution, Phase 8, and TDD
simplification are not authorized.

## EXP-20260811-002 - Local Repository Intelligence Core Skills

Date: 2026-08-11
Status: ACCEPTED

Problem:
CMA has a protected core-skill standard, registry, and three platform profiles,
but Graphify, Serena, and ast-grep do not yet have narrow canonical contracts,
native inactive projections, or independent trigger and parity validation.

Evidence:
The registry already assigns architecture analysis to Graphify, symbol
intelligence to Serena, and structural search to ast-grep. The approved profiles
define native projection constraints, while the current repository-tool router
keeps exact text and path lookup on `rg`. No tool-specific core-skill definitions
or projections exist under `core-skills/`. The user approved exactly one bounded
line-limit exception for EXP-20260811-002 in the already over-800-line experiment
log. This exception applies only to this record and does not authorize editing,
reordering, refactoring, archiving, cleaning, or maintaining existing records.

Hypothesis:
Three short instruction-only canonical skills plus native inactive Codex,
Claude, and stable-V1 OpenCode projections can preserve semantic parity and
route one primary local evidence need per skill without installing, configuring,
activating, or silently substituting tools.

Solution Attempt:
Add canonical Graphify, Serena, and ast-grep definitions; project each into the
repository-owned native candidate locations defined by the approved profiles;
add only compact routing references; and add one read-only validator with
independent per-skill tests. Do not add scripts to the skills, change TDD, or
touch active runtime configuration.

Test:
Capture meaningful RED before implementation. For each skill validate explicit
and natural positive triggers, required negative and overlap cases, fail-closed
tool absence, registry metadata, native platform metadata, and normalized
semantic parity across Codex, Claude, and OpenCode. Run focused coverage,
applicable regressions, the full suite, code review, security review, and active
runtime isolation checks.

Success Criteria:
- Each canonical skill contains all required standard fields and matches its
  protected registry entry.
- Exact text/path remains `rg`; architecture, symbol intelligence, and
  structural AST evidence select one distinct primary skill by default.
- Every required negative trigger and overlap case rejects the wrong skill.
- Missing required tools report `availability=unavailable`,
  `status=unverified`, `success=false`, and stop without fallback.
- Native projections preserve normalized semantics without byte-identity
  requirements, implicit activation, installation, configuration, or runtime
  writes.
- Routing remains compact; focused and applicable full tests plus independent
  code and security reviews pass.

Result:
Meaningful RED first failed only for the 18 absent Phase 6 surfaces. Two later
code-review regressions proved that prompt labels were self-fulfilling and that
synchronized invalid registry semantics could pass; both then failed closed.
Security RED reproduced hidden or duplicate instructions, synchronized unsafe
authority text, routing symlinks and authority widening, unknown Codex metadata,
unsafe native descriptions, and deeply nested JSON before each bypass was
closed.

The final implementation contains three instruction-only canonical skills and
nine inactive native projections. Exact text and path lookup remains on `rg`;
Graphify, Serena, and ast-grep have distinct architecture, symbol, and
structural-AST routes. Required-tool absence stops unavailable and unverified
with `success=false`, without fallback, installation, or configuration. The
read-only validator enforces registry authority, independent prompt routing,
exact safety and unavailable contracts, native metadata, normalized semantic
parity, bounded no-follow reads, and compact routing authority.

Final verification passed 20/20 focused tests with 85% branch coverage and
239/239 full repository tests. Skill format checks, cache-isolated compilation,
direct CLI validation, diff checks, code review, security review, and exact
pre/post active runtime manifests passed. No active Codex, Claude, or OpenCode
skill or configuration was changed.

Decision:
ACCEPTED

Notes:
The line-limit exception is exclusive to EXP-20260811-002. Experiment-log
maintenance remains a separate task. Phase 7 and TDD simplification are not
authorized.

## EXP-20260811-001 - Minimal OpenCode Core Skill Profile

Date: 2026-08-11
Status: ACCEPTED

Problem:
CMA has a canonical core-skill standard, protected registry, and native Codex
and Claude profiles, but no stable OpenCode representation contract for future
protected core-skill projections.

Evidence:
Current official stable OpenCode V1 documentation defines native Agent Skills
through `SKILL.md`, project/global/compatibility discovery, model-visible skill
descriptions, on-demand loading through the `skill` tool, and `allow`, `ask`,
or `deny` skill permissions. The repository launcher delegates to stable
`opencode`, and the installed binary reports `1.18.16`; official OpenCode V2 is
a separate changing beta invoked as `opencode2`. Stable V1 does not document a
per-skill explicit-only or autoinvoke-off field. The user approved exactly one
bounded exception to add EXP-20260811-001 to the already over-800-line log.
This exception applies only to this record and does not authorize editing,
reordering, refactoring, archiving, cleaning, or otherwise maintaining existing
experiment records.

Hypothesis:
One inactive stable-V1-native JSON profile plus a small stdlib-only read-only
validator can preserve every canonical semantic field, registry authority,
lazy loading, approval-gated future activation, platform limitations, and
routing-only global guidance without creating or activating any skill, agent,
plugin, MCP, permission, or runtime configuration.

Solution Attempt:
Add `core-skills/profiles/opencode.json`,
`bin/cma-opencode-core-skill-profile`, and focused
`tests/test_opencode_core_skill_profile.py`. The profile is representation-only.
The validator may read and report but must never install, configure, project,
enable, disable, activate, sync, prune, repair, or mutate state.

Test:
Capture meaningful RED for the absent profile and validator. Validate all 15
canonical mappings, exact registry authority, stable-V1 native structure and
discovery, the documented lack of explicit-only metadata, lazy approval-gated
future activation, strict types, metadata fingerprint isolation,
unavailable-tool behavior, routing, agent/plugin/MCP/config separation,
secret-safe dependency reuse, and active-runtime isolation. Run focused branch
coverage, Phase 2-5 and full regressions, static checks, code review, and
security review.

Success Criteria:
- Every canonical field maps exactly once to supported stable-V1 OpenCode
  targets; V2-only or unknown fields fail clearly.
- `registry.json` remains the sole core/protected authority and OpenCode
  metadata cannot change canonical semantics.
- The profile remains inactive with zero projections or configuration writes;
  future use is exact-ID user routing plus native `skill: ask`, without claiming
  undocumented explicit-only enforcement.
- Required-tool absence stops unverified with `success=false`; no tool install,
  configuration, activation, emulation, or widened evidence route is allowed.
- Candidate values, paths, tracebacks, secrets, and dependency substitutions do
  not leak through validator output.
- No active OpenCode state, OpenCode variant, canonical source, Codex/Claude
  profile, TDD, sync, archive, tool-specific skill, or Phase 6 surface changes.
- Focused tests and coverage, applicable and full regressions, code review, and
  security review pass before acceptance.

Result:
Meaningful RED failed only for the absent OpenCode profile and validator. The
completed profile maps all 15 canonical fields once, remains inactive with zero
projections, targets stable V1 only, and records the lack of a documented
explicit-only switch. The read-only validator rejects semantic drift, V2-only
or behavioral metadata, registry type confusion, unavailable-tool widening,
write-like flags, sibling-validator substitution, symlinked or replaced JSON
inputs, inputs above 1 MiB, more than 64 levels, more than 50,000 nodes, and
parser recursion without tracebacks, path disclosure, or candidate-value
leakage. Focused tests passed 14/14 with 89% branch coverage; Phase 2-5 tests
passed 62/62; the full suite passed 219/219. JSON, cache-isolated compilation,
direct CLI, diff/static, canonical-source identity, OpenCode variant isolation,
code review, and security review passed. No active OpenCode file was modified.

Decision:
ACCEPTED

Notes:
The line-limit exception is exclusive to EXP-20260811-001. Existing experiment
records remain unchanged and unarchived. Experiment-log maintenance is a
separate future task requiring explicit approval.

## EXP-20260810-011 - Minimal Claude Core Skill Profile

Date: 2026-08-10
Status: ACCEPTED

Problem:
CMA has a canonical core-skill standard, protected registry, and Codex variant
profile, but no native Claude representation contract for future protected core
skill projections.

Evidence:
Current official Anthropic documentation defines Claude Code skills through
`SKILL.md`, user/project/managed/plugin discovery, explicit `/name` invocation,
description-driven model invocation, `disable-model-invocation`, plugin and MCP
boundaries, scoped settings, and `CLAUDE.md` loading. No Claude core-skill
profile or focused validator exists. The user approved exactly one bounded
exception to add this EXP-20260810-011 record to the already over-800-line log.
The exception applies only to EXP-011, does not authorize editing, reordering,
refactoring, archiving, or cleaning existing records, keeps Phase 4 unchanged,
and reserves experiment-log maintenance for a separate approved task.

Hypothesis:
One inactive Claude-native JSON profile plus a small stdlib-only read-only
validator can preserve all canonical semantics, registry authority,
explicit-only lazy activation, native discovery, plugin/MCP separation, and
routing-only `CLAUDE.md` guidance without creating or activating any skill or
runtime integration.

Solution Attempt:
Add `core-skills/profiles/claude.json`,
`bin/cma-claude-core-skill-profile`, and focused
`tests/test_claude_core_skill_profile.py`. The profile is representation-only.
The validator may read and report but must never install, configure, project,
enable, disable, activate, sync, prune, repair, or mutate state.

Test:
Capture meaningful RED for the absent profile and validator, then validate all
canonical mappings, exact registry authority, native Claude structure and
discovery, explicit-only activation, strict types, metadata fingerprint
isolation, unavailable-tool behavior, `CLAUDE.md` routing, plugin/MCP/agent
boundaries, secure read-only dependency reuse, and active-runtime isolation.
Run focused branch coverage, applicable and full regressions, static/diff
checks, code review, and security review.

Success Criteria:
- All 15 canonical fields map exactly once to supported Claude-native targets.
- Future core skills use deterministic `name`, `description`,
  `disable-model-invocation: true`, and `user-invocable: true` without any
  implicit opt-in, disabled core ID, settings override, or projection.
- `registry.json` remains the sole core/protected authority; Claude metadata,
  plugins, agents, MCP, or SDK filters cannot change canonical semantics.
- Unknown mappings, type confusion, permission-granting metadata, silent tool
  fallback/setup, mutation commands, and dependency substitution fail closed.
- No tool-specific skill, active Claude state, Claude variant, canonical
  source, Codex/OpenCode profile, TDD, sync, archive, MCP, or Phase 5 surface
  changes.
- Focused tests and branch coverage, applicable and full regressions, code
  review, and security review pass before acceptance.

Result:
Initial focused discovery produced meaningful RED because the Claude profile
and validator did not exist. The implementation then passed the native
structure, exact canonical mapping, registry authority, explicit-only lazy
activation, metadata isolation, unavailable-tool, routing, integration,
read-only, and dependency-substitution contracts.

The first security review found that raw Phase 2 registry findings could echo a
sensitive candidate value to stdout. A focused regression reproduced the leak
with a controlled sentinel before the validator reduced dependency findings to
validated `code` and optional `field` values. Code and security re-reviews both
passed after the fix.

Final verification passed 14/14 focused tests with 92% branch coverage for
`bin/cma-claude-core-skill-profile`, 48/48 Phase 2-4 core-skill regressions, and
205/205 full repository tests. JSON parsing, cache-free source compilation,
direct CLI validation, diff checks, and exact active Claude, Claude variant,
canonical-source, and Codex-profile hashes passed. No active Claude state,
Claude variant, tool-specific skill, plugin, MCP, agent, scanner, TDD, sync,
archive, OpenCode profile, or Phase 5 surface was changed.

Decision:
ACCEPT

Notes:
The line-limit exception is exclusive to EXP-20260810-011. Existing experiment
records remain unchanged and unarchived. Experiment-log maintenance is a
separate future task requiring explicit approval.
