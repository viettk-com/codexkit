# Spec-driven development

This kit uses a strict but lightweight chain:

1. `spec.md` captures the product-facing problem and acceptance criteria
2. `architecture.md` and `nfr.md` capture design and quality constraints
3. `plan.md` turns that into technical milestones, validation, rollout, and rollback
4. `tasks.md` breaks milestones into reviewable units of work
5. implementation happens one slice at a time
6. `/review`, `$docs-sync`, and `$release-readiness` close the loop

## Why this matters

Spec-driven work lowers the chance that Codex runs ahead with the wrong scope.
Adding architecture and NFR artifacts lowers the chance that correct-looking code still violates boundaries, scale assumptions, or operational needs.

## Recommended folder structure

```text
plans/active/<date>-<slug>/
├── spec.md
├── architecture.md
├── nfr.md
├── plan.md
├── tasks.md
├── phases/
├── reports/
├── research/
└── artifacts/
```

## Anti-patterns

- skipping from vague request to large implementation
- planning with no architecture or NFR artifact for risky work
- claiming a milestone is done without validation evidence
- silently changing contracts or data shapes
