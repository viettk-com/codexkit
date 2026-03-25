---
name: release-readiness
description: "use before a release, merge train, or deployment freeze to check changelog, migrations, rollback notes, docs impact, and known risks. do not use for tiny local-only changes."
---

# Release Readiness

Assess whether the current repository state is safe to ship.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Read the current diff, release notes, migration artifacts, and runbooks.
2. Check must-fix ship blockers, docs drift, operator notes, and rollback clarity.
3. Call out anything that still depends on tribal knowledge.
4. Produce a concise go/no-go style summary.
5. Stop after a release owner could make a decision from the note.

## Output format

### summary
### must-fix before ship
### nice-to-have
### rollback notes
### docs or comms updates

## Rules

- treat unclear rollback as a blocker for risky changes
- do not fake certainty when evidence is missing
