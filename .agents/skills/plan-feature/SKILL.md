---
name: plan-feature
description: "use when the task is ambiguous, risky, cross-cutting, or larger than a small one-file edit. best for turning a spec or request into a phased technical plan with validation, rollout, rollback, and docs impact."
---

# Plan Feature

Turn a request, spec, or architecture review into a phased implementation plan.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Restate the task in the four-part contract: goal, context, constraints, done when.
2. Read the nearest relevant files, docs, tests, and architecture artifacts first.
3. Identify touched interfaces, data changes, rollout and rollback risk, observability, and docs impact.
4. Write or update `plan.md` using the template and reference `architecture.md` and `nfr.md` where relevant.
5. Stop after planning unless the user explicitly asks to implement.

## Output format

### summary
### milestones
### validation commands
### risks
### rollback notes
### docs to update

## Rules

- do not propose a big-bang rewrite unless the user asked for one
- prefer milestones that can be reviewed independently
- include exact validation commands per milestone
