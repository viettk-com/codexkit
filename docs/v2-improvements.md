# Why v2 is stronger than v1

## The main change

v1 was plan-first.
v2 is **architecture-first plus plan-first**.

That matters because many bad AI-generated changes fail long before code quality:
they fail at boundaries, contracts, migrations, operability, or scaling assumptions.

## What changed

- new project and brownfield lanes
- explicit change classes from `L0` to `L3`
- architecture gate before implementation
- NFR capture and observability templates
- richer domain, architecture, and reliability agents
- plan validator that checks artifact completeness
- GitHub architecture gate workflow and PR template

## What stayed intentionally lean

- no giant custom command tree
- no hidden hooks
- no provider-specific telemetry logic
- no duplicated features that Codex already provides natively
