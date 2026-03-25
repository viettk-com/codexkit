---
name: research-openai-docs
description: "use when the task depends on current openai or codex behavior, apis, cli flags, mcp setup, skills, subagents, automations, security settings, or github action details."
---

# Research OpenAI Docs

Verify current OpenAI and Codex behavior from primary sources.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Search or read primary OpenAI documentation first.
2. Separate confirmed behavior from inference.
3. Bring back only the details that affect the current task or repo setup.
4. Prefer concise summaries over copy-paste.
5. Stop after the main agent has enough evidence to continue safely.

## Output format

### summary
### confirmed behavior
### inference
### repo implications

## Rules

- do not rely on stale memory when the platform behavior might have changed
- prefer official docs over third-party summaries
