# Continuity memory

This kit uses a four-layer memory model inspired by production AI workflows.

## Memory tiers

### Working memory
Temporary context for the current slice of work.

Primary locations:
- `plans/active/<initiative>/`
- the current branch or worktree
- the current PR or issue thread

### Episodic memory
Records of completed efforts, incidents, or migrations.

Primary locations:
- `plans/archive/`
- initiative `report.md`
- `lessons-learned.md`

### Semantic memory
Durable project knowledge that future work should reuse.

Primary locations:
- `docs/project-context/`
- runbooks
- architecture notes and ADRs

### Deep-search memory
Machine-readable indices that make the repo searchable without rediscovering everything manually.

Primary locations:
- `.codex/project-context/profile.json`
- `.codex/project-context/module-index.json`
- `.codex/project-context/rules.json`
- `.codex/project-context/dashboard.json`

## How to keep continuity healthy

- refresh context after structural repo changes
- archive initiatives when they finish
- convert painful surprises into reusable lessons
- keep the dashboard honest about active work and open risks
