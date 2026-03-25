---
name: observability-review
description: "use when a change affects critical workflows, background jobs, migrations, or user-facing paths and you need explicit logs, metrics, traces, alerts, and runbook notes."
---

# Observability Review

Make the change observable and operable before it ships.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Review what signals will prove the change is healthy in production.
2. Update `observability.md` or rollout notes with logs, metrics, traces, dashboards, and alerts.
3. Capture which failures should page, warn, or simply log.
4. Link any required runbook changes.
5. Stop after operators will be able to see and debug the change.

## Output format

### summary
### signals to add
### alerts
### runbook impact
### blind spots

## Rules

- do not ship important behavior with no visibility
- prefer actionable signals over noisy dashboards
