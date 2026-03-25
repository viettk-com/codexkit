---
name: continuity-memory
description: "use when resuming work in a repository, switching between initiatives, or after incidents, reviews, or migrations so codex can recover project memory and avoid repeating past mistakes."
---

# Continuity Memory

Recover the repository's durable memory before taking action.

## Workflow

Use `docs/project-context/14-continuity.md`, `docs/project-context/dashboard.md`, and `plans/archive/` as the starting point.

1. Read the active initiative summaries, recent archived work, and reusable lessons.
2. Identify what this task must preserve from previous decisions, incidents, or migration notes.
3. Write back any new durable lesson, recurring pitfall, or important unresolved risk to `docs/project-context/14-continuity.md`.
4. If the repo context looks stale, refresh it with `$bootstrap`.
5. Stop after the current task is anchored in the existing project memory.

## Output format

### relevant prior context
### reusable lessons
### current continuity risks
### memory updates made

## Rules

- store only durable lessons, not noisy chat summaries
- prefer concrete guidance like file paths, commands, and invariants
- when unsure whether a lesson is durable, record it as a question instead of a rule
