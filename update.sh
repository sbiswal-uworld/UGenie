#!/usr/bin/env bash
# UWorld WebGenie — Claude Code Skills Updater
# Run this after git pull to sync latest versions.
# Usage: bash update.sh

set -e

SKILLS_DIR="$HOME/.claude/skills"
COMMANDS_DIR="$HOME/.claude/commands"
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

mkdir -p "$COMMANDS_DIR"

SKILLS=(
  "page-audit"
  "cms-format"
  "content-match"
  "visual-diff"
  "table-compare"
  "figma-to-code"
  "figma-to-elementor"
  "feature-table"
  "gdoc-to-html"
)

updated=0
skipped=0

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill/SKILL.md"
  dst_dir="$SKILLS_DIR/$skill"
  dst="$dst_dir/SKILL.md"
  cmd="$COMMANDS_DIR/$skill.md"
  skill_changed=false

  if [[ ! -f "$src" ]]; then
    echo "  SKIP  /$skill  (source not found)"
    ((skipped++)) || true
    continue
  fi

  mkdir -p "$dst_dir"

  # Update ~/.claude/skills/<name>/SKILL.md
  if [[ ! -f "$dst" ]] || ! cmp -s "$src" "$dst"; then
    cp "$src" "$dst"
    skill_changed=true
  fi

  # Update ~/.claude/commands/<name>.md
  if [[ ! -f "$cmd" ]] || ! cmp -s "$src" "$cmd"; then
    cp "$src" "$cmd"
    skill_changed=true
  fi

  if $skill_changed; then
    echo "  ✓     /$skill  (updated)"
    ((updated++)) || true
  else
    echo "  --    /$skill  (no changes)"
    ((skipped++)) || true
  fi
done

echo ""
echo "══════════════════════════════════════════════════════"
echo "  Done: $updated updated, $skipped unchanged"
echo "  Changes take effect immediately — no restart needed."
echo "══════════════════════════════════════════════════════"
echo ""
