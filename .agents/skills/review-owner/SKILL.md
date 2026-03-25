---
name: review-owner
description: "use when you want an owner-style review of the working tree, a proposed diff, or a milestone implementation. best for correctness, regression, security, and missing test review."
---

# Review Owner

Review the current change like a responsible code owner.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Read the current diff and the most relevant surrounding code.
2. Check correctness, regression risk, security, test coverage, maintainability, and docs impact.
3. Use `docs/code-review.md` as the default rubric.
4. Summarize material issues first and keep style-only comments secondary.
5. Stop after the review is specific enough for an engineer to act on.

## Output format

### summary
### blockers
### high-risk findings
### validation gaps
### optional suggestions

## Rules

- lead with evidence, not style
- say clearly when no material issues are found
