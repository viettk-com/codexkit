# Bootstrap playbook

Use bootstrap when CodexKit first lands in a repo, when the repo has changed materially, or when you do not trust the current project context.

## Recommended sequence

1. Run `python3 scripts/bootstrap-codexkit.py --apply`
2. Read `docs/project-context/index.md`, `08-project-constitution.md`, `13-agent-context.md`, and `14-continuity.md`
3. Review `docs/project-context/07-bootstrap-report.md` for low-confidence guesses
4. If needed, refine with:
   - `bootstrap_curator`
   - `system_mapper`
   - `chief_architect`
   - `domain_modeler`
5. Continue with `$project-bootstrap` or `$brownfield-mapping`

## What bootstrap updates

- `.codex/project-context/profile.json`
- `docs/project-context/*.md`
- the managed bootstrap block inside `AGENTS.md`
- the repo-specific defaults later used by plans, tasks, and reviews

## Safe editing model

Bootstrap overwrites only generated project-context files and the managed block in `AGENTS.md`.
Manual notes outside the managed block stay untouched.

## Refresh triggers

Re-run bootstrap after:

- adding or splitting services
- changing package managers or build systems
- major migrations
- large architecture decisions or directory reshapes
- onboarding a new team into the repo
