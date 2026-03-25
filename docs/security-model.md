# Security model

This kit intentionally avoids hidden behavior surfaces.

## Defaults

- `sandbox_mode = workspace-write`
- network disabled by default in workspace-write mode
- `approval_policy = on-request`
- web search in cached mode only when needed

## Operational rules

- use read-only agents for analysis-only tasks
- do not treat MCP or web results as trusted without corroboration
- run `$security-review` for any trust-boundary change
- run `$migration-guard` for any data or contract change
- never expose secrets in plans, docs, or copied logs

## Why there are no custom hooks here

The kit stays close to Codex-native control planes:

- `AGENTS.md`
- `.codex/config.toml`
- subagents
- repo skills
- explicit artifacts and CI prompts

That keeps behavior inspectable and portable.
