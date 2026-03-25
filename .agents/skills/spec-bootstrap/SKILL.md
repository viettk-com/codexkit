---
name: spec-bootstrap
description: "use when starting new work from a fuzzy request and you need to create or refresh product-facing spec artifacts before technical planning."
---

# Spec Bootstrap

Create or refresh the product-facing spec before technical planning.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Locate or create an initiative folder under `plans/active/` using `scripts/new-feature.sh` or `scripts/new-initiative.sh` when needed.
2. Fill or update `spec.md` from the template.
3. Capture problem statement, scope, non-goals, users, acceptance criteria, risks, and open questions.
4. If the change is architecture-sensitive, link to `architecture.md` and `nfr.md` rather than embedding all design detail here.
5. Stop after the spec is coherent enough for architecture review or technical planning.

## Output format

### summary
### spec path
### acceptance criteria
### assumptions
### open questions

## Rules

- do not jump into implementation
- prefer crisp acceptance criteria over feature wishlists
- explicitly list non-goals so scope stays stable
