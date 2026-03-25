# External benchmark analysis

This document records which external systems influenced the final CodexKit bundle and why.

## Why this analysis exists

Good agent tooling is less about collecting dozens of commands and more about choosing the few workflow patterns that reliably protect architecture, delivery quality, and continuity. This bundle intentionally imports the strongest patterns from each benchmark and rejects the parts that would make the kit brittle, host-specific, or hard to maintain.

## 1. Superpowers

### Strong patterns observed
- mandatory multi-step workflow instead of "ask once and improvise"
- separation between discovery, planning, implementation, review, and finish-the-branch rituals
- strong subagent and worktree discipline
- explicit tdd and debugging habits

### What was imported
- `worktree-routine` already in the kit remains a first-class path
- new `tdd-loop`, `systematic-debugging`, and `closeout-learning` skills
- stronger emphasis on reviewable slices and branch/initiative closure
- thin `/ck:` alias surface so quick commands stay wrappers over canonical workflows

### What was deliberately not copied
- host-specific rituals that assume a particular runtime or plugin implementation
- giant command DSLs that duplicate the canonical skill layer instead of acting as thin wrappers

## 2. GitHub Spec Kit

### Strong patterns observed
- constitution first
- separate durable artifacts for spec, plan, tasks, and implementation
- branch or initiative context should be discoverable and auditable
- pre-implementation consistency checks are worth enforcing

### What was imported
- `constitution-governance`
- `artifact-consistency`
- `implementation-readiness`
- stronger `validate-plans.py` rules
- better initiative bootstrap flow and clearer artifact grammar
- a namespaced quick-command grammar that also works in skill form as `$ck-*`

### What was deliberately not copied
- dependence on slash commands or a single cli style
- any pattern that hides reasoning only inside the branch and not in repository artifacts

## 3. CodyMaster

### Strong patterns observed
- lifecycle coverage from idea to learning
- continuity and memory across sessions
- deeper operational stance: tests, security, isolation, deployment, monitoring, documentation, and learning

### What was imported
- `continuity-memory`
- dashboard and continuity json outputs
- `close-initiative.py`
- reusable lessons-learned flow
- `knowledge_librarian` agent
- a short, memorable command namespace inspired by `/cm:*`, but mapped back to CodexKit primitives

### What was deliberately not copied
- very large command surfaces that would add maintenance cost without equivalent value in Codex
- generalized memory complexity beyond what this repository-based kit can maintain clearly

## 4. UI/UX Pro Max Skill

### Strong patterns observed
- UI work improves when the agent can consult structured design-system knowledge rather than generic frontend advice
- domain-specific knowledge packs should remain portable across agent runtimes

### What was imported
- `design-system-forensics`
- `ui_ux_auditor`
- generated design-system context as part of bootstrap refresh

### What was deliberately not copied
- giant static style databases that can become stale quickly
- visual taste rules detached from the actual component and token system of the current repo

## 5. OpenAI Codex platform patterns

### Strong patterns observed
- `AGENTS.md` as an open control-plane format
- nested `AGENTS.md` files for monorepos and large modular repos
- safer default posture for internet access and external docs

### What was imported
- optional nested `AGENTS.md` generation
- docs-research and internet-safety guidance
- project-context driven instructions rather than a giant monolithic rules file

## Design conclusion

The final bundle is intentionally opinionated in five places:

1. bootstrap is mandatory before risky work in unfamiliar repos
2. architecture and nfrs are mandatory before non-trivial coding
3. consistency and readiness checks happen before implementation, not after regressions
4. continuity and closeout are durable repository artifacts, not chat-only memory
5. frontend work must respect the design system just as backend work must respect contracts

This is the smallest set of imported patterns that materially improves maintainability, scalability, and long-term correctness without turning the kit into a fragile command framework.
