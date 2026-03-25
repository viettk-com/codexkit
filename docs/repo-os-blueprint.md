# Repo operating system blueprint

A healthy AI coding repo has four layers:

1. **Durable guidance**
   - `AGENTS.md`
   - release, review, and architecture docs

2. **Reusable workflows**
   - `.agents/skills/`

3. **Specialized delegation**
   - `.codex/agents/`

4. **Deterministic automation**
   - GitHub workflows
   - local validation scripts
   - plan and release artifacts

## Why this structure works

- guidance stays small and durable
- workflows become discoverable and reusable
- noisy analysis can move to specialist agents
- automation stays visible and reviewable
- future sessions inherit the same grammar
