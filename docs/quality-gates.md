# Quality gates

Use these gates in order. Skip only with an explicit reason.

| Gate | Question | Artifact or evidence |
|---|---|---|
| 0. Request quality | Is the goal, context, constraints, and done-when clear enough? | prompt contract |
| 1. Scope quality | Is the change class correct and proportional? | `spec.md` or task note |
| 2. Architecture quality | Do we understand boundaries, contracts, risks, and NFRs? | `architecture.md`, `nfr.md` |
| 3. Decision quality | Was the target design chosen deliberately? | `decision-matrix.md`, ADRs |
| 4. Plan quality | Are milestones safe, reversible, and validated? | `plan.md` |
| 5. Task quality | Are slices small and reviewable? | `tasks.md` |
| 6. Implementation quality | Is the diff the smallest useful change? | diff + summary |
| 7. Validation quality | Did the most relevant checks actually run? | commands + outputs |
| 8. Review quality | Did an owner-style review happen? | `/review` or `$review-owner` |
| 9. Release quality | Are rollout, rollback, docs, and ops notes clear? | `rollout.md`, release note, docs |

## Gate escalations

Treat these as automatic “slow down” signals:

- auth or permission model changes
- schema or contract changes
- cross-service or cross-module coupling
- performance-sensitive hot paths
- infra, workflow, or secret handling changes
- anything that lacks rollback clarity
