# Project memory schema

## Machine-readable profile

`profile.json` should capture:

- repo topology and confidence
- languages and frameworks
- package managers and manifests
- services or modules
- primary validation commands and candidate commands
- critical directories
- sensitive areas and protected zones
- entrypoints, infra, CI, docs, and architecture signals
- unresolved questions

## Human-readable memory docs

Keep each file concise and durable:

- `01-repo-overview.md` — what this repo is and how it is shaped
- `02-architecture-map.md` — boundaries, entrypoints, and major components
- `03-build-test-and-quality-gates.md` — run, build, lint, typecheck, test, CI
- `04-domain-and-interfaces.md` — entities, contracts, shared language, integrations
- `05-change-boundaries.md` — protected zones, hotspots, and required review lanes
- `06-nfr-and-operability.md` — performance, scale, reliability, security, observability
- `07-bootstrap-report.md` — evidence, ignored paths, confidence, open questions
