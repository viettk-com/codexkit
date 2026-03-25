# Design-system forensics

Use this playbook when a frontend codebase has drift, legacy UI, or inconsistent component patterns.

## Goals

- identify the real UI stack and token sources
- map which components are foundational versus duplicated
- surface accessibility, spacing, typography, and interaction rules that should remain stable
- stop new UI work from inventing a new style every sprint

## Typical evidence sources

- `tailwind.config.*`, theme files, CSS variable files, design token packages
- `components/`, `packages/ui/`, shared primitives, Storybook configs
- accessibility tests or lint rules
- screenshots and design QA notes when available

## Deliverables

- update `docs/project-context/12-design-system-and-ux.md`
- identify stable primitives to reuse
- identify anti-patterns to avoid in future tasks
- reflect those guardrails in the active initiative artifacts
