# Implementation readiness

Implementation readiness is the gate between planning and code.

## A change is ready only when

- the change class still matches the real scope
- planning artifacts agree with each other
- validation commands are explicit
- rollback notes exist for risky changes
- observability expectations are defined for important paths
- specialist reviews are identified when needed
- the first slice can be implemented safely without architecture guesswork

## Suggested workflow

1. `$artifact-consistency`
2. `$implementation-readiness`
3. `$execute-plan` or `$fix-issue`

## Common false positives

A plan is **not** ready just because:
- there is a long `plan.md`
- tasks exist but ignore rollout or validation
- architecture diagrams exist but boundaries are still fuzzy
- test strategy says "add tests" without exact commands or layers
