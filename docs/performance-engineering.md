# Performance engineering

This kit treats performance as a design concern, not a late-stage panic.

## Rules of thumb

- measure hot paths before optimizing them
- prefer simple wins: batching, indexing, pagination, caching, less work
- connect every optimization to a budget or expected load
- watch for N+1 patterns, cross-service fan-out, and lock contention
- performance changes without rollback notes are still risky changes

## Useful artifacts

- `nfr.md`
- `perf-budget.md`
- `architecture.md`
- `plan.md`
- `observability.md`

## Questions for the performance pass

- what is the expected traffic or batch size?
- what are the latency and throughput budgets?
- which path is user-facing or revenue-critical?
- what query or network patterns could fan out?
- what evidence will tell us the change is safe?
