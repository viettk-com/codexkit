---
name: api-contract-review
description: "use when the change touches public or cross-module contracts such as request or response shapes, events, schemas, queues, or sdk behavior."
---

# API Contract Review

Inspect contract changes for compatibility and clarity.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Identify the public and internal contracts affected by the change.
2. Review backwards compatibility, versioning, validation, and error behavior.
3. Document compatibility notes in `interfaces.md`, ADRs, or rollout notes.
4. Recommend contract tests or consumer verification when appropriate.
5. Stop after the compatibility story is explicit.

## Output format

### summary
### contracts touched
### compatibility notes
### required tests
### rollout implications

## Rules

- do not change a contract silently
- prefer additive evolution before breaking changes
