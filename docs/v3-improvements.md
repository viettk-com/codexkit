# v3 improvements

## Major additions

- new `$bootstrap` skill for deep repository understanding and CodexKit adaptation
- `bootstrap_curator` subagent for repo scan, memory refresh, and managed updates
- deterministic `scripts/bootstrap-codexkit.py` scanner
- machine-readable project profile at `.codex/project-context/profile.json`
- human-readable project memory under `docs/project-context/`
- bootstrap validator and wrapper script
- plan templates now expect repo context sources

## Why this matters

v2 already enforced architecture-first work, but it still assumed humans would manually tailor repo context.
v3 closes that gap by making context creation a first-class workflow.
