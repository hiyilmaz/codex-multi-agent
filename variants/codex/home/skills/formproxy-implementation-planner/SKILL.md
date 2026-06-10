---
name: "formproxy-implementation-planner"
description: "Plan bounded implementation work for FormProxy using PRD, TEST_PLAN, and AGENTS.md."
origin: "global"
---

# FormProxy Implementation Planner

Use this skill when a task is large enough to need discovery, phase planning, or explicit scope control.

## When to Use

- The task touches more than 3 files
- The current state is unclear
- The request affects architecture, module boundaries, or multiple subsystems
- The user asks for a plan, breakdown, or implementation sequence

## Workflow

1. Read the global `~/.codex/AGENTS.md` and the project `AGENTS.md`
2. Identify the exact in-scope requirement IDs from `docs/PRD.md`
3. Map those requirements to verification targets in `docs/TEST_PLAN.md`
4. Split the work into bounded phases with observable outputs
5. List assumptions and blockers explicitly before implementation

## Output Shape

- Architecture understanding
- Files/modules likely affected
- Ordered implementation phases
- Verification plan linked to PRD and TEST_PLAN
- Risks and assumptions

## Project Notes

- Do not expand beyond documented v1 scope
- Use Turkish for user dialogue only
- Keep code, comments, docs, and plans in English
- Prefer discovery first when the current state is unknown
