#!/usr/bin/env python3
"""Deeply scan a repository and adapt CodexKit guidance to it.

This script is intentionally dependency-free so it can run in fresh repos.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

IGNORE_DIRS = {
    '.git', '.hg', '.svn', '.idea', '.vscode', '.next', '.nuxt', '.turbo', '.yarn', '.codex', '.agents', '.claude', '.cursor', '.windsurf',
    '.pnpm-store', '.venv', 'venv', '__pycache__', '.mypy_cache', '.pytest_cache',
    'node_modules', 'dist', 'build', 'coverage', 'vendor', 'target', 'bin', 'obj',
    '.codex/cache', 'docs/project-context', '.codex/project-context', '.agents', '.codex/agents'
}
MAX_FILES = 15000
MAX_ENTRYPOINTS = 20
MAX_LIST = 12
MAX_DOCS = 20
BOOTSTRAP_START = '<!-- CODEXKIT:BOOTSTRAP:START -->'
BOOTSTRAP_END = '<!-- CODEXKIT:BOOTSTRAP:END -->'

LANGUAGE_EXTENSIONS = {
    '.ts': 'typescript', '.tsx': 'typescript', '.js': 'javascript', '.jsx': 'javascript',
    '.mjs': 'javascript', '.cjs': 'javascript', '.py': 'python', '.rb': 'ruby', '.go': 'go',
    '.rs': 'rust', '.java': 'java', '.kt': 'kotlin', '.kts': 'kotlin', '.swift': 'swift',
    '.php': 'php', '.cs': 'csharp', '.scala': 'scala', '.sh': 'shell', '.sql': 'sql',
    '.yml': 'yaml', '.yaml': 'yaml', '.json': 'json', '.toml': 'toml'
}

FRAMEWORK_HINTS = {
    'next': 'next.js', 'react': 'react', 'vue': 'vue', 'nuxt': 'nuxt', 'svelte': 'svelte',
    'angular': 'angular', 'express': 'express', 'nestjs': 'nest', 'fastify': 'fastify',
    'koa': 'koa', 'fastapi': 'fastapi', 'django': 'django', 'flask': 'flask',
    'celery': 'celery', 'pytest': 'pytest', 'ruff': 'ruff', 'mypy': 'mypy',
    'pydantic': 'pydantic', 'sqlalchemy': 'sqlalchemy', 'prisma': 'prisma',
    'typeorm': 'typeorm', 'sequelize': 'sequelize', 'drizzle-orm': 'drizzle',
    'tailwindcss': 'tailwind', 'vite': 'vite', 'vitest': 'vitest', 'jest': 'jest',
    '@playwright/test': 'playwright', 'cypress': 'cypress', 'storybook': 'storybook',
    'rails': 'rails', 'rspec': 'rspec', 'rubocop': 'rubocop', 'sinatra': 'sinatra',
    'gin': 'gin', 'fiber': 'fiber', 'echo': 'echo', 'axum': 'axum', 'actix-web': 'actix',
    'tokio': 'tokio', 'spring-boot-starter-web': 'spring boot', 'laravel/framework': 'laravel'
}

DATASTORE_HINTS = {
    'pg': 'postgres', 'postgresql': 'postgres', 'psycopg': 'postgres', 'psycopg2': 'postgres',
    'mysql': 'mysql', 'sqlite': 'sqlite', 'redis': 'redis', 'mongodb': 'mongodb',
    'mongoose': 'mongodb', 'prisma': 'sql database', 'sqlalchemy': 'sql database',
    'typeorm': 'sql database', 'sequelize': 'sql database', 'drizzle-orm': 'sql database',
    'kysely': 'sql database'
}

INTEGRATION_HINTS = {
    'stripe': 'stripe', 'braintree': 'payments', 'paypal': 'payments', 'sentry': 'sentry',
    '@sentry/': 'sentry', 'opentelemetry': 'opentelemetry', 'prometheus': 'prometheus',
    'datadog': 'datadog', 'newrelic': 'new relic', 'kafka': 'kafka', 'rabbitmq': 'rabbitmq',
    'nats': 'nats', 'bullmq': 'bullmq', 'aws-sdk': 'aws', '@aws-sdk/': 'aws',
    'google-cloud': 'gcp', '@google-cloud/': 'gcp', 'firebase': 'firebase',
    'supabase': 'supabase', 'cloudflare': 'cloudflare'
}

QUALITY_SCRIPT_PRIORITY = {
    'test': ['test:ci', 'test', 'check', 'verify'],
    'lint': ['lint', 'lint:ci', 'eslint', 'check:lint'],
    'typecheck': ['typecheck', 'check-types', 'types', 'tsc', 'check:type'],
    'build': ['build', 'compile', 'package'],
    'perf-smoke': ['perf', 'perf:smoke', 'benchmark']
}

SENSITIVE_KEYWORDS = [
    'auth', 'login', 'oauth', 'permission', 'policy', 'security', 'secret', 'secrets',
    'payment', 'billing', 'invoice', 'checkout', 'subscription', 'customer',
    'db', 'database', 'schema', 'migration', 'migrations', 'alembic', 'prisma',
    'terraform', 'infra', 'k8s', 'kubernetes', 'helm', 'deploy', 'release', 'prod',
    'queue', 'worker', 'cron', 'session', 'token', 'gateway', 'public-api', 'openapi'
]

DOC_PRIORITY = [
    'AGENTS.md', 'README.md', 'ARCHITECTURE.md', 'docs/README.md', 'docs/architecture.md',
    'docs/system-architecture.md', 'docs/project-overview-pdr.md', 'CLAUDE.md'
]


def git_root(start: Path) -> Path:
    try:
        out = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=start, stderr=subprocess.DEVNULL)
        return Path(out.decode('utf-8').strip()).resolve()
    except Exception:
        return start.resolve()


def should_ignore(path: Path) -> bool:
    parts = set(path.parts)
    return any(token in parts for token in IGNORE_DIRS)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob('*'):
        if path.is_dir() and should_ignore(path.relative_to(root)):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if should_ignore(rel):
            continue
        files.append(rel)
        if len(files) >= MAX_FILES:
            break
    return files


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return ''
    except Exception:
        return ''


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(safe_read(path))
    except Exception:
        return {}


def load_toml(path: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}
    try:
        return tomllib.loads(safe_read(path))
    except Exception:
        return {}


def uniq(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def trim(items: list[str], limit: int = MAX_LIST) -> list[str]:
    return items[:limit]


def detect_languages(files: list[Path]) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for rel in files:
        lang = LANGUAGE_EXTENSIONS.get(rel.suffix.lower())
        if lang:
            counter[lang] += 1
    return [{'name': name, 'files': count} for name, count in counter.most_common(10)]


def manifest_type(rel: Path) -> str:
    name = rel.name
    if name == 'package.json':
        return 'node'
    if name == 'pyproject.toml' or name == 'requirements.txt' or name == 'requirements-dev.txt':
        return 'python'
    if name == 'Gemfile':
        return 'ruby'
    if name == 'go.mod':
        return 'go'
    if name == 'Cargo.toml':
        return 'rust'
    if name in {'pom.xml', 'build.gradle', 'build.gradle.kts'}:
        return 'java'
    if name == 'composer.json':
        return 'php'
    if name == 'Dockerfile' or name.startswith('docker-compose'):
        return 'container'
    return 'other'


def collect_manifests(root: Path, files: list[Path]) -> list[dict[str, str]]:
    wanted = {
        'package.json', 'pyproject.toml', 'requirements.txt', 'requirements-dev.txt', 'Gemfile', 'go.mod',
        'Cargo.toml', 'pom.xml', 'build.gradle', 'build.gradle.kts', 'composer.json', 'Dockerfile',
        'pnpm-workspace.yaml', 'turbo.json', 'nx.json', 'docker-compose.yml', 'docker-compose.yaml',
        'Makefile', 'justfile'
    }
    manifests = []
    for rel in files:
        if rel.name in wanted:
            manifests.append({'path': rel.as_posix(), 'type': manifest_type(rel)})
    return manifests


def package_dir_label(rel: Path) -> str:
    parent = rel.parent.as_posix()
    return '.' if parent == '.' else parent


def node_info(root: Path, files: list[Path]) -> dict[str, Any]:
    packages = []
    dependencies: Counter[str] = Counter()
    scripts_by_package: dict[str, dict[str, str]] = {}
    workspace_signals = []
    for rel in files:
        if rel.name != 'package.json':
            continue
        data = load_json(root / rel)
        deps: dict[str, Any] = {}
        for key in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
            deps.update(data.get(key, {}) or {})
        for dep in deps:
            dependencies[dep] += 1
        scripts = data.get('scripts', {}) or {}
        package_name = data.get('name') or package_dir_label(rel)
        scripts_by_package[package_name] = {str(k): str(v) for k, v in scripts.items()}
        workspaces = data.get('workspaces')
        if workspaces:
            workspace_signals.append(rel.as_posix())
        packages.append({
            'path': rel.as_posix(),
            'name': package_name,
            'private': bool(data.get('private')),
            'scripts': sorted(str(k) for k in scripts.keys())[:20],
        })
    for marker in ['pnpm-workspace.yaml', 'turbo.json', 'nx.json']:
        if (root / marker).exists():
            workspace_signals.append(marker)
    return {
        'packages': packages,
        'dependencies': dependencies,
        'scripts_by_package': scripts_by_package,
        'workspace_signals': uniq(workspace_signals),
    }


def python_info(root: Path, files: list[Path]) -> dict[str, Any]:
    deps: Counter[str] = Counter()
    tools: set[str] = set()
    pyprojects = []
    requirements = []
    for rel in files:
        if rel.name == 'pyproject.toml':
            data = load_toml(root / rel)
            pyprojects.append(rel.as_posix())
            project = data.get('project', {}) if isinstance(data, dict) else {}
            for dep in project.get('dependencies', []) or []:
                name = str(dep).split()[0]
                deps[name] += 1
            optional = project.get('optional-dependencies', {}) or {}
            for values in optional.values():
                for dep in values or []:
                    name = str(dep).split()[0]
                    deps[name] += 1
            tool = data.get('tool', {}) if isinstance(data, dict) else {}
            for key in ['pytest', 'ruff', 'mypy', 'black', 'pyright', 'poetry', 'hatch']:
                if key in tool:
                    tools.add(key)
        elif rel.name.startswith('requirements') and rel.suffix == '.txt':
            requirements.append(rel.as_posix())
            for line in safe_read(root / rel).splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                line = re.split(r'[<>=\[]', line, maxsplit=1)[0].strip()
                if line:
                    deps[line] += 1
        elif rel.name in {'tox.ini', 'noxfile.py'}:
            tools.add(rel.name)
    return {'dependencies': deps, 'tools': sorted(tools), 'pyprojects': pyprojects, 'requirements': requirements}


def ruby_info(root: Path, files: list[Path]) -> dict[str, Any]:
    deps: Counter[str] = Counter()
    gemfiles = []
    for rel in files:
        if rel.name != 'Gemfile':
            continue
        gemfiles.append(rel.as_posix())
        for line in safe_read(root / rel).splitlines():
            match = re.search(r"gem\s+[\"']([^\"']+)[\"']", line)
            if match:
                deps[match.group(1)] += 1
    return {'dependencies': deps, 'gemfiles': gemfiles}


def go_info(root: Path, files: list[Path]) -> dict[str, Any]:
    deps: Counter[str] = Counter()
    modules = []
    for rel in files:
        if rel.name != 'go.mod':
            continue
        modules.append(rel.as_posix())
        for line in safe_read(root / rel).splitlines():
            line = line.strip()
            if line.startswith('require '):
                parts = line.split()
                if len(parts) >= 2:
                    deps[parts[1].split('/')[-1]] += 1
    return {'dependencies': deps, 'modules': modules}


def rust_info(root: Path, files: list[Path]) -> dict[str, Any]:
    deps: Counter[str] = Counter()
    cargo_files = []
    for rel in files:
        if rel.name != 'Cargo.toml':
            continue
        cargo_files.append(rel.as_posix())
        data = load_toml(root / rel)
        dependencies = data.get('dependencies', {}) if isinstance(data, dict) else {}
        if isinstance(dependencies, dict):
            for dep in dependencies:
                deps[str(dep)] += 1
    return {'dependencies': deps, 'cargo': cargo_files}


def frameworks_from_dependencies(*counters: Counter[str]) -> list[str]:
    found = []
    for counter in counters:
        for dep, count in counter.most_common():
            for hint, label in FRAMEWORK_HINTS.items():
                if dep == hint or dep.startswith(hint):
                    found.append(label)
    return trim(sorted(set(found)))


def detect_package_managers(root: Path, node: dict[str, Any], py: dict[str, Any], manifests: list[dict[str, str]]) -> list[str]:
    managers = []
    if (root / 'pnpm-lock.yaml').exists() or (root / 'pnpm-workspace.yaml').exists():
        managers.append('pnpm')
    if (root / 'yarn.lock').exists():
        managers.append('yarn')
    if (root / 'package-lock.json').exists():
        managers.append('npm')
    if py['pyprojects'] and (root / 'poetry.lock').exists():
        managers.append('poetry')
    if py['pyprojects'] and (root / 'uv.lock').exists():
        managers.append('uv')
    if py['requirements']:
        managers.append('pip')
    if any(m['type'] == 'go' for m in manifests):
        managers.append('go modules')
    if any(m['type'] == 'rust' for m in manifests):
        managers.append('cargo')
    if any(m['type'] == 'ruby' for m in manifests):
        managers.append('bundler')
    if any(m['path'].endswith('pom.xml') for m in manifests):
        managers.append('maven')
    if any(m['path'].endswith('build.gradle') or m['path'].endswith('build.gradle.kts') for m in manifests):
        managers.append('gradle')
    return uniq(managers)


def choose_root_scripts(root: Path, node: dict[str, Any]) -> dict[str, Any]:
    candidates: dict[str, list[str]] = {k: [] for k in QUALITY_SCRIPT_PRIORITY}
    commands: dict[str, str] = {}
    confidence: dict[str, str] = {}
    root_scripts = {}
    root_pkg = root / 'package.json'
    if root_pkg.exists():
        data = load_json(root_pkg)
        root_scripts = {str(k): str(v) for k, v in (data.get('scripts', {}) or {}).items()}
    for slot, ordered_names in QUALITY_SCRIPT_PRIORITY.items():
        for name in ordered_names:
            if name in root_scripts:
                commands[slot] = f'npm run {name}'
                confidence[slot] = 'high'
                break
        for package_name, scripts in node['scripts_by_package'].items():
            for script_name in scripts:
                if slot == 'test' and 'test' in script_name:
                    candidates[slot].append(f'{package_name}:{script_name}')
                elif slot == 'lint' and 'lint' in script_name:
                    candidates[slot].append(f'{package_name}:{script_name}')
                elif slot == 'typecheck' and ('type' in script_name or 'check' in script_name or script_name == 'tsc'):
                    candidates[slot].append(f'{package_name}:{script_name}')
                elif slot == 'build' and 'build' in script_name:
                    candidates[slot].append(f'{package_name}:{script_name}')
                elif slot == 'perf-smoke' and ('perf' in script_name or 'bench' in script_name):
                    candidates[slot].append(f'{package_name}:{script_name}')
    return {'commands': commands, 'candidates': {k: trim(uniq(v), 8) for k, v in candidates.items()}, 'confidence': confidence}


def detect_commands(root: Path, node: dict[str, Any], py: dict[str, Any], ruby: dict[str, Any], manifests: list[dict[str, str]]) -> dict[str, Any]:
    info = choose_root_scripts(root, node)
    commands = dict(info['commands'])
    confidence = dict(info['confidence'])
    candidates = dict(info['candidates'])

    makefile = root / 'Makefile'
    justfile = root / 'justfile'
    helper_targets = []
    for file in [makefile, justfile]:
        if file.exists():
            for line in safe_read(file).splitlines():
                match = re.match(r'^([A-Za-z0-9_.-]+):', line)
                if match:
                    helper_targets.append(match.group(1))
    if helper_targets:
        candidates['make_targets'] = trim(sorted(set(helper_targets)), 20)

    if 'test' not in commands:
        if py['pyprojects'] or py['requirements']:
            if 'pytest' in py['tools'] or any('pytest' in dep for dep in py['dependencies']):
                commands['test'] = 'pytest'
                confidence['test'] = 'medium'
        elif any(m['type'] == 'go' for m in manifests):
            commands['test'] = 'go test ./...'
            confidence['test'] = 'medium'
        elif any(m['type'] == 'rust' for m in manifests):
            commands['test'] = 'cargo test'
            confidence['test'] = 'medium'
        elif ruby['gemfiles']:
            if any('rspec' in dep for dep in ruby['dependencies']):
                commands['test'] = 'bundle exec rspec'
                confidence['test'] = 'medium'
            else:
                commands['test'] = 'bin/rails test'
                confidence['test'] = 'low'
    if 'lint' not in commands:
        if 'ruff' in py['tools'] or any('ruff' in dep for dep in py['dependencies']):
            commands['lint'] = 'ruff check .'
            confidence['lint'] = 'medium'
        elif ruby['gemfiles'] and any('rubocop' in dep for dep in ruby['dependencies']):
            commands['lint'] = 'bundle exec rubocop'
            confidence['lint'] = 'medium'
        elif any(m['type'] == 'rust' for m in manifests):
            commands['lint'] = 'cargo clippy --all-targets --all-features -- -D warnings'
            confidence['lint'] = 'medium'
    if 'typecheck' not in commands:
        if 'mypy' in py['tools'] or any('mypy' in dep for dep in py['dependencies']):
            commands['typecheck'] = 'mypy .'
            confidence['typecheck'] = 'medium'
        elif any(m['type'] == 'rust' for m in manifests):
            commands['typecheck'] = 'cargo check'
            confidence['typecheck'] = 'medium'
    if 'build' not in commands:
        if any(m['type'] == 'go' for m in manifests):
            commands['build'] = 'go build ./...'
            confidence['build'] = 'medium'
        elif any(m['type'] == 'rust' for m in manifests):
            commands['build'] = 'cargo build'
            confidence['build'] = 'medium'
        elif any(m['path'].endswith('pom.xml') for m in manifests):
            commands['build'] = 'mvn verify'
            confidence['build'] = 'medium'
        elif any(m['path'].endswith('build.gradle') or m['path'].endswith('build.gradle.kts') for m in manifests):
            commands['build'] = './gradlew build'
            confidence['build'] = 'medium'
        elif py['pyprojects']:
            commands['build'] = 'python -m build'
            confidence['build'] = 'low'
    return {'commands': commands, 'confidence': confidence, 'candidates': candidates}


def detect_topology(root: Path, manifests: list[dict[str, str]], node: dict[str, Any], files: list[Path]) -> dict[str, Any]:
    signals = []
    style = 'single-repo application'
    confidence = 'low'
    manifest_dirs = {Path(item['path']).parent.as_posix() for item in manifests if item['type'] in {'node', 'python', 'ruby', 'go', 'rust', 'java', 'php'}}
    if node['workspace_signals']:
        style = 'monorepo'
        confidence = 'high'
        signals.extend(node['workspace_signals'])
    elif len([m for m in manifests if m['type'] in {'node', 'python', 'ruby', 'go', 'rust', 'java', 'php'}]) >= 4:
        style = 'multi-package repository'
        confidence = 'medium'
        signals.append('multiple language/runtime manifests detected')
    elif any(d.startswith('services/') for d in manifest_dirs):
        style = 'service-oriented repository'
        confidence = 'medium'
        signals.append('service manifests under services/')
    elif any(d.startswith('apps/') for d in manifest_dirs) and any(d.startswith('packages/') for d in manifest_dirs):
        style = 'application plus shared-packages repository'
        confidence = 'medium'
        signals.append('manifests under apps/ and packages/')
    elif any(rel.parts[:1] == ('backend',) for rel in files) and any(rel.parts[:1] == ('frontend',) for rel in files):
        style = 'split frontend-backend repository'
        confidence = 'medium'
        signals.append('backend/ and frontend/ directories detected')
    elif len(manifest_dirs) <= 2 and any(d in {'src', 'app', '.'} for d in manifest_dirs):
        style = 'single service or modular monolith'
        confidence = 'medium'
        signals.append('one primary runtime manifest')
    return {'style': style, 'confidence': confidence, 'signals': trim(uniq(signals), 8)}


def detect_services(manifests: list[dict[str, str]]) -> list[dict[str, str]]:
    services = []
    for item in manifests:
        path = Path(item['path'])
        parent = path.parent.as_posix()
        if parent == '.':
            continue
        if parent.startswith(('apps/', 'services/', 'packages/', 'libs/', 'backend/', 'frontend/', 'web/', 'api/')):
            services.append({'path': parent, 'kind': item['type']})
    unique = []
    seen = set()
    for item in services:
        key = (item['path'], item['kind'])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:20]


def detect_critical_directories(files: list[Path]) -> list[str]:
    priority_prefixes = ['apps', 'packages', 'services', 'libs', 'src', 'app', 'web', 'api', 'server', 'backend', 'frontend', 'workers', 'db', 'infra', 'docs', 'scripts']
    found: list[str] = []
    for prefix in priority_prefixes:
        for rel in files:
            if not rel.parts or rel.parts[0] != prefix:
                continue
            if len(rel.parts) >= 2 and not Path(rel.parts[1]).suffix:
                found.append('/'.join(rel.parts[:2]))
            else:
                found.append(prefix)
    if not found:
        top_dirs = Counter(rel.parts[0] for rel in files if rel.parts and not rel.parts[0].startswith('.'))
        found = [name for name, _ in top_dirs.most_common(8)]
    return trim(uniq(found), 12)


def detect_sensitive_areas(files: list[Path]) -> list[str]:
    areas = []
    for rel in files:
        lower = rel.as_posix().lower()
        if any(keyword in lower for keyword in SENSITIVE_KEYWORDS):
            base = rel.parent if rel.parent.as_posix() != '.' else rel
            parts = base.parts
            if len(parts) >= 3:
                areas.append('/'.join(parts[:3]))
            elif len(parts) >= 2:
                areas.append('/'.join(parts[:2]))
            else:
                areas.append(base.as_posix())
    return trim(uniq(sorted(areas)), 20)


def detect_docs(files: list[Path]) -> list[str]:
    docs = []
    names = {rel.as_posix() for rel in files}
    for item in DOC_PRIORITY:
        if item in names:
            docs.append(item)
    for rel in files:
        lower = rel.as_posix().lower()
        if lower.endswith('.md') and ('architecture' in lower or 'adr' in lower or 'runbook' in lower or 'onboard' in lower):
            docs.append(rel.as_posix())
    return trim(uniq(docs), MAX_DOCS)


def detect_ci(root: Path, files: list[Path]) -> list[str]:
    workflows = []
    for rel in files:
        if rel.parts[:2] == ('.github', 'workflows') and rel.suffix in {'.yml', '.yaml'}:
            workflows.append(rel.as_posix())
    if (root / '.gitlab-ci.yml').exists():
        workflows.append('.gitlab-ci.yml')
    return trim(uniq(workflows), 12)


def detect_infra(files: list[Path]) -> list[str]:
    infra = []
    for rel in files:
        lower = rel.as_posix().lower()
        if rel.name == 'Dockerfile' or lower.startswith('docker-compose'):
            infra.append(rel.as_posix())
        elif any(token in lower for token in ['terraform', 'helm', 'k8s', 'kubernetes', 'compose', 'deploy', 'infra/']):
            infra.append(rel.as_posix())
    return trim(uniq(infra), 16)


def detect_entrypoints(files: list[Path]) -> list[str]:
    patterns = {
        'main.py', 'app.py', 'manage.py', 'main.go', 'server.ts', 'server.js', 'index.ts', 'index.js',
        'src/main.rs', 'src/lib.rs', 'bin/www', 'next.config.js', 'next.config.ts', 'vite.config.ts', 'vite.config.js'
    }
    entries = []
    for rel in files:
        text = rel.as_posix()
        if rel.name in patterns or text in patterns or text.startswith('cmd/') or text.startswith('apps/') and rel.name in {'main.ts', 'main.js', 'main.py'}:
            entries.append(text)
    return trim(uniq(entries), MAX_ENTRYPOINTS)


def detect_datastores_and_integrations(counters: list[Counter[str]]) -> tuple[list[str], list[str]]:
    datastores = []
    integrations = []
    for counter in counters:
        for dep in counter:
            for hint, label in DATASTORE_HINTS.items():
                if dep == hint or dep.startswith(hint):
                    datastores.append(label)
            for hint, label in INTEGRATION_HINTS.items():
                if dep == hint or dep.startswith(hint):
                    integrations.append(label)
    return trim(sorted(set(datastores))), trim(sorted(set(integrations)))


def repo_title(root: Path, docs: list[str]) -> str:
    readme = root / 'README.md'
    if readme.exists():
        for line in safe_read(readme).splitlines():
            if line.startswith('# '):
                return line[2:].strip()
    return root.name


def open_questions(profile: dict[str, Any]) -> list[str]:
    questions = []
    commands = profile['commands']['commands']
    if 'test' not in commands:
        questions.append('confirm the canonical test command')
    if 'lint' not in commands:
        questions.append('confirm the canonical lint command')
    if 'typecheck' not in commands and any(lang['name'] in {'typescript', 'python'} for lang in profile['languages']):
        questions.append('confirm the canonical typecheck command')
    if profile['topology']['confidence'] == 'low':
        questions.append('confirm whether this repo is a monorepo, modular monolith, or single service')
    if not profile['docs']:
        questions.append('add or confirm the architecture and onboarding docs that should be treated as durable guidance')
    return trim(questions, 10)


def build_profile(root: Path) -> dict[str, Any]:
    files = iter_files(root)
    manifests = collect_manifests(root, files)
    node = node_info(root, files)
    py = python_info(root, files)
    ruby = ruby_info(root, files)
    go = go_info(root, files)
    rust = rust_info(root, files)
    languages = detect_languages(files)
    frameworks = frameworks_from_dependencies(node['dependencies'], py['dependencies'], ruby['dependencies'], go['dependencies'], rust['dependencies'])
    topology = detect_topology(root, manifests, node, files)
    commands = detect_commands(root, node, py, ruby, manifests)
    datastores, integrations = detect_datastores_and_integrations([node['dependencies'], py['dependencies'], ruby['dependencies'], go['dependencies'], rust['dependencies']])
    profile = {
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'repo_name': repo_title(root, []),
        'root': str(root),
        'topology': topology,
        'languages': languages,
        'frameworks': frameworks,
        'package_managers': detect_package_managers(root, node, py, manifests),
        'manifests': manifests,
        'services': detect_services(manifests),
        'critical_directories': detect_critical_directories(files),
        'sensitive_areas': detect_sensitive_areas(files),
        'docs': detect_docs(files),
        'ci_workflows': detect_ci(root, files),
        'infra': detect_infra(files),
        'entrypoints': detect_entrypoints(files),
        'commands': commands,
        'datastores': datastores,
        'integrations': integrations,
        'file_count_scanned': len(files),
    }
    profile['open_questions'] = open_questions(profile)
    return profile


def join_list(items: list[str], empty: str = 'none detected') -> str:
    return ', '.join(items) if items else empty


def summary_line(profile: dict[str, Any]) -> str:
    langs = ', '.join(item['name'] for item in profile['languages'][:3]) or 'unknown stack'
    frameworks = ', '.join(profile['frameworks'][:4]) or 'no clear framework detected'
    return f"{profile['topology']['style']} | languages: {langs} | frameworks: {frameworks}"


def build_guardrail_rules(profile: dict[str, Any]) -> list[str]:
    rules = []
    sensitive = ' '.join(profile['sensitive_areas']).lower()
    if any(token in sensitive for token in ['auth', 'permission', 'policy', 'session', 'token', 'security']):
        rules.append('auth, permission, token, and policy changes require `$security-review` before implementation')
    if any(token in sensitive for token in ['payment', 'billing', 'invoice', 'subscription']):
        rules.append('billing and payment changes require architecture review, explicit rollback notes, and conservative validation')
    if any(token in sensitive for token in ['migration', 'schema', 'database', 'db', 'prisma', 'alembic']):
        rules.append('schema and migration work require `$migration-guard`, staged rollout, and rollback planning')
    if any(token in sensitive for token in ['infra', 'terraform', 'k8s', 'deploy', 'release']):
        rules.append('infra and deployment changes require human review and should stay narrowly scoped')
    if profile['datastores'] or profile['integrations']:
        rules.append('treat external integrations and persistent storage as contract boundaries, not implementation details')
    if profile['commands']['commands'].get('perf-smoke') or profile['topology']['style'] in {'monorepo', 'service-oriented repository'}:
        rules.append('for hot paths or scale-sensitive work, run `$perf-check` and update observability expectations')
    return uniq(rules)


def render_index(profile: dict[str, Any]) -> str:
    return f"""# Project context index

Generated: {profile['generated_at']}

## Repo profile

- Summary: {summary_line(profile)}
- Package managers: {join_list(profile['package_managers'])}
- Datastores: {join_list(profile['datastores'])}
- Integrations: {join_list(profile['integrations'])}

## Read in this order

1. `01-repo-overview.md`
2. `02-architecture-map.md`
3. `03-build-test-and-quality-gates.md`
4. `05-change-boundaries.md`
5. `06-nfr-and-operability.md`
6. `07-bootstrap-report.md`

## Use this memory for

- planning features without rediscovering the repo shape
- protecting architecture and sensitive boundaries
- reusing the same validation commands across tasks
- keeping agents aligned on the same repo facts
"""


def render_overview(profile: dict[str, Any]) -> str:
    services = [f"- `{item['path']}` ({item['kind']})" for item in profile['services'][:12]] or ['- no multi-package service layout detected']
    manifests = [f"- `{item['path']}` ({item['type']})" for item in profile['manifests'][:20]] or ['- no major manifests detected']
    docs = [f"- `{item}`" for item in profile['docs']] or ['- no durable docs detected yet']
    return f"""# Repository overview

## What this repo appears to be

- Repo: {profile['repo_name']}
- Topology: {profile['topology']['style']} ({profile['topology']['confidence']} confidence)
- Primary languages: {join_list([item['name'] for item in profile['languages'][:5]])}
- Frameworks: {join_list(profile['frameworks'])}
- Package managers: {join_list(profile['package_managers'])}

## Manifest inventory

{os.linesep.join(manifests)}

## Services or modules

{os.linesep.join(services)}

## Durable docs already present

{os.linesep.join(docs)}

## Entry points

{os.linesep.join(f'- `{item}`' for item in profile['entrypoints']) if profile['entrypoints'] else '- no clear entrypoints detected'}
"""


def render_architecture(profile: dict[str, Any]) -> str:
    critical = [f"- `{item}`" for item in profile['critical_directories']] or ['- no critical directories inferred']
    topology_signals = [f"- {item}" for item in profile['topology']['signals']] or ['- topology inferred mostly from manifest layout']
    return f"""# Architecture map

## Current architecture snapshot

- Style: {profile['topology']['style']}
- Confidence: {profile['topology']['confidence']}
- Datastores: {join_list(profile['datastores'])}
- External integrations: {join_list(profile['integrations'])}

## Why this shape was inferred

{os.linesep.join(topology_signals)}

## Critical directories

{os.linesep.join(critical)}

## Likely ownership and boundary guidance

- treat manifests and top-level runtime directories as ownership boundaries
- prefer extending existing modules before creating new deployables
- if a change crosses more than one critical directory, classify it at least `L2` until proven otherwise
- validate public contracts whenever code touches API, worker, queue, migration, or shared-package boundaries
"""


def render_commands(profile: dict[str, Any]) -> str:
    commands = profile['commands']['commands']
    lines = []
    for key in ['test', 'lint', 'typecheck', 'build', 'perf-smoke']:
        value = commands.get(key)
        conf = profile['commands']['confidence'].get(key, 'unknown')
        if value:
            lines.append(f'- {key}: `{value}` ({conf} confidence)')
        else:
            lines.append(f'- {key}: not confidently inferred')
    candidates = []
    for key, values in sorted(profile['commands']['candidates'].items()):
        if values:
            candidates.append(f'- {key}: {join_list(values)}')
    if not candidates:
        candidates = ['- no extra command candidates collected']
    workflows = [f'- `{item}`' for item in profile['ci_workflows']] or ['- no CI workflows detected']
    return f"""# Build, test, and quality gates

## Primary validation commands

{os.linesep.join(lines)}

## Command candidates worth confirming

{os.linesep.join(candidates)}

## CI and automation

{os.linesep.join(workflows)}

## Operational advice

- keep validation commands in `AGENTS.md` aligned with this file
- prefer the narrowest command that proves the current slice
- if no canonical command exists, create one before relying on ad hoc shell pipelines
"""


def render_domain(profile: dict[str, Any]) -> str:
    services = [item['path'] for item in profile['services'][:12]]
    guessed_domains = []
    for item in services + profile['critical_directories']:
        token = item.split('/')[-1].replace('-', ' ').replace('_', ' ')
        if token not in {'src', 'app', 'apps', 'packages', 'services', 'libs', 'web', 'api', 'server'}:
            guessed_domains.append(token)
    guessed_domains = trim(uniq(guessed_domains), 12)
    return f"""# Domain and interfaces

## Candidate bounded contexts or domains

{os.linesep.join(f'- {item}' for item in guessed_domains) if guessed_domains else '- domain language was not obvious from directory names alone'}

## Contract surfaces to treat carefully

- APIs, queues, migrations, shared packages, and persistent schema changes
- modules that sit between `web`, `api`, `server`, `workers`, or `packages` directories
- any integration using {join_list(profile['integrations'], empty='external services')}

## Notes

- this file is intentionally conservative; enrich it with real business vocabulary after the first bootstrap review
- if the repo has public APIs or multiple consumers, add contract references and compatibility rules here
"""


def render_boundaries(profile: dict[str, Any]) -> str:
    sensitive = [f'- `{item}`' for item in profile['sensitive_areas']] or ['- no sensitive zones were inferred automatically']
    rules = [f'- {item}' for item in build_guardrail_rules(profile)] or ['- no special guardrails were inferred automatically']
    return f"""# Change boundaries

## Protected zones

{os.linesep.join(sensitive)}

## Required review lanes

{os.linesep.join(rules)}

## Architecture-preserving defaults

- avoid changing multiple protected zones in one diff unless the task is explicitly cross-cutting
- prefer additive or reversible changes in boundary-heavy areas
- if a protected zone lacks tests or observability, record that debt before coding around it
"""


def render_nfr(profile: dict[str, Any]) -> str:
    infra = [f'- `{item}`' for item in profile['infra']] or ['- no major infra files detected']
    hints = []
    if 'sentry' in profile['integrations'] or 'opentelemetry' in profile['integrations'] or 'prometheus' in profile['integrations']:
        hints.append('- observability libraries are already present; extend existing telemetry instead of inventing parallel channels')
    if profile['datastores']:
        hints.append(f"- persistent state exists via {join_list(profile['datastores'])}; migrations and rollback must stay explicit")
    if profile['topology']['style'] in {'monorepo', 'service-oriented repository'}:
        hints.append('- cross-package and cross-service changes should define compatibility and rollout sequencing early')
    if not hints:
        hints.append('- add measurable latency, throughput, availability, and rollback expectations before major changes')
    return f"""# NFR and operability

## Infra and deployment signals

{os.linesep.join(infra)}

## Default NFR guidance

{os.linesep.join(hints)}

## Reliability and release defaults

- changes that touch data, background jobs, or release automation should document rollback and alerting impact
- prefer explicit budgets and SLO references over vague terms like fast or scalable
- if production-critical paths are touched, add or update runbook notes before calling the work done
"""


def render_report(profile: dict[str, Any]) -> str:
    questions = [f'- {item}' for item in profile['open_questions']] or ['- no open bootstrap questions']
    return f"""# Bootstrap report

## Summary

- {summary_line(profile)}
- Files scanned: {profile['file_count_scanned']}
- Critical directories: {join_list(profile['critical_directories'])}
- Sensitive areas: {join_list(profile['sensitive_areas'])}

## Confidence notes

- topology confidence: {profile['topology']['confidence']}
- command inference coverage: {join_list([f"{k}={v}" for k, v in profile['commands']['confidence'].items()]) or 'no commands inferred with confidence'}

## Open questions

{os.linesep.join(questions)}

## Refresh triggers

- rerun bootstrap after major repo restructures, build-system changes, migrations, new services, or large architecture decisions
- rerun bootstrap when `AGENTS.md` placeholders drift away from reality
"""


def managed_block(profile: dict[str, Any]) -> str:
    commands = profile['commands']['commands']
    rules = build_guardrail_rules(profile)
    lines = [
        BOOTSTRAP_START,
        '## Project bootstrap profile (managed)',
        '',
        f"- Generated: {profile['generated_at']}",
        f"- Repo summary: {summary_line(profile)}",
        f"- Primary validation commands: test=`{commands.get('test', 'confirm manually')}`, lint=`{commands.get('lint', 'confirm manually')}`, typecheck=`{commands.get('typecheck', 'confirm manually')}`, build=`{commands.get('build', 'confirm manually')}`",
        f"- Critical directories: {join_list(profile['critical_directories'])}",
        f"- Sensitive areas: {join_list(profile['sensitive_areas'])}",
        '- Durable repo memory: `docs/project-context/index.md` plus the linked files under `docs/project-context/`',
        '- Bootstrap rule: when entering an unfamiliar area or when context looks stale, read the project context docs before planning or editing.',
    ]
    if rules:
        lines.append('- Protected-zone defaults:')
        lines.extend(f'  - {rule}' for rule in rules)
    if profile['open_questions']:
        lines.append('- Open bootstrap questions:')
        lines.extend(f'  - {item}' for item in profile['open_questions'])
    lines.extend([BOOTSTRAP_END, ''])
    return '\n'.join(lines)


def patch_agents_md(root: Path, profile: dict[str, Any]) -> None:
    path = root / 'AGENTS.md'
    existing = safe_read(path) if path.exists() else '# AGENTS.md\n\n'
    block = managed_block(profile)
    if BOOTSTRAP_START in existing and BOOTSTRAP_END in existing:
        existing = re.sub(
            re.escape(BOOTSTRAP_START) + r'.*?' + re.escape(BOOTSTRAP_END),
            block.strip(),
            existing,
            flags=re.DOTALL,
        )
    else:
        anchor = '## Repo-specific placeholders to customize'
        if anchor in existing:
            existing = existing.replace(anchor, block + '\n' + anchor)
        else:
            existing = existing.rstrip() + '\n\n' + block

    replacements = {
        'test: `<replace-me>`': f"test: `{profile['commands']['commands'].get('test', 'confirm manually')}`",
        'lint: `<replace-me>`': f"lint: `{profile['commands']['commands'].get('lint', 'confirm manually')}`",
        'typecheck: `<replace-me>`': f"typecheck: `{profile['commands']['commands'].get('typecheck', 'confirm manually')}`",
        'build: `<replace-me>`': f"build: `{profile['commands']['commands'].get('build', 'confirm manually')}`",
        'perf-smoke: `<replace-me>`': f"perf-smoke: `{profile['commands']['commands'].get('perf-smoke', 'confirm manually')}`",
        'Critical directories: `<replace-me>`': f"Critical directories: `{join_list(profile['critical_directories'])}`",
        'Sensitive areas: `<replace-me>`': f"Sensitive areas: `{join_list(profile['sensitive_areas'])}`",
        'SLO or latency budget references: `<replace-me>`': 'SLO or latency budget references: `docs/project-context/06-nfr-and-operability.md`',
    }
    for old, new in replacements.items():
        existing = existing.replace(old, new)
    path.write_text(existing, encoding='utf-8')


def write_outputs(root: Path, profile: dict[str, Any]) -> None:
    machine_dir = root / '.codex/project-context'
    docs_dir = root / 'docs/project-context'
    machine_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    (machine_dir / 'profile.json').write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    (docs_dir / 'index.md').write_text(render_index(profile), encoding='utf-8')
    (docs_dir / '01-repo-overview.md').write_text(render_overview(profile), encoding='utf-8')
    (docs_dir / '02-architecture-map.md').write_text(render_architecture(profile), encoding='utf-8')
    (docs_dir / '03-build-test-and-quality-gates.md').write_text(render_commands(profile), encoding='utf-8')
    (docs_dir / '04-domain-and-interfaces.md').write_text(render_domain(profile), encoding='utf-8')
    (docs_dir / '05-change-boundaries.md').write_text(render_boundaries(profile), encoding='utf-8')
    (docs_dir / '06-nfr-and-operability.md').write_text(render_nfr(profile), encoding='utf-8')
    (docs_dir / '07-bootstrap-report.md').write_text(render_report(profile), encoding='utf-8')
    patch_agents_md(root, profile)

    helper = root / 'scripts' / 'refresh-project-context.py'
    if helper.exists():
        subprocess.run(['python3', str(helper), str(root)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description='Deeply scan a repo and adapt CodexKit guidance to it.')
    parser.add_argument('--root', default='.', help='repository root or any path inside the repository')
    parser.add_argument('--apply', action='store_true', help='write profile, project memory docs, and AGENTS managed block')
    parser.add_argument('--json', action='store_true', help='print the profile JSON to stdout')
    args = parser.parse_args()

    root = git_root(Path(args.root))
    profile = build_profile(root)

    if args.apply:
        write_outputs(root, profile)
        print(f'[codexkit] bootstrap applied at {root}')
        print('[codexkit] profile: .codex/project-context/profile.json')
        print('[codexkit] docs: docs/project-context/index.md')
    if args.json or not args.apply:
        print(json.dumps(profile, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
