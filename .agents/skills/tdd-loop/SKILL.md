---
name: tdd-loop
description: "use during implementation when regression risk is non-trivial, when changing business logic, or when a bug needs a durable proof of fix through a red-green-refactor loop."
---

# TDD Loop

Use a disciplined red-green-refactor cycle instead of coding by hope.

## Workflow

Use the active initiative artifacts and repository test conventions before adding or changing code.

1. Capture the behavior in a test or executable repro first.
2. Run the test to prove it fails for the expected reason.
3. Implement the smallest change that makes the test pass.
4. Refactor only while keeping the behavior protected by tests.
5. Record any remaining coverage gap in `test-strategy.md` or the task notes.

## Output format

### failing proof
### minimal fix
### passing proof
### remaining risks

## Rules

- do not skip the failing proof unless the repo genuinely cannot express one yet
- prefer the narrowest test layer that still protects the behavior
- if you must defer a test, explain why and what temporary evidence replaces it
