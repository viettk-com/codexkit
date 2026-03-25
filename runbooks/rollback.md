# Rollback runbook

- define the fastest safe rollback path before shipping
- know which changes are code-only vs schema or data-shape changes
- prefer feature flags or staged cutovers when available
- record any data cleanup or replay required after rollback
