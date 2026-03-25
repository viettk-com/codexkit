# New project playbook

Use this when the work is effectively greenfield or a major new subsystem.

## Commands

```bash
scripts/new-project.sh <slug>
```

Recommended prompts:

```text
$bootstrap
$continuity-memory
$constitution-governance
$project-bootstrap
$architecture-review
$architecture-decision
$plan-feature
$artifact-consistency
$implementation-readiness
$task-breakdown
```

## Mandatory outputs

- `spec.md`
- `analysis.md`
- `architecture.md`
- `nfr.md`
- `consistency-report.md`
- `decision-matrix.md`
- `plan.md`
- `tasks.md`
- `context-map.md`
- `interfaces.md`
- `data-model.md`
- `rollout.md`
- `observability.md`
- `runbook.md`

## What good looks like

- bootstrap has produced repo context and guardrails even if the codebase is still mostly empty
- the architecture style is justified
- the module or service boundaries are explicit
- the data model and contracts are understandable
- the security model is credible
- performance, availability, and cost targets are measurable
- the first release path is staged and reversible
- the implementation plan is broken into milestones a small team can review

## Anti-patterns

- choosing microservices because they sound scalable
- letting framework defaults become architecture by accident
- ignoring operability until after launch
- skipping ADRs for decisions that will confuse future contributors
