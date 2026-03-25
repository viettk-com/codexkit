---
name: pr-prep
description: "use when implementation is done and you need a clean pull request or merge request summary with risks, validation, rollout notes, and reviewer guidance."
---

# PR Prep

Prepare a reviewer-friendly handoff note for the current change.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Summarize what changed and why.
2. List validation run, remaining risk, rollout notes, and rollback notes.
3. Link relevant plan, architecture, ADR, or migration artifacts.
4. Call out reviewer hotspots and known limitations.
5. Stop after the summary is ready to paste into a PR.

## Output format

### summary
### validation
### risk
### rollout and rollback
### reviewer hotspots

## Rules

- do not oversell the change
- include limitations and follow-ups honestly
