---
name: architecture-decision
description: "use when a change needs an explicit architectural decision record, trade-off note, or rationale summary so future agents and reviewers can understand why the team chose this path."
---

# Architecture Decision

Write or update an ADR when a design choice should become durable context.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Identify the architectural question being decided.
2. Capture context, options considered, decision, trade-offs, and consequences.
3. Write or update an ADR using `plans/templates/adr.md` or the repo ADR format.
4. Link the ADR from the plan, rollout notes, or architecture doc.
5. Stop after the decision and its consequences are clear.

## Output format

### decision summary
### adr path
### trade-offs
### follow-up implications

## Rules

- do not write an ADR for every tiny refactor
- be explicit about rejected options and why they lost
