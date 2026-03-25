---
name: architecture-discovery
description: "use when starting a new feature or subsystem and you must understand module boundaries, interfaces, dependencies, and architectural constraints before writing a plan."
---

# Architecture Discovery

Discover the architecture that already exists and the constraints a safe change must respect.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Map the touched layers, modules, or services.
2. Identify current interface contracts, state transitions, and dependency directions.
3. Capture architectural constraints, anti-patterns, and existing extension points.
4. Update or draft `architecture.md` with current-state notes and boundary assumptions.
5. Hand the findings to the architecture review or planning step.

## Output format

### summary
### boundaries
### interfaces
### constraints
### change risk

## Rules

- do not propose broad refactors without evidence
- if boundaries are already unclear, say so explicitly
