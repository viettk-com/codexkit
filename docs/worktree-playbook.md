# Worktree playbook

Use worktrees for isolated background work, risky spikes, and parallel agent sessions.

## Bootstrap

Point your Codex app or local flow at:

```bash
scripts/worktree-bootstrap.sh
```

## Rules

- prefer worktrees for automations
- keep the active plan folder available in the worktree
- do not mix unrelated changes in one worktree
- archive or delete stale worktrees quickly
