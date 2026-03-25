# Command palette

CodexKit supports a thin quick-command layer inspired by command-driven kits like Superpowers, Spec Kit, and CodyMaster, but kept Codex-native: aliases resolve into the same canonical skills, agents, scripts, and artifacts that already power the repository workflow.

## Supported forms

- chat shorthand: `/ck:<alias> [payload]`
- skill shorthand: `$ck-<alias> [payload]`
- canonical skill form: `$<skill-name>`

Aliases are **wrappers, not a second workflow system**. They should never bypass architecture, readiness, or review gates.

## Routing rules

- exact alias matches win over synonyms and typo recovery
- the most specific alias wins over a broader category alias
- safe typo normalization is allowed for common mistakes like plan-furture -> plan-feature
- aliases are thin wrappers around canonical skills, scripts, agents, and artifacts; they do not bypass architecture gates
- script-backed aliases should run the mapped script first, then continue with the mapped skills

## Quick examples

- `/ck:bootstrap`
- `/ck:feature tenant-rate-limits`
- `/ck:plan-feature add per-tenant rate limits with rollback-safe migration`
- `/ck:ready`
- `/ck:build phase 1`
- `/ck:review`
- `/ck:ship`
- `$ck-plan add rate limits to tenant middleware`

## Command groups

### Meta

Shortcuts that help you remember or route the rest of the command surface.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:help` | `$command-router` | — | show the codexkit command palette, routing rules, and the safest matching aliases for the current request. |

### Discover

Commands that recover repository understanding and durable project memory.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:bootstrap` | `$bootstrap` | agents: `bootstrap_curator`<br>scripts: `python3 scripts/bootstrap-codexkit.py --apply` | deeply scan the repository, refresh durable project memory, and update codexkit guidance for the current architecture. |
| `/ck:refresh` | `$bootstrap`, `$continuity-memory` | agents: `bootstrap_curator`, `knowledge_librarian`<br>scripts: `python3 scripts/bootstrap-codexkit.py --apply` | refresh repository context, continuity memory, and managed codexkit guidance when context looks stale. |
| `/ck:ctx` | `$continuity-memory` | agents: `knowledge_librarian` | recover continuity memory, active initiative context, and durable lessons before planning or implementation. |
| `/ck:constitution` | `$constitution-governance` | agents: `constitution_keeper` | check the current project constitution, invariants, and architecture guardrails before risky work. |

### Scaffold

Commands that create initiative artifacts or kick off a new project or feature lane.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:project` | `$project-bootstrap`, `$architecture-review`, `$plan-feature` | agents: `chief_architect`, `plan_architect`<br>scripts: `scripts/new-project.sh <project-name-or-title>` | scaffold a new project or major subsystem initiative and start the greenfield architecture lane. |
| `/ck:feature` | `$brownfield-mapping`, `$architecture-discovery`, `$plan-feature` | agents: `system_mapper`, `plan_architect`<br>scripts: `scripts/new-feature.sh <feature-name-or-title>` | scaffold a new feature initiative in an existing codebase and start the brownfield architecture lane. |
| `/ck:init` | `$spec-bootstrap`, `$plan-feature` | agents: `plan_architect`<br>scripts: `scripts/new-initiative.sh [--branch] <L0|L1|L2|L3> <slug-or-title>` | create a new initiative of any change class and seed the right artifact set before planning. |

### Design

Commands for spec, architecture, NFRs, planning, and implementation readiness.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:map` | `$brownfield-mapping` | agents: `system_mapper` | map the current system, hotspots, boundaries, and blast radius before changing an existing codebase. |
| `/ck:spec` | `$spec-bootstrap` | agents: `plan_architect` | turn a fuzzy request into a product-facing spec before technical planning. |
| `/ck:arch` | `$architecture-discovery`, `$architecture-review` | agents: `chief_architect`, `system_mapper`, `domain_modeler` | analyze boundaries and produce an architecture review before coding a non-trivial change. |
| `/ck:nfr` | `$nfr-capture` | agents: `reliability_engineer`, `perf_investigator`, `security_reviewer` | capture measurable performance, reliability, security, cost, and operability constraints. |
| `/ck:decision` | `$architecture-decision` | agents: `chief_architect` | write or update an architecture decision record with options, trade-offs, and rationale. |
| `/ck:plan` | `$plan-feature` | agents: `plan_architect` | turn the request and architecture into a phased implementation plan with validation, rollout, rollback, and docs impact. |
| `/ck:tasks` | `$task-breakdown` | agents: `plan_architect` | break the plan into ordered, reviewable implementation tasks with dependencies and validation checkpoints. |
| `/ck:ready` | `$artifact-consistency`, `$implementation-readiness` | agents: `consistency_auditor`, `test_guardian` | prove that the current initiative is internally consistent and safe to implement before touching code. |

### Build

Commands for implementation, debugging, testing, contracts, and migrations.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:build` | `$execute-plan`, `$tdd-loop` | agents: `plan_architect`, `test_guardian` | implement the next safe slice with small diffs, narrow checks, and an explicit red-green-refactor loop. |
| `/ck:fix` | `$fix-issue` | agents: `debug_detective`, `test_guardian` | debug a concrete bug report and deliver a minimal regression-safe fix. |
| `/ck:debug` | `$systematic-debugging` | agents: `debug_detective` | run a disciplined hypothesis-and-evidence debugging loop for unclear or cross-cutting failures. |
| `/ck:test` | `$test-strategy` | agents: `test_guardian` | design the right validation mix across unit, integration, contract, performance, and rollout checks. |
| `/ck:api` | `$api-contract-review` | agents: `domain_modeler` | review api, schema, event, or sdk contract changes before they leak across boundaries. |
| `/ck:migrate` | `$migration-guard` | agents: `migration_planner` | design a safe staged migration with expand-contract, backfill, cutover, and rollback discipline. |

### Quality

Commands for review, security, performance, docs, design-system fit, and CI.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:review` | `$review-owner` | agents: `reviewer` | perform an owner-style review of the current working tree, diff, or milestone implementation. |
| `/ck:sec` | `$security-review` | agents: `security_reviewer` | review security posture for auth, secrets, trust boundaries, injection, and abuse paths. |
| `/ck:perf` | `$perf-check` | agents: `perf_investigator` | check latency, throughput, hot paths, query shape, caching, and scaling assumptions. |
| `/ck:obs` | `$observability-review` | agents: `reliability_engineer` | review logs, metrics, traces, alerts, and runbook coverage for critical changes. |
| `/ck:ux` | `$design-system-forensics` | agents: `ui_ux_auditor` | inspect design-system fit, component primitives, accessibility, and visual consistency. |
| `/ck:docs` | `$docs-sync` | agents: `docs_curator` | synchronize architecture notes, setup docs, release notes, and operational guidance after changes. |
| `/ck:ci` | `$ci-triage` | agents: `ci_triager` | triage red or flaky ci with a root-cause-first read of the failing jobs and logs. |

### Ship

Commands for PR prep, release readiness, incident triage, and initiative closeout.

| Alias | Expands to | Related agents / scripts | Use for |
|---|---|---|---|
| `/ck:pr` | `$pr-prep` | agents: `reviewer`, `docs_curator` | prepare a clean pull request summary with risks, validation, rollout notes, and reviewer guidance. |
| `/ck:ship` | `$release-readiness` | agents: `release_manager`, `reliability_engineer` | assess release readiness, rollout safety, rollback clarity, and communication gaps before shipping. |
| `/ck:incident` | `$incident-response` | agents: `incident_triager` | triage an active incident with mitigation-first analysis, next actions, and follow-up checks. |
| `/ck:close` | `$closeout-learning`, `$continuity-memory` | agents: `knowledge_librarian`<br>scripts: `python3 scripts/close-initiative.py` | close the active initiative, archive durable lessons, and update continuity memory for future agents. |

## Payload handling

Anything after the first alias token is payload. Preserve that payload and pass it into the resolved workflow.

Examples:

- `/ck:project billing-platform` -> run `scripts/new-project.sh billing-platform`, then continue with `$project-bootstrap`, `$architecture-review`, and `$plan-feature`
- `/ck:init L2 tenant import backfill` -> run `scripts/new-initiative.sh [--branch] <L0|L1|L2|L3> <slug-or-title>` with the supplied class and title, then continue with the mapped planning lane
- `/ck:plan-furture add tenant quotas` -> normalize to `/ck:plan-feature`, then run `$plan-feature`

## Customizing aliases

1. Edit `.codex/command-aliases.json`.
2. Run `python3 scripts/render-command-palette.py` to regenerate this document and the prompt wrappers.
3. Run `python3 scripts/validate-aliases.py` and then `scripts/check-kit.sh`.

## Source of truth

- registry: `.codex/command-aliases.json`
- router skill: `.agents/skills/command-router/SKILL.md`
- resolver cli: `python3 scripts/resolve-command-alias.py /ck:plan-feature`

