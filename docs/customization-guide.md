# Customization guide

## Required edits

1. run bootstrap once and review `docs/project-context/`
2. `AGENTS.md` managed block plus any manual notes you want to add around it
3. `.codex/config.toml`
4. validation commands that bootstrap could not infer confidently
5. sensitive areas, release, and runbook expectations

## Recommended edits

- remove agents you never plan to use
- remove skills that do not fit your stack
- adapt templates to your repo naming and ADR format
- wire only the GitHub workflows you trust

## After customization

Run:

```bash
python3 scripts/bootstrap-codexkit.py --apply
scripts/audit-placeholders.py
scripts/check-kit.sh
```
