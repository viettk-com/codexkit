# Skill catalog

## Quick alias index

Use these when you want CodyMaster-style short commands without losing the canonical CodexKit workflow:

- `/ck:bootstrap` -> `$bootstrap`
- `/ck:ctx` -> `$continuity-memory`
- `/ck:project` -> scaffold + `$project-bootstrap`
- `/ck:feature` -> scaffold + `$brownfield-mapping`, `$architecture-discovery`, `$plan-feature`
- `/ck:arch` -> `$architecture-discovery`, `$architecture-review`
- `/ck:nfr` -> `$nfr-capture`
- `/ck:plan` or `/ck:plan-feature` -> `$plan-feature`
- `/ck:tasks` -> `$task-breakdown`
- `/ck:ready` -> `$artifact-consistency`, `$implementation-readiness`
- `/ck:build` -> `$execute-plan`, `$tdd-loop`
- `/ck:review` -> `$review-owner`
- `/ck:ship` -> `$release-readiness`
- `/ck:close` -> `$closeout-learning`, `$continuity-memory`

Read `docs/command-palette.md` for the full registry and alias rules.

| Skill | Primary trigger |
|---|---|
| `$command-router` | use when the prompt begins with /ck: or $ck-, when you need codexkit quick commands, or when shorthand like /ck:plan-feature and /ck:ready must be resolved into the right skill chain, agent, script, and artifact workflow. |
| `$bootstrap` | use when codexkit is first added to a repository, when the codebase is unfamiliar, when project context docs are missing or stale, or when you explicitly ask to bootstrap. deeply scans the repo, generates durable project memory, and updates codexkit guidance for the current architecture. |
| `$project-bootstrap` | use when starting a new project, product area, or major subsystem and you need architecture, non-functional requirements, and delivery artifacts before any code is written. |
| `$brownfield-mapping` | use when the repository already exists and you must map current architecture, hotspots, ownership boundaries, and change risk before planning a new feature or refactor. |
| `$architecture-discovery` | use when starting a new feature or subsystem and you must understand module boundaries, interfaces, dependencies, and architectural constraints before writing a plan. |
| `$nfr-capture` | use when a feature or project needs measurable non-functional requirements for performance, reliability, security, compliance, cost, or operability before planning implementation. |
| `$architecture-review` | use when a new feature, subsystem, or refactor needs an explicit target architecture, option matrix, and trade-off review before coding begins. |
| `$spec-bootstrap` | use when starting new work from a fuzzy request and you need to create or refresh product-facing spec artifacts before technical planning. |
| `$plan-feature` | use when the task is ambiguous, risky, cross-cutting, or larger than a small one-file edit. best for turning a spec or request into a phased technical plan with validation, rollout, rollback, and docs impact. |
| `$task-breakdown` | use after a technical plan exists and you need to convert milestones into ordered, reviewable implementation tasks with dependencies, validation, and ownership hints. |
| `$execute-plan` | use when architecture, spec, plan, and tasks already exist and the next job is to implement one milestone or one tightly scoped slice with small diffs and explicit validation. |
| `$fix-issue` | use when the user reports a bug and can provide reproduction steps, logs, or symptoms. best for root-cause-first debugging with a minimal fix and regression validation. |
| `$test-strategy` | use when a change needs an explicit validation plan across unit, integration, contract, performance, or rollout checks before or during implementation. |
| `$api-contract-review` | use when the change touches public or cross-module contracts such as request or response shapes, events, schemas, queues, or SDK behavior. |
| `$observability-review` | use when a change affects critical workflows, background jobs, migrations, or user-facing paths and you need explicit logs, metrics, traces, alerts, and runbook notes. |
| `$review-owner` | use when you want an owner-style review of the working tree, a proposed diff, or a milestone implementation. best for correctness, regression, security, and missing test review. |
| `$security-review` | use when the change touches auth, permissions, secrets, external input, file access, templates, redirects, database queries, shell calls, or any trust boundary. |
| `$perf-check` | use when the change may affect hot paths, database queries, rendering, caching, concurrency, throughput, or large data volume behavior. |
| `$docs-sync` | use after code changes when behavior, architecture, setup, release notes, migrations, or operational guidance may now be stale. do not use for pure internal refactors with no durable context impact. |
| `$ci-triage` | use when ci is red, flaky, or noisy and you need a root-cause-oriented read of logs, failing jobs, or pre-merge checks. |
| `$release-readiness` | use before a release, merge train, or deployment freeze to check changelog, migrations, rollback notes, docs impact, and known risks. do not use for tiny local-only changes. |
| `$research-openai-docs` | use when the task depends on current openai or codex behavior, apis, cli flags, mcp setup, skills, subagents, automations, security settings, or github action details. |
| `$worktree-routine` | use when starting a new codex app worktree, background automation, or delegated branch and the repository needs a repeatable bootstrap routine. |
| `$incident-response` | use when production symptoms, alerts, or support escalations suggest an active incident and you need a concise triage note, mitigation-first plan, and follow-up checklist. |
| `$pr-prep` | use when implementation is done and you need a clean pull request or merge request summary with risks, validation, rollout notes, and reviewer guidance. |
| `$migration-guard` | use when a change touches schemas, contracts, queues, caches, search indexes, or data backfills and you need staged rollout and rollback discipline before merge or deploy. |
| `$architecture-decision` | use when a change needs an explicit architectural decision record, trade-off note, or rationale summary so future agents and reviewers can understand why the team chose this path. |
| `$constitution-governance` | use when a plan, task list, or implementation must align with project invariants, boundaries, and architecture rules captured by bootstrap and durable decisions. |
| `$artifact-consistency` | use when you need to verify that spec, analysis, architecture, nfr, plan, tasks, rollout, and test artifacts do not contradict each other before implementation. |
| `$continuity-memory` | use when starting work, resuming a paused initiative, or after closeout so future agents inherit the right active context, recurring lessons, and current priorities. |
| `$implementation-readiness` | use after planning and before coding to prove the next slice is safe, testable, reversible, and consistent with architecture and rollout constraints. |
| `$tdd-loop` | use when implementing a non-trivial slice and you want an explicit red-green-refactor loop with narrow tests and frequent validation. |
| `$systematic-debugging` | use when symptoms are unclear, flaky, or cross-cutting and you need a disciplined hypothesis-and-evidence debugging loop instead of random edits. |
| `$design-system-forensics` | use when frontend or design work must respect existing tokens, component primitives, interaction patterns, and visual system constraints. |
| `$closeout-learning` | use when a milestone or initiative finishes and you need to archive durable lessons, update continuity memory, and leave a clean handoff for future agents. |


## Final-release additions

- `command-router`
- `constitution-governance`
- `artifact-consistency`
- `continuity-memory`
- `implementation-readiness`
- `tdd-loop`
- `systematic-debugging`
- `design-system-forensics`
- `closeout-learning`
