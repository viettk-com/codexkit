# Observability and operations

If a change matters in production, people must be able to see and operate it.

## Minimum bar for important changes

- logs for key state transitions or failures
- metrics for throughput, latency, and error rate
- traces for distributed or multi-step flows
- alerts for user-visible impact or data-loss risk
- a short runbook note for mitigation and rollback

## Useful artifacts

- `observability.md`
- `rollout.md`
- `runbook.md`
- `incident.md`

## Anti-patterns

- dashboards with no actionability
- alerts with no owner or no threshold rationale
- release notes that omit rollback conditions
- migrations with no verification query
