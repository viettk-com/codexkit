#!/usr/bin/env python3
"""Resolve CodexKit quick commands from the alias registry."""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / '.codex' / 'command-aliases.json'


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding='utf-8'))


def normalize(token: str) -> str:
    token = token.strip().lower()
    if not token:
        return ''
    if token.startswith('/ck:'):
        token = token[4:]
    elif token.startswith('$ck-'):
        token = token[4:]
    token = token.replace('_', '-').replace(' ', '-')
    while '--' in token:
        token = token.replace('--', '-')
    return token.strip('-')


def registry_index(data: dict) -> tuple[dict[str, dict], dict[str, str]]:
    by_alias: dict[str, dict] = {}
    by_token: dict[str, str] = {}
    for entry in data['aliases']:
        alias = entry['alias']
        by_alias[alias] = entry
        tokens = {alias, *entry.get('synonyms', []), *entry.get('typos', [])}
        for form in entry.get('slash_forms', []) + entry.get('skill_forms', []):
            tokens.add(normalize(form))
        for token in tokens:
            key = normalize(token)
            if key and key not in by_token:
                by_token[key] = alias
    return by_alias, by_token


def resolve(query: str, data: dict) -> tuple[dict | None, list[str]]:
    by_alias, by_token = registry_index(data)
    key = normalize(query)
    if key in by_alias:
        return by_alias[key], []
    alias = by_token.get(key)
    if alias:
        return by_alias[alias], []
    choices = sorted(set(by_token) | set(by_alias))
    suggestions = difflib.get_close_matches(key, choices, n=5, cutoff=0.55)
    return None, suggestions


def print_help(data: dict) -> None:
    print('CodexKit quick commands')
    print('')
    for category in ('meta', 'discover', 'scaffold', 'design', 'build', 'quality', 'ship'):
        group = [entry for entry in data['aliases'] if entry['category'] == category]
        if not group:
            continue
        print(f'[{category}]')
        for entry in group:
            print(f"- {entry['slash_forms'][0]:<18} -> {', '.join(entry['skills'])}")
        print('')


def main(argv: list[str]) -> int:
    data = load_registry()
    if len(argv) < 2 or argv[1] in {'help', '--help', '-h', '/ck:help', '$ck-help'}:
        print_help(data)
        return 0

    query = argv[1]
    entry, suggestions = resolve(query, data)
    if not entry:
        print(f'No exact alias for: {query}')
        if suggestions:
            print('Closest matches:')
            for item in suggestions:
                print(f'- /ck:{item}')
        return 1

    print(f"alias: {entry['alias']}")
    print(f"summary: {entry['summary']}")
    print('slash forms: ' + ', '.join(entry['slash_forms']))
    print('skill forms: ' + ', '.join(entry['skill_forms']))
    print('canonical skills: ' + (', '.join(entry['skills']) or '—'))
    print('agents: ' + (', '.join(entry['agents']) or '—'))
    print('scripts: ' + (', '.join(entry['scripts']) or '—'))
    print('artifacts: ' + (', '.join(entry['artifacts']) or '—'))
    print('notes: ' + entry['notes'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
