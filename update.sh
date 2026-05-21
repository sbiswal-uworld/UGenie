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

echo "Checking skills..."
echo ""

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

  # ── Extract version from repo SKILL.md ────────────────────────────────────
  new_ver=$(grep -m1 '^version:' "$src" 2>/dev/null | awk '{print $2}' || true)

  # ── Extract version currently installed ───────────────────────────────────
  old_ver=""
  if [[ -f "$dst" ]]; then
    old_ver=$(grep -m1 '^version:' "$dst" 2>/dev/null | awk '{print $2}' || true)
  fi

  mkdir -p "$dst_dir"

  # ── Update ~/.claude/skills/<name>/SKILL.md ───────────────────────────────
  if [[ ! -f "$dst" ]] || ! cmp -s "$src" "$dst"; then
    cp "$src" "$dst"
    skill_changed=true
  fi

  # ── Update ~/.claude/commands/<name>.md ───────────────────────────────────
  if [[ ! -f "$cmd" ]] || ! cmp -s "$src" "$cmd"; then
    cp "$src" "$cmd"
    skill_changed=true
  fi

  if $skill_changed; then
    if [[ -n "$old_ver" && -n "$new_ver" && "$old_ver" != "$new_ver" ]]; then
      echo "  ✓     /$skill  (v$old_ver → v$new_ver)"
    elif [[ -n "$new_ver" ]]; then
      echo "  ✓     /$skill  (updated  v$new_ver)"
    else
      echo "  ✓     /$skill  (updated)"
    fi
    ((updated++)) || true
  else
    if [[ -n "$new_ver" ]]; then
      echo "  --    /$skill  (v$new_ver — no changes)"
    else
      echo "  --    /$skill  (no changes)"
    fi
    ((skipped++)) || true
  fi
done

echo ""
echo "══════════════════════════════════════════════════════"
printf "  Done: %d updated, %d unchanged\n" "$updated" "$skipped"
echo "  Changes take effect immediately — no restart needed."
echo "══════════════════════════════════════════════════════"
echo ""
