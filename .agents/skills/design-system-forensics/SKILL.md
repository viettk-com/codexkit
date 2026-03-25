---
name: design-system-forensics
description: "use when the repository has a frontend, design drift, inconsistent components, or a legacy ui that needs tokens, component patterns, accessibility rules, or interaction standards extracted before more ui work ships."
---

# Design System Forensics

Map the current design system before adding more UI complexity.

## Workflow

Use `docs/project-context/12-design-system-and-ux.md`, frontend source files, theme files, style tokens, and component directories.

1. Identify the current UI stack, component sources, design tokens, and accessibility signals.
2. Document the stable patterns worth preserving and the drift worth correcting.
3. Update `docs/project-context/12-design-system-and-ux.md` or the active initiative artifacts with the discovered guardrails.
4. If a new UI feature is planned, ensure the architecture and task plan point to existing primitives before inventing new ones.
5. Stop after later UI work can follow a coherent system instead of improvising styles per screen.

## Output format

### current ui stack
### stable design primitives
### drift and anti-patterns
### guidance for upcoming work

## Rules

- preserve existing tokens and component primitives when they are healthy
- treat accessibility regressions as architecture issues, not polish
- do not invent a new design language when the repo already has one worth extending
