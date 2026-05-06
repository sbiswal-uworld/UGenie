#!/usr/bin/env bash
# UWorld WebGenie — Claude Code Commands Installer
# Run this ONCE on each team member's machine.
# Usage: bash install.sh

set -e

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     UWorld WebGenie — Claude Code Installer      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Check Claude Code is installed ─────────────────────────────────────────────
if ! command -v claude &>/dev/null; then
  echo "ERROR: Claude Code ('claude') is not installed or not in PATH."
  echo "Install it from: https://claude.ai/code"
  exit 1
fi

echo "✓  Claude Code found: $(claude --version 2>/dev/null || echo 'installed')"

# ── Create skills directory ─────────────────────────────────────────────────────
mkdir -p "$SKILLS_DIR"
echo "✓  Skills directory ready: $SKILLS_DIR"

# ── Copy skill directories ──────────────────────────────────────────────────────
SKILLS=(
  "page-audit"
  "cms-format"
  "content-match"
  "visual-diff"
  "table-compare"
  "figma-to-code"
  "feature-table"
)

echo ""
echo "Installing skills..."
echo ""

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill/SKILL.md"
  dst_dir="$SKILLS_DIR/$skill"
  dst="$dst_dir/SKILL.md"

  if [[ ! -f "$src" ]]; then
    echo "  SKIP  /$skill  (source SKILL.md not found)"
    continue
  fi

  mkdir -p "$dst_dir"

  # Back up existing file if it differs
  if [[ -f "$dst" ]] && ! cmp -s "$src" "$dst"; then
    cp "$dst" "${dst}.bak"
  fi

  cp "$src" "$dst"
  echo "  ✓     /$skill"
done

echo ""
echo "══════════════════════════════════════════════════════"
echo "  Installation complete! 7 skills installed."
echo ""
echo "  Type / in Claude Code to see all commands:"
echo ""
echo "    /page-audit     — Full page QA audit"
echo "    /cms-format     — Format CMS question HTML"
echo "    /content-match  — Compare brief vs live page"
echo "    /visual-diff    — Design vs live comparison"
echo "    /table-compare  — Cell-by-cell table comparison"
echo "    /figma-to-code  — Design screenshot to code"
echo "    /feature-table  — Generate comparison table HTML"
echo ""
echo "  To update skills later, run: bash update.sh"
echo "══════════════════════════════════════════════════════"
echo ""
