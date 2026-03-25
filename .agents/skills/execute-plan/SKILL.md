---
name: execute-plan
description: "use when architecture, spec, plan, and tasks already exist and the next job is to implement one milestone or one tightly scoped slice with small diffs and explicit validation."
---

# Execute Plan

Implement one approved slice only.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Confirm the current slice in `tasks.md` or `plan.md`.
2. Read the closest relevant code, tests, and architecture constraints first.
3. Implement only the current slice, keeping the diff narrow and reversible.
4. Run focused validation before broader checks.
5. Stop and summarize once the slice is implemented and validated.

## Output format

### slice summary
### files changed
### validation run
### remaining risks
### next slice

## Rules

- do not absorb adjacent work just because you found it
- if architecture or plan gaps appear, stop and refresh the artifacts first
- do not mark the slice done without real validation evidence
