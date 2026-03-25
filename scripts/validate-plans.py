#!/usr/bin/env python3
"""Validate active plan folders for required artifacts and stronger readiness sections."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

COMMON_REQUIRED = {
    'spec.md': ['Problem', 'Scope', 'Acceptance criteria'],
    'analysis.md': ['Problem framing', 'Current system understanding', 'Constraints and invariants'],
    'architecture.md': ['Problem framing', 'Current state snapshot', 'Proposed target architecture', 'Boundaries and modules'],
    'nfr.md': ['Performance and latency', 'Availability and recovery', 'Observability and operability'],
    'plan.md': ['Overview', 'Milestones', 'Validation strategy', 'Risks and rollout'],
    'tasks.md': ['Milestones', 'Ordered tasks', 'Validation per task'],
    'test-strategy.md': ['Test layers', 'Commands', 'Manual verification'],
    'consistency-report.md': ['Artifact coverage', 'Gaps to fix before implementation', 'Readiness verdict'],
}

L2_REQUIRED = {
    'decision-matrix.md': ['Decision criteria', 'Recommendation'],
    'rollout.md': ['Rollout steps', 'Rollback conditions and steps'],
    'observability.md': ['Logs', 'Metrics', 'Alerts'],
    'risk-register.md': [],
}

L3_REQUIRED = {
    'context-map.md': ['Bounded contexts', 'Ownership'],
    'interfaces.md': ['Public interfaces', 'Compatibility notes'],
    'data-model.md': ['Entities and aggregates', 'Invariants'],
    'runbook.md': ['Health signals', 'Mitigation steps'],
    'adr.md': ['Context', 'Decision', 'Consequences'],
}


def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in HEADING_RE.finditer(text)}


def frontmatter_value(text: str, key: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        raw_key, raw_value = line.split(':', 1)
        if raw_key.strip() == key:
            return raw_value.strip().strip('"').strip("'")
    return None


def validate_file(path: Path, required_headings: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f'{path}: missing']
    text = path.read_text(encoding='utf-8')
    found = headings(text)
    for heading in required_headings:
        if heading not in found:
            errors.append(f"{path}: missing heading '{heading}'")
    return errors


def ensure_context_sources(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8')
    if 'docs/project-context/index.md' not in text:
        return [f"{path}: should reference docs/project-context/index.md in context sources"]
    return []


def validate_plan_dir(plan_dir: Path) -> list[str]:
    errors: list[str] = []
    plan_md = plan_dir / 'plan.md'
    if not plan_md.exists():
        return [f'{plan_dir}: missing plan.md']
    text = plan_md.read_text(encoding='utf-8')
    change_class = frontmatter_value(text, 'change_class') or 'L1'

    for name, req in COMMON_REQUIRED.items():
        path = plan_dir / name
        errors.extend(validate_file(path, req))
        errors.extend(ensure_context_sources(path))

    if change_class in {'L2', 'L3'}:
        for name, req in L2_REQUIRED.items():
            path = plan_dir / name
            errors.extend(validate_file(path, req))
            errors.extend(ensure_context_sources(path))

    if change_class == 'L3':
        for name, req in L3_REQUIRED.items():
            path = plan_dir / name
            errors.extend(validate_file(path, req))
            errors.extend(ensure_context_sources(path))

    report = plan_dir / 'consistency-report.md'
    if report.exists():
        verdict_text = report.read_text(encoding='utf-8').lower()
        if 'ready' not in verdict_text:
            errors.append(f'{report}: should contain an explicit readiness verdict')

    return errors


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('plans/active')
    if not base.exists():
        print(f'{base} does not exist')
        return 1

    plan_dirs = sorted(p for p in base.iterdir() if p.is_dir())
    if not plan_dirs:
        print('no active plan folders found')
        return 0

    errors: list[str] = []
    for plan_dir in plan_dirs:
        errors.extend(validate_plan_dir(plan_dir))

    if errors:
        print('\n'.join(errors))
        return 1

    print(f'validated {len(plan_dirs)} plan folders')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
