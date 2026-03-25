---
name: worktree-routine
description: "use when starting a new codex app worktree, background automation, or delegated branch and the repository needs a repeatable bootstrap routine."
---

# Worktree Routine

Bootstrap an isolated worktree in a repeatable way.

## Workflow

Use `docs/project-context/index.md` and the linked project-context files as the default repo memory when they exist.

1. Create or enter the target worktree.
2. Run `scripts/worktree-bootstrap.sh` and project-specific setup commands.
3. Confirm validation commands and current plan artifacts are available in the worktree.
4. Write down any environment assumptions that the automation needs.
5. Stop after the worktree is ready for focused work.

## Output format

### summary
### bootstrap status
### missing dependencies
### ready commands

## Rules

- prefer isolated worktrees for automations and parallel work
- do not edit the main checkout if the task was meant to be isolated
