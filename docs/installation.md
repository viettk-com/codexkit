# Installation

## 1. Preferred install path: npm / npx

This repository now includes a publish-ready installer package.

After publishing it to npm as `create-codexkit`, you can use:

```bash
npm create codexkit@latest my-repo
```

Or install the kit into an existing repository:

```bash
npx create-codexkit@latest init .
```

That installer copies the CodexKit payload, merges a CodexKit block into `.gitignore`, and then leaves you on the same bootstrap flow as a manual install.

## 2. Manual fallback: copy the kit into your repository root

Copy or unpack this bundle into the repository root so these paths exist:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/`
- `.agents/skills/`
- `plans/templates/`
- `docs/`
- `scripts/`

If you copy from the source repository directly, exclude npm packaging files such as `package.json`, `bin/`, and `installer/`.

## 3. Bootstrap repo context

Run:

```bash
python3 scripts/bootstrap-codexkit.py --apply
```

Then review:

- `docs/project-context/index.md`
- `docs/project-context/07-bootstrap-report.md`
- the managed bootstrap block in `AGENTS.md`

## 4. Review Codex defaults

Open `.codex/config.toml` and decide:

- approval policy
- sandbox mode
- whether cached web search is acceptable
- which subagents you actually want

## 5. Enable only the MCP servers you need

Start from `.codex/config.mcp.example.toml`.
Prefer the smallest tool surface that still helps your workflow.

## 6. Check the kit locally

```bash
scripts/check-kit.sh
```

## 7. Learn the quick commands

CodexKit now supports a quick command palette for faster day-to-day use:

- `/ck:bootstrap`
- `/ck:new-project billing-platform`
- `/ck:feature tenant-rate-limits`
- `/ck:plan-feature add per-tenant rate limits`
- `/ck:ready`
- `/ck:build phase 1`
- `/ck:review`
- `/ck:ship`

Read `docs/command-palette.md` for the full alias map, script-backed shortcuts, and payload rules.

## 8. Bootstrap a first initiative

### New project

```bash
scripts/new-project.sh billing-platform
```

### New feature

```bash
scripts/new-feature.sh tenant-rate-limits
```

## 9. Read these docs first

- `docs/bootstrap-playbook.md`
- `docs/project-memory-system.md`
- `docs/architecture-first-development.md`
- `docs/new-project-playbook.md`
- `docs/new-feature-playbook.md`
- `docs/brownfield-playbook.md`
- `docs/quality-gates.md`
