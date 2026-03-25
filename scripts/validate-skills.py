#!/usr/bin/env python3
"""Validate repository skills with a minimal dependency-free check."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED = {"name", "description", "license", "allowed-tools", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9-]+$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing or invalid YAML frontmatter")
    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data

def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]
    try:
        text = skill_md.read_text(encoding="utf-8")
        data = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_dir}: {exc}"]

    extra = set(data) - ALLOWED
    if extra:
        errors.append(f"{skill_dir}: unexpected frontmatter keys: {', '.join(sorted(extra))}")

    name = data.get("name", "")
    description = data.get("description", "")
    if not name:
        errors.append(f"{skill_dir}: missing name")
    elif not NAME_RE.match(name):
        errors.append(f"{skill_dir}: invalid name '{name}'")
    if not description:
        errors.append(f"{skill_dir}: missing description")
    elif description.lower() != description:
        errors.append(f"{skill_dir}: description should stay lowercase for better triggering consistency")

    if "## Workflow" not in text:
        errors.append(f"{skill_dir}: missing '## Workflow' section")
    if "## Rules" not in text:
        errors.append(f"{skill_dir}: missing '## Rules' section")
    return errors

def iter_skill_dirs(base: Path) -> list[Path]:
    if (base / "SKILL.md").exists():
        return [base]
    return sorted(p for p in base.iterdir() if p.is_dir())

def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".agents/skills")
    if not base.exists():
        print(f"missing skill directory: {base}")
        return 1

    all_errors: list[str] = []
    skill_dirs = iter_skill_dirs(base)
    for skill_dir in skill_dirs:
        all_errors.extend(validate_skill(skill_dir))

    if all_errors:
        print("\n".join(all_errors))
        return 1

    print(f"validated {len(skill_dirs)} skills")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
