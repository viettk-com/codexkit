Use the `$release-readiness`, `$migration-guard`, and `$observability-review` skill logic even if you do not invoke them explicitly.

Assess whether the current repository state is ready to ship.

Review:
- changelog or release note impact
- migrations or data changes
- rollback requirements
- operational or runbook impact
- observability or alerting blind spots
- missing docs or release communication

Output format:
# Release readiness
## Must-fix before ship
## Nice-to-have before ship
## Rollback notes
## Docs / comms updates
