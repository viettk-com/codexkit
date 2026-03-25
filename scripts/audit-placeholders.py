#!/usr/bin/env python3
"""Find remaining install-time placeholders that should be customized after adding the kit to a repo."""
from __future__ import annotations

import sys
from pathlib import Path

TOKENS = ["<replace-me>", "TODO(repo)"]
SKIP_DIRS = {".git", "node_modules", ".venv", "dist", "build", "__pycache__"}

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for token in TOKENS:
            if token in text:
                findings.append(f"{path}: contains {token}")
    if findings:
        print("\n".join(findings))
        return 1
    print("no install-time placeholders found")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
