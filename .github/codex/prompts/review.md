Use the `$review-owner`, `$security-review`, and `$perf-check` skill logic where relevant.

Review this pull request like a strict code owner.

Use the repository guidance in `AGENTS.md`, the rubric in `docs/code-review.md`, and any linked architecture artifacts.

Focus on:
- correctness and regression risk
- security and secrets handling
- missing tests or weak validation
- architecture drift or boundary violations
- migration, rollout, or observability gaps
- docs gaps if behavior changed

Instructions:
- lead with material issues only
- cite files and symbols when possible
- avoid style-only comments unless they hide a real bug
- if there are no material issues, say so clearly
- keep the output short enough to post as a PR comment
