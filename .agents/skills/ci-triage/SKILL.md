---
name: ci-triage
description: "use when ci is red, flaky, or noisy and you need a root-cause-oriented read of logs, failing jobs, or pre-merge checks."
---

# CI Triage

Find the first real failure in CI and recommend the next small confirmation step.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Read the failing job from the first meaningful error upward.
2. Classify the failure: code, tests, environment, infra, flaky, or policy.
3. Separate root cause from secondary failures.
4. Suggest the smallest local or branch-level command to confirm the diagnosis.
5. Stop after the recovery path is clear.

## Output format

### summary
### failure class
### root cause hypothesis
### next command
### follow-up checks

## Rules

- do not recommend blind reruns first
- be explicit when the failure is probably environment-only
