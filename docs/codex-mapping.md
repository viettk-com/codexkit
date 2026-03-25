# ClaudeKit to Codex mapping in v2 and v3

| ClaudeKit idea | Codex-native equivalent in this kit |
|---|---|
| planner agent and plan flow | `chief_architect`, `system_mapper`, `plan_architect`, repo skills, and plan templates |
| tester and reviewer agents | `test_guardian`, `reviewer`, `security_reviewer`, `perf_investigator` |
| docs manager | `docs_curator` and `$docs-sync` |
| worktree setup | Codex worktrees + `scripts/worktree-bootstrap.sh` |
| plan folders and reports | `plans/active/<date>-<slug>/...` |
| hook-governed safety | visible artifacts + Codex config + CI workflows instead of hidden hooks |
| broad skill catalog | repo-native skills under `.agents/skills/` |

## Core rule

Do not clone mechanics 1:1 when Codex already has a stronger native primitive.
