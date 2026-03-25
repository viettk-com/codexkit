---
name: architecture-review
description: "use when a new feature, subsystem, or refactor needs an explicit target architecture, option matrix, and trade-off review before coding begins."
---

# Architecture Review

Review design options and choose a target architecture deliberately.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Compare at least two realistic options in `decision-matrix.md` when the choice is meaningful.
2. Document the recommended target architecture in `architecture.md`.
3. Call out module boundaries, data ownership, interface contracts, migration strategy, and operational model.
4. Create or update an ADR when the decision should become durable team context.
5. Stop after the chosen path is defensible and planning can begin.

## Output format

### decision summary
### recommended option
### trade-offs
### required ADRs
### follow-up work

## Rules

- prefer boring architecture that future teammates can operate
- do not choose distributed complexity unless scale, ownership, or isolation truly require it
- if no option is clearly superior, say what evidence is still missing
