# Brownfield playbook

Use this when the repository is large, under-documented, or already carries historical complexity.

## Recommended sequence

1. `$bootstrap`
2. `$brownfield-mapping`
3. `system_mapper` subagent
4. `$architecture-discovery`
5. `$nfr-capture`
6. `$architecture-review`
7. `$plan-feature`

## What to capture

- entrypoints and critical workflows
- subsystem boundaries and shared utilities
- data ownership and cross-module coupling
- known flaky areas or operational hotspots
- likely blast radius of the intended change

## Practical rules

- prefer extending stable seams over refactoring the world
- surface hidden coupling early
- if the change reveals a structural problem, document it separately instead of smuggling a rewrite into the feature
- treat migrations, queues, caches, and search indexes as architecture, not implementation detail
