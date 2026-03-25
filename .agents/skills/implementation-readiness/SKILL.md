---
name: implementation-readiness
description: "use after planning and before coding on l1+ work to verify that the artifacts, approvals, tests, rollback plan, observability, and review triggers are strong enough for safe execution."
---

# Implementation Readiness

Decide whether a change is genuinely ready to implement.

## Workflow

Use the active initiative directory, `docs/project-context/08-project-constitution.md`, and `docs/project-context/13-agent-context.md`.

1. Read the planning artifacts and confirm the change class still matches the real scope.
2. Check that validation commands, rollback notes, observability expectations, and protected zones are explicit.
3. Verify that any required specialized reviews have been called out, such as security, migration, performance, or UX.
4. Write or update `consistency-report.md` with the final readiness verdict.
5. Stop if the work is still architecture-ambiguous, under-tested, or operationally unsafe.

## Output format

### readiness verdict
### missing prerequisites
### required specialist reviews
### safe first slice

## Rules

- readiness means the first implementation slice is safe, not that the whole project is solved
- treat missing rollback and observability notes as blocking for risky changes
- prefer delaying code over accelerating uncertainty into the codebase
