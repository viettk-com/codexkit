#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

python3 scripts/validate-skills.py .agents/skills
python3 scripts/validate-aliases.py
python3 scripts/validate-bootstrap.py
python3 -m compileall scripts >/dev/null

if [ -f package.json ] && command -v node >/dev/null 2>&1; then
  node --check bin/create-codexkit.js
fi

if [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  npm pack --dry-run >/dev/null 2>&1
fi

if [ -d plans/active ] && find plans/active -mindepth 1 -maxdepth 1 -type d | grep -q .; then
  python3 scripts/validate-plans.py plans/active
else
  echo "[codexkit] no active plans to validate"
fi

for f in scripts/*.sh; do
  bash -n "$f"
done

echo "[codexkit] agents: $(find .codex/agents -name '*.toml' | wc -l | tr -d ' ')"
echo "[codexkit] skills: $(find .agents/skills -name 'SKILL.md' | wc -l | tr -d ' ')"
echo "[codexkit] templates: $(find plans/templates -name '*.md' | wc -l | tr -d ' ')"
