---
name: command-router
description: "use when the prompt begins with /ck: or $ck-, when the user asks for codexkit quick commands or aliases, or when shorthand like /ck:plan-feature, /ck:arch, /ck:ready, /ck:build, or /ck:help must be resolved into the right codexkit skill, agent, script, and artifact workflow."
---

# Command Router

Resolve CodexKit shorthand commands into the correct canonical workflow.

## Workflow

1. If the prompt begins with `/ck:` or `$ck-`, treat the first token as a CodexKit alias and everything after the first space as payload.
2. Read `.codex/command-aliases.json` and `docs/command-palette.md` to resolve aliases, synonyms, and safe typo fixes.
3. Prefer the most specific exact alias. If there is no exact match, use the closest safe match only when confidence is high; otherwise show `/ck:help` plus the best matches.
4. Briefly restate the resolution: alias, canonical skill chain, companion agent, script, and the next artifact to touch.
5. Continue as if the user had invoked the resolved canonical skills directly.
6. For script-backed aliases such as `/ck:project`, `/ck:feature`, or `/ck:init`, run the mapped scaffold script first, then continue with the mapped skills.
7. For multi-step aliases such as `/ck:ready`, `/ck:build`, or `/ck:close`, execute the mapped skills in order and stop before code unless the alias explicitly implies implementation.

## Output format

### resolved alias
### canonical workflow
### next artifact or command
### assumptions

## Rules

- do not silently map a destructive or shipping alias to a different action
- preserve any payload after the alias and pass it to the resolved workflow
- accept common typos like `plan-future`, `plan-furture`, and `planfeature` for `/ck:plan-feature`
- when the alias is `/ck:help`, show the short command palette grouped by discover, design, build, review, and ship
- aliases are wrappers only; they must still respect bootstrap, architecture, readiness, and review gates
