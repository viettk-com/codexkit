---
name: systematic-debugging
description: "use when the root cause is unclear, symptoms are noisy, tests are flaky, or a production issue needs a disciplined hypothesis-and-evidence workflow before changing code."
---

# Systematic Debugging

Debug by narrowing the search space with evidence instead of guesswork.

## Workflow

Use logs, repro steps, failing tests, screenshots, and relevant project-context docs as evidence.

1. Write down the symptom, expected behavior, and best current repro.
2. Build a short hypothesis list ordered by likelihood and blast radius.
3. Gather evidence that eliminates whole classes of causes quickly.
4. Change one variable at a time until the root cause is isolated.
5. Add a regression guard, then document what actually caused the issue.

## Output format

### symptom
### hypotheses
### evidence
### root cause
### durable fix and guard

## Rules

- separate observed facts from hypotheses clearly
- avoid stacking speculative fixes in one diff
- if the issue is still not isolated, say what evidence is missing before making broader changes
