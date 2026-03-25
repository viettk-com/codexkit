#!/usr/bin/env python3
"""Validate bootstrap outputs when project context has been generated."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_DOCS = [
    'docs/project-context/index.md',
    'docs/project-context/01-repo-overview.md',
    'docs/project-context/02-architecture-map.md',
    'docs/project-context/03-build-test-and-quality-gates.md',
    'docs/project-context/04-domain-and-interfaces.md',
    'docs/project-context/05-change-boundaries.md',
    'docs/project-context/06-nfr-and-operability.md',
    'docs/project-context/07-bootstrap-report.md',
    'docs/project-context/08-project-constitution.md',
    'docs/project-context/09-module-index.md',
    'docs/project-context/10-delivery-system.md',
    'docs/project-context/11-hotspots-and-change-history.md',
    'docs/project-context/12-design-system-and-ux.md',
    'docs/project-context/13-agent-context.md',
    'docs/project-context/14-continuity.md',
    'docs/project-context/dashboard.md',
    '.codex/project-context/profile.json',
    '.codex/project-context/module-index.json',
    '.codex/project-context/dashboard.json',
    '.codex/project-context/continuity.json',
    '.codex/project-context/rules.json',
]


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    profile_path = root / '.codex/project-context/profile.json'
    docs_index = root / 'docs/project-context/index.md'

    if not profile_path.exists() and not docs_index.exists():
        print('[codexkit] no bootstrap outputs found')
        return 0

    missing = [path for path in REQUIRED_DOCS if not (root / path).exists()]
    if missing:
        print('\n'.join(f'missing bootstrap artifact: {item}' for item in missing))
        return 1

    try:
        data = json.loads(profile_path.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'invalid bootstrap profile json: {exc}')
        return 1

    for key in ['generated_at', 'repo_name', 'topology', 'commands', 'critical_directories', 'sensitive_areas']:
        if key not in data:
            print(f'bootstrap profile missing key: {key}')
            return 1

    agents_md = root / 'AGENTS.md'
    if agents_md.exists():
        text = agents_md.read_text(encoding='utf-8')
        if '<!-- CODEXKIT:BOOTSTRAP:START -->' not in text or '<!-- CODEXKIT:BOOTSTRAP:END -->' not in text:
            print('AGENTS.md missing bootstrap managed block markers')
            return 1

    print('[codexkit] bootstrap artifacts validated')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
