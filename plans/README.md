# Plans

Use `plans/active/` for live work and `plans/archive/` for completed or abandoned work.

## Suggested flow

1. create a folder with `scripts/new-feature.sh`, `scripts/new-project.sh`, or `scripts/new-initiative.sh`
2. shape architecture and NFRs
3. plan and break down the work
4. implement slice by slice
5. archive the folder when the work is done

## Initiative folder layout

```text
plans/active/<date>-<slug>/
├── spec.md
├── architecture.md
├── nfr.md
├── plan.md
├── tasks.md
├── phases/
├── reports/
├── research/
└── artifacts/
```


Always start non-trivial work from `docs/project-context/index.md` when bootstrap has been run.
