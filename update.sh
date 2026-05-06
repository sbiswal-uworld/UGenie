#!/usr/bin/env bash
# UWorld WebGenie — Claude Code Skills Updater
# Run this after git pull to sync latest versions.
# Usage: bash update.sh

set -e

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     UWorld WebGenie — Updating Skills            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "Skills directory not found. Running install instead..."
  bash "$SCRIPT_DIR/install.sh"
  exit 0
fi

SKILLS=(
  "page-audit"
  "cms-format"
  "content-match"
  "visual-diff"
  "table-compare"
  "figma-to-code"
  "feature-table"
)

updated=0
skipped=0

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill/SKILL.md"
  dst_dir="$SKILLS_DIR/$skill"
  dst="$dst_dir/SKILL.md"

  if [[ ! -f "$src" ]]; then
    echo "  SKIP  /$skill  (source not found)"
    ((skipped++)) || true
    continue
  fi

  mkdir -p "$dst_dir"

  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    echo "  --    /$skill  (no changes)"
    ((skipped++)) || true
  else
    cp "$src" "$dst"
    echo "  ✓     /$skill  (updated)"
    ((updated++)) || true
  fi
done

echo ""
echo "══════════════════════════════════════════════════════"
echo "  Done: $updated updated, $skipped unchanged"
echo "  Changes take effect immediately — no restart needed."
echo "══════════════════════════════════════════════════════"
echo ""
