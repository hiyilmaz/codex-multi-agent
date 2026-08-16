# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

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
