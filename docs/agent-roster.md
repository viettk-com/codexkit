# Agent roster

| Agent | Primary use | Sandbox | Default model |
|---|---|---:|---|
| `bootstrap_curator` | Deep repo scan, project memory refresh, and managed CodexKit adaptation. | `workspace-write` | `gpt-5.4` |
| `chief_architect` | Architecture lead for greenfield systems, large features, and long-lived design decisions. | `read-only` | `gpt-5.4` |
| `system_mapper` | Brownfield mapper for current-state architecture, dependencies, hotspots, and change impact. | `read-only` | `gpt-5.4-mini` |
| `domain_modeler` | Domain and contract specialist for entities, invariants, APIs, schemas, and event flows. | `read-only` | `gpt-5.4` |
| `plan_architect` | Planning-first architect for phased implementation plans, safe slices, and rollout design. | `read-only` | `gpt-5.4` |
| `reviewer` | Owner-style code reviewer focused on correctness, regressions, and maintainability. | `read-only` | `gpt-5.4` |
| `security_reviewer` | Security specialist for auth, trust boundaries, secrets, injection, and abuse paths. | `read-only` | `gpt-5.4` |
| `perf_investigator` | Performance and scale specialist for latency, throughput, hot paths, concurrency, and caching. | `read-only` | `gpt-5.4` |
| `reliability_engineer` | Reliability and operability specialist for failure modes, SLOs, alerts, and runbooks. | `read-only` | `gpt-5.4` |
| `migration_planner` | Schema and compatibility planner for staged migrations, backfills, and safe cutovers. | `read-only` | `gpt-5.4` |
| `test_guardian` | Testing specialist for reproductions, regression coverage, and validation commands. | `workspace-write` | `gpt-5.4-mini` |
| `docs_researcher` | Read-only researcher for current framework, API, and platform behavior from primary sources. | `read-only` | `gpt-5.4-mini` |
| `docs_curator` | Documentation specialist for architecture notes, onboarding, changelog, and release docs. | `workspace-write` | `gpt-5.4-mini` |
| `ci_triager` | CI failure analyst for flaky checks, red pipelines, and minimal recovery plans. | `read-only` | `gpt-5.4-mini` |
| `browser_debugger` | UI debugger for browser reproduction, screenshots, console logs, and network evidence. | `workspace-write` | `gpt-5.4` |
| `release_manager` | Release specialist for ship readiness, rollout sequencing, communications, and rollback notes. | `read-only` | `gpt-5.4` |
| `incident_triager` | Incident response specialist for mitigation-first production issue handling. | `read-only` | `gpt-5.4` |

| `constitution_keeper` | Keeps architecture invariants, project constitution, and boundary rules visible during planning and review. | `read-only` | `gpt-5.4` |
| `consistency_auditor` | Audits whether specs, plans, tasks, rollout notes, and tests agree before implementation starts. | `read-only` | `gpt-5.4-mini` |
| `knowledge_librarian` | Curates continuity memory, dashboards, initiative lifecycle state, and reusable lessons. | `workspace-write` | `gpt-5.4-mini` |
| `debug_detective` | Runs systematic debugging loops with hypotheses, evidence, isolation steps, and root-cause tracking. | `read-only` | `gpt-5.4` |
| `ui_ux_auditor` | Reviews frontend and design-system consistency, component reuse, and UX regressions. | `read-only` | `gpt-5.4` |


## Final-release additions

- `constitution_keeper`
- `consistency_auditor`
- `knowledge_librarian`
- `debug_detective`
- `ui_ux_auditor`
