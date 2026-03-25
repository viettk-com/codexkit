#!/usr/bin/env python3
"""Infer the most relevant active initiative for the current branch or repo state."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def git_branch(root: Path) -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=root, stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except Exception:
        return ''


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else Path('.')
    root = root.resolve()
    active_dir = root / 'plans/active'
    if not active_dir.exists():
        return 1
    plans = sorted(p for p in active_dir.iterdir() if p.is_dir())
    if not plans:
        return 1
    branch = git_branch(root)
    match = None
    for plan in plans:
        slug = plan.name
        parts = slug.split('-')
        short_slug = '-'.join(parts[2:]) if len(parts) > 2 else slug
        if slug in branch or short_slug in branch:
            match = plan
            break
    if match is None:
        match = max(plans, key=lambda p: p.stat().st_mtime)
    data = {'path': match.as_posix(), 'name': match.name, 'branch': branch}
    if '--json' in sys.argv:
        print(json.dumps(data, ensure_ascii=False))
    else:
        print(match.as_posix())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
