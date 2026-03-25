---
name: test-strategy
description: "use when a change needs an explicit validation plan across unit, integration, contract, performance, or rollout checks before or during implementation."
---

# Test Strategy

Define what to verify, where to verify it, and how much confidence is enough for this change.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Draft or update `test-strategy.md` for the initiative.
2. Identify the smallest meaningful checks first, then broader confidence layers.
3. Separate deterministic tests, manual verification, load/performance checks, and rollout checks.
4. Call out gaps that cannot be closed cheaply right now.
5. Feed the strategy back into `plan.md` and `tasks.md`.

## Output format

### summary
### test layers
### commands
### manual checks
### known validation gaps

## Rules

- do not confuse quantity of tests with confidence
- prefer stable, targeted checks over noisy suites
