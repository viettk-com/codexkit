#!/usr/bin/env bash
set -euo pipefail

create_branch="false"
if [ "${1:-}" = "--branch" ]; then
  create_branch="true"
  shift
fi

if [ "$#" -lt 2 ]; then
  echo "usage: scripts/new-initiative.sh [--branch] <L0|L1|L2|L3> <slug or title>"
  exit 1
fi

change_class="$1"
shift

case "$change_class" in
  L0|L1|L2|L3) ;;
  *)
    echo "invalid change class: $change_class"
    exit 1
    ;;
esac

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

raw="$*"
slug="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"
date_prefix="$(date +%Y%m%d-%H%M)"
plan_dir="plans/active/${date_prefix}-${slug}"
title="$(printf '%s' "$raw" | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
today="$(date +%F)"
branch_name="${date_prefix}-${slug}"

mkdir -p "$plan_dir" "$plan_dir/phases" "$plan_dir/reports" "$plan_dir/research" "$plan_dir/artifacts"

copy_template() {
  local src="$1"
  local dest="$2"
  sed \
    -e "s/{{TITLE}}/${title//\//-}/g" \
    -e "s/{{SLUG}}/${slug}/g" \
    -e "s/{{DATE}}/${today}/g" \
    -e "s/{{CHANGE_CLASS}}/${change_class}/g" \
    "$src" > "$dest"
}

# Common files
for name in spec analysis architecture nfr plan tasks test-strategy report consistency-report; do
  copy_template "plans/templates/${name}.md" "${plan_dir}/${name}.md"
done
copy_template "plans/templates/phase.md" "${plan_dir}/phases/01-discovery.md"

# L2 and L3 artifacts
if [ "$change_class" = "L2" ] || [ "$change_class" = "L3" ]; then
  for name in decision-matrix rollout observability risk-register perf-budget threat-model; do
    copy_template "plans/templates/${name}.md" "${plan_dir}/${name}.md"
  done
fi

# L3 artifacts
if [ "$change_class" = "L3" ]; then
  for name in context-map interfaces data-model runbook adr; do
    copy_template "plans/templates/${name}.md" "${plan_dir}/${name}.md"
  done
fi

if [ "$create_branch" = "true" ] && git rev-parse --git-dir >/dev/null 2>&1; then
  current_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
  if [ -n "$current_branch" ] && [ "$current_branch" != "$branch_name" ]; then
    git switch -c "$branch_name" >/dev/null 2>&1 || echo "[codexkit] branch already exists or could not be created: $branch_name"
  fi
fi

cat <<EOF
[codexkit] created: $plan_dir
[codexkit] change class: $change_class
[codexkit] branch: $branch_name

recommended next prompts:
  \$project-bootstrap         # for L3
  \$brownfield-mapping        # for existing systems
  \$architecture-discovery
  \$nfr-capture
  \$architecture-review
  \$plan-feature
  \$task-breakdown
EOF
