# Detection rubric

## High-confidence signals

- root package manager files and lockfiles
- explicit root scripts in `package.json`, `Makefile`, `justfile`, `tox.ini`, `noxfile.py`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle*`
- framework dependencies in manifest files
- dedicated architecture docs, ADRs, or runbooks

## Medium-confidence signals

- directory names such as `apps/`, `packages/`, `services/`, `src/`, `api/`, `web/`, `workers/`
- test directories and config files
- observability or infrastructure dependencies

## Low-confidence signals

- inferred domain language from folder names only
- guessed validation commands when no scripts or build files exist
- topology guesses without manifests or docs

Low-confidence output should stay explicitly marked as a guess.
