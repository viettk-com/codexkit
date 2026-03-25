# Codex app playbook

## Recommended setup

1. Open the repository in the Codex app.
2. Point worktree setup at `scripts/worktree-bootstrap.sh`.
3. Use worktrees for background automations or risky branches.
4. Keep the plan folder committed so every session sees the same artifacts.

## Good automations

- nightly docs drift audit
- PR review
- architecture gate on risky labels
- release readiness sweep before merge trains
