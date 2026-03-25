---
name: nfr-capture
description: "use when a feature or project needs measurable non-functional requirements for performance, reliability, security, compliance, cost, or operability before planning implementation."
---

# NFR Capture

Turn vague quality expectations into measurable non-functional requirements.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Create or update `nfr.md` from the template.
2. Capture traffic expectations, latency budgets, throughput, batch volume, and concurrency assumptions.
3. Define availability, recovery, observability, privacy, and compliance requirements.
4. Record cost constraints and explicit trade-offs when all goals cannot be optimized at once.
5. Feed the resulting budgets and constraints back into architecture and planning artifacts.

## Output format

### summary
### nfr path
### budgets
### gating requirements
### open risks

## Rules

- avoid generic words like scalable, secure, or reliable without numbers or concrete conditions
- if the business has not chosen a target yet, provide a range and state the assumption
