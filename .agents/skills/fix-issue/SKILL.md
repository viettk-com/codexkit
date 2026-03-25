---
name: fix-issue
description: "use when the user reports a bug and can provide reproduction steps, logs, or symptoms. best for root-cause-first debugging with a minimal fix and regression validation."
---

# Fix Issue

Diagnose a bug, localize the cause, and apply the smallest safe fix.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Turn the bug report into deterministic reproduction steps.
2. Read the likely fault area and surrounding tests before editing.
3. Identify the root cause or the most likely fault boundary.
4. Apply the smallest useful fix and add regression validation where appropriate.
5. Summarize the cause, fix, and validation evidence.

## Output format

### bug summary
### root cause
### fix path
### validation
### follow-up risk

## Rules

- avoid speculative rewrites
- if the bug is really a design or architecture issue, say so and point back to planning
