---
name: incident-response
description: "use when production symptoms, alerts, or support escalations suggest an active incident and you need a concise triage note, mitigation-first plan, and follow-up checklist."
---

# Incident Response

Triage incidents with mitigation first and diagnosis second.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Capture severity, user impact, blast radius, and the fastest safe mitigation.
2. Prefer reversible mitigations and narrow rollback over speculative fixes.
3. Write or update `incident.md` or a report under `plans/active/.../reports/`.
4. Separate immediate actions from follow-up diagnostics.
5. Stop after the on-call engineer has a clear next move.

## Output format

### summary
### severity
### mitigation
### blast radius
### follow-up diagnostics

## Rules

- mitigation beats perfect diagnosis during active impact
- be explicit when human approval is needed
