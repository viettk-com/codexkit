---
name: migration-guard
description: "use when a change touches schemas, contracts, queues, caches, search indexes, or data backfills and you need staged rollout and rollback discipline before merge or deploy."
---

# Migration Guard

Enforce migration discipline for data and contract changes.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Review all schema, contract, index, cache, or data-shape changes.
2. Document expand-and-contract, dual-read/write, backfill, cutover, and rollback steps.
3. Require verification queries or health checks.
4. Link the migration plan into `plan.md`, `rollout.md`, or `runbook.md`.
5. Stop after the migration is boring enough for a cautious release owner.

## Output format

### summary
### change type
### compatibility plan
### verification
### rollback

## Rules

- avoid big-bang cutovers
- treat unverified backfills as unfinished work
