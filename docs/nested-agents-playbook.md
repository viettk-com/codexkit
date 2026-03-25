# Nested agents playbook

Large repositories often need more than one `AGENTS.md`.

## When to add nested `AGENTS.md`

Add module-level guidance when:
- the repo is a monorepo or modular monolith
- different packages use different frameworks or commands
- one module has stricter contracts or deployment rules than the rest of the repo

## Recommended workflow

1. Run `$bootstrap`
2. Review `docs/project-context/09-module-index.md`
3. Run `python3 scripts/generate-nested-agents.py` if the repo would benefit from module-local guidance
4. Keep each nested file short and module-specific

## Good nested guidance

- exact local test and build commands
- sensitive files or boundaries in that module
- generated-code or migration caveats
- public contract or compatibility rules
