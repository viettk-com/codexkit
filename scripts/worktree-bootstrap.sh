#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "[codexkit] bootstrapping worktree in $ROOT"

if [ -f package.json ]; then
  if [ -f pnpm-lock.yaml ] && command -v pnpm >/dev/null 2>&1; then
    pnpm install --frozen-lockfile || pnpm install
  elif [ -f yarn.lock ] && command -v yarn >/dev/null 2>&1; then
    yarn install --frozen-lockfile || yarn install
  elif [ -f bun.lockb ] && command -v bun >/dev/null 2>&1; then
    bun install --frozen-lockfile || bun install
  else
    npm ci || npm install
  fi
fi

if [ -f pyproject.toml ]; then
  if command -v uv >/dev/null 2>&1; then
    uv sync || true
  elif command -v poetry >/dev/null 2>&1; then
    poetry install || true
  elif command -v python3 >/dev/null 2>&1; then
    python3 -m pip install -e . || true
  fi
fi

if [ -f Cargo.toml ] && command -v cargo >/dev/null 2>&1; then
  cargo fetch || true
fi

if [ -f go.mod ] && command -v go >/dev/null 2>&1; then
  go mod download || true
fi

echo "[codexkit] bootstrap complete"
echo "[codexkit] reminder: ensure your active plan folder is committed or copied into this worktree if the task depends on it"
