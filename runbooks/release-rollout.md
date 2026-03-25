# Release rollout runbook

## Before rollout

- confirm release note and known risk summary
- verify migrations and rollback notes
- verify dashboards and alerts exist
- confirm who owns the rollout

## During rollout

- watch latency, error rate, and key business metrics
- verify health checks and migration queries
- pause if unknown errors spike or data diverges

## Rollback triggers

- user-visible regression with no fast mitigation
- migration verification fails
- alert storm without clear containment
