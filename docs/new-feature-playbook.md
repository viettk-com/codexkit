# New feature playbook

Use this for bounded features or significant changes in an existing repository.

## Commands

```bash
scripts/new-feature.sh <slug>
```

Recommended prompts:

```text
$bootstrap
$continuity-memory
$constitution-governance
$brownfield-mapping
$architecture-discovery
$nfr-capture
$plan-feature
$artifact-consistency
$implementation-readiness
$task-breakdown
$tdd-loop
$execute-plan
```

## Minimum artifact set

For a normal `L1` feature:

- `spec.md`
- `analysis.md`
- `architecture.md`
- `nfr.md`
- `plan.md`
- `tasks.md`
- `test-strategy.md`
- `consistency-report.md`

If the feature crosses subsystems or changes contracts, treat it as `L2` and add rollout, observability, decision matrix, and risk artifacts.

## Questions to answer before code

- does `docs/project-context/` reflect the current repo, or is bootstrap stale?
- which existing module or service should own the feature?
- what public behavior must remain stable?
- what data or contract changes are required?
- what tests prove the feature without expensive noise?
- how would we roll this back if early production signals look bad?

## Execution advice

- implement one slice only
- keep public APIs stable unless the spec says otherwise
- verify the narrowest relevant checks first
- refresh plan artifacts if new architecture facts appear mid-flight
