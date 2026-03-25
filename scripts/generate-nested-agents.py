#!/usr/bin/env python3
"""Generate simple nested AGENTS.md files for major modules."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TEMPLATE = '''# AGENTS.md

This file adds local guidance for the `{path}` module.

## Relationship to root guidance

Read the repository root `AGENTS.md` first. This file only adds module-local notes.

## Module summary

- kind: {kind}
- manifests: {manifests}

## Local guidance to customize

- local test command: `<replace-me>`
- local build command: `<replace-me>`
- module-sensitive paths: `<replace-me>`
- public contracts owned here: `<replace-me>`
- generated files to avoid editing directly: `<replace-me>`
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    module_index = root / '.codex/project-context/module-index.json'
    if not module_index.exists():
        print('[codexkit] missing module index, run bootstrap first')
        return 1
    data = json.loads(module_index.read_text(encoding='utf-8'))
    count = 0
    for module in data.get('modules', []):
        path = root / module['path']
        if not path.exists() or not path.is_dir():
            continue
        target = path / 'AGENTS.md'
        if target.exists() and not args.force:
            continue
        text = TEMPLATE.format(path=module['path'], kind=module.get('kind', 'module'), manifests=', '.join(module.get('manifests', [])) or 'none')
        target.write_text(text, encoding='utf-8')
        count += 1
    print(f'[codexkit] wrote {count} nested AGENTS.md files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
