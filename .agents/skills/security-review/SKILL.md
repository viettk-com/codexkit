---
name: security-review
description: "use when the change touches auth, permissions, secrets, external input, file access, templates, redirects, database queries, shell calls, or any trust boundary."
---

# Security Review

Inspect the change for practical security risk.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Find every trust boundary the change touches.
2. Check authorization, secret handling, validation, escaping, query construction, and external calls.
3. Call out exploitability, blast radius, and required mitigations.
4. Recommend concrete hardening steps and focused tests.
5. Stop after the risk is understandable and actionable.

## Output format

### summary
### trust boundaries
### findings
### required mitigations
### test ideas

## Rules

- focus on realistic abuse paths
- avoid generic security theater
