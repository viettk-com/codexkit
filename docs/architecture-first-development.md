# Architecture-first development

This kit assumes that serious work should move through a predictable chain:

1. discover current state or project scope
2. capture architecture drivers and non-functional requirements
3. choose a target design deliberately
4. plan implementation in safe slices
5. implement one slice only
6. verify, review, and release with evidence

## Why this exists

AI agents are excellent at producing code quickly.
They are much worse when the real failure is:

- missing architectural boundaries
- fuzzy non-functional requirements
- migration risk
- hidden operational burden
- code that technically works but will not scale or stay maintainable

This kit treats those concerns as first-class artifacts instead of afterthoughts.

## The architecture gate

For `L1` and above, do not code until these files exist and are plausible:

- `spec.md`
- `architecture.md`
- `nfr.md`
- `plan.md`
- `tasks.md`

For `L2` and `L3`, add:

- `decision-matrix.md`
- `rollout.md`
- `observability.md`
- `risk-register.md`

For `L3`, add:

- `context-map.md`
- `interfaces.md`
- `data-model.md`
- `runbook.md`
- ADRs

## Key questions the architecture step must answer

- Where does this capability belong?
- Which modules or services own the data and behavior?
- What must remain backward compatible?
- How will this roll out safely?
- What breaks if it fails in production?
- What metrics, logs, traces, and alerts prove it is healthy?
- What load, latency, or cost budget must it stay within?
- Which design alternatives were considered and rejected?

## Keep it proportional

Architecture-first does not mean writing a novel.

- `L0`: short note and validation
- `L1`: lightweight but explicit architecture and NFR notes
- `L2`: serious design review and rollout thinking
- `L3`: full subsystem or project shaping

The goal is to avoid accidental architecture, not to create bureaucracy.
