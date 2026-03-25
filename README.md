# CodexKit Engineer Pro Final Plus

English | [Tiếng Việt](README.vi.md) | [简体中文](README.zh-CN.md)

CodexKit Engineer Pro Final Plus is a **Codex-native engineering operating system** for teams that want AI coding agents to behave less like “vibe coders” and more like senior engineers.

This version is intentionally more opinionated than v1:

- **architecture-first, not code-first**
- **spec -> architecture -> nfr -> plan -> tasks -> execute**
- **explicit change classes** for tiny fixes, bounded features, cross-cutting changes, and new projects
- **maintainability, scalability, performance, reliability, and rollback** treated as first-class artifacts
- **repo-native skills + subagents + CI prompts** instead of a giant custom command DSL

## What is new in the final release

1. A mandatory **bootstrap + architecture gate** for new projects and non-trivial features
2. A deep bootstrap lane that scans the repo, generates project memory, and updates CodexKit guidance for the current architecture
3. A `bootstrap_curator` agent and deterministic bootstrap scripts
4. Generated project-context docs plus machine-readable repo profiles, dashboards, continuity memory, and constitution rules
5. Existing greenfield and brownfield lanes:
   - `$project-bootstrap`
   - `$brownfield-mapping`
   - `$architecture-discovery`
   - `$architecture-review`
   - `$nfr-capture`
6. More architecture-heavy agents, now including `bootstrap_curator`, `constitution_keeper`, `consistency_auditor`, `knowledge_librarian`, `debug_detective`, and `ui_ux_auditor`
7. Richer templates that cite project context sources and enforce analysis, test strategy, and implementation readiness artifacts
8. Stronger local validation:
   - `scripts/validate-plans.py`
   - `scripts/validate-bootstrap.py`
   - `scripts/audit-placeholders.py`
9. A GitHub **architecture gate** workflow and a new **artifact consistency** workflow
10. A **constitution + continuity + artifact-consistency + closeout** layer inspired by the best parts of spec-driven and agentic workflow systems
11. Extended project-context outputs: constitution, module index, delivery system, hotspots, design-system map, agent context, continuity, and dashboard
12. New implementation disciplines: `$artifact-consistency`, `$implementation-readiness`, `$tdd-loop`, `$systematic-debugging`, `$closeout-learning`, and `$design-system-forensics`
13. Optional nested `AGENTS.md` generation for large repos

## Quick command layer

This edition adds a thin alias surface so you can invoke the kit quickly without memorizing every canonical skill name.

Supported forms:

- `/ck:<alias> [payload]` in chat
- `$ck-<alias> [payload]` in skill-style mode
- canonical direct skills like `$plan-feature` still work

Examples:

```text
/ck:bootstrap
/ck:feature tenant-rate-limits
/ck:plan-feature add per-tenant rate limits
/ck:ready
/ck:build phase 1
/ck:review
/ck:ship
```

Read `docs/command-palette.md` for the full alias catalog and routing rules.

## Design principles

1. **Understand the system before changing it**
2. **Do architecture early, but keep it proportional**
3. **Use the simplest design that can survive growth**
4. **Prefer reversible slices and boring migrations**
5. **Measure hot paths; do not guess**
6. **Make operations, observability, and rollback explicit**
7. **Leave durable artifacts, not just chat history**

## Core workflow

### New project or major subsystem

```bash
scripts/new-project.sh billing-platform
```

Then use:

```text
$bootstrap
$continuity-memory
$constitution-governance
$project-bootstrap
$architecture-review
$plan-feature
$artifact-consistency
$implementation-readiness
$task-breakdown
```

### New feature in an existing codebase

```bash
scripts/new-feature.sh tenant-rate-limits
```

Then use:

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

### Small bug fix

```text
$fix-issue
```

Use the architecture lane only if the bug exposes a deeper design problem.

## Required artifacts by work size

| Change class | Typical scope | Minimum artifacts |
|---|---|---|
| `L0` | tiny fix, docs, one-file safe change | validation note, optional repro |
| `L1` | bounded feature in one subsystem | `spec.md`, `analysis.md`, `architecture.md`, `nfr.md`, `plan.md`, `tasks.md`, `test-strategy.md`, `consistency-report.md` |
| `L2` | cross-cutting change, migration, multiple modules | `L1` artifacts plus `decision-matrix.md`, `rollout.md`, `observability.md`, `risk-register.md`, `perf-budget.md`, `threat-model.md` |
| `L3` | new project, platform capability, large subsystem | everything in `L2` plus `context-map.md`, `interfaces.md`, `data-model.md`, `runbook.md`, and `adr.md` |

## Repository layout

```text
.
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── config.mcp.example.toml
│   └── agents/
├── .agents/
│   └── skills/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── codex/prompts/
│   └── workflows/
├── docs/
│   └── project-context/
├── plans/
│   ├── active/
│   ├── archive/
│   └── templates/
├── runbooks/
└── scripts/
```

## Suggested adoption order

1. Copy the kit into the root of your repository.
2. Run `python3 scripts/bootstrap-codexkit.py --apply`.
3. Review `docs/project-context/` and the managed bootstrap block in `AGENTS.md`.
4. Review `.codex/config.toml`.
5. Keep `plans/templates/` committed so all agents share the same delivery grammar.
6. Run `scripts/check-kit.sh`.
7. Enable GitHub workflows after your tests and secrets are stable.
8. Run `scripts/audit-placeholders.py` after tailoring the kit to your repo.

## Files worth reading first

- `docs/bootstrap-playbook.md`
- `docs/project-memory-system.md`
- `docs/architecture-first-development.md`
- `docs/new-project-playbook.md`
- `docs/new-feature-playbook.md`
- `docs/brownfield-playbook.md`
- `docs/quality-gates.md`
- `docs/agent-roster.md`
- `docs/command-palette.md`
- `docs/skill-catalog.md`
- `docs/v3-improvements.md`
- `docs/final-improvements.md`
- `docs/external-benchmark-analysis.md`
- `docs/source-patterns.md`
- `docs/constitution-playbook.md`
- `docs/continuity-memory.md`
- `docs/implementation-readiness.md`
- `docs/systematic-debugging.md`
- `docs/design-system-forensics.md`
- `docs/initiative-lifecycle.md`
