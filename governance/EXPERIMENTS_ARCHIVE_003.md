# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

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
