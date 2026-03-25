---
name: project-bootstrap
description: "use when starting a new project, product area, or major subsystem and you need architecture, non-functional requirements, and delivery artifacts before any code is written."
---

# Project Bootstrap

Bootstrap a greenfield or greenfield-like initiative with explicit architecture and delivery artifacts.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Create or refresh an initiative folder with `scripts/new-project.sh` or `scripts/new-initiative.sh L3 ...`.
2. Write `spec.md`, `architecture.md`, and `nfr.md` before discussing implementation details.
3. Choose the simplest viable architecture style: single service, modular monolith, or multiple deployables only when justified.
4. Record a decision matrix, ADR seed, observability expectations, and a first release/rollback model.
5. Stop after the project is shaped well enough for technical planning.

## Output format

### summary
### initiative path
### target architecture
### critical risks
### open questions

## Rules

- do not jump straight to framework boilerplate or code generation
- prefer clear module boundaries and ownership over shiny patterns
- if scale or compliance assumptions are weak, mark them explicitly
