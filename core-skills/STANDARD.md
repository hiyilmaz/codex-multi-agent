# CMA Core Skill Standard v1

**Status:** Phase 1 canonical semantic standard  
**Scope:** Codex, Claude, and OpenCode  
**Standard version:** 1.0.0

## 1. Proposed CMA Core Skill Standard v1

A CMA core skill is a protected capability in the official CMA capability set.
Protection does not imply automatic activation: a core skill remains discoverable
but loads only when its positive activation conditions match the current evidence
need.

CMA uses one canonical semantic specification with three platform-native
projections. Codex, Claude, and OpenCode must preserve the same meaning while
using their own packaging and runtime conventions. This standard defines only
that shared meaning; it does not define a platform file format or runtime setup.

Each core skill should be instruction-only by default, short enough to load
economically, and focused on one primary evidence need. Detailed commands and
documentation may live in optional references loaded only when required. Add a
script only when deterministic automation is necessary and instructions alone
cannot provide reliable behavior.

## 2. Required Semantic Fields

Every canonical core-skill specification must define the following governance
metadata:

| Field | Requirement |
| --- | --- |
| Stable Skill ID | Unique, stable, lowercase kebab-case identifier. Renaming is a semantic change. |
| Display Name | Short human-readable name. |
| Capability Category | Stable category used for CMA capability routing. |
| Core / Protected Status | Must state `core/protected`. This is classification metadata, not an activation instruction. |
| Tool Dependency | Declare `none`, `optional: <tool>`, or `required: <tool>`. Do not infer or hide a dependency. |
| Semantic Version | Semantic version of the canonical skill contract. |

Every specification must also define these behavioral fields:

| Field | Requirement |
| --- | --- |
| Purpose | One bounded capability and its primary evidence need. |
| Use When | Clear positive activation conditions. |
| Do Not Use When | Clear negative and overlap boundaries. |
| Preconditions | Required inputs, authority, state, and dependency checks before work begins. |
| Workflow | Small ordered procedure that stops when sufficient evidence exists. |
| Stop Conditions | Conditions that require completion, refusal, or an unavailable/unverified result. |
| Output Contract | Required evidence, provenance, limitations, and truthful result status. |
| Safety / Authority Boundary | Allowed side effects, required approvals, actions the skill never authorizes, and mandatory secret-safe handling of sensitive evidence. |
| Tool Unavailable Behavior | Explicit behavior for each declared dependency mode, including not-applicable, fail-closed, and any predeclared reduced-scope path. |

## 3. Recommended Optional Fields

Include an optional field only when it changes correct use of the skill:

- Non-goals for important exclusions not already covered by `Do Not Use When`.
- Examples for ambiguous positive, negative, or boundary triggers.
- References for detailed commands, versioned documentation, or large lookup
  material. Keep references directly linked from the main instructions.
- Compatibility notes when tool or runtime versions materially affect behavior.
- Evidence retention notes for non-sensitive temporary output. Sensitive output
  handling is mandatory in `Safety / Authority Boundary`, not optional.
- Idempotency or rollback notes when the skill is explicitly authorized to mutate
  state.
- Owner or maintainer and license when repository governance requires them.
- Scripts or assets only when their necessity is justified by the workflow.

Optional fields must not weaken, replace, or contradict a required field.

## 4. Minimal Canonical Skill Template

This is a semantic template, not a Codex, Claude, or OpenCode file format.

```markdown
# <Display Name>

## Governance Metadata

- Stable Skill ID: <lowercase-kebab-case-id>
- Display Name: <human-readable name>
- Capability Category: <one stable category>
- Core / Protected Status: core/protected
- Tool Dependency: <none | optional: tool-id | required: tool-id>
- Semantic Version: <major.minor.patch>

## Purpose

<One bounded capability and one primary evidence need.>

## Use When

- <Positive activation condition.>

## Do Not Use When

- <Negative or overlap boundary.>

## Preconditions

- <Required input, authority, state, and dependency check.>

## Workflow

1. <Perform the smallest sufficient first step.>
2. <Collect and source-check the required evidence.>
3. <Stop when the output contract is satisfied.>

## Stop Conditions

- <Completion, refusal, unavailable, or unverified condition.>

## Output Contract

- <Evidence, provenance, limitations, and truthful status.>

## Safety / Authority Boundary

- <Allowed actions and required approvals.>
- <Actions this skill never authorizes.>
- Do not expose secrets. Minimize sensitive evidence and, when applicable,
  define private storage and bounded retention or require no persistence.

## Tool Unavailable Behavior

- For `none`, state `availability=not_applicable`; no tool-unavailable branch runs.
- For `required: tool-id`, report `availability=unavailable`,
  `status=unverified`, and `success=false`, name the blocked evidence need, and
  stop the dependent workflow.
- For `optional: tool-id`, report `availability=unavailable` and either stop as
  unverified or use only an explicitly predeclared tool-free path. Identify its
  reduced scope and mark every tool-dependent claim `status=unverified` and
  `success=false`. The reduced result may pass only when its own output contract
  requires no tool-dependent evidence.
- Never install, configure, activate, replace, or silently emulate the tool.
```

## 5. Rules Every Core Skill Must Follow

1. Treat core/protected as governance classification, never as always-active.
2. Load lazily from specific positive triggers and preserve explicit negative
   activation boundaries.
3. Serve one primary evidence need with one primary skill by default. Do not run
   overlapping skills for the same evidence need without a stated reason.
4. Keep the main instructions short. Use progressive disclosure and load only
   the reference needed for the current task.
5. Prefer instruction-only design. Add scripts only for clearly necessary,
   deterministic automation; do not add convenience scripts by default.
6. Keep tool-specific commands, behavior, and safety constraints inside the
   skill or its direct references. Global CMA instructions contain routing only.
7. Check preconditions before tool use. Never silently install, configure,
   activate, authenticate, or broaden access to a dependency.
8. Never silently fall back to a different tool or widen the evidence route.
9. Define unavailable behavior for the declared dependency mode. For `none`,
   use `not_applicable`. For an unavailable required tool, stop fail-closed. For
   an unavailable optional tool, either stop or use only an explicitly defined
   bounded tool-free path. Never claim tool-dependent evidence or hide reduced
   scope.
10. Do not treat discovery or activation as authority. Preserve higher-priority
    approval, security, scope, and destructive-operation rules.
11. Never expose credentials, tokens, private keys, or suspected secret values.
    Minimize sensitive evidence; require redacted reporting and, when persistence
    is necessary, explicit private storage and bounded retention rules.
12. Report success only from reviewed evidence. Missing or incomplete evidence
    must remain unverified or not executed with `success=false`.
13. Keep the canonical semantics provider-, model-, and platform-neutral.

## 6. Rules That Must Remain Variant-Specific

Later Codex, Claude, and OpenCode projections own these concerns:

- Native file format, frontmatter, metadata keys, and wrapper files.
- Installation and file locations.
- Discovery, invocation, and activation mechanisms.
- Plugin, MCP, agent, permission, and tool-binding syntax.
- Runtime-specific configuration and compatibility constraints.
- Native progressive-disclosure mechanisms and UI metadata.

A projection may translate or split the canonical fields to fit its platform,
but it must not change their triggers, negative boundaries, workflow meaning,
stop conditions, output guarantees, authority limits, or unavailable behavior.
Platform limitations must be disclosed; they must not be hidden by semantic
divergence or an undeclared fallback.

Phase 1 does not define, create, or validate any projection.

## 7. Validation Requirements

A core-skill specification is conformant only when all applicable checks pass:

1. **Structure:** all required governance metadata and behavioral fields exist,
   are non-empty, and use stable names.
2. **Positive activation:** explicit calls and natural positive triggers select
   the skill for its primary evidence need.
3. **Negative activation:** `Do Not Use When` prevents unrelated and cheaper
   evidence needs from loading the skill.
4. **Boundary and overlap:** adjacent skills have a deterministic primary route;
   additional skills require a distinct evidence need or an explicit reason.
5. **Unavailable dependency:** `none`, `optional`, and `required` modes each
   produce their declared result. Required-tool absence stops fail-closed;
   optional-tool absence exposes reduced scope or stops; `none` is explicitly
   not applicable. No mode permits silent execution, installation, or fallback.
6. **Output and safety:** success, evidence, side effects, and authority match the
   declared contracts, including negative and stop paths. Sensitive evidence is
   minimized and redacted; any persistence is private and retention-bounded.
7. **Size and disclosure:** the main instructions remain focused; detailed
   commands and documentation load only through directly linked references.
8. **Semantic parity:** when projections exist, Codex, Claude, and OpenCode are
   compared by required meaning, not byte identity.
9. **Scope:** validation rejects tool-specific skills, variant packaging,
   runtime configuration, sync logic, or governance automation introduced as
   part of this Phase 1 standard.

Keyword or heading presence alone is insufficient. Review must verify the
meaning of each field and must fail an absent, blank, contradictory, or
hardcoded-success contract. Each future skill remains independently testable
and rollbackable.

## 8. Expected Repository Location for the Canonical Standard

The canonical Phase 1 source is:

```text
core-skills/STANDARD.md
```

`core-skills/` is provider-neutral and separate from runtime-owned
`variants/codex/`, `variants/claude/`, and `variants/opencode/` projections.
Tool-specific specifications may later live under this canonical root, but none
are created in Phase 1.

## 9. Open Decisions

These decisions are intentionally deferred and do not block the semantic v1
contract:

- The stable capability-category vocabulary.
- Whether a later phase adds a machine-readable schema beside this document.
- The semantic-version bump and compatibility policy beyond initial v1.
- The exact semantic-parity representation and validator used by later phases.
- Whether a future separately approved scope extends the standard beyond Codex,
  Claude, and OpenCode.

None of these decisions authorizes Phase 2 work.

## 10. Phase 1 Readiness: PASS

Phase 1 is ready because the canonical semantic fields, minimal template,
universal rules, variant boundary, validation contract, repository location,
and non-blocking open decisions are defined.

This PASS applies only to the design readiness of CMA Core Skill Standard v1.
Tool-specific skills, platform projections, governance automation, installation,
runtime configuration, synchronization, activation, and Phase 2 remain not
executed and are not authorized by this document.
