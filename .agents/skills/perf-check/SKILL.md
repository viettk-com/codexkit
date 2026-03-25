---
name: perf-check
description: "use when the change may affect hot paths, database queries, rendering, caching, concurrency, throughput, or large data volume behavior."
---

# Performance Check

Assess performance and scale risk for the proposed or completed change.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Identify the hot paths or large-volume paths touched by the change.
2. Compare the design against latency, throughput, and cost budgets from `nfr.md` or `perf-budget.md`.
3. Recommend the smallest measurements or benchmarks needed for confidence.
4. Call out caching, batching, pagination, or indexing implications.
5. Stop after performance risk is explicit and proportionate to the feature size.

## Output format

### summary
### hot paths
### risk level
### measurements to run
### optimization ideas

## Rules

- do not optimize cold code without evidence
- if load assumptions are missing, say that clearly
