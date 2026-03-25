# Constitution playbook

Use this playbook when a repository needs durable engineering principles that outlive any one feature.

## What belongs in the constitution

Keep only durable rules:
- architecture invariants that must not be broken casually
- quality gates required before merge or release
- review triggers for migrations, contracts, security, performance, or UX
- forbidden shortcuts that repeatedly caused pain

Do not store temporary ticket details or personal style preferences here.

## Recommended timing

Create or refresh the constitution when:
- CodexKit is first added to a repo
- a new subsystem or platform capability is introduced
- recurring incidents show the team keeps relearning the same lesson
- the repository grows into a monorepo or modular monolith

## Suggested workflow

1. Run `$bootstrap`
2. Run `$constitution-governance`
3. Review `docs/project-context/08-project-constitution.md`
4. Reflect any new rule in active plans and review rubrics

## Good constitution principles

- prefer additive migrations before destructive cutovers
- protect public contracts and shared schemas with explicit compatibility notes
- keep validation commands executable by another engineer, not implied by chat
- preserve existing design tokens and component primitives unless a deliberate redesign is approved
- update continuity memory after incidents, migrations, and significant reviews
