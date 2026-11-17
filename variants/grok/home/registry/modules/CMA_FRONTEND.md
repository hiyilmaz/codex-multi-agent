# CMA Frontend Module

## Load When

Load for UI implementation, browser verification, screenshots, responsive
layouts, accessibility, visual regressions, or interaction flows.

## Do Not Load When

Do not load for backend-only, documentation-only, or non-visual tasks.

## Rules

- Verify the requested user flow in the real rendered interface.
- Test relevant viewport sizes, overflow, loading, empty, error, and success
  states.
- Prefer semantic selectors and observable behavior over implementation detail.
- Preserve accessibility semantics, keyboard operation, focus, contrast, and
  reduced-motion behavior where relevant.
- Use screenshots only when visual evidence materially supports acceptance.
- Distinguish source tests, browser proof, and deployed-runtime proof.
