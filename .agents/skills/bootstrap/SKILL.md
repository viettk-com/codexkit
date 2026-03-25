---
name: bootstrap
description: "use when codexkit is first added to a repository, when starting a new project in this repo, when the codebase is unfamiliar, when project context docs are missing or stale, or when you explicitly ask to bootstrap. deeply scan the repo, generate durable project memory, and update codexkit guidance so later plans and tasks preserve the current architecture."
---

# Bootstrap

Create or refresh a durable repository understanding before major planning or implementation.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Determine whether the repository is effectively greenfield, brownfield, or a mixed state.
2. Run `python3 scripts/bootstrap-codexkit.py --apply` from the repo root. This now refreshes the extended project context too.
3. Read `docs/project-context/index.md`, `08-project-constitution.md`, `13-agent-context.md`, and `14-continuity.md` before doing deeper planning.
4. If architecture signals are incomplete or contradictory, use `system_mapper`, `chief_architect`, `domain_modeler`, and `reliability_engineer` to refine the generated context.
5. If the repo is greenfield or greenfield-like, continue with `$project-bootstrap`; if it is brownfield, continue with `$brownfield-mapping` and `$architecture-discovery`.
6. Validate the bootstrap outputs with `python3 scripts/validate-bootstrap.py` and then continue with planning.

## Output format

### bootstrap summary
### repo profile
### architecture guardrails
### constitution and continuity updates
### validation commands
### protected zones
### unresolved questions

## Rules

- prefer managed blocks and additive edits over destructive rewrites
- separate durable facts from assumptions and mark low-confidence guesses clearly
- do not claim the repo is understood until the generated context docs are read back and sanity-checked
- if bootstrap surfaces auth, billing, migrations, infra, or public-contract risk, route later work through the matching review skills before implementation
