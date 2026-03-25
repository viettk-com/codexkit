---
name: brownfield-mapping
description: "use when the repository already exists and you must map current architecture, hotspots, ownership boundaries, and change risk before planning a new feature or refactor."
---

# Brownfield Mapping

Map the current system before proposing meaningful changes.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Read the nearest architecture, onboarding, and operational docs first.
2. Identify entrypoints, major modules, shared libraries, data stores, and external integrations.
3. Capture hotspots, hidden coupling, and likely blast radius for the proposed work.
4. Write a concise current-state memo into `research/` or `architecture.md`.
5. Stop after the current system is understandable enough for architecture review or planning.

## Output format

### summary
### current-state map
### hotspots
### likely blast radius
### unknowns

## Rules

- do not redesign the system yet
- prefer repo evidence over memory or guesswork
- name unstable seams and accidental complexity clearly
