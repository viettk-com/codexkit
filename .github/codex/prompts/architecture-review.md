Use the `$architecture-review`, `$migration-guard`, `$observability-review`, and `$review-owner` skill logic where relevant.

Review the current pull request or branch for architecture readiness.

Check:
- is the change class plausible?
- are the required artifacts present for the implied change class?
- does the diff stay inside believable module or service boundaries?
- are contracts, migrations, rollout, rollback, and observability handled?
- is the design proportionate, or is it introducing accidental complexity?

Output format:
# Architecture gate
## Must-fix before merge
## Architecture concerns
## Missing artifacts
## Rollout or migration concerns
## No-op confirmation
