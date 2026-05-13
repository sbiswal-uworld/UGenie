# 🧠 UWorld WebGenie — Claude Code Skills

> **8 production-ready Claude Code slash commands** for the UWorld web team.  
> No API key. No extra cost. Works on every team member's machine instantly.

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-6B46C1?style=for-the-badge&logo=anthropic&logoColor=white)
![Skills](https://img.shields.io/badge/Skills-8%20Commands-0066CC?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-28A745?style=for-the-badge)

---

## 📋 Table of Contents

1. [What Are Claude Code Skills?](#1-what-are-claude-code-skills)
2. [Prerequisites](#2-prerequisites)
3. [Repository Structure](#3-repository-structure)
4. [The 8 Skills](#4-the-8-skills)
5. [Installation Guide](#5-installation-guide)
6. [How to Use Each Skill](#6-how-to-use-each-skill)
7. [How to Create a New Skill](#7-how-to-create-a-new-skill)
8. [How to Update Skills](#8-how-to-update-skills)

---

## 1. What Are Claude Code Skills?

Claude Code Skills are **custom slash commands** that extend what Claude Code can do. Each skill is a Markdown file with a YAML frontmatter header. When you type `/skill-name` in Claude Code, it loads that file as the system prompt and executes it.

```
You type:  /page-audit https://uworld.com/cfa/
Claude:    Fetches the page → runs full SEO + QA audit → returns structured report
```

Skills live in a folder on your machine:

```
~/.claude/skills/
├── page-audit/
│   └── SKILL.md        ← this is a slash command: /page-audit
├── cms-format/
│   └── SKILL.md        ← this is a slash command: /cms-format
└── ...
```

> **No server. No API key. No extra subscription.**  
> Skills use your existing Claude Code session.

---

## 2. Prerequisites

Before installing, make sure you have:

| Requirement | How to Check | Install Link |
|---|---|---|
| Claude Code | Run `claude --version` in terminal | [claude.ai/code](https://claude.ai/code) |
| Git | Run `git --version` | [git-scm.com](https://git-scm.com) |
| Terminal / Git Bash | Open Git Bash on Windows | Included with Git |

### ✅ Verify Claude Code is installed

Open your terminal (Git Bash on Windows) and run:

```bash
claude --version
```

Expected output:
```
2.1.114 (Claude Code)
```

---

## 3. Repository Structure

```
uworld-webgenie-commands/
│
├── 📄 README.md              ← You are here
├── 📄 install.sh             ← Run once to install all skills
├── 📄 update.sh              ← Run after git pull to update
│
├── 📁 skills/                ← Source files for all 8 skills
│   ├── page-audit/
│   │   └── SKILL.md
│   ├── cms-format/
│   │   └── SKILL.md
│   ├── content-match/
│   │   └── SKILL.md
│   ├── visual-diff/
│   │   └── SKILL.md
│   ├── table-compare/
│   │   └── SKILL.md
│   ├── figma-to-code/
│   │   └── SKILL.md
│   ├── figma-to-elementor/
│   │   └── SKILL.md
│   └── feature-table/
│       └── SKILL.md
│
└── 📁 docs/                  ← Detailed guides
    ├── create-a-skill.md
    ├── install-guide.md
    ├── usage-guide.md
    └── troubleshooting.md
```

---

## 4. The 8 Skills

| Skill | Command | Role | What It Does |
|---|---|---|---|
| Page Audit | `/page-audit` | QA Engineers | Full SEO, images, links, and schema audit on any URL |
| CMS Formatter | `/cms-format` | CMS / Content | Converts raw CMS HTML to UWorld golden standard |
| Content Match | `/content-match` | Content / QA | Compares brief/doc against live page, flags every discrepancy |
| Visual Diff | `/visual-diff` | QA / Dev | Compares Figma design vs live page (pixel-perfect fidelity scoring) |
| Table Compare | `/table-compare` | QA / Content | Cell-by-cell table comparison |
| Figma to Code | `/figma-to-code` | Developers | Converts design screenshot to HTML/Tailwind/React |
| **Figma to Elementor** | **`/figma-to-elementor`** | **Developers** | **Converts Figma designs to production-ready Elementor JSON for WordPress** |
| Feature Table | `/feature-table` | Developers | Generates UWorld comparison table HTML |

---

## 5. Installation Guide

### Step 1 — Clone the Repository

Open **Git Bash** (Windows) or your terminal (Mac/Linux):

```bash
git clone https://github.com/sbiswal-uworld/UGenie.git
cd UGenie/uworld-webgenie-commands
```

### Step 2 — Run the Installer

```bash
bash install.sh
```

You should see:

```
╔══════════════════════════════════════════════════╗
║     UWorld WebGenie — Claude Code Installer      ║
╚══════════════════════════════════════════════════╝

✓  Claude Code found: 2.1.114 (Claude Code)
✓  Skills directory ready: /c/Users/yourname/.claude/skills

Installing skills...

  ✓     /page-audit
  ✓     /cms-format
  ✓     /content-match
  ✓     /visual-diff
  ✓     /table-compare
  ✓     /figma-to-code
  ✓     /figma-to-elementor
  ✓     /feature-table

══════════════════════════════════════════════════════
  Installation complete! 8 skills installed.
══════════════════════════════════════════════════════
```

### Step 3 — Open Claude Code and Verify

Open a new terminal and run:

```bash
claude
```

Type `/` — you should see all 8 skills appear in the autocomplete menu.

---

## 6. How to Use Each Skill

### `/page-audit` — Full Page QA Audit

```
/page-audit <url> [product|pillar|blog]
```

**Examples:**
```
/page-audit https://finance.uworld.com/cfa/level-1/courses/
/page-audit https://gradschool.uworld.com/mcat/prep-books/ product
/page-audit https://www.uworld.com/blog/cfa-exam-tips pillar
```

**Returns:** Overall score, section scores (SEO/Images/Links/Schema), full image table, link table, QA checklist, and P1/P2/P3 fix list.

---

### `/cms-format` — CMS Question Formatter

```
/cms-format
[paste your raw CMS HTML or question text here]
```

**Example input:**
```
/cms-format
Which of the following best describes duration?

A ) A measure of credit risk
B ) A measure of interest rate sensitivity
[correct]
C ) A measure of liquidity risk
```

**Returns:** Clean UWorld-standard HTML with proper radio buttons, explanation structure, and MathJax script tag.

---

### `/content-match` — Compare Brief vs Live Page

```
/content-match <live-url>
[paste your source brief or Google Doc content here]
```

**Example:**
```
/content-match https://finance.uworld.com/cfa/level-1/
Hero headline: Pass the CFA® Level I Exam
CTA button: Start Free Trial
Price: $399
```

**Returns:** Section-by-section comparison table with MATCH/MISMATCH/MISSING status and P1/P2/P3 severity.

---

### `/visual-diff` — Design vs Live Comparison

```
/visual-diff <figma-url|file-key> <live-url>
```

**Example:**
```
/visual-diff https://figma.com/design/a1b2c3d4/Design-File?node-id=123-456 https://live.uworld.com/page/
```

**Returns:** Fidelity scores per section, design token comparison, component inventory, full pixel-perfect diff report.

---

### `/table-compare` — Cell-by-Cell Table Comparison

```
/table-compare

SOURCE TABLE (Doc):
Feature | UWorld      | Competitors
QBank   | 3,000+      | 1,500

LIVE TABLE (Page):
[paste live table content or provide URL]
```

**Returns:** Cell-by-cell MATCH/WRONG/MISSING/EXTRA status with overall match rate.

---

### `/figma-to-code` — Design to Code

```
/figma-to-code html
[attach design screenshot]

/figma-to-code react
[attach design screenshot]

/figma-to-code tailwind
[attach design screenshot]
```

**Returns:** Raw production-ready HTML+CSS, React component, or Tailwind HTML.

---

### `/figma-to-elementor` — Figma to WordPress Elementor

```
/figma-to-elementor <figma-url|file-key> [node-id]
```

**Example:**
```
/figma-to-elementor https://figma.com/design/a1b2c3d4e5f6/UGenie?node-id=123-456
```

**What it does:**
- Extracts all design tokens from Figma (colors, fonts, spacing, shadows, layout)
- Generates production-ready Elementor JSON
- Validates structure with pre-flight checklist
- Includes responsive breakpoints (desktop, tablet, mobile)
- Ready to import directly into WordPress Elementor

**Returns:** Valid Elementor JSON export file + import instructions

**Time savings:**
- Manual Figma→Elementor: 4–6 hours per page
- With this skill: 20–30 minutes per page
- **10x faster** for landing pages, course pages, module layouts

---

### `/feature-table` — Comparison Table Generator

```
/feature-table
[paste feature comparison list]
```

**Example:**
```
/feature-table
Core Plan: 2,800 questions, 5 mock exams, video lectures
Advanced Plan: 3,500 questions, 10 mock exams, video lectures, flashcards
Elite Plan: Full access + live Q&A, instructor sessions, coaching
```

**Returns:** Desktop HTML table + mobile accordion HTML, both production-ready.

---

## 7. How to Create a New Skill

1. Create a new directory: `skills/[skill-name]/`
2. Create `SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill
description: What this skill does (one line)
author: Your Name
version: 1.0.0
category: development
user-invokable: true
argument-hint: "<arg1> [arg2]"
license: MIT
---

# My Skill

[Your skill content here...]
```

3. Run `bash update.sh` to sync to your local `~/.claude/skills/`
4. Test with `/my-skill` in Claude Code

---

## 8. How to Update Skills

After pulling the latest changes from GitHub:

```bash
git pull origin main
bash update.sh
```

This copies all updated SKILL.md files to your local `~/.claude/skills/` directory and refreshes Claude Code's skill index.

---

## 🚀 Common Workflows

### Workflow 1: Design → Live Page (Figma → WordPress)
```
Designer uploads Figma
  ↓
Run: /figma-to-elementor <figma-url>
  ↓
Get Elementor JSON export
  ↓
Import JSON into WordPress Elementor
  ↓
Test on staging server
  ↓
Publish to production
```
**Time:** Design → Live = ~30 min (vs. 6–8 hours manual)

### Workflow 2: Pre-Launch SEO Check
```
Page is designed & content drafted
  ↓
Run: /page-audit <staging-url>
  ↓
Get comprehensive SEO report + fix list
  ↓
Fix P1 issues (schema, meta description, alt text)
  ↓
Re-run /page-audit to verify
  ↓
Launch with confidence
```
**Time:** ~45 min → Catches 90% of SEO issues pre-launch

### Workflow 3: Design QA (Figma vs Live)
```
Page is live, design looks different
  ↓
Run: /visual-diff <figma-url> <live-url>
  ↓
Get component-by-component comparison
  ↓
Fidelity scoring + P1/P2/P3 issues flagged
  ↓
Prioritize design backlog
```
**Time:** ~30 min → Quantified design debt

---

## 📚 Documentation

Each skill has complete documentation in its SKILL.md file:
- Full methodology
- Step-by-step process
- Output format examples
- Error handling
- Key distinctions

---

## 🤝 Contributing

To contribute a new skill or improve an existing one:

1. Create your skill in `uworld-webgenie-commands/skills/`
2. Test with `/skill-name`
3. Submit a pull request with clear description
4. Update this README with the new skill in Section 4

---

## 📝 License

MIT License — All skills are open-source and free to use within UWorld development.

---

## 👤 Author

**Sangram Biswal** — UWorld Web Engineering & SEO Optimization

---

**Built with ❤️ for faster, smarter development.**
