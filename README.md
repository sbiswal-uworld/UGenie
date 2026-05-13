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
9. [Sharing with Your Team](#9-sharing-with-your-team)
10. [Troubleshooting](#10-troubleshooting)
11. [Role Guide](#11-role-guide)

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
├── 📁 skills/                ← Source files for all 7 skills
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
| Visual Diff | `/visual-diff` | QA / Dev | Compares Figma design vs live page |
| Table Compare | `/table-compare` | QA / Content | Cell-by-cell table comparison |
| Figma to Code | `/figma-to-code` | Developers | Converts design screenshot to HTML/Tailwind/React |
| Figma to Elementor | `/figma-to-elementor` | Developers | Converts Figma design to pixel-perfect Elementor JSON — **requires Figma MCP** |
| Feature Table | `/feature-table` | Developers | Generates UWorld comparison table HTML |

---

## 5. Installation Guide

### Step 1 — Clone the Repository

Open **Git Bash** (Windows) or your terminal (Mac/Linux):

```bash
git clone https://github.com/YOUR-ORG/uworld-webgenie-commands.git
```

> Replace `YOUR-ORG` with your actual GitHub organization name.

### Step 2 — Navigate Into the Folder

```bash
cd uworld-webgenie-commands
```

### Step 3 — Run the Installer

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

### Step 4 — Open Claude Code and Verify

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
/visual-diff <live-url>
[attach your Figma screenshot or design export]
```

**Returns:** Fidelity scores per section, design token comparison, full diff report.

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

### `/figma-to-elementor` — Figma Design to Elementor JSON

> **Connecting Figma MCP to Elementor is mandatory.**  
> The Figma MCP must be active and connected before running this skill.  
> It is the only way to accurately extract design tokens (colors, spacing, fonts, shadows, gradients).  
> If `get_design_context` returns an error, stop and reconnect Figma MCP before proceeding.

**Trigger phrase:**

```
Implement this design from Figma.
@https://www.figma.com/design/...
```

**Example:**

```
Implement this design from Figma.
@https://www.figma.com/design/AbCdEf123456/UWorld-Homepage?node-id=1-2
```

**What it does:**

1. Parses the Figma URL to extract `fileKey` and `nodeId`
2. Calls `get_design_context` via Figma MCP to extract every design token
3. Builds Elementor JSON bottom-up (leaf widgets → containers → root)
4. Runs the pre-flight checklist to validate JSON structure
5. Saves the output file to `C:\Users\sbiswal\Downloads\Productivity Tool\Elementor JSON Exports\`

**Returns:** A valid Elementor JSON file importable directly into WordPress via Elementor > Import.

**Requirements:**

| Requirement | Details |
|---|---|
| Figma MCP | Must be connected — skill will not proceed without it |
| Figma URL | Must include `node-id` parameter pointing to the specific frame/section |
| Output folder | `C:\Users\sbiswal\Downloads\Productivity Tool\Elementor JSON Exports\` must exist |

---

### `/feature-table` — Comparison Table Generator

```
/feature-table
[paste feature comparison list]
```

**Returns:** Desktop HTML table + mobile accordion HTML, both production-ready.

---

## 7. How to Create a New Skill

> Full guide: [docs/create-a-skill.md](docs/create-a-skill.md)

### Step 1 — Create the Skill Directory

```bash
mkdir -p skills/my-new-skill
```

### Step 2 — Create the SKILL.md File

```bash
touch skills/my-new-skill/SKILL.md
```

### Step 3 — Add YAML Frontmatter (Required)

Open the file and add this at the very top:

```yaml
---
name: my-new-skill
description: "One sentence describing what this skill does and when to use it."
user-invokable: true
argument-hint: "<required-arg> [optional-arg]"
---
```

**Required fields:**

| Field | Required | Description |
|---|---|---|
| `name` | ✅ Yes | The slash command name (no spaces, use hyphens) |
| `description` | ✅ Yes | Shown in autocomplete. Claude also uses this to auto-trigger. |
| `user-invokable` | ✅ Yes | Must be `true` for the user to invoke with `/` |
| `argument-hint` | Optional | Shown as hint in autocomplete |

### Step 4 — Write the Skill Instructions

After the closing `---`, write your skill instructions in Markdown:

```markdown
---
name: my-new-skill
description: "Does X when Y happens."
user-invokable: true
argument-hint: "<url>"
---

# My New Skill

You are a [role]. When the user provides [input], do [task].

## Steps

1. First do this
2. Then do this
3. Output in this format

## Output Format

[describe exact output structure]
```

### Step 5 — Install the New Skill

```bash
bash install.sh
```

Or manually copy it:

```bash
mkdir -p ~/.claude/skills/my-new-skill
cp skills/my-new-skill/SKILL.md ~/.claude/skills/my-new-skill/SKILL.md
```

### Step 6 — Test It

Open Claude Code and type `/my-new-skill` — it should appear immediately (no restart needed).

---

## 8. How to Update Skills

When a skill is updated in the repository:

```bash
# Get latest changes
git pull

# Apply updates
bash update.sh
```

Output:
```
  ✓     /page-audit  (updated)
  --    /cms-format  (no changes)
  --    /content-match  (no changes)
  ...
  Done: 1 updated, 6 unchanged
  Changes take effect immediately — no restart needed.
```

Changes are picked up **live** — no need to restart Claude Code.

---

## 9. Sharing with Your Team

### Option A — GitHub (Recommended)

1. Create a private GitHub repository
2. Push this folder to it:

```bash
git init
git add .
git commit -m "Initial WebGenie skills"
git remote add origin https://github.com/YOUR-ORG/uworld-webgenie-commands.git
git push -u origin main
```

3. Each team member runs **once**:

```bash
git clone https://github.com/YOUR-ORG/uworld-webgenie-commands.git
cd uworld-webgenie-commands
bash install.sh
```

4. When skills are updated, each team member runs:

```bash
cd uworld-webgenie-commands
git pull
bash update.sh
```

### Option B — Shared Network Drive

Copy the folder to a shared drive. Each team member runs `bash install.sh` from the shared location.

### Option C — USB / ZIP

Share the zip file. Each member extracts and runs `bash install.sh`.

---

## 10. Troubleshooting

### ❌ "Unknown command: /page-audit"

**Cause:** Flat `.md` files in `~/.claude/commands/` don't work. Skills must be in `~/.claude/skills/<name>/SKILL.md`.

**Fix:**
```bash
bash install.sh
```

Then restart Claude Code.

---

### ❌ Skill not showing in `/` autocomplete

**Cause 1:** Missing or malformed YAML frontmatter.

**Fix:** Open the SKILL.md and verify the frontmatter block:
```yaml
---
name: skill-name        ← must match folder name
description: "..."      ← must be present
user-invokable: true    ← must be exactly this
---
```

**Cause 2:** New `~/.claude/skills/` directory didn't exist when session started.

**Fix:** Restart Claude Code.

---

### ❌ "claude: command not found"

Claude Code is not installed or not in PATH.

**Fix:** Install from [claude.ai/code](https://claude.ai/code), then restart your terminal.

---

### ❌ `bash install.sh` gives "Permission denied"

**Fix:**
```bash
chmod +x install.sh update.sh
bash install.sh
```

---

### ✅ Verify Skills Are Installed

```bash
ls ~/.claude/skills/
```

Expected output:
```
cms-format/     content-match/      feature-table/  figma-to-code/
figma-to-elementor/  page-audit/   table-compare/  visual-diff/
```

---

## 11. Role Guide

| Role | Primary Skills |
|---|---|
| QA Engineer | `/page-audit` `/table-compare` `/visual-diff` `/content-match` |
| Frontend Developer | `/figma-to-code` `/figma-to-elementor` `/feature-table` `/page-audit` |
| CMS / Content Editor | `/cms-format` `/content-match` `/table-compare` |
| Full-Stack Developer | `/page-audit` `/content-match` `/figma-to-code` |

---

## Contributing

To add or update a skill:

1. Create a branch: `git checkout -b add/skill-name`
2. Add your skill under `skills/<skill-name>/SKILL.md`
3. Test it locally with `bash install.sh`
4. Open a pull request

See [docs/create-a-skill.md](docs/create-a-skill.md) for the full authoring guide.

---

*Built for the UWorld web team · Powered by [Claude Code](https://claude.ai/code)*
