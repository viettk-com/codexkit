#!/usr/bin/env python3
"""Generate extended project context from the bootstrap profile."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IGNORE = {'.git', '.hg', '.svn', 'node_modules', '.next', '.nuxt', 'dist', 'build', 'coverage', '.venv', 'venv', '__pycache__'}
CODE_EXTS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs', '.rb', '.java', '.kt', '.php', '.swift', '.css', '.scss', '.sql'}


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        try:
            return path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return ''


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(safe_read(path))
    except Exception:
        return {}


def run_git(root: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except Exception:
        return ''


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---', 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def list_plans(base: Path) -> list[dict[str, str]]:
    if not base.exists():
        return []
    plans: list[dict[str, str]] = []
    for plan_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        plan_md = plan_dir / 'plan.md'
        meta = parse_frontmatter(safe_read(plan_md)) if plan_md.exists() else {}
        plans.append({
            'path': plan_dir.as_posix(),
            'name': plan_dir.name,
            'title': meta.get('title', plan_dir.name.replace('-', ' ')),
            'status': meta.get('status', 'unknown'),
            'change_class': meta.get('change_class', 'unknown'),
        })
    return plans


def current_branch(root: Path) -> str:
    branch = run_git(root, ['rev-parse', '--abbrev-ref', 'HEAD'])
    return branch or '(no git branch)'


def recent_commits(root: Path, limit: int = 8) -> list[dict[str, str]]:
    raw = run_git(root, ['log', f'-n{limit}', '--date=short', '--pretty=format:%ad|%h|%s'])
    out: list[dict[str, str]] = []
    for line in raw.splitlines():
        parts = line.split('|', 2)
        if len(parts) == 3:
            out.append({'date': parts[0], 'sha': parts[1], 'subject': parts[2]})
    return out


def hotspot_counts(root: Path) -> list[dict[str, Any]]:
    raw = run_git(root, ['log', '--since=180.days', '--name-only', '--pretty=format:'])
    counter: Counter[str] = Counter()
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        counter[line] += 1
    return [{'path': path, 'touches': count} for path, count in counter.most_common(15)]


def top_modules(root: Path, profile: dict[str, Any]) -> list[dict[str, Any]]:
    module_paths: set[str] = set()
    for item in profile.get('services', []):
        path = item.get('path')
        if path:
            module_paths.add(path)
    for item in profile.get('critical_directories', []):
        module_paths.add(item)
    for child in root.iterdir():
        if not child.is_dir() or child.name.startswith('.') or child.name in IGNORE:
            continue
        if child.name in {'docs', 'plans', 'runbooks', 'scripts'}:
            continue
        code_files = sum(1 for p in child.rglob('*') if p.is_file() and p.suffix.lower() in CODE_EXTS)
        if code_files:
            module_paths.add(child.relative_to(root).as_posix())
    modules: list[dict[str, Any]] = []
    for path in sorted(module_paths):
        abs_path = root / path
        if not abs_path.exists() or not abs_path.is_dir():
            continue
        code_files = [p for p in abs_path.rglob('*') if p.is_file() and p.suffix.lower() in CODE_EXTS][:200]
        manifest_names = [p.name for p in abs_path.rglob('*') if p.is_file() and p.name in {'package.json', 'pyproject.toml', 'go.mod', 'Cargo.toml', 'Gemfile'}][:10]
        kind = 'module'
        low = path.lower()
        if any(token in low for token in ('api', 'server', 'backend', 'service')):
            kind = 'service'
        elif any(token in low for token in ('web', 'frontend', 'ui', 'app')):
            kind = 'application'
        elif 'test' in low:
            kind = 'test surface'
        elif any(token in low for token in ('infra', 'deploy', 'terraform', 'helm')):
            kind = 'infrastructure'
        elif path.startswith('docs'):
            kind = 'documentation'
        modules.append({
            'path': path,
            'kind': kind,
            'code_files': len(code_files),
            'manifests': manifest_names,
        })
    return modules[:30]


def design_signals(root: Path, profile: dict[str, Any]) -> dict[str, Any]:
    frameworks = [str(x) for x in profile.get('frameworks', [])]
    frontend_stack = [fw for fw in frameworks if fw in {'react', 'next.js', 'vue', 'nuxt', 'svelte', 'angular', 'tailwind', 'storybook'}]
    paths: list[str] = []
    exact_names = {
        'tailwind.config.js', 'tailwind.config.ts', 'tailwind.config.cjs', 'tailwind.config.mjs',
        'postcss.config.js', 'postcss.config.cjs'
    }
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in IGNORE for part in rel.parts):
            continue
        rel_str = rel.as_posix()
        if path.is_dir() and rel.name in {'components', 'ui', 'styles', '.storybook', 'storybook'}:
            paths.append(rel_str)
        elif path.is_file() and path.name in exact_names:
            paths.append(rel_str)
        if len(paths) >= 20:
            break
    frontend_present = bool(frontend_stack or paths)
    return {
        'frontend_present': frontend_present,
        'frontend_stack': frontend_stack,
        'signals': sorted(dict.fromkeys(paths))[:20],
    }


def recurring_lessons(root: Path) -> list[str]:
    lessons: list[str] = []
    archive = root / 'plans/archive'
    if not archive.exists():
        return lessons
    for path in sorted(archive.rglob('lessons-learned.md'))[-12:]:
        text = safe_read(path)
        capture = False
        for line in text.splitlines():
            if line.strip().startswith('# Reusable lessons'):
                capture = True
                continue
            if capture:
                if line.startswith('#'):
                    break
                line = line.strip().lstrip('-').strip()
                if line:
                    lessons.append(line)
    uniq: list[str] = []
    seen: set[str] = set()
    for lesson in lessons:
        if lesson not in seen:
            uniq.append(lesson)
            seen.add(lesson)
    return uniq[:12]


def default_principles(profile: dict[str, Any], design: dict[str, Any]) -> list[str]:
    principles = [
        'understand the current boundary before editing across it',
        'prefer small reversible slices over broad speculative rewrites',
        'keep validation commands explicit and runnable by another engineer',
        'treat rollback, observability, and docs updates as part of delivery, not afterthoughts',
    ]
    if profile.get('datastores'):
        principles.append('use additive migrations and explicit compatibility notes for persistent data changes')
    if profile.get('sensitive_areas'):
        principles.append('route changes touching sensitive areas through the matching specialist review before merge')
    if design.get('frontend_present'):
        principles.append('extend existing design tokens and component primitives before inventing new ui patterns')
    if profile.get('topology', {}).get('style') in {'monorepo', 'service-oriented repository'}:
        principles.append('keep module-local guidance close to the module when commands or contracts differ materially')
    return principles


def dashboard_data(root: Path, profile: dict[str, Any], modules: list[dict[str, Any]], design: dict[str, Any]) -> dict[str, Any]:
    active = list_plans(root / 'plans/active')
    archived = list_plans(root / 'plans/archive')
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'branch': current_branch(root),
        'repo_summary': {
            'name': profile.get('repo_name', root.name),
            'topology': profile.get('topology', {}),
            'frameworks': profile.get('frameworks', []),
            'critical_directories': profile.get('critical_directories', []),
            'sensitive_areas': profile.get('sensitive_areas', []),
        },
        'active_initiatives': active,
        'archived_initiative_count': len(archived),
        'recent_commits': recent_commits(root),
        'hotspots': hotspot_counts(root),
        'modules': modules,
        'design': design,
        'recurring_lessons': recurring_lessons(root),
    }


def md_list(items: list[str], empty: str = 'none') -> str:
    return '\n'.join(f'- {item}' for item in items) if items else f'- {empty}'


def render_constitution(profile: dict[str, Any], design: dict[str, Any]) -> str:
    principles = default_principles(profile, design)
    sensitive = profile.get('sensitive_areas', [])
    commands = profile.get('commands', {}).get('commands', {}) or {}
    critical = profile.get('critical_directories', [])
    lines = [
        '# Project constitution',
        '',
        f'Generated: {datetime.now(timezone.utc).isoformat(timespec="seconds")}',
        '',
        '## Why this exists',
        '',
        'This document turns repository facts and durable lessons into a small set of principles that future plans, tasks, and reviews should follow by default.',
        '',
        '## Product and engineering principles',
        '',
        md_list(principles),
        '',
        '## Architecture invariants',
        '',
        md_list([f'preserve the boundary around `{item}` unless the change explicitly redesigns it' for item in critical], empty='no critical directories inferred yet'),
        '',
        '## Review triggers',
        '',
        md_list([f'changes touching `{item}` should trigger the relevant specialist review' for item in sensitive], empty='no specialist review triggers were inferred automatically'),
        '',
        '## Quality gates',
        '',
        md_list([f'{key}: `{value}`' for key, value in commands.items()], empty='confirm canonical validation commands manually'),
        '',
        '## Forbidden shortcuts',
        '',
        '- skipping architecture work for l1+ changes just because implementation feels easy',
        '- merging risky changes without rollback notes',
        '- changing contracts or schemas without compatibility reasoning',
        '- adding new ui primitives when existing shared primitives should be extended instead',
        '',
    ]
    return '\n'.join(lines)


def render_module_index(modules: list[dict[str, Any]]) -> str:
    lines = ['# Module index', '', 'This file is a bootstrap-generated index of the modules or subsystems most likely to matter for planning and review.', '']
    if not modules:
        lines.append('No module candidates were inferred.')
        lines.append('')
        return '\n'.join(lines)
    for module in modules:
        manifests = ', '.join(module.get('manifests', [])) or 'no local manifest detected'
        lines.extend([
            f"## `{module['path']}`",
            '',
            f"- kind: {module['kind']}",
            f"- code files observed: {module['code_files']}",
            f"- manifests: {manifests}",
            '',
        ])
    return '\n'.join(lines)


def render_delivery(profile: dict[str, Any], dashboard: dict[str, Any]) -> str:
    commands = profile.get('commands', {}).get('commands', {}) or {}
    active_lines = [f"- `{item['name']}` ({item['change_class']}, {item['status']})" for item in dashboard['active_initiatives']]
    lines = [
        '# Delivery system',
        '',
        '## Canonical commands',
        '',
        md_list([f'{key}: `{value}`' for key, value in commands.items()], empty='confirm commands manually'),
        '',
        '## Default lifecycle',
        '',
        '1. `$bootstrap`',
        '2. `$continuity-memory`',
        '3. `$constitution-governance`',
        '4. `$architecture-discovery` and `$nfr-capture`',
        '5. `$plan-feature`',
        '6. `$task-breakdown`',
        '7. `$artifact-consistency`',
        '8. `$implementation-readiness`',
        '9. `$execute-plan` or `$fix-issue`',
        '10. `$closeout-learning`',
        '',
        '## Active initiatives',
        '',
        '\n'.join(active_lines) if active_lines else '- no active initiatives detected',
        '',
        '## Branch and initiative hygiene',
        '',
        '- prefer one initiative directory per meaningful change',
        '- keep tasks small enough that a reviewer can reason about them in one sitting',
        '- refresh project context after major structural changes or initiative closeout',
        '',
    ]
    return '\n'.join(lines)


def render_hotspots(dashboard: dict[str, Any]) -> str:
    hotspot_lines = [f"- `{item['path']}` ({item['touches']} touches in recent git history)" for item in dashboard['hotspots']]
    commit_lines = [f"- {item['date']} `{item['sha']}` {item['subject']}" for item in dashboard['recent_commits']]
    lines = [
        '# Hotspots and recent change history',
        '',
        '## Current branch',
        '',
        f"- `{dashboard['branch']}`",
        '',
        '## Recent commit headlines',
        '',
        '\n'.join(commit_lines) if commit_lines else '- no recent commit history available',
        '',
        '## Git hotspots',
        '',
        '\n'.join(hotspot_lines) if hotspot_lines else '- no recent git hotspot data available',
        '',
    ]
    return '\n'.join(lines)


def render_design(design: dict[str, Any]) -> str:
    lines = [
        '# Design system and UX',
        '',
        '## Frontend present',
        '',
        f"- {'yes' if design['frontend_present'] else 'no clear frontend signals detected'}",
        '',
        '## Frontend stack hints',
        '',
        md_list(design.get('frontend_stack', []), empty='no stack hints detected'),
        '',
        '## Design-system evidence',
        '',
        md_list([f'`{item}`' for item in design.get('signals', [])], empty='no obvious design-system files or directories detected'),
        '',
        '## Guardrails',
        '',
        '- prefer existing shared components over one-off ui primitives',
        '- preserve token sources and theme files as system boundaries',
        '- treat accessibility rules as part of architecture quality, not polish',
        '',
    ]
    return '\n'.join(lines)


def render_agent_context(profile: dict[str, Any], dashboard: dict[str, Any]) -> str:
    commands = profile.get('commands', {}).get('commands', {}) or {}
    lines = [
        '# Agent context',
        '',
        'Read this file after `index.md` when you need a condensed repo brief.',
        '',
        '## First things to know',
        '',
        f"- repo summary: {profile.get('topology', {}).get('style', 'unknown topology')} | frameworks: {', '.join(profile.get('frameworks', [])[:6]) or 'none inferred'}",
        f"- critical directories: {', '.join(profile.get('critical_directories', [])) or 'none inferred'}",
        f"- sensitive areas: {', '.join(profile.get('sensitive_areas', [])) or 'none inferred'}",
        f"- current branch: {dashboard['branch']}",
        '',
        '## Use these commands first',
        '',
        md_list([f'{key}: `{value}`' for key, value in commands.items()], empty='confirm commands manually'),
        '',
        '## Active work',
        '',
        md_list([f"`{item['name']}` ({item['change_class']}, {item['status']})" for item in dashboard['active_initiatives']], empty='no active initiatives detected'),
        '',
        '## Where to look next',
        '',
        '- architecture: `docs/project-context/02-architecture-map.md`',
        '- constitution: `docs/project-context/08-project-constitution.md`',
        '- continuity: `docs/project-context/14-continuity.md`',
        '- module map: `docs/project-context/09-module-index.md`',
        '',
    ]
    return '\n'.join(lines)


def render_continuity(dashboard: dict[str, Any]) -> str:
    lines = [
        '# Continuity',
        '',
        '## Memory tiers in this repo',
        '',
        '- working: `plans/active/`',
        '- episodic: `plans/archive/`, initiative reports, lessons learned',
        '- semantic: `docs/project-context/` and runbooks',
        '- deep-search: `.codex/project-context/*.json`',
        '',
        '## Active initiatives',
        '',
        md_list([f"`{item['name']}` ({item['change_class']}, {item['status']})" for item in dashboard['active_initiatives']], empty='no active initiatives detected'),
        '',
        '## Reusable lessons',
        '',
        md_list(dashboard['recurring_lessons'], empty='no archived reusable lessons detected yet'),
        '',
        '## Keep this healthy',
        '',
        '- update continuity after incidents, migrations, and surprising reviews',
        '- archive completed initiatives',
        '- refresh context after structural repo changes',
        '',
    ]
    return '\n'.join(lines)


def render_dashboard(dashboard: dict[str, Any]) -> str:
    active_lines = [f"- `{item['name']}` | {item['change_class']} | {item['status']}" for item in dashboard['active_initiatives']]
    hotspot_lines = [f"- `{item['path']}` ({item['touches']})" for item in dashboard['hotspots'][:10]]
    lesson_lines = [f"- {item}" for item in dashboard['recurring_lessons']]
    lines = [
        '# Dashboard',
        '',
        f"Generated: {dashboard['generated_at']}",
        '',
        '## Repo summary',
        '',
        f"- branch: `{dashboard['branch']}`",
        f"- topology: {dashboard['repo_summary']['topology'].get('style', 'unknown')}",
        f"- frameworks: {', '.join(dashboard['repo_summary'].get('frameworks', [])[:6]) or 'none inferred'}",
        '',
        '## Active initiatives',
        '',
        '\n'.join(active_lines) if active_lines else '- no active initiatives detected',
        '',
        '## Hotspots',
        '',
        '\n'.join(hotspot_lines) if hotspot_lines else '- no hotspot data available',
        '',
        '## Reusable lessons',
        '',
        '\n'.join(lesson_lines) if lesson_lines else '- no reusable lessons detected yet',
        '',
    ]
    return '\n'.join(lines)


def update_index(docs_dir: Path) -> None:
    index = docs_dir / 'index.md'
    if not index.exists():
        return
    text = safe_read(index)
    extension = (
        '## Extended repository memory\n\n'
        '- `08-project-constitution.md`\n'
        '- `09-module-index.md`\n'
        '- `10-delivery-system.md`\n'
        '- `11-hotspots-and-change-history.md`\n'
        '- `12-design-system-and-ux.md`\n'
        '- `13-agent-context.md`\n'
        '- `14-continuity.md`\n'
        '- `dashboard.md`\n'
    )
    if '## Extended repository memory\n' in text:
        text = re.sub(r'## Extended repository memory\n(?:.|\n)*', extension, text)
    else:
        text = text.rstrip() + '\n\n' + extension
    index.write_text(text, encoding='utf-8')


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    root = root.resolve()
    profile_path = root / '.codex/project-context/profile.json'
    if not profile_path.exists():
        print('[codexkit] missing bootstrap profile, run bootstrap first')
        return 1

    profile = load_json(profile_path)
    docs_dir = root / 'docs/project-context'
    machine_dir = root / '.codex/project-context'
    docs_dir.mkdir(parents=True, exist_ok=True)
    machine_dir.mkdir(parents=True, exist_ok=True)

    modules = top_modules(root, profile)
    design = design_signals(root, profile)
    dashboard = dashboard_data(root, profile, modules, design)

    (docs_dir / '08-project-constitution.md').write_text(render_constitution(profile, design), encoding='utf-8')
    (docs_dir / '09-module-index.md').write_text(render_module_index(modules), encoding='utf-8')
    (docs_dir / '10-delivery-system.md').write_text(render_delivery(profile, dashboard), encoding='utf-8')
    (docs_dir / '11-hotspots-and-change-history.md').write_text(render_hotspots(dashboard), encoding='utf-8')
    (docs_dir / '12-design-system-and-ux.md').write_text(render_design(design), encoding='utf-8')
    (docs_dir / '13-agent-context.md').write_text(render_agent_context(profile, dashboard), encoding='utf-8')
    (docs_dir / '14-continuity.md').write_text(render_continuity(dashboard), encoding='utf-8')
    (docs_dir / 'dashboard.md').write_text(render_dashboard(dashboard), encoding='utf-8')

    (machine_dir / 'module-index.json').write_text(json.dumps({'modules': modules}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (machine_dir / 'dashboard.json').write_text(json.dumps(dashboard, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (machine_dir / 'continuity.json').write_text(json.dumps({'recurring_lessons': dashboard['recurring_lessons'], 'active_initiatives': dashboard['active_initiatives']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (machine_dir / 'rules.json').write_text(json.dumps({
        'generated_at': dashboard['generated_at'],
        'branch': dashboard['branch'],
        'critical_directories': profile.get('critical_directories', []),
        'sensitive_areas': profile.get('sensitive_areas', []),
        'commands': profile.get('commands', {}).get('commands', {}),
        'principles': default_principles(profile, design),
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    (docs_dir / 'README.md').write_text(
        '# Project context memory\n\n'
        'Run `scripts/bootstrap-codexkit.py --apply` or call `$bootstrap` to populate this directory.\n\n'
        'Bootstrap now writes both the original repo profile and the extended memory set:\n\n'
        '- `01-repo-overview.md`\n'
        '- `02-architecture-map.md`\n'
        '- `03-build-test-and-quality-gates.md`\n'
        '- `04-domain-and-interfaces.md`\n'
        '- `05-change-boundaries.md`\n'
        '- `06-nfr-and-operability.md`\n'
        '- `07-bootstrap-report.md`\n'
        '- `08-project-constitution.md`\n'
        '- `09-module-index.md`\n'
        '- `10-delivery-system.md`\n'
        '- `11-hotspots-and-change-history.md`\n'
        '- `12-design-system-and-ux.md`\n'
        '- `13-agent-context.md`\n'
        '- `14-continuity.md`\n'
        '- `dashboard.md`\n',
        encoding='utf-8',
    )

    (machine_dir / 'README.md').write_text(
        '# Project context machine profile\n\n'
        'This directory is managed by CodexKit bootstrap.\n\n'
        'After running `scripts/bootstrap-codexkit.py --apply`, it contains:\n\n'
        '- `profile.json` - machine-readable repository profile\n'
        '- `module-index.json` - discovered modules and subsystem map\n'
        '- `dashboard.json` - active initiatives, hotspots, and recent git signals\n'
        '- `continuity.json` - recurring lessons and active initiative summaries\n'
        '- `rules.json` - condensed guardrails for agents and automations\n',
        encoding='utf-8',
    )

    update_index(docs_dir)
    print('[codexkit] refreshed extended project context')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
