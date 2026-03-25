---
name: docs-sync
description: "use after code changes when behavior, architecture, setup, release notes, migrations, or operational guidance may now be stale. do not use for pure internal refactors with no durable context impact."
---

# Docs Sync

Update only the durable docs affected by the current change.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Compare the current diff against architecture, setup, release, and operational docs.
2. Update only the docs the change actually makes stale.
3. Keep rollout, rollback, and migration notes aligned with code behavior.
4. Mention docs you intentionally did not touch and why.
5. Stop after the repo's durable context matches reality again.

## Output format

### summary
### docs changed
### docs intentionally untouched
### remaining docs debt

## Rules

- avoid doc sprawl
- prefer short, durable explanations over changelog fiction
