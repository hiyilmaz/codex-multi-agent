# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

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

## EXP-20260811-007 - Native TDD Simplification Evaluation

Date: 2026-08-11
Status: NEED_MORE_DATA

Problem:
EXP-20260811-006 showed that static fixtures and token proxies cannot prove
whether a smaller TDD contract preserves real native-agent output quality or
reduces actual runtime cost across Codex, Claude, and OpenCode.

Evidence:
The Phase 10 candidate was rolled back after independent review found its
quality and tool-use evidence self-declared. All three native CLIs are locally
available, but their raw traces must first prove comparable input/output token,
tool-call, repository-read/search, core-skill, wall-clock, and final-output
measurement. The user approved exactly one bounded line-limit exception for
EXP-20260811-007 in the already over-800-line experiment log. This exception
applies only to this record and does not authorize editing, reordering,
refactoring, archiving, cleaning, or maintaining existing experiment records.

Hypothesis:
Running one fixed baseline and one fixed temporary Phase 10 candidate through
the real native TDD-agent mechanism on four identical bounded tasks can provide
trustworthy cost and behavior evidence without permanently modifying TDD,
runtime configuration, permissions, orchestration, or core skills.

Solution Attempt:
Freeze exactly four task inputs and two prompt contracts before scored runs.
Use ephemeral or isolated invocation inputs only, execute baseline and
candidate natively for Codex, Claude, and OpenCode, retain raw redacted traces
outside active runtime configuration, and score actual final TDD contracts with
one fixed rubric. Do not tune prompts after seeing results or implement the
candidate even if it passes.

Test:
First run a non-scored bounded preflight for each native runtime. Continue to
the 24 scored runs only if every runtime exposes trustworthy actual input and
output tokens, tool calls, repository reads/searches, core-skill invocations,
wall-clock, and final output without persistent runtime/config mutation. Use
the same four inputs for baseline and candidate. Compare acceptance mapping,
meaningful RED, positive, negative, boundary, regression, anti-hardcode, and
missing-information behavior. Require candidate quality to be component-wise
no weaker, repository discovery to decrease, tool calls and input tokens not to
increase, and semantic alignment across all variants.

Success Criteria:
- Baseline and candidate execute as real native TDD agents in all three
  variants with attributable raw measurements.
- The fixed four task inputs and fixed prompt contracts do not change after the
  first scored result.
- Candidate quality is not weaker for any task, dimension, or variant.
- Repository discovery decreases; tool calls and input tokens decrease or stay
  equal; no core skill, scanner, or external knowledge route is invoked.
- Active TDD, runtime configuration, permissions, orchestration, and core-skill
  files remain unchanged.
- If any native trace cannot support trustworthy measurement, stop before
  scored comparison and report `UNVERIFIED` with `success=false`.

Result:
Preflight stopped before any native model evaluation or scored run. The
installed Codex CLI (`codex-cli 0.147.0`) exposes no named-agent selector for
`codex exec`, so a direct native `tdd-guide` run and agent-attributable token
and tool measurements could not be established. OpenCode (`1.18.16`) exposes
`--agent`, but its plugin-free active runtime reported `Agent tdd-guide not
found`; creating or activating a temporary runtime agent definition would
change the evaluation surface prohibited by this phase. Claude exposes native
agent and stream-event options, but all three variants are required, so no
Claude model call was made in isolation. Consequently there are no real
baseline/candidate token, tool, discovery, wall-clock, or quality measurements.
The evaluation is `UNVERIFIED` with `success=false`.

Decision:
NEED_MORE_DATA

Notes:
The line-limit exception is exclusive to EXP-20260811-007. Experiment-log
maintenance remains a separately approved task. This phase evaluates only and
does not authorize permanent candidate installation or later work.

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

## EXP-20260810-010 - Minimal Codex Core Skill Profile

Date: 2026-08-10
Status: ACCEPTED

Problem:
CMA Core Skill Standard v1 and the protected core registry are provider-neutral,
but they do not yet define a testable, native Codex representation, discovery,
or lazy activation contract for future core-skill projections.

Evidence:
Current official OpenAI documentation defines Codex skills through `SKILL.md`,
optional `agents/openai.yaml`, repository/user/admin/system discovery scopes,
explicit and implicit invocation, and `AGENTS.md` instruction layering. The
repository has no Codex core-skill profile or focused profile validator. The
user approved exactly one bounded exception to add this EXP-010 record to the
already over-800-line experiment log; the exception applies only to EXP-010,
does not authorize edits or archiving of existing records, does not change
Phase 3 scope, and requires later log maintenance to be separately approved.

Hypothesis:
A single inactive JSON profile plus a small stdlib-only read-only validator can
preserve every canonical semantic field, protected ownership, explicit-only
lazy activation, native Codex structure, and routing-only global guidance
without creating skills, projecting files, or touching active runtime state.

Solution Attempt:
Add `core-skills/profiles/codex.json`,
`bin/cma-codex-core-skill-profile`, and focused
`tests/test_codex_core_skill_profile.py`. The profile is representation-only;
the validator may read and report but must never install, project, sync,
activate, disable, configure, prune, repair, or mutate anything.

Test:
Capture meaningful RED for the absent profile and validator. Then validate the
complete canonical mapping, registry authority for core/protected status,
official native structure and discovery, explicit-only lazy activation,
unknown mapping rejection, non-semantic UI metadata isolation, fail-closed
unavailable-tool behavior, routing-only global guidance, strict JSON types,
and read-only operation. Run focused coverage, Phase 2-3 regression, the full
suite, diff integrity checks, code review, and security review.

Success Criteria:
- All required canonical fields map exactly once to supported Codex targets.
- `registry.json` remains authoritative for core/protected semantics and no
  Codex-native metadata is misrepresented as the protection source.
- Future core skills remain discoverable and explicit-callable, load lazily,
  default to `allow_implicit_invocation: false`, and are never disabled by this
  inactive profile.
- Unknown mappings, behavioral `default_prompt`, silent fallback, tool setup,
  type confusion, mutation commands, and runtime/config writes fail closed.
- No tool-specific skill, variant projection, active runtime/config, MCP,
  scanner, permission, TDD, Claude, OpenCode, sync, archive, or Phase 4 surface
  is created or changed.
- Focused tests and branch coverage, applicable and full regressions, code
  review, and security review pass before acceptance.

Result:
The valid repository discovery command first produced meaningful RED with 13
tests discovered, two explicit missing-profile/missing-validator failures, and
11 controlled skips. An earlier package-style unittest command was discarded
because this repository's `tests/` directory is not a Python package and it
failed at import rather than at the intended behavior boundary.

The initial implementation passed 13/13 focused tests. Code review then found
three fail-open gaps: self-shrunk registries, structured JSON type confusion,
and missing `AGENTS.md` layering semantics. New regression tests reproduced all
three before the profile added the bounded official layering contract and the
validator reused the exact Phase 2 registry validator with type-safe mapping
checks. Code re-review passed.

Security review then found symlink-based sibling-validator substitution,
unwanted bytecode persistence risk, and unstructured dependency-load failures.
New tests reproduced the substitution and traceback paths before the loader was
anchored to the resolved real script, restricted to a regular non-symlink
sibling, changed to cache-free in-memory source execution, and made dependency
failures redacted and structured. Final code and security re-reviews passed.

Final verification passed 19/19 focused tests with 84% branch coverage for
`bin/cma-codex-core-skill-profile`, 34/34 Phase 2-3 focused regressions, and
191/191 full repository tests. JSON parsing, compilation, direct CLI validation,
diff checks, exact active-runtime hashes, and the Codex variant tree hash all
passed. No active `~/.codex` file, Codex variant file, tool-specific skill, MCP,
scanner, permission, TDD, sync, archive, Claude, OpenCode, or Phase 4 surface
was changed.

Decision:
ACCEPT

Notes:
The line-limit exception is exclusive to EXP-20260810-010. No existing
experiment record may be modified, archived, refactored, or cleaned up in this
task. Experiment-log maintenance remains a separate future task requiring
explicit approval.

## EXP-20260810-009 - Minimal Core Skill Governance

Date: 2026-08-10
Status: ACCEPTED

Problem:
CMA Core Skill Standard v1 defines protected, lazy, provider-neutral skills,
but no canonical registry or executable read-only checks currently make core
ownership, removal protection, missing entries, governance drift, semantic
parity, custom-skill separation, or no-prune behavior testable.

Evidence:
`core-skills/STANDARD.md` is the canonical semantic standard, while Codex,
Claude, and OpenCode runtime trees contain only existing platform-owned assets.
There is no `core-skills/registry.json`, governance validator, or focused core
registry test. The user explicitly approved a one-record exception to append
this experiment to the already over-800-line active record without refactoring
or archiving it.

Hypothesis:
A single canonical JSON registry plus a small stdlib-only read-only validator
will make protected core ownership and governance drift independently testable
without creating skill implementations, variant projections, pruning, repair,
sync, runtime configuration, or a management subsystem.

Solution Attempt:
Add `core-skills/registry.json`, `bin/cma-core-skill-governance`, and focused
`tests/test_core_skill_governance.py`. The validator may only validate the
registry, compare baseline/candidate registries, and compare synthetic normalized
Codex, Claude, and OpenCode inventories. It must never write, remove, prune,
repair, synchronize, install, configure, or activate anything.

Test:
Capture meaningful RED from focused tests written before the registry and
validator. Then verify the valid registry, missing protected entries, accidental
removal rejection, duplicate IDs, invalid core/protected metadata, custom-skill
separation, semantic versions, governance drift, semantic-not-byte parity, and
no-prune/no-mutation behavior. Run focused coverage, the applicable full suite,
diff checks, code review, and security review.

Success Criteria:
- The registry contains exactly the ten approved core capabilities with required
  metadata and Context7 alone marked as an optional capability.
- Removal of a protected entry fails with explicit approval required; missing,
  duplicate, invalid, and drifted entries fail with deterministic provenance.
- Byte-different normalized inventories for Codex, Claude, and OpenCode pass
  when semantics match and fail on semantic drift.
- User/custom skills remain outside protected-core ownership and all input files
  remain byte-identical after passing and failing checks.
- No pruning, mutation, approval-bypass, repair, sync, skill implementation,
  projection, TDD-policy, install, runtime, archive, daemon, or Phase 3 surface
  is introduced.
- Focused tests, branch coverage, full regressions, code review, and security
  review pass before acceptance.

Result:
The initial focused run produced meaningful RED: 12 tests ran with exit 1 and
failed on explicit missing-registry and missing-validator assertions, not import,
syntax, permission, or transport errors. The first implementation passed 12/12
focused tests and direct validator branch coverage reached 81%. Two additional
pre-review boundary tests then produced behavioral RED for record-only protected
removal and a custom/core ID collision before their scoped fixes.

Code review found that a self-shrunk empty roster and invalid capability/tool
optionality could pass, and that display-name parity was omitted. New mutation
tests reproduced both failures before the validator locked the exact ten-ID
roster, Context7-only optional capability rule, required invocation dependencies,
and display-name semantic parity. Code re-review passed. Security review then
confirmed Python boolean/integer equality allowed numeric `0`/`1` to spoof JSON
policy and core/protected booleans. Four new type-confusion cases failed before
recursive type-strict comparison was added; security re-review passed.

Final verification passed 15/15 focused tests. Direct positive and negative CLI
execution measured 83% branch coverage for `bin/cma-core-skill-governance`.
The full repository suite passed 172/172 in 42.930 seconds with exit 0. JSON
parsing, executable mode, file-size bounds, and `git diff --check` passed. The
validator remained read-only and no skill implementation, projection, pruning,
approval bypass, repair, sync, install, runtime, archive, daemon, permission,
or Phase 3 surface was added.

Decision:
ACCEPT

Notes:
Only the user-approved single experiment-record exception applies. Existing
unrelated dirty work must remain unchanged. Commit, push, active-runtime sync,
and Phase 3 are not authorized. Full skill-body semantic parity remains not
executed because Phase 2 intentionally created no skills or projections.

## EXP-20260810-008 - Planner-to-TDD Structured Evidence Envelope v0

Date: 2026-08-10
Status: REJECTED

Problem:
The planner and tdd-guide contracts require bounded handoffs and discourage
repeated broad discovery, but they have no structured, identity-bound way for
the TDD guide to consume a planner source fact. The same current repository
fact can therefore be independently rediscovered between the two stages.

Evidence:
This experiment will first replay the real EXP-20260804-002 temporal-TDD
bugfix against the immutable pre-fix Git tree
`2f0f84e768504eddc6895cf27899ab46c64808de` at commit
`ff6592e171b3fb6827141f44aa5b45bad960797f`. Candidate mutation is forbidden
unless the unchanged planner and TDD contracts produce a complete behavioral
RED trace containing at least one non-verification duplicate canonical fact.

Hypothesis:
When planner supplies current, source-identity-bound discovery evidence in a
minimal Envelope v0, tdd-guide will consume that evidence and avoid repeating
the same discovery operation unless it identifies an explicit unresolved gap,
while producing an equal-or-stronger test contract.

Solution Attempt:
If and only if behavioral RED passes, define Envelope v0 in the portable Codex
orchestration registry, require the default planner to emit it, require the
default tdd-guide to validate and consume it, and add fail-closed contract tests.
Limit production/test scope to
`variants/codex/home/registry/ORCHESTRATION.md`,
`variants/codex/home/agents/planner.toml`,
`variants/codex/home/agents/tdd-guide.toml`, and
`tests/test_cma_lazy_runtime.py`. Do not synchronize active runtime files or
add storage, helpers, runtimes, tools, scanners, MCPs, or graph behavior.

Test:
Run fresh sequential planner and tdd-guide baseline sessions on a read-only
complete repository fixture using the approved natural prompt. Normalize exact
and evidence-equivalent discovery by canonical fact key, path, query/range, and
source identity. If meaningful RED passes, add static negative contract tests,
capture their failure, make the minimum candidate change, rerun static tests,
replay the identical live task, compare AC-TEMP-1 through AC-TEMP-7, run focused
and full regressions, then complete code and security review.

Success Criteria:
- Baseline planner-to-TDD duplicate discovery count is at least one and the TDD
  contract completes normally without source invalidation.
- Static candidate tests fail before implementation and reject plausible
  weakened, stale, conflicting, unresolved-gap, schema, and chain contracts.
- Candidate duplicate discovery count is zero; current sufficient evidence IDs
  are consumed and every new discovery is tied to a named unresolved gap.
- Envelope top-level fields are limited to the eight approved v0 fields and its
  measured transport cost does not exceed the duplicate evidence it replaces.
- AC-TEMP-1 through AC-TEMP-7 and positive, negative, boundary, regression,
  meaningful-RED, anti-hardcoding, and no-weakened-oracle protections remain.
- Focused and full tests, code review, and security review pass; active runtime,
  config, mandatory chain, and unrelated work remain unchanged.

Result:
Behavioral RED passed on the locked 325-node fixture with manifest
`7dd6c6e5817d6a5eccc740e63c79bb28d87a302784bc6987c71c4306fa3671b2`.
Planner completed with six tool calls and TDD completed with four; TDD
re-read the records contract, TDD module, installer, and existing test seams
already identified by planner, giving a conservative duplicate count of four.
The first focused invocation was a transport-only import error; the corrected
unchanged four-test command then produced meaningful static RED because the
orchestration registry lacked Envelope v0. After the minimum four-file
candidate, five focused contract/chain tests passed.

Live candidate planner emitted a parseable eight-field envelope, but expanded
the historical two-file task to six unrelated policy/test/changelog paths.
Candidate TDD reported consuming `E1` through `E4` and claimed no additional
discovery, while its complete JSONL trace contained one compound command that
re-hashed and re-ran `rg` against all four supplied evidence paths. Excluding
the hashes as identity checks still leaves four evidence-equivalent discovery
repetitions, so the required candidate duplicate count of zero was not met.
The candidate TDD contract also omitted the AC-TEMP-2 exact-once/ordering
obligation and the AC-TEMP-4 fenced/quoted-heading boundary.

Code review returned three HIGH blocking findings: failed primary behavioral
gate, empty/untyped source and evidence identity, and weakened-contract tests
that accepted duplicate/quoted headings and appended contradictory prose.
Security review confirmed fail-open evidence laundering, bypassable presence
tests, false provenance in `consumed_evidence_ids`, and an unverified path/
symlink containment exposure. No correction was attempted because the approved
stop conditions require rejection without a second solution attempt.

All four candidate production/test files were restored byte-for-byte with
their original `0644` modes. Post-rollback focused tests passed 26/26 and the
full suite passed 157/157. Active runtime files were not synchronized.

Decision:
REJECT

Notes:
The hypothesis is unsupported by this v0 policy-only envelope: the observed
duplicate was not removed, the audit claim contradicted the trace, and the
minimal schema/tests did not safely bind trusted evidence. The changelog is
unchanged because the candidate was rejected. Exact preimages, runtime hashes,
fixture, traces, and temporary validation artifacts were task-owned under a
private `0700` root and were removed after rollback verification. No later
optimization phase is authorized by this experiment.

## EXP-20260810-007 - Direct Local Lookup Fast Path

Date: 2026-08-10
Status: REJECTED

Problem:
The main Graphify/router task has four rejected independent attempts. Natural
exact lookups still activate the broad repository-tools router and Graphify,
while a prescriptive command prompt can mask that routing behavior.

Evidence:
EXP-20260810-005 reproduced a module read and Graphify false positive with a
natural lookup prompt. EXP-20260810-006 was rejected before publication because
its command-prescriptive baseline already passed and could not distinguish the
candidate. This is the fifth and final permitted attempt.

Hypothesis:
An explicit pre-router fast path directing exact repository text, filename, and
path lookups to local `rg`, combined with an advanced-only router row and a
positive-only Graphify description, will make natural simple lookups lightweight
without breaking advanced routing or explicit Graphify behavior.

Solution Attempt:
Add one literal fast-path rule before the lazy-router table; narrow its
repository-tools row in the template, portable Codex policy, and active global
policy; change only Graphify frontmatter description. Preserve module and skill
bodies. No sixth attempt is permitted.

Test:
Require static RED and a completed natural live behavioral RED before publishing
production changes. Then run focused static GREEN and six fresh sequential
trace-validated probes: exact text, filename, known file, generic content,
literal help, and a real two-file architecture graph. Finish with regressions,
parity, independent reviews, permission hardening, and exact cleanup.

Success Criteria:
- Baseline natural exact lookup returns the correct match and shows a module or
  Graphify false-positive; otherwise publish nothing and reject.
- GREEN exact and filename probes use only contained successful `rg` commands,
  return exact results, and show no module or Graphify activity.
- Known/generic probes use only bounded contained `rg`/`sed` readers and show no
  module or Graphify activity.
- Help returns the captured Usage block byte-for-byte with zero task commands.
- Architecture loads the exact module and skill, executes real Graphify on two
  Python sources, and creates a fresh source-verified `EXTRACTED` calls edge
  without semantic, subagent, network, or fabricated evidence.
- Literal fast path precedes the router; advanced triggers remain; all three
  policies are byte-identical; module/body/config/other variants retain preimages.
- Focused/full tests, reviews, permissions, and task-owned cleanup pass. Any
  completed violation rejects and rolls back without retry.

Result:
Both required RED gates passed. The natural baseline returned the correct exact
match but first read the complete Graphify skill and repository-tools module and
announced Graphify routing. After publishing the candidate, the focused 26-test
suite passed; fresh exact-text and filename probes used only contained `rg`, and
the known-file probe used one bounded `sed`, all with correct outputs and no
module or Graphify activity. The generic-content probe returned the correct
value but executed two composed shell commands containing `rg`, `sed`, `ls`, and
`wc`, violating the immutable bounded-reader and no-shell-composition criteria.
No retry was permitted after completed task activity. Remaining help and
architecture probes were not run. All candidate policy, metadata, and test
changes were restored to their verified preimages.

Decision:
REJECT

Notes:
One retry is allowed only for an incomplete zero-activity transport failure.
Authorized scope excludes installs, module-body/config-schema changes, network,
MCP/scanners, repository-root graph construction, commit, push, deployment, and
archive mutation. Acceptance criteria will not be weakened.
This was failed independent attempt 5 of 5. Per the user-defined ceiling, no
sixth attempt or further candidate change will be started.
Independent code review passed the rejection, trace evidence, and exact rollback.
Security review confirmed no changed trust-boundary residue or task-created graph
artifact and identified four subagent session logs for `0600` hardening before
removing only the verified task-owned temporary root.
The terminal archive check returned `ACTION_REQUIRED` (`active=5`, `archive=41`,
`moved=7`); no archive mutation was applied because it is outside this task.

## EXP-20260810-006 - Repository Router Trigger Boundary

Date: 2026-08-10
Status: REJECTED

Problem:
The main Graphify trigger-narrowing task remains incomplete after three
independent attempts. EXP-20260810-005 proved that a narrow Graphify description
prevents the false-positive skill load, but the broad repository-tools router
still reads `CMA_REPO_TOOLS.md` before an exact lookup and violates the strict
`rg`-only contract.

Evidence:
The first EXP-20260810-005 GREEN exact-text trace completed a `sed` read of the
repository-tools module before its successful `rg` command. The active,
portable, and template policies all use a router trigger beginning with
`Repository text/path`, so exact lookups necessarily activate that module.

Hypothesis:
Removing exact text/path and generic repository-content vocabulary from the
router trigger, while publishing a positive-only Graphify description, will
keep simple lookups on their prescribed local readers and preserve explicit
Graphify plus architecture and advanced repository-tool routing.

Solution Attempt:
Replace the single repository-tools router row in the template, portable Codex
policy, and active global policy; change only Graphify's frontmatter description.
Keep the repository-tools module body, config, other variants, and Graphify body
unchanged. This is independent solution attempt 4 of at most 5.

Test:
Capture static and fresh live exact-lookup RED evidence before publication.
Then run fresh sequential exact-text, filename, known-file, generic-content,
literal help, and two-file architecture probes. Validate raw JSONL lifecycle,
exact commands and bounded paths, positive Graphify execution provenance, a
source-verified EXTRACTED calls edge, parity, regressions, reviews, and cleanup.

Success Criteria:
- Exact text and filename probes each run exactly the prescribed successful
  `rg` command, with no policy/module or Graphify activity.
- Known-file and generic-content probes run only their prescribed bounded local
  reader, with no policy/module or Graphify activity or out-of-corpus access.
- Literal `/graphify --help` returns the captured Usage block byte-for-byte and
  runs no task command.
- The architecture probe reads the repository-tools module and Graphify skill,
  executes the real local Graphify build on exactly two Python files, and
  produces a source-verified `EXTRACTED` `calls` edge from
  `consumer.render_label` to `provider.canonical_label`, without semantic,
  subagent, network, or fabricated evidence.
- The narrowed row retains architecture, structural AST, symbol, dependency,
  security, and public-source triggers; template, portable, and active policies
  are byte-identical.
- The repository-tools module, config/trust state, Graphify body, other variants,
  and unrelated work retain their preimages; focused/full tests, independent
  reviews, permissions, and exact task-owned cleanup pass.
- A retry is allowed only after an incomplete lifecycle with zero observable
  task activity. Any completed violation rejects this attempt without retry.

Result:
The static contract produced meaningful RED because neither the narrow router
row nor the positive-only Graphify description was present. However, the
required fresh live pre-change exact-text probe already passed the immutable
oracle: it executed exactly the prescribed `rg` command, returned the exact
normalized line, and showed no repository-tools module or Graphify activity.
The prescriptive prompt therefore bypassed the behavior this attempt intended
to distinguish. No policy or Graphify production change was published, and the
test-only contract edit was restored.

Decision:
REJECT

Notes:
The user authorized autonomous continuation through at most five independent
attempts. This attempt authorizes the bounded active policy and metadata changes
plus exact rollback, but not dependency installation, module-body/config-schema
changes, network/MCP/scanner use, repository-root graph construction, commit,
push, deployment, or archive mutation. Acceptance criteria will not be weakened.
This is failed independent attempt 4 of 5. The final attempt must use a
non-prescriptive natural lookup prompt whose baseline reproduces the unwanted
activation, while retaining strict trace-based command and provenance checks.
Independent code review passed the rejection and rollback evidence. Security
review confirmed all policy, skill, module, test, config, and trust preimages;
four task-created subagent session logs were identified for `0600` hardening
before exact temporary-root cleanup.

## EXP-20260810-005 - Graphify Activation Boundary

Date: 2026-08-10
Status: REJECTED

Problem:
Graphify's broad frontmatter description still activates for simple repository
content work, while EXP-20260810-004 could not be accepted because it coupled
the activation boundary to an over-broad `rg`-only command-purity criterion.

Evidence:
EXP-20260810-003 observed a full Graphify skill load before an exact lookup.
EXP-20260810-004 showed that a narrower description prevents Graphify false
positives, but also showed that mandatory policy bootstrap and bounded known-file
reading can legitimately use `sed` without making Graphify the selected tool.

Hypothesis:
A Graphify description limited to architecture, cross-file, data-flow,
call-path, coupling, relationship, and explicit `/graphify` requests will remove
simple-task false positives while preserving real help and architecture flows.

Solution Attempt:
Change only the active Graphify frontmatter description. Keep its body, global
policy, repository-tools module, config schema, and portable CMA assets
unchanged.

Test:
Capture same-scope static and live exact-lookup RED evidence, then validate six
fresh sequential sessions: exact text, filename, one known file, generic project
content, literal `/graphify --help`, and a two-file code-only architecture
fixture. Validate raw JSONL lifecycle, commands, outputs, graph edges, source
behavior, permissions, config/trust parity, and cleanup.

Success Criteria:
- Exact text and filename probes use successful `rg` and show no Graphify load,
  invocation, announcement, or artifact.
- Known-file and generic-content probes use only bounded `rg`/`sed` readers and
  show no Graphify activity.
- Literal help returns the current Usage block byte-for-byte with zero task
  commands.
- The architecture probe uses exactly two Python files, performs no semantic
  extraction or subagent work, and produces a source-verified EXTRACTED `calls`
  edge from `consumer.render_label` to `provider.canonical_label`.
- At most one transport-only retry is allowed only after a zero-activity
  incomplete lifecycle; retries after task activity are forbidden.
- Global policy, repository-tools module, config, trust entries, Graphify body,
  source fixtures, and unrelated dirty work remain byte-identical; tests,
  independent reviews, permissions, and exact task-owned cleanup pass.

Result:
The static pre-change assertion and fresh exact-text probe both produced
meaningful RED evidence. After publishing the candidate description, the first
fresh exact-text probe returned the correct normalized match and did not load
Graphify, but its trace first read `CMA_REPO_TOOLS.md` with `sed` before running
`rg`. This violated the immutable exact-lookup requirement that every task
command be `rg`. Because the attempt contained completed task commands and a
final answer, the transport-only retry rule prohibited a retry. The active
Graphify skill was restored byte-for-byte from its verified preimage.

Decision:
REJECT

Notes:
Approval includes exact incidental trust-entry cleanup, session/log permission
hardening, and deletion of only the validated task-owned temporary root. It does
not include dependency installation, policy/router/config-schema edits, graph
building in the CMA repository root, commit, push, or deployment.
The failure is outside the permitted Graphify-description-only scope: the
repository-tool policy bootstrap itself caused the extra reader. The remaining
five GREEN probes were not run after this fail-closed rejection.
Independent code review also found that the disposable validator's unexecuted
architecture branch could accept a fabricated graph without positive Graphify
provenance, and that its known-file/generic path checks did not reject every
absolute out-of-corpus read. These gaps reinforce rejection; no result from
those branches was used as acceptance evidence.
The focused lazy-runtime suite passed 26 tests and the full suite passed 157
tests after rollback. Security review confirmed active skill/config parity and
safe containment; four task-created subagent session logs were hardened from
`0644` to `0600`, then the verified task-owned temporary root was deleted and
its absence confirmed. The terminal record archive check returned
`ACTION_REQUIRED`; no archive mutation was applied because it would exceed this
experiment's approved scope.

## EXP-20260810-004 - Narrow Graphify Skill Activation

Date: 2026-08-10
Status: REJECTED

Problem:
Graphify's broad skill description activates for exact repository text and path
lookups that the repository-tool router assigns to `rg`, adding unnecessary
skill loading and commands.

Evidence:
EXP-20260810-003 rejected the routing pilot after a fresh exact-text task loaded
the complete Graphify skill through four shell commands before running `rg`.

Hypothesis:
Replacing only the active Graphify frontmatter description with explicit
architecture and relationship triggers plus explicit `rg` exclusions will keep
exact lookups on `rg` while preserving literal `/graphify` and architecture
activation.

Solution Attempt:
Change only the active Graphify skill description. Keep the skill body, active
repository-tool router, global policy, configuration, and portable CMA assets
unchanged.

Test:
Capture a pre-change static and fresh-session RED, then run static metadata
checks and bounded sequential fresh-session probes for exact lookup, filename
lookup, single-file reading, generic project content, `/graphify --help`, and a
cross-file dependency question. Validate the JSONL traces rather than trusting
final prose.

Success Criteria:
- Four simple repository-content probes use only `rg` and never load or invoke
  Graphify.
- `/graphify --help` returns the unchanged Usage section without task commands.
- A cross-file dependency prompt produces real Graphify activation evidence.
- The Graphify body, router, global policy, configuration, and unrelated dirty
  work remain byte-identical.
- Focused CMA lazy-router regression tests and diff checks pass.

Result:
The metadata assertion changed from RED to GREEN without altering the Graphify
skill body. Fresh exact-text, filename, and generic project-content runs no
longer activated Graphify; literal help and cross-file dependency runs still
activated it. However, the defined success criteria were not met: the exact
run loaded the repository-tools module with `sed` before `rg`, the generic
README run used `sed`, and the single-known-file run stalled after lifecycle
start and was terminated without retry. The architecture probe also added one
temporary trust entry for its disposable corpus; that exact entry was removed
and the active config hash returned to its pre-test value. The active Graphify
description and changelog entry were rolled back after code review.

Decision:
REJECT

Notes:
No installation, graph build in this repository, MCP connection, config change,
commit, push, or deployment is authorized by this experiment.
The global policy, repository-tools module, config, and Graphify skill returned
to their pre-attempt hashes. Code review identified unmet acceptance criteria as
a HIGH blocker. A narrower acceptance contract or a broader router-policy change
would be a separate approved task.

## EXP-20260810-003 - Repository Router Usage Measurement

Date: 2026-08-10
Status: REJECTED

Problem:
The active policy-only router has not been observed in a fresh Codex task, so
its routing behavior, latency, and token use remain unverified.

Evidence:
EXP-20260810-002 verified activation but explicitly deferred tool use and cost
evaluation. A strict router-disabled baseline would require prohibited policy
or authentication changes.

Hypothesis:
One exact-text lookup will select only `rg`, while one simple control will use
no tools; two ephemeral JSONL runs can measure their elapsed time and tokens
without changing repository or active runtime state.

Solution Attempt:
Run exactly two sequential `codex exec --ephemeral --json` tasks in a read-only
sandbox: one fixed exact-text lookup and one fixed no-tool control.

Test:
Validate synthetic failure fixtures before live execution, then require exact
JSONL lifecycle and usage events, an allowlisted successful `rg` command for
the routed task, zero tools for the control, distinct thread IDs, and pre/post
state parity.

Success Criteria:
- Both original runs exit zero with exactly one valid usage event.
- The routed run uses only the narrowest approved local command and returns the
  exact expected path.
- The control returns the exact sentinel with zero tool events.
- Repository, active policy/config, and session inventories remain unchanged.
- Results report observed time and tokens without claiming causal speedup or
  actual account billing.

Result:
The synthetic validator produced meaningful RED before implementation and then
passed 7/7 fixtures. The first and only live routed run exited at the Codex
transport level with one valid usage event, but the pilot failed closed before
the control run. Instead of selecting only `rg`, the fresh session announced
Graphify, read all 699 lines of the Graphify skill using four shell commands,
then ran an `rg` pipeline and emitted two agent messages. Observed usage was
163,172 input tokens, including 132,864 cached input tokens, plus 839 output
tokens and 294 reasoning output tokens. The exact path result was correct, but
the route violated the narrowest-tool and minimal-command criteria. The control
run was not executed and no retry occurred. Active policy/module parity and
repository status were checked afterward; the only repository change is this
experiment record. Exact monotonic latency and full pre/post inventory parity
are unverified because validation stopped before the runner persisted them.

Decision:
REJECT

Notes:
No retry, installation, MCP connection, scan, graph build, policy change,
commit, or push occurred. The ephemeral thread identifier is absent from the
persisted session tree. The failure indicates a routing conflict: the broad
Graphify skill trigger overrides the compact exact-text route and adds material
context cost. Independent code and security reviews returned PASS. The exact
task-owned private harness and raw JSONL directory was removed after review.
Any correction is a separate task and approval gate.

## EXP-20260810-002 - Active Repository Tool Router Pilot

Date: 2026-08-10
Status: ACCEPTED

Problem:
The approved repository-tool router exists only in the managed Codex source.
The active local `~/.codex` runtime cannot be evaluated until its policy and
module are synchronized, but activation must preserve the current runtime and
provide a verified rollback point.

Evidence:
The active policy differs from the approved template by exactly the missing
router row, and the active `CMA_REPO_TOOLS.md` module is absent. The active
runtime contains 7.8 GB of recoverable files plus one live IPC socket. A live
copy cannot be an atomic point-in-time snapshot, and macOS `ditto` intentionally
excludes sockets and pipes.

Hypothesis:
A private, verified backup of all recoverable active runtime state followed by
preimage-bound atomic publication of only the module and router row will enable
a reversible usage pilot without widening runtime authority.

Solution Attempt:
Create a unique external `0700` backup with source-before, payload, and
source-after manifests, explicitly classify volatile and excluded special
entries, validate stable parity, and write the completion marker last. Direct
`ditto` was rejected after a socket error/FIFO hang; `rsync` and `bsdtar`
attempts were then rejected for macOS metadata drift. The final method builds a
simplified BOM containing only recoverable paths and applies BOM-filtered
`ditto`, preventing special-file access while preserving required metadata.
Then publish the module and policy atomically, with the policy as the activation
point and fixture-proven rollback on partial failure.

Test:
Capture active RED drift, run disposable backup/corruption/unique-name and
partial-sync rollback fixtures, validate the real backup and active source
parity, run focused and full CMA tests, and complete independent code and
security reviews.

Success Criteria:
- The experiment record predates the first backup attempt.
- A private external backup contains every recoverable stable entry with
  verified content and metadata parity.
- Live sockets, pipes, and changing files are truthfully classified rather than
  reported as stable backup parity.
- Active policy and module match their approved repository sources exactly.
- No unrelated active surface, tool installation, tool execution, fresh-session
  claim, commit, or push occurs.
- Rollback fixtures, focused/full tests, and independent reviews pass.

Result:
The approved planner and TDD stages completed. Active RED was captured. The
first disposable backup fixture rejected direct `ditto`; subsequent real
`rsync` and `bsdtar` staging attempts were rejected for xattr/creation-metadata
drift and preserved without completion markers. A BOM-filtered `ditto` fixture
preserved content, symlink target, mode, xattr, and ACL while excluding
socket/FIFO objects; corruption and destination collision were also rejected.
The atomic sync fixture passed wrong-preimage, symlink, both partial-publication
rollback, target-drift rejection, and positive postimage checks. The private
recoverable backup completed with an explicit special-file and system-metadata
boundary. Active policy and module hashes now match their approved repository
sources. The hardened fixture passed both partial-publication rollback cases and
target-drift rejection. Focused 26-test and full 157-test suites passed, and
independent code and security reviews returned PASS. No repository tool or
fresh Codex session was executed; runtime usefulness and cost remain a separate
usage evaluation.

Decision:
ACCEPT

Notes:
The user approved a live recoverable backup and accepted explicit exclusion of
ephemeral socket/FIFO objects. A complete runtime restore remains separately
gated and requires quiescence.

## EXP-20260810-001 - Selective CMA-ARK Rollback

Date: 2026-08-10
Status: ROLLED_BACK

Problem:
The CMA-ARK work expanded a simple lazy-tool integration into a large inactive
adapter, hook, lifecycle, and host-evidence stack. The implementation adds
substantial maintenance and review cost while no CMA-ARK hook, skill, or managed
runtime path is active.

Evidence:
The ARK and CMA-ARK implementation surfaces are entirely untracked at the
current Git HEAD, while tracked changelog and experiment ledgers contain mixed
ARK and unrelated CMA changes. The approved assessment found roughly 7,500
lines in the CMA-ARK integration layer versus roughly 1,400 lines in ARK, with
115 adapter tests but no active integration surface.

Hypothesis:
A selective, recoverable rollback can return ARK to one planning-only proposal
without losing audit history or changing unrelated dirty CMA work. Moving the
implementation to a private checksum-bound external backup and applying exact
preimage transforms to mixed tracked files should be safer than a repository
reset or broad patch reversal.

Solution Attempt:
Create an external private rollback manifest and RED-first acceptance checker,
move only approved ARK/CMA-ARK implementation artifacts into its payload, remove
only the four ARK ignore rules, transition the thirteen historical ARK
experiment statuses to `ROLLED_BACK`, add one truthful changelog entry, and
retain exactly one non-executable planning proposal.

Test:
Require meaningful RED before mutation, exact source-to-backup hash and metadata
parity, planning-only repository surface, deterministic tracked-file postimages,
anti-hardcoded-success mutation probes, full remaining root regressions,
read-only record checks, diff integrity, and independent code and security
reviews.

Success Criteria:
- Every approved implementation artifact is absent from the repository and
  recoverable from a private verified external backup.
- Exactly one CMA-ARK planning proposal remains and grants no implementation,
  runtime, activation, tool-execution, commit, or push authority.
- All thirteen historical ARK experiment records occur once and have current
  status `ROLLED_BACK` without rewriting their historical evidence or decisions.
- All unrelated tracked and non-ignored untracked CMA state remains
  byte-identical; generated ignored files are outside this rollback claim.
- RED, GREEN, mutation probes, remaining regressions, record validation, and
  independent reviews pass.

Result:
The approved ARK and CMA-ARK implementation surfaces were moved to a private
checksum-bound recovery backup, leaving one non-executable planning proposal.
Meaningful RED, final acceptance, all nine mutation probes, 152 remaining root
regressions under Python 3.10, record checks, diff integrity, and independent
code and security reviews passed. An initial Python 3.9 run failed on existing
Python 3.10 union-type syntax and was not counted as success.

Decision:
ROLLBACK

Notes:
The user explicitly approved the selective rollback and mandatory orchestration
chain. Commit, push, backup deletion, global runtime changes, and any future ARK
implementation or activation remain outside scope.

## EXP-20260809-012 - Disposable CMA-ARK Host Evidence Wrapper

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-011 accepted a deterministic same-run evidence contract, but no
test-only wrapper or disposable host harness implements it. The accepted design
therefore cannot yet prove that real hook/candidate evidence and a paired Codex
JSONL lane are bound, non-compensating, private, and truthfully cleaned up.

Evidence:
The inactive hook candidate can already produce a real plan-only artifact, and
its focused tests prove zero routed-tool execution. The repository has no host
evidence wrapper or harness, canonical `UserPromptSubmit` activation remains
absent, and the accepted schema has not yet been exercised by a same-child
disposable boundary.

Hypothesis:
A fixed isolated wrapper plus a three-pair disposable host harness can implement
the accepted contract without widening runtime authority. Executing the real
candidate/coordinator path inside each fake-host child and independently
validating exact artifacts, JSONL, identity, hashes, cleanup, and final status
will reject missing, altered, dirty, or hardcoded evidence.

Solution Attempt:
Add separate bounded wrapper, contract-validation, and harness modules plus a
disposable fake Codex host fixture and RED-first tests. Keep the canonical hook,
candidate, coordinator, adapter, ARK, trust configuration, dependencies, and
routed-tool authority unchanged. If truthful missing-artifact failure cannot be
represented by the accepted schema, stop before implementation and request a
narrow contract correction instead of fabricating evidence.

Test:
Capture meaningful RED from absent wrapper/harness behavior. Then run focused
positive, negative, boundary, cleanup, same-child binding, hardcoded-success,
three-run stability, and branch-coverage checks followed by relevant hook,
adapter, ARK, root-governance, code-review, and security-review regressions.

Success Criteria:
- Every disposable pair invokes the real wrapper and real inactive candidate
  exactly once while executing no routed tool.
- Candidate and Codex lanes are independently required and bound to the same
  run, session/thread identity, fixed query, prompt, reviewed files, and hashes.
- Three fresh pairs pass without retry or replacement and share one normalized
  candidate hash.
- Private artifacts are exact, bounded, mode-safe, hashed before deletion, and
  absent after successful cleanup; cleanup failure cannot report success.
- Missing hook execution, dirty JSONL, identity/hash drift, timeout, stderr,
  nonzero exit, malformed input, or hardcoded success fails closed.
- Focused branch coverage is at least 80%, relevant regressions pass, and
  independent code and security reviews have no blocking findings.
- No canonical activation, trust action, real Codex session, global change,
  dependency, routed-tool execution, commit, or push occurs.

Result:
Planner and TDD review independently confirmed a blocking contract gap before
implementation began. When the hook does not run, the accepted
contract correctly leaves both pass-only candidate artifacts absent. A valid
assessment cannot then provide their required raw hashes or normalized candidate
hash, while `final_result` still requires `assessment_sha256`. Hashing a sentinel
or fabricating passing-shaped failure artifacts would violate the contract.
The minimum truthful correction retains the field but permits
`assessment_sha256=null` only in a failed or unverified final result when no
valid assessment could be constructed; a passing final still requires a
lowercase 64-character assessment hash. The user approved that correction; its
meaningful RED failed 1/9 on the old schema and the corrected design passed 9/9.

The wrapper/harness RED then failed because the three implementation modules
were absent. The first implementation slice passes 5/5 contract tests and 2/2
real wrapper-to-candidate tests. The disposable harness passes 5/6 tests, but
three clean real candidate runs produce different normalized hashes even though
their query hashes are identical. Source inspection confirms that
`plan_sha256` covers the coordinator-generated UUID request ID, so it is
intentionally different on every invocation. The accepted empty volatile-field
allowlist is therefore incompatible with the real candidate. Excluding
`plan_sha256` only from cross-run normalization, while retaining and validating
every raw per-run plan hash, is the narrowest feasible correction; changing the
real coordinator request identity would exceed this test-only scope. The user
approved that correction. The resulting focused suite reached 19/19 with 84%,
81%, and 84% branch coverage for wrapper, contract, and harness sources.

The approved containment correction gives the candidate one wrapper-owned
process group and makes the candidate, coordinator, adapter, and plan-only ARK
boundary inherit it. Timeout and semantic-failure paths now terminate the full
group and reap direct children. A checked-in reviewed manifest binds the exact
hook-definition bytes plus wrapper, candidate, coordinator, contract, and
schema hashes before contract import; ownership, permission, path, type, and
bytes-only drift checks fail closed.

Final verification passed 27/27 focused host-evidence tests with 84% combined
branch coverage (wrapper 89%, contract 81%, harness 84%), 115/115 adapter tests,
and the previously completed 55/55 relevant root contracts. Independent code
and security re-reviews returned PASS with no blocking findings. Canonical hook
activation, trust, real Codex sessions, global changes, dependencies, routed
tool execution, commit, and push did not occur.

Decision:
ACCEPTED

Notes:
This experiment owns only the test-only wrapper/harness implementation and its
focused tests and records. Real activation and three fresh Codex sessions remain
separate approval gates.

## EXP-20260809-011 - Deterministic CMA-ARK Host Evidence Contract

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-010 correctly rolled back canonical hook activation after the
first fresh Codex session omitted bound plan fields from its final response and
JSONL trace. Later diagnosis established that the acceptance gate conflated
hook `additionalContext`, which is model context, with deterministic final or
JSONL evidence.

Evidence:
The inactive hook candidate directly returns the exact target, query and plan
digests, `success=true`, and `execution_performed=false` in the documented
`UserPromptSubmit` envelope. Official OpenAI documentation defines that output
as extra developer context, defines `codex exec --json` as an emitted event
stream, and recommends `--output-schema` for stable final-response fields; it
does not define the model response as canonical hook evidence.

Hypothesis:
A same-run two-lane acceptance contract will provide deterministic evidence
without widening runtime authority: a test-only external wrapper will be the
actual hook command, validate the candidate/coordinator plan artifact, and bind
it to its paired ephemeral read-only Codex JSONL behavior. Neither lane may
rescue a failure in the other, and model output will remain non-authoritative.

Solution Attempt:
Define same-host identity binding, a machine-readable schema bundle for the
external evidence artifacts and final result, three-run stability, private
temporary lifecycle, independent gating, failure rules, and future TDD contract
in the CMA-ARK design. Keep production hook/coordinator code, canonical
activation, trust, App Server, dependencies, and routed-tool behavior unchanged.

Test:
Capture meaningful RED failures from new documentation-contract tests before
updating the design. Then run the focused design test, relevant adapter and root
regressions, `git diff --check`, independent code review, and security review.

Success Criteria:
- Canonical candidate evidence and Codex behavioral events are separate,
  independently required lanes bound to the same host run and reviewed hook.
- Four private temporary artifacts have exact schemas, hashes, normalization,
  cleanup, and fail-closed assessment rules.
- Three candidate runs and three Codex runs are required; no later run can
  replace a failed required run.
- Final model text and `--output-schema` output are presentation only and never
  authenticate plan identity, digest binding, or zero execution.
- App Server remains deferred and production hook/coordinator code, activation,
  trust, dependencies, and routed-tool authority remain unchanged.
- New tests fail against the pre-change design, then focused and relevant
  regressions pass with no blocking code or security review findings.

Result:
The documentation contract produced the required meaningful RED: the existing
two tests passed while all four initial evidence-contract tests failed on
absent design requirements. The first bounded design then passed 6/6 focused
tests after a whitespace-only harness correction for Markdown wrapping. Code
review exposed missing same-host identity binding, narrative-only artifact
schemas, and phrase-only test weakness. The remediated contract added a parsed
machine-readable schema test; code re-review passed. Security review then found
that contradictory success/lane/cleanup states remained schema-valid and that
embedding a fresh run ID in the candidate query made the three-run stability
rule unsatisfiable. The remediated contract uses conditional result variants, a
single post-comparison session/thread identity, and a fixed candidate query with
the run ID outside it. The current focused suite passes 8/8, alongside 6/6
plan-only hook candidate tests and 3/3 passive CMA-ARK contract tests. Direct
Draft 2020-12 validation accepts the coherent assessment and rejects both a
failed-lane passing assessment and failed-cleanup passing final result.
`git diff --check` also passes. Independent code and security re-reviews passed
with both security blockers closed. No wrapper, fresh Codex session, hook
activation, trust change, routed tool, dependency, commit, or push occurred.
Final governance regressions passed 11/11 orchestration, 7/7 hypothesis, and
19/19 record-archive tests. The terminal-record check reported every managed
record below its archive threshold, so no archive apply was required.

Decision:
ACCEPT

Notes:
This experiment is documentation and test-contract scope only. Wrapper
implementation and real three-session validation require a distinct approval.

## EXP-20260809-010 - Canonical CMA-ARK Hook Activation

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
EXP-20260809-009 proved a deterministic plan-only `UserPromptSubmit` transport
and a descriptor-anchored disposable lifecycle, but the canonical CMA repository
still has no active prompt hook. The existing pilot intentionally rejects the
canonical root, so the approved activation cannot be installed or rolled back
through the reviewed lifecycle.

Evidence:
The canonical `.codex/hooks.json` contains only empty `SessionStart` and `Stop`
events, `.codex/cma-ark-user-prompt.py` is absent, and the pilot accepts only
`install|rollback --target` against a marked disposable repository. Codex CLI
0.147.0 reports stable hook support. Official OpenAI documentation requires
review and trust of the exact non-managed hook definition through `/hooks` and
records trust against its current hash.

Hypothesis:
Fixed no-target `repo-install` and `repo-rollback` operations, built on the
existing descriptor-relative lifecycle and separated from the bounded CLI,
will permit exact canonical activation and recovery without reactivating the
failed repo skill or granting execution authority. A user-reviewed exact hook
definition should then produce deterministic fresh-session plans with
`execution_performed=false` and no routed tool execution.

Solution Attempt:
Split the lifecycle primitives into one adjacent private module, keep the pilot
as a thin isolated CLI/router, and add fixed canonical operations that derive
only their own repository root. Prove the lifecycle first in copied layouts,
then rehearse canonical install and rollback, reinstall exact bytes, use the
supported `/hooks` trust flow without bypass, and run three fresh plan-only
sessions.

Test:
Capture RED evidence for the absent repo operations. Verify copied-layout
install, idempotency, exact preservation, rollback, reinstall, path and content
drift refusal, atomic failure reporting, hostile environment isolation, and
anti-hardcoded-success behavior. Run focused branch coverage, adapter, ARK,
and root regressions before canonical rehearsal. Verify the exact live hook in
three fresh Codex sessions after trust.

Success Criteria:
- Repo operations derive one fixed canonical root and reject all caller targets.
- Disposable operations retain their marker and canonical-refusal behavior.
- Install and rollback mutate only the exact owned hook entry and script,
  preserve unrelated config, and truthfully report committed cleanup failures.
- The installed script is byte-identical to the reviewed candidate and mode
  `0600`; no skill activation, global skill, dependency, MCP/cplt, or Graphify
  execution is added.
- Exact trust uses the supported `/hooks` review only; no trust bypass, manual
  trust-state edit, or unrelated hook approval occurs.
- Three fresh sessions return usable matching CMA-ARK plans with
  `execution_performed=false`, no routed tool execution, retry, or fallback.
- Focused branch coverage is at least 80%, relevant regressions pass, and code
  plus security review have no blocking findings.

Result:
The missing canonical operations produced the expected initial RED: all three
copied-layout tests failed because the existing parser rejected `repo-install`
with exit 2. The bounded implementation then passed 23/23 focused tests with
80.70% combined CLI/lifecycle branch coverage, 83/83 adapter tests, 33/33 ARK
tests, and 166/166 root regressions. Code and security review both passed after
three false-state cleanup paths were found and closed. The real canonical
lifecycle installed, restored the original config SHA-256 exactly on rollback,
and reinstalled the byte-identical mode-`0600` hook with no lock/temp residue.
Exact trust was then granted only to the displayed project hook through
`/hooks`; no broad trust or bypass was used. The first fresh ephemeral
read-only Codex session exited 0 and returned a five-step generic `rg` plan with
no tool calls, but its JSONL trace omitted the required target/query/plan
digests, `success=true`, and literal `execution_performed=false` fields. It was
therefore not a usable bound CMA-ARK plan. The remaining two sessions were not
executed. The governed rollback removed the hook entry and script, restored the
original config SHA-256
`49ebbad6f600dbb37355f63e80bde9457a77023891a6bbca4157dee381abd071`,
and left no lock/temp or skill surface.

Decision:
ROLLBACK

Notes:
The hook lifecycle implementation remains as a tested inactive recovery tool,
but canonical activation is rejected by the fresh-host acceptance gate. The
Codex-owned exact-definition trust record is inert after config removal and was
not manually edited. Commit, push, deployment, global skill changes, routed
tool execution, and the remaining two fresh sessions did not occur.

## EXP-20260809-009 - Deterministic CMA-ARK Hook Transport

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The rolled-back repo-local skill activation depended on a model-generated
subprocess call carrying request JSON on stdin. Three fresh Codex sessions
discovered the skill, but none produced a usable host plan; the final attempt
omitted stdin and failed closed with `invalid_request`.

Evidence:
EXP-20260809-008 records the three failed host attempts and governed rollback.
The active Codex CLI reports stable hook support, and the official
`UserPromptSubmit` contract supplies the user prompt to a repo-local command
hook as JSON on stdin. The repository already contains one tracked private
`.codex/hooks.json` with no active prompt hook.

Hypothesis:
A repo-local `UserPromptSubmit` hook that recognizes only the existing literal
`$cma-ark <query>` grammar can translate the host event into the coordinator's
compact JSON request exactly once without placing the raw query in argv or new
persistent state. Descriptor-anchored install and rollback in a disposable
copy can bound config/script mutations without claiming protection from a
malicious process running as the same user.

Solution Attempt:
Build an inactive hook candidate and a separate disposable-only hook pilot.
The handler validates the exact host event, invokes the existing plan-only
coordinator through fixed literal argv and stdin, and emits only bounded
sanitized hook context. The pilot uses Python 3.9 `dir_fd`, `O_NOFOLLOW`,
relative atomic operations, and exact owned-content checks to add or remove one
hook entry and script in a disposable repository. It does not activate the
canonical repository.

Test:
Capture meaningful RED failures for missing hook transport and descriptor
operations. Then verify exact invocation grammar, input boundaries, one
coordinator delivery, query non-disclosure, hostile environment isolation,
protocol failure handling, config preservation, idempotency, drift refusal,
path-swap rejection, atomic cleanup, and anti-hardcoded-success behavior.

Success Criteria:
- Only an exact whole-prompt `$cma-ark <query>` event reaches the coordinator.
- The raw query appears only in the coordinator stdin inherited from the host
  prompt and never in argv, hook output, environment, or new files/state.
- A valid request invokes the coordinator once and returns plan-only evidence
  with `execution_performed=false`; invalid or contradictory evidence fails
  closed without fallback or retry.
- Disposable install and rollback preserve unrelated hooks, are idempotent,
  refuse drift/symlinks/path replacement, and truthfully report committed
  cleanup failures.
- Focused branch coverage is at least 80%, relevant regressions pass, and an
  always-success dummy fails the acceptance tests.
- No canonical hook trust/activation, skill activation, global config,
  dependency, MCP, cplt, Graphify, tool execution, commit, push, or deployment
  occurs.

Result:
The initial existence tests failed as expected because neither hook candidate
nor hook pilot existed. The completed handler accepted only the exact literal
invocation, delivered the compact coordinator request through stdin once,
rejected malformed and hardcoded-success responses, and returned digest-only
plan context. A real handler-to-coordinator-to-adapter-to-ARK black-box plan
returned `success=true`, `execution_performed=false`, and selected `rg` without
executing it. The disposable CLI installed and rolled back its exact hook entry
and script while restoring unrelated hook configuration.

Independent code review found and closed one swallowed combined
publish/cleanup failure; the final branch reports
`not_applied_cleanup_failed` when a residual staged script remains. Independent
security review found and closed compact-to-pretty JSON size expansion that
could strand an unreadable active config; encoded size is now rejected before
publication and staged state is removed. Final focused tests passed 18/18 with
85% combined branch coverage, the complete adapter suite passed 78/78, CMA-ARK
root contracts passed 5/5, ARK passed 33/33, and the broader root suite passed
166/166. Code and security re-reviews both returned PASS. The canonical hook
config, hook trust, repo/global skill discovery, dependencies, and execution
authority remained unchanged.

Decision:
ACCEPT. Retain the inactive hook candidate and descriptor-anchored disposable
pilot as the verified replacement transport design. Keep canonical hook trust
and activation as a distinct future task requiring explicit approval.

Notes:
Codex hook trust remains a separate user-controlled activation gate. This
experiment proved the candidate and disposable lifecycle only; it did not
silently trust or activate a repository hook.

## EXP-20260809-008 - Repo-Local CMA-ARK Plan Activation

Date: 2026-08-09
Status: ROLLED_BACK

Problem:
The reviewed CMA-ARK skill remains outside Codex discovery, so the repository
cannot use its explicit-only, plan-only routing boundary. The disposable pilot
correctly refuses the canonical repository and therefore cannot safely express
the separately approved real activation.

Evidence:
EXP-20260809-007 accepted the hardened launcher, identity binding, and atomic
disposable install/rollback pilot while reserving real repo-local activation
for a separate explicit approval. That approval is now present, and the real
`.agents/skills/cma-ark` path is absent.

Hypothesis:
Adding fixed `repo-install` and `repo-rollback` operations that derive the
canonical source root internally, while leaving disposable target validation
unchanged, will permit a bounded repo-local activation without adding global or
execution authority.

Solution Attempt:
Reuse the existing exact manifest, private state, exclusive operation lock,
atomic publication, identity-bound idempotency, drift-refusing rollback, and
truthful committed-failure reporting. The new operations accept no target
argument and can act only on the pilot's canonical repository root.

Test:
Capture copied-layout RED evidence for the missing operations, then verify
exact install, idempotency, rollback, drift refusal, pre-commit cleanup, and
target-argument rejection. After GREEN regressions, execute the approved real
install, verify plan-only zero-execution behavior, rehearse rollback, reinstall,
and leave only the repo-local explicit skill active.

Success Criteria:
- Disposable operations continue rejecting the canonical repository.
- Repo operations derive one fixed target and accept no `--target` input.
- The installed surface equals the reviewed three-file candidate byte-for-byte
  and retains `allow_implicit_invocation: false`.
- Installed-path planning returns `execution_performed=false` and never invokes
  routed `rg` or adapter `run` behavior.
- Rollback removes only unchanged installer-owned state and final reinstall is
  exact.
- No global skill, dependency, MCP/cplt, Graphify, commit, push, or deployment
  change occurs.

Result:
Copied-layout repo operations passed exact install, idempotency, rollback,
reinstall, drift refusal, target rejection, and pre-publication cleanup tests.
The real lifecycle installed, verified a direct `success=true` plan with
`execution_performed=false`, rolled back cleanly, and reinstalled exact files.
Three fresh Codex sessions discovered the repo skill and never executed routed
search, but none returned a usable plan: two failed under the macOS
`/usr/bin/python3` shim, and the revised pinned-interpreter attempt omitted the
required JSON stdin and returned fail-closed `invalid_request`. The governed
installer then removed the repo-local discovery surface and state.

Decision:
ROLLBACK. Remove the canonical repo operations and the unproven bootstrap
revision, preserve only the inactive EXP-20260809-007 candidate, and require a
separately approved deterministic host input and descriptor-safe installation
design before another activation attempt.

Notes:
Fresh Codex discovery loaded the repo-local skill, but both read-only and
workspace-write host sessions returned fail-closed `process_failed` because the
outer `/usr/bin/python3` developer-tool shim attempted a denied temporary cache
write. The attempt was revised to invoke the coordinator through its already
identity-pinned root-owned real interpreter binary; adapter and ARK child
boundaries remained unchanged. That revision also failed host validation and
was removed with the activation-only repo operations.

## EXP-20260806-003 - PTY Package Install Stdin Continuation

Date: 2026-08-06
Status: REVISED

Problem:
The approved apt installation completed, but the SSH PTY session returned to a
shell prompt without executing the remaining pinned Codex npm installation and
version-verification commands from the submitted stdin stream.

Evidence:
A separate read-only SSH check confirms `nodejs` 18.19.1 and `npm` 9.2.0 are
installed, no apt or dpkg process remains, and `codex` is still missing. The
original PTY session remains open at a root shell prompt after `needrestart`.

Hypothesis:
The interactive apt/needrestart path consumed or interrupted the remaining
heredoc stdin. Sending the bounded remaining commands directly to the already
open PTY session will complete the approved package step without rerunning apt.

Solution Attempt:
Write only the exact pinned npm install and version/path verification commands
to the existing SSH session, followed by `exit`. Do not rerun apt, open another
package source, or restart services.

Test:
Require the existing session to exit zero, then use a fresh read-only SSH
connection to verify the installed package version, executable path, and
`codex --version` output.

Success Criteria:
- Apt is not invoked again.
- `@openai/codex@0.146.1` is installed through npm's verified global prefix.
- `codex --version` reports the pinned release.
- The original SSH session exits successfully.
- No service or host restart is performed.

Result:
The tool rejected the write with `stdin is closed for this session`; no npm
command was delivered and Codex remained uninstalled. The open-session
continuation mechanism is therefore unavailable even though the remote shell
had previously displayed a prompt.

Decision:
REVISE

Notes:
This experiment addresses only stdin continuation after the already completed
approved package transaction.
