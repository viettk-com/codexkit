---
name: constitution-governance
description: "use when a new repository, subsystem, or major feature needs explicit engineering principles, architecture invariants, or change governance before planning and implementation start."
---

# Constitution Governance

Create or refresh the project constitution that all later plans and reviews must obey.

## Workflow

Use `docs/project-context/08-project-constitution.md`, `docs/project-context/13-agent-context.md`, and `docs/project-context/14-continuity.md` as the default context when they exist.

1. Read the repo profile, current architecture map, and continuity memory first.
2. Capture the durable principles that should survive across features, not just the needs of one ticket.
3. Write or update `docs/project-context/08-project-constitution.md` with architecture invariants, quality gates, review triggers, and forbidden shortcuts.
4. Reflect the constitution in the active initiative artifacts when it changes the plan, test strategy, rollout, or review gates.
5. Stop after the constitution is explicit enough that future agents can follow it without re-deriving core rules.

## Output format

### decision summary
### proposed principles
### review triggers
### required follow-up updates

## Rules

- prefer a small number of strong principles over a long policy dump
- encode durable architecture and delivery rules, not personal preferences
- call out which principles are facts from the repo and which are inferred defaults
