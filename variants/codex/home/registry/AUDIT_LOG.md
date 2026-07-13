# Registry Audit Log

Append-only log for changes made to reusable skills, agents, and registry
indexes.

## 2026-07-14

- [FIX] Removed three FormProxy skills and the crypto strategy discovery skill
  from the generic portable runtime and active skill index.
- [FEAT] Added the MIT-licensed ECC `tdd-workflow` skill to the portable Codex
  runtime and active skill index.
- [DOCS] Recorded the upstream ECC source and license attribution.

## 2026-06-24

- [INFRA] Added `orchestration-gate` as the decision skill for
  `ORCHESTRATION_MODE`.
- [INFRA] Documented project-level orchestration modes: `skip`,
  `ask-approval`, and `run-chain`.

## 2026-05-22

- [INFRA] Created user-global registry for active agents, active skills,
  orchestration policy, and controlled self-improvement governance.
- [INFRA] Added active core orchestration agents: `planner`, `tdd-guide`,
  `code-reviewer`, and `security-reviewer`.
- [INFRA] Added default status messages and YOLO-mode boundary policy.
