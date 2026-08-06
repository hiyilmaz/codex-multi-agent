# CMA TDD Module

## Load When

Load for features, bugfixes, refactors, behavior changes, tests, coverage, or
test-integrity review.

## Do Not Load When

Do not load for answer-only, read-only, or formatting tasks without behavior
changes.

## Rules

- Use `tdd-workflow` and write acceptance tests before implementation.
- Map every acceptance criterion to positive, negative, boundary, and
  regression evidence using the lightest sufficient test layer.
- Capture a meaningful RED failure before GREEN implementation.
- Tests must fail for an absent, dummy, or hardcoded implementation.
- Never weaken assertions, skip tests, add test-only production branches,
  swallow errors, or mock the target behavior.
- Run focused tests first and the relevant regression suite before closure.
- Passing tests alone do not prove completion; review the diff and observable
  behavior independently.
