# Project memory system

CodexKit v3 uses two layers of durable repository memory.

## 1. Machine-readable profile

Location: `.codex/project-context/profile.json`

Purpose:
- deterministic scanner output
- compact facts for future scripts and automation
- a stable place to store topology, frameworks, commands, critical directories, and protected zones

## 2. Human-readable project context

Location: `docs/project-context/`

Purpose:
- architecture and guardrail notes that humans can review in pull requests
- a shared memory surface for plans, tasks, reviews, and onboarding
- explicit open questions instead of hidden assumptions

## Why both layers matter

- machine-readable artifacts make bootstrap repeatable
- human-readable artifacts make architecture reviewable
- `AGENTS.md` stays concise because it points at these files instead of trying to hold the whole repo in one prompt

## Operating rule

After bootstrap, any non-trivial plan or change should start from `docs/project-context/index.md` rather than rediscovering the repo from scratch.
