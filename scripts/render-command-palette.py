#!/usr/bin/env python3
"""Render command palette docs and prompt wrappers from the alias registry."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / '.codex' / 'command-aliases.json'
DOC_PATH = ROOT / 'docs' / 'command-palette.md'
PROMPT_DIR = ROOT / '.github' / 'codex' / 'prompts'

CATEGORY_TITLES = {
    'meta': 'Meta',
    'discover': 'Discover',
    'scaffold': 'Scaffold',
    'design': 'Design',
    'build': 'Build',
    'quality': 'Quality',
    'ship': 'Ship',
}

CATEGORY_INTRO = {
    'meta': 'Shortcuts that help you remember or route the rest of the command surface.',
    'discover': 'Commands that recover repository understanding and durable project memory.',
    'scaffold': 'Commands that create initiative artifacts or kick off a new project or feature lane.',
    'design': 'Commands for spec, architecture, NFRs, planning, and implementation readiness.',
    'build': 'Commands for implementation, debugging, testing, contracts, and migrations.',
    'quality': 'Commands for review, security, performance, docs, design-system fit, and CI.',
    'ship': 'Commands for PR prep, release readiness, incident triage, and initiative closeout.',
}


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding='utf-8'))


def fmt_list(values: list[str], limit: int | None = None) -> str:
    items = values if limit is None else values[:limit]
    return ', '.join(f'`{item}`' for item in items) if items else '—'


def short_examples(data: dict) -> list[str]:
    return [
        '`/ck:bootstrap`',
        '`/ck:feature tenant-rate-limits`',
        '`/ck:plan-feature add per-tenant rate limits with rollback-safe migration`',
        '`/ck:ready`',
        '`/ck:build phase 1`',
        '`/ck:review`',
        '`/ck:ship`',
        '`$ck-plan add rate limits to tenant middleware`',
    ]


def render_doc(data: dict) -> str:
    lines: list[str] = []
    lines.append('# Command palette')
    lines.append('')
    lines.append('CodexKit supports a thin quick-command layer inspired by command-driven kits like Superpowers, Spec Kit, and CodyMaster, but kept Codex-native: aliases resolve into the same canonical skills, agents, scripts, and artifacts that already power the repository workflow.')
    lines.append('')
    lines.append('## Supported forms')
    lines.append('')
    lines.append(f'- chat shorthand: `{data["forms"]["chat"]}`')
    lines.append(f'- skill shorthand: `{data["forms"]["skill"]}`')
    lines.append(f'- canonical skill form: `{data["forms"]["canonical_skill"]}`')
    lines.append('')
    lines.append('Aliases are **wrappers, not a second workflow system**. They should never bypass architecture, readiness, or review gates.')
    lines.append('')
    lines.append('## Routing rules')
    lines.append('')
    for rule in data['routing_rules']:
        lines.append(f'- {rule}')
    lines.append('')
    lines.append('## Quick examples')
    lines.append('')
    for item in short_examples(data):
        lines.append(f'- {item}')
    lines.append('')
    lines.append('## Command groups')
    lines.append('')

    aliases = data['aliases']
    for category in CATEGORY_TITLES:
        group = [entry for entry in aliases if entry['category'] == category]
        if not group:
            continue
        lines.append(f'### {CATEGORY_TITLES[category]}')
        lines.append('')
        lines.append(CATEGORY_INTRO[category])
        lines.append('')
        lines.append('| Alias | Expands to | Related agents / scripts | Use for |')
        lines.append('|---|---|---|---|')
        for entry in group:
            alias = f'`{entry["slash_forms"][0]}`'
            expands = fmt_list(entry['skills'])
            related_parts: list[str] = []
            if entry['agents']:
                related_parts.append(f"agents: {fmt_list(entry['agents'], limit=3)}")
            if entry['scripts']:
                related_parts.append(f"scripts: {fmt_list(entry['scripts'], limit=2)}")
            related = '<br>'.join(related_parts) if related_parts else '—'
            summary = entry['summary']
            lines.append(f'| {alias} | {expands} | {related} | {summary} |')
        lines.append('')

    lines.append('## Payload handling')
    lines.append('')
    lines.append('Anything after the first alias token is payload. Preserve that payload and pass it into the resolved workflow.')
    lines.append('')
    lines.append('Examples:')
    lines.append('')
    lines.append('- `/ck:project billing-platform` -> run `scripts/new-project.sh billing-platform`, then continue with `$project-bootstrap`, `$architecture-review`, and `$plan-feature`')
    lines.append('- `/ck:init L2 tenant import backfill` -> run `scripts/new-initiative.sh [--branch] <L0|L1|L2|L3> <slug-or-title>` with the supplied class and title, then continue with the mapped planning lane')
    lines.append('- `/ck:plan-furture add tenant quotas` -> normalize to `/ck:plan-feature`, then run `$plan-feature`')
    lines.append('')
    lines.append('## Customizing aliases')
    lines.append('')
    lines.append('1. Edit `.codex/command-aliases.json`.')
    lines.append('2. Run `python3 scripts/render-command-palette.py` to regenerate this document and the prompt wrappers.')
    lines.append('3. Run `python3 scripts/validate-aliases.py` and then `scripts/check-kit.sh`.')
    lines.append('')
    lines.append('## Source of truth')
    lines.append('')
    lines.append('- registry: `.codex/command-aliases.json`')
    lines.append('- router skill: `.agents/skills/command-router/SKILL.md`')
    lines.append('- resolver cli: `python3 scripts/resolve-command-alias.py /ck:plan-feature`')
    lines.append('')
    return '\n'.join(lines) + '\n'


def prompt_slug(entry: dict) -> str:
    return f"ck-{entry['alias']}.md"


def render_prompt(entry: dict) -> str:
    slash = ', '.join(f'`{form}`' for form in entry['slash_forms'])
    skill = ', '.join(f'`{form}`' for form in entry['skill_forms'])
    skills = '\n'.join(f'- {item}' for item in entry['skills']) or '- (none)'
    agents = '\n'.join(f'- {item}' for item in entry['agents']) or '- (none)'
    scripts = '\n'.join(f'- {item}' for item in entry['scripts']) or '- (none)'
    artifacts = '\n'.join(f'- {item}' for item in entry['artifacts']) or '- (none)'
    lines = [
        '<!-- generated by scripts/render-command-palette.py -->',
        f'# {entry["alias"]}',
        '',
        f'Equivalent quick commands: {slash}.',
        f'Equivalent skill shorthands: {skill}.',
        '',
        f'Use the `command-router` alias logic, then route to these canonical skills:',
        skills,
        '',
        'Related agents:',
        agents,
        '',
        'Related scripts:',
        scripts,
        '',
        'Typical artifacts touched:',
        artifacts,
        '',
        'Instructions:',
        '- preserve any payload after the alias and pass it into the resolved workflow',
        '- read `docs/project-context/index.md` and `AGENTS.md` before risky work',
        '- keep the result architecture-safe and proportional to the change class',
        f'- note: {entry["notes"]}',
        '',
        'Output format:',
        '# Resolved command',
        '## Canonical workflow',
        '## Next artifact or command',
        '## Key risks or assumptions',
        '',
    ]
    return '\n'.join(lines)


def render_prompts(data: dict) -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in PROMPT_DIR.glob('ck-*.md'):
        stale.unlink()
    for entry in data['aliases']:
        if not entry.get('prompt_wrapper'):
            continue
        (PROMPT_DIR / prompt_slug(entry)).write_text(render_prompt(entry), encoding='utf-8')


def main() -> int:
    data = load_registry()
    DOC_PATH.write_text(render_doc(data), encoding='utf-8')
    render_prompts(data)
    count = sum(1 for entry in data['aliases'] if entry.get('prompt_wrapper'))
    print(f'rendered {DOC_PATH} and {count} quick prompt wrappers')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
