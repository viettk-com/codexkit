---
name: task-breakdown
description: "use after a technical plan exists and you need to convert milestones into ordered, reviewable implementation tasks with dependencies, validation, and ownership hints."
---

# Task Breakdown

Break a good plan into reviewable slices.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Read the current `plan.md` and relevant architecture notes first.
2. Convert milestones into ordered tasks that can each produce one reviewable diff or one clear validation step.
3. Mark dependencies, owner hints, and validation commands.
4. Write or update `tasks.md` using the template.
5. Stop after the tasks are scoped well enough for implementation.

## Output format

### summary
### task path
### ordered tasks
### dependencies
### validation checkpoints

## Rules

- do not add new scope not present in the spec, architecture, or plan
- prefer vertical slices over layer-by-layer churn when feasible
