---
name: closeout-learning
description: "use when a milestone, branch, or initiative is finishing and codex should archive the work, capture lessons learned, refresh project context, and leave the repository in a maintainable state."
---

# Closeout Learning

Close work deliberately so the next agent inherits more than a diff.

## Workflow

Use the active initiative directory, `docs/project-context/dashboard.md`, and `docs/project-context/14-continuity.md` as the base context.

1. Confirm what changed, what was verified, and what remains risky.
2. Write or update `report.md` and `lessons-learned.md` for the initiative.
3. Run `python3 scripts/close-initiative.py` when the initiative should move from active to archive.
4. Refresh the project context so dashboards, continuity memory, and module guidance stay current.
5. Stop only after future agents can understand the outcome without re-reading the whole branch history.

## Output format

### completion summary
### validation evidence
### lessons learned
### follow-up actions
### archive status

## Rules

- never archive work without leaving reusable lessons when the task exposed hidden risk
- keep lessons action-oriented and architecture-aware
- if the change is not truly finished, say what still blocks closeout
