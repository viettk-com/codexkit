# Source patterns adopted in this kit

This file documents the strongest patterns borrowed and adapted from external repositories.

## Workflow discipline

Borrowed pattern:
- treat brainstorming, planning, implementation, review, and closeout as separate phases

Adaptation in this kit:
- architecture-first workflow in `AGENTS.md`
- skills for planning, readiness, debugging, and closeout
- active initiative artifacts under `plans/active/`

## Spec-driven delivery

Borrowed pattern:
- constitution + spec + plan + tasks + implementation as separate durable artifacts

Adaptation in this kit:
- `analysis.md`, `spec.md`, `architecture.md`, `nfr.md`, `plan.md`, `tasks.md`, `consistency-report.md`
- stronger validation in `scripts/validate-plans.py`

## Continuity and lifecycle coverage

Borrowed pattern:
- memory should survive across sessions and across initiatives

Adaptation in this kit:
- `docs/project-context/14-continuity.md`
- closeout script with lessons learned
- dashboard and machine-readable rules files

## UI and design intelligence

Borrowed pattern:
- UI work improves when the agent consults design-system knowledge, not generic frontend advice

Adaptation in this kit:
- `design-system-forensics` skill
- generated design-system context doc

## Thin command wrappers

Borrowed pattern:
- short command namespaces make good workflows easier to remember and easier to trigger consistently

Adaptation in this kit:
- `/ck:` chat aliases and `$ck-` skill aliases resolve through `command-router`
- `.codex/command-aliases.json` keeps aliases as a thin layer over existing skills, scripts, agents, and artifacts
- generated quick prompt wrappers live under `.github/codex/prompts/ck-*.md`
