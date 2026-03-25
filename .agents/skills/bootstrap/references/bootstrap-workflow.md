# Bootstrap workflow

## Purpose

Bootstrap exists to turn a raw repository into a repo-aware operating environment for CodexKit.

## Phases

1. **Scan**
   - inventory manifests, languages, frameworks, quality tools, CI, infra, docs, and sensitive areas
2. **Synthesize**
   - generate a machine-readable profile and human-readable project memory docs
3. **Tune**
   - update the managed bootstrap block in `AGENTS.md`
   - fill repo-specific validation commands and sensitive paths where confidence is high
4. **Refine**
   - if the repo is complex, call read-only agents to tighten boundaries and challenge weak assumptions
5. **Validate**
   - run `scripts/validate-bootstrap.py`

## Output locations

- `.codex/project-context/profile.json`
- `docs/project-context/index.md`
- `docs/project-context/01-repo-overview.md`
- `docs/project-context/02-architecture-map.md`
- `docs/project-context/03-build-test-and-quality-gates.md`
- `docs/project-context/04-domain-and-interfaces.md`
- `docs/project-context/05-change-boundaries.md`
- `docs/project-context/06-nfr-and-operability.md`
- `docs/project-context/07-bootstrap-report.md`
