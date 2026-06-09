#!/usr/bin/env bash
# UWorld WebGenie — Claude Code Skills Installer
# Run this ONCE on each team member's machine.
# Usage: bash install.sh

set -e

SKILLS_DIR="$HOME/.claude/skills"
COMMANDS_DIR="$HOME/.claude/commands"
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

# ── Create directories ──────────────────────────────────────────────────────────
mkdir -p "$SKILLS_DIR"
mkdir -p "$COMMANDS_DIR"
echo "✓  Skills directory ready:   $SKILLS_DIR"
echo "✓  Commands directory ready: $COMMANDS_DIR"

# ── Skill list ──────────────────────────────────────────────────────────────────
SKILLS=(
  "page-audit"
  "cms-format"
  "content-match"
  "QA-content-verify"
  "visual-diff"
  "table-compare"
  "figma-to-code"
  "figma-to-elementor"
  "feature-table"
  "gdoc-to-html"
)

echo ""
echo "Installing skills..."
echo ""

installed=0

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill/SKILL.md"

  if [[ ! -f "$src" ]]; then
    echo "  SKIP  /$skill  (source SKILL.md not found)"
    continue
  fi

  # ── Extract version from SKILL.md frontmatter (if present) ────────────────
  ver=$(grep -m1 '^version:' "$src" 2>/dev/null | awk '{print $2}' || true)
  ver_label=${ver:+" v$ver"}

  # ── Copy to ~/.claude/skills/<name>/SKILL.md ──────────────────────────────
  dst_dir="$SKILLS_DIR/$skill"
  dst="$dst_dir/SKILL.md"
  mkdir -p "$dst_dir"
  if [[ -f "$dst" ]] && ! cmp -s "$src" "$dst"; then
    cp "$dst" "${dst}.bak"
  fi
  cp "$src" "$dst"

  # ── Copy to ~/.claude/commands/<name>.md ──────────────────────────────────
  cmd="$COMMANDS_DIR/$skill.md"
  if [[ -f "$cmd" ]] && ! cmp -s "$src" "$cmd"; then
    cp "$cmd" "${cmd}.bak"
  fi
  cp "$src" "$cmd"

  echo "  ✓     /$skill${ver_label}"
  ((installed++)) || true
done

echo ""
echo "══════════════════════════════════════════════════════"
printf "  Installation complete! %d skills installed.\n" "$installed"
echo ""
echo "  Type / in Claude Code to see all commands:"
echo ""
echo "    /page-audit          v2.5.0  — Full SEO + QA audit (9 dimensions)"
echo "    /cms-format                  — Format CMS question HTML to UWorld standard"
echo "    /content-match       v4.0.0  — Full compliance audit: brief vs live page"
echo "                                   (Google Drive MCP recommended)"
echo "    /QA-content-verify   v1.0.0  — Senior QA audit: source doc vs Elementor HTML"
echo "                                   (9 content categories, checkbox tables, PMM flagging)"
echo "    /visual-diff         v2.0.0  — Figma design vs live comparison"
echo "                                   (Figma MCP required)"
echo "    /table-compare               — Cell-by-cell table comparison"
echo "    /figma-to-code               — Design screenshot → HTML / React / Tailwind"
echo "    /figma-to-elementor          — Figma design → Elementor JSON"
echo "                                   (Figma MCP required)"
echo "    /feature-table               — Generate UWorld comparison table HTML"
echo "    /gdoc-to-html                — Google Doc / Word → UWorld-standard HTML"
echo ""
echo "  To update skills later, run: bash update.sh"
echo "══════════════════════════════════════════════════════"
echo ""
