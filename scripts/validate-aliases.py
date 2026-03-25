#!/usr/bin/env python3
"""Validate the CodexKit quick-command registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / '.codex' / 'command-aliases.json'
CONFIG = ROOT / '.codex' / 'config.toml'
SKILLS_DIR = ROOT / '.agents' / 'skills'
PROMPT_DIR = ROOT / '.github' / 'codex' / 'prompts'

FORM_RE = re.compile(r'^(?:/ck:[a-z0-9-]+|\$ck-[a-z0-9-]+)$')
AGENT_RE = re.compile(r'^\[agents\.([a-z_]+)\]$', re.MULTILINE)
SCRIPT_PATH_RE = re.compile(r'(scripts/[A-Za-z0-9._/-]+)')


def load_registry() -> dict:
    try:
        return json.loads(REGISTRY.read_text(encoding='utf-8'))
    except FileNotFoundError:
        raise SystemExit(f'missing registry: {REGISTRY}')


def main() -> int:
    data = load_registry()
    errors: list[str] = []

    if data.get('namespace') != 'ck':
        errors.append('namespace must be ck')

    aliases = data.get('aliases', [])
    if not aliases:
        errors.append('registry must contain aliases')

    seen_alias: set[str] = set()
    seen_forms: set[str] = set()
    known_skills = {p.name for p in SKILLS_DIR.iterdir() if (p / 'SKILL.md').exists()}
    known_agents = set(AGENT_RE.findall(CONFIG.read_text(encoding='utf-8')))

    required = {'help', 'bootstrap', 'plan', 'build', 'review', 'ship', 'close'}

    for entry in aliases:
        alias = entry.get('alias', '')
        if not alias:
            errors.append('alias entry missing alias')
            continue
        if alias in seen_alias:
            errors.append(f'duplicate alias: {alias}')
        seen_alias.add(alias)
        if '/' in alias or ':' in alias or ' ' in alias:
            errors.append(f"invalid alias token: {alias}")

        for field in ('slash_forms', 'skill_forms', 'skills', 'agents', 'scripts', 'artifacts'):
            value = entry.get(field)
            if not isinstance(value, list):
                errors.append(f'{alias}: {field} must be a list')

        for form in entry.get('slash_forms', []) + entry.get('skill_forms', []):
            if not FORM_RE.match(form):
                errors.append(f'{alias}: invalid form {form}')
            if form in seen_forms:
                errors.append(f'duplicate form: {form}')
            seen_forms.add(form)

        for skill in entry.get('skills', []):
            if not skill.startswith('$'):
                errors.append(f'{alias}: skill must start with $: {skill}')
                continue
            skill_name = skill[1:]
            if skill_name not in known_skills:
                errors.append(f'{alias}: unknown skill {skill}')

        for agent in entry.get('agents', []):
            if agent not in known_agents:
                errors.append(f'{alias}: unknown agent {agent}')

        for command in entry.get('scripts', []):
            for match in SCRIPT_PATH_RE.findall(command):
                if not (ROOT / match).exists():
                    errors.append(f'{alias}: missing script path {match}')

        if entry.get('prompt_wrapper'):
            prompt_path = PROMPT_DIR / f'ck-{alias}.md'
            if not prompt_path.exists():
                errors.append(f'{alias}: missing generated prompt wrapper {prompt_path.relative_to(ROOT)}')

    missing = required - seen_alias
    if missing:
        errors.append(f'missing required aliases: {", ".join(sorted(missing))}')

    if errors:
        print('\n'.join(errors))
        return 1

    print(f'validated {len(aliases)} aliases')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
