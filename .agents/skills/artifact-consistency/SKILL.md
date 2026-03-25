---
name: artifact-consistency
description: "use after spec, architecture, nfr, plan, tasks, or test strategy artifacts exist and before implementation or merge, especially for l1+ changes where cross-artifact drift could cause rework or architecture breakage."
---

# Artifact Consistency

Check whether the planning artifacts still agree with each other and with the repository context.

## Workflow

Use `docs/project-context/index.md`, `docs/project-context/08-project-constitution.md`, and the active initiative directory as the primary sources.

1. Read `spec.md`, `analysis.md`, `architecture.md`, `nfr.md`, `plan.md`, `tasks.md`, and `test-strategy.md`.
2. Check whether goals, constraints, interfaces, validation commands, and rollout assumptions stay consistent across those files.
3. Write or update `consistency-report.md` with the coverage, mismatches, and blockers.
4. Route gaps to the right follow-up skill, such as `$architecture-review`, `$nfr-capture`, `$test-strategy`, or `$implementation-readiness`.
5. Stop before coding if material contradictions remain.

## Output format

### artifact coverage
### mismatches
### blockers before implementation
### ready or not ready

## Rules

- treat missing rollback, observability, or contract notes as real drift, not cosmetic debt
- prefer explicit contradictions over vague comfort language
- do not mark the change ready when the artifacts only look complete on the surface
