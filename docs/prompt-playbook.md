# Prompt playbook

## Greenfield shaping

```text
$project-bootstrap
Goal: create the first production-ready architecture for a billing platform.
Constraints: small team, strict auditability, no premature microservices, clear rollback model.
Done when: architecture, NFRs, first milestones, and runbook expectations are documented.
```

## Brownfield feature shaping

```text
$brownfield-mapping
Goal: add tenant-aware rate limits.
Context: @src/api @src/middleware @docs/architecture.md
Constraints: keep public API stable, no unsafe Redis migration.
Done when: current-state map, blast radius, and hotspots are captured.
```

## Architecture review

```text
$architecture-review
Use the current architecture notes and NFRs.
Compare at least two realistic options.
Recommend the simplest design that satisfies the budgets and operational model.
```

## Planning

```text
$plan-feature
Turn the approved architecture into milestones.
Each milestone must include exact validation commands and rollback notes.
```

## Implementation

```text
$execute-plan
Implement Milestone 1 only.
Keep the diff narrow.
Do not absorb adjacent refactors.
```

## Performance pass

```text
$perf-check
Assess the current change against latency, throughput, and cost expectations.
Tell me what to measure, not just what to fear.
```

## Release pass

```text
$release-readiness
Assess whether the branch is safe to ship.
Call out must-fix blockers, docs gaps, rollback gaps, and observability blind spots.
```
