#!/usr/bin/env python3
"""Archive an initiative, capture lessons learned, and refresh project context."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path


def detect_active(root: Path) -> Path | None:
    script = root / 'scripts/detect-active-initiative.py'
    if not script.exists():
        return None
    try:
        out = subprocess.check_output([sys.executable, str(script), str(root)], cwd=root, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return Path(out)
    except Exception:
        return None


def ensure_lessons(root: Path, plan_dir: Path) -> None:
    target = plan_dir / 'lessons-learned.md'
    if target.exists():
        return
    template = root / 'plans/templates/lessons-learned.md'
    if template.exists():
        text = template.read_text(encoding='utf-8')
        text = text.replace('{{TITLE}}', plan_dir.name).replace('{{DATE}}', str(date.today()))
    else:
        text = '# What changed\n\n# What worked well\n\n# What surprised us\n\n# Follow-up actions\n\n# Reusable lessons\n'
    target.write_text(text, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('initiative', nargs='?', help='path to initiative directory under plans/active')
    parser.add_argument('--root', default='.')
    parser.add_argument('--no-archive', action='store_true')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.initiative:
        candidate = Path(args.initiative)
        plan_dir = candidate if candidate.is_absolute() else (root / args.initiative)
    else:
        plan_dir = detect_active(root)
        if plan_dir is None:
            print('[codexkit] could not infer active initiative')
            return 1

    if not plan_dir.exists() or not plan_dir.is_dir():
        print(f'[codexkit] missing initiative directory: {plan_dir}')
        return 1

    ensure_lessons(root, plan_dir)
    target_dir = plan_dir
    if not args.no_archive:
        archive_dir = root / 'plans/archive'
        archive_dir.mkdir(parents=True, exist_ok=True)
        target_dir = archive_dir / plan_dir.name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.move(str(plan_dir), str(target_dir))

    refresh = root / 'scripts/refresh-project-context.py'
    if refresh.exists() and (root / '.codex/project-context/profile.json').exists():
        subprocess.run([sys.executable, str(refresh), str(root)], cwd=root, check=True)

    print(f'[codexkit] closeout complete: {target_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
