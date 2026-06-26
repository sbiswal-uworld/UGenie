# 🧠 UWorld WebGenie — Claude Code Skills

> **10 production-ready Claude Code slash commands** for the UWorld web team.  
> No API key. No extra cost. Works on every team member's machine instantly.

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-6B46C1?style=for-the-badge&logo=anthropic&logoColor=white)
![Skills](https://img.shields.io/badge/Skills-10%20Commands-0066CC?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-28A745?style=for-the-badge)

---

## 📋 Table of Contents

1. [What Are Claude Code Skills?](#1-what-are-claude-code-skills)
2. [Prerequisites](#2-prerequisites)
3. [Repository Structure](#3-repository-structure)
4. [The 10 Skills](#4-the-10-skills)
5. [Installation Guide](#5-installation-guide)
6. [How to Use Each Skill](#6-how-to-use-each-skill)
7. [How to Create a New Skill](#7-how-to-create-a-new-skill)
8. [How to Update Skills](#8-how-to-update-skills)
9. [Troubleshooting](#9-troubleshooting)
10. [Role Guide](#10-role-guide)

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
├── 📁 skills/                ← Source files for all 10 skills
│   ├── page-audit/
│   │   └── SKILL.md
│   ├── cms-format/
│   │   └── SKILL.md
│   ├── content-match/
│   │   └── SKILL.md
│   ├── QA-content-verify/
│   │   └── SKILL.md
│   ├── visual-diff/
│   │   └── SKILL.md
│   ├── table-compare/
│   │   └── SKILL.md
│   ├── figma-to-code/
│   │   └── SKILL.md
│   ├── figma-to-elementor/
│   │   └── SKILL.md
│   ├── feature-table/
│   │   └── SKILL.md
│   └── gdoc-to-html/
│       └── SKILL.md
│
└── 📁 docs/                  ← Detailed guides
    ├── create-a-skill.md
    ├── install-guide.md
    ├── usage-guide.md
    └── troubleshooting.md
```

---

## 4. The 10 Skills

| Skill | Command | Role | What It Does |
|---|---|---|---|
| Page Audit | `/page-audit` | QA Engineers | Full SEO, images, links, and schema audit on any URL |
| CMS Formatter | `/cms-format` | CMS / Content | Converts raw CMS HTML to UWorld golden standard |
| Content Match | `/content-match` | Content / QA | **v4.0.0** — Full compliance audit: semantic diff + Elementor ID tracking + link audit + error classification (❌ Fail / ⚠️ PMM) + 4 structured reports — **Google Drive MCP recommended** |
| **QA Content Verify** | **`/QA-content-verify`** | **QA / Developers** | **v1.0.0** — Manual QA audit: Line-by-line verification of source docs vs live Elementor HTML with checkbox tables, Quick Fix List, PMM List — **9 content categories** |
| Visual Diff | `/visual-diff` | QA / Dev | Compares Figma design vs live page with pixel-perfect fidelity scores — **requires Figma MCP** |
| Table Compare | `/table-compare` | QA / Content | Cell-by-cell table comparison |
| Figma to Code | `/figma-to-code` | Developers | Converts design screenshot to HTML/Tailwind/React |
| Figma to Elementor | `/figma-to-elementor` | Developers | Converts Figma design to pixel-perfect Elementor JSON — **requires Figma MCP** |
| Feature Table | `/feature-table` | Developers | Generates UWorld comparison table HTML |
| GDoc to HTML | `/gdoc-to-html` | CMS / Content | Converts pasted Google Doc or Word content to clean UWorld-standard HTML |
| CWV Audit | `/cwv-audit` | Dev / QA | Core Web Vitals & PageSpeed audit for WordPress/Elementor/WP Rocket — field-data-first optimization plan after page development |

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
  ✓     /QA-content-verify
  ✓     /visual-diff
  ✓     /table-compare
  ✓     /figma-to-code
  ✓     /figma-to-elementor
  ✓     /feature-table
  ✓     /gdoc-to-html

══════════════════════════════════════════════════════
  Installation complete! 10 skills installed.
══════════════════════════════════════════════════════
```

### Step 4 — Open Claude Code and Verify

Open a new terminal and run:

```bash
claude
```

Type `/` — you should see all 10 skills appear in the autocomplete menu.

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

### `/content-match` — Full Compliance Audit (Brief vs Live Page)

> **v4.0.0** — Full compliance audit engine. Compares every element of the approved source document against the live Elementor page. Every mismatch is flagged, classified, and reported with actionable fixes across 4 structured reports.
>
> ⚠️ **Google Drive MCP is recommended** to access Google Docs directly via URL. Without it, paste the CONTENT section text manually instead.

**Three ways to provide source content:**

```
# Option 1 — Google Doc URL (recommended, requires Google Drive MCP)
/content-match https://finance.uworld.com/cfa/level-1/ https://docs.google.com/document/d/[ID]/edit

# Option 2 — Paste CONTENT section
/content-match https://finance.uworld.com/cfa/level-1/
[paste CONTENT section here — excludes SUMMARY, DEVELOPER NOTES, SEO OUTLINE, etc.]

# Option 3 — Public Google Doc link
/content-match https://finance.uworld.com/cfa/level-1/ https://docs.google.com/document/d/[ID]/edit?usp=sharing
```

**What it does:**

1. **Auto-fetches** source document via Google Drive MCP (any access level) or curl — never asks you to manually copy-paste
2. Extracts **CONTENT section only** — ignores SUMMARY, DEVELOPER NOTES, SEO OUTLINE, DESIGN DELIVERABLES, etc.
3. Parses both source and live page into typed semantic blocks (H1/H2/H3, paragraphs, lists, CTAs, tables, FAQs, testimonials, disclaimers)
4. Runs **line-by-line semantic diff** using Jaro-Winkler + Levenshtein similarity scoring
5. Tracks **Elementor element IDs** (`data-id`) for every live page element
6. Audits **every link** for `target="_blank"` (external) and `rel="noopener noreferrer"` rules
7. Classifies every mismatch as ❌ FAIL (HTML error) or ⚠️ PMM (source doc error)
8. Generates **4 structured reports**: Checkbox Audit Table, Quick Fix List, PMM List, Summary KPI

**Match statuses:** `EXACT` / `SIMILAR` / `CHANGED` / `MISSING` / `EXTRA` / `REORDERED`

**Error classifications:**
| Code | Meaning | Who Fixes It |
|---|---|---|
| ✅ PASS | Perfect match | — |
| ❌ FAIL | HTML differs from approved doc | Developer / CMS |
| ⚠️ PMM | Error in BOTH doc AND live — source needs correction | Content / PMM |
| 🔗 LINK-FAIL | Link rule violation (wrong `target`, missing `rel`) | Developer |
| 🔴 P1 | Critical: brand, pricing, trademark, heading level | Fix immediately |
| 🟡 P2 | High: content mismatch, list order, CTA URL | Fix this sprint |
| 🟢 P3 | Medium: minor wording, whitespace, formatting | Fix next sprint |

**Severity levels:**
| Pass Rate | Level |
|---|---|
| 95–100% | ✅ PASS |
| 85–94% | ⚠️ NEEDS ATTENTION |
| 70–84% | ❌ MAJOR ISSUES |
| < 70% | 🚨 CRITICAL |

**Returns:** 4 reports — Checkbox Audit Table (every element), Quick Fix List (P1/P2/P3 dev fixes), PMM List (source doc errors), Summary KPI counts + Visual Diff (diffchecker-style side-by-side for all changed/missing blocks) + Trademark & Legal Audit (19 UWorld product names).

**Requirements:**

| Requirement | Details |
|---|---|
| Google Drive MCP | Recommended — enables direct Google Doc access at any sharing level. Without it, paste CONTENT section manually. |
| Source input | CONTENT section only — no metadata, no SUMMARY, no DEVELOPER NOTES |
| Live URL | Any publicly accessible UWorld page URL |

---

### `/QA-content-verify` — Manual QA Content Audit

> **v1.0.0** — Line-by-line QA verification of source documents against live Elementor HTML. Professional checkpoint audit with checkbox tables, Quick Fix lists, and PMM flagging.

```
/QA-content-verify

Internal Domain: [your-domain.uworld.com]
Page URL: [full page URL]

[PASTE SOURCE DOCUMENT]

[PASTE ELEMENTOR HTML]
```

**Example:**
```
/QA-content-verify

Internal Domain: finance.uworld.com
Page URL: https://finance.uworld.com/cfa-level-1/study-guides/

# SOURCE DOCUMENT
H1: CFA Level 1 Study Books & Guides
Price: $299 starting at $27/month with Affirm
Button: Buy Now

# ELEMENTOR HTML
<h1>CFA Level 1 Study Books & Guides</h1>
...
```

**What it does:**

1. **9 Content Categories Audited:**
   - Text content (headings H1/H2/H3, body paragraphs, lists, inline formatting)
   - Structured content (tables, FAQ Q&A, mobile accordion variations)
   - Media (images, alt text, captions)
   - CTAs & Links (button text, URLs, `target="_blank"` compliance)
   - Icons (Font Awesome class validation)
   - Pricing & JS-rendered values
   - Popups & Modals
   - Missing sections (bidirectional check)
   - Document-level issues (PMM flagging for source doc errors)

2. **Professional Output:**
   - Section-by-section checkbox tables (Check # | What | Status | Element ID | Doc Says | HTML Says | Action)
   - Quick Fix List (❌ Fail items sorted top-to-bottom, P1/P2/P3 severity)
   - PMM List (⚠️ items for content team review)
   - Summary Counts (Total Pass / Fail / PMM)

3. **Key Features:**
   - Elementor element ID tracking on every row
   - Character-level accuracy (spaces, punctuation, trademarks ® ™)
   - One issue per row (never combines multiple failures)
   - Desktop + Mobile dual-audit support (separate rows per version)
   - Global check numbering across all sections
   - Strict "Match" shorthand for identical Pass rows

**Status Classifications:**
| Status | Meaning | Action | Owner |
|---|---|---|---|
| ✅ **Pass** | Content matches exactly | None | — |
| ❌ **Fail** | HTML differs from source doc | Developer fixes | Dev Team |
| ⚠️ **PMM** | Error in BOTH doc and HTML — source needs approval | Content team reviews | PMM / Content |

**Link Audit Rules:**
| Link Type | Requirement | Violation |
|---|---|---|
| External | Must have `target="_blank"` | ❌ Fail |
| Internal | Must NOT have `target="_blank"` | ❌ Fail |

**Returns:** Complete audit report with all sections checked, no skips, actionable fixes, and clear ownership (Dev vs. PMM).

**Time savings:** ~30 min audit → Catches 100% of content mismatches before launch.

**Requirements:**

| Requirement | Details |
|---|---|
| Source document | Pasted text or HTML content (Google Doc, brief, specification) |
| Live page HTML | Elementor HTML (section or full page) |
| Internal domain | Your domain name (e.g., `finance.uworld.com`) for link auditing |

---

### `/visual-diff` — Design vs Live Comparison

> **v2.0.0** — Pixel-perfect design-to-live comparison using the Figma MCP API.
>
> ⚠️ **Figma MCP is required.** This skill extracts exact design tokens (colors, spacing, fonts, shadows) directly from Figma via MCP. It will not proceed without an active Figma MCP connection and a configured `FIGMA_ACCESS_TOKEN`.

```
/visual-diff <figma-url> <live-url>
```

**Example:**
```
/visual-diff https://www.figma.com/design/AbCdEf123456/UWorld-Homepage?node-id=1-2 https://finance.uworld.com/cfa/
```

**What it does:**

1. Extracts all design tokens from Figma via MCP (`get_design_context`) — colors, spacing, fonts, shadows, border-radius
2. Captures live page at desktop (1280×800) and mobile (375×812) viewports
3. Compares Figma values vs live computed CSS — section by section
4. Returns fidelity % per section and a full Design Token Comparison Table

**Returns:** Overall visual fidelity score, section-by-section fidelity breakdown, design token comparison table, component inventory, and P1/P2/P3 fix list.

**Requirements:**

| Requirement | Details |
|---|---|
| Figma MCP | **Must be connected** — skill will not proceed without it |
| Figma Access Token | `FIGMA_ACCESS_TOKEN` must be set in your MCP config (Figma → Account Settings → Security → Personal access tokens) |
| Figma URL | Must include `node-id` parameter pointing to the specific frame or section |
| Live URL | Any publicly accessible page URL |

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

> **Two mandatory prerequisites must be completed before running this skill.**
>
> **Step A — Connect Figma MCP:** The Figma MCP server must be active and connected.
> It is the only way to accurately extract design tokens (colors, spacing, fonts, shadows, gradients).
>
> **Step B — Configure Figma Access Token:** After connecting the MCP, set `FIGMA_ACCESS_TOKEN` to a valid personal access token generated from your Figma account under **Account Settings → Security → Personal access tokens**.
> The MCP uses this token to authenticate all API requests to Figma.
>
> If `get_design_context` returns an error, stop and verify both the MCP connection and the access token before proceeding.

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

1. Verifies Figma MCP is connected and `FIGMA_ACCESS_TOKEN` is configured
2. Parses the Figma URL to extract `fileKey` and `nodeId`
3. Calls `get_design_context` via Figma MCP to extract every design token
4. Builds Elementor JSON bottom-up (leaf widgets → containers → root)
5. Runs the pre-flight checklist to validate JSON structure
6. Saves the output file to `C:\Users\sbiswal\Downloads\Productivity Tool\Elementor JSON Exports\`

**Returns:** A valid Elementor JSON file importable directly into WordPress via Elementor > Import.

**Requirements:**

| Requirement | Details |
|---|---|
| Figma MCP | Must be connected — skill will not proceed without it |
| Figma Access Token | `FIGMA_ACCESS_TOKEN` must be set in your MCP config (Figma → Account Settings → Security → Personal access tokens) |
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

### `/gdoc-to-html` — Google Doc / Word to HTML

```
/gdoc-to-html
[paste your Google Doc or Word content here]
```

**Example:**
```
/gdoc-to-html
What Is the CFA® Exam?

The CFA® exam is one of the most respected credentials in finance...

[H2] Why Candidates Fail

Most candidates underestimate the time commitment...
```

**What it does:**

Applies the UWorld Golden HTML Rule Set — strictly, in order:

1. Wraps every paragraph in `<p class="custom-para">` — the final paragraph gets `no-margin-bottom`
2. Converts `<ul>` / `<ol>` to UWorld list classes
3. Processes `<h2>` / `<h3>` — strips `[H2]`/`[H3]` markers and `<strong>`, generates `id` from original text
4. Adds `target="_blank"` only to non-uworld.com links
5. Preserves every character, entity, and inline element exactly

**Returns:** Clean, paste-ready HTML — no explanations, no wrappers, no markdown fences.

**Requirements:**

| Requirement | Details |
|---|---|
| Input | Paste raw Google Doc text, exported HTML, or any mixed content |
| Headings | Tag with `[H2]` or `[H3]` in the text if not already `<h2>`/`<h3>` tags |
| Links | Internal UWorld links are auto-detected; all others get `target="_blank"` |

---

### `/cwv-audit` — Core Web Vitals & PageSpeed Audit

```
/cwv-audit <page-url> [benchmark-url]
[attach: PSI mobile+desktop (field+lab), GTmetrix, WP Rocket settings JSON, view-source]
```

**Example:**
```
/cwv-audit https://finance.uworld.com/cfa/level-1/courses/
```

**What it does:**

Acts as a senior WordPress performance engineer and produces a prioritized, root-cause-driven plan to pass Core Web Vitals (mobile-first) on the WordPress + Astra + Elementor Pro + WP Rocket + Cloudflare stack — without breaking client-side pricing, Affirm widgets, sample quizzes, popups, or nested Elementor widgets. Field-data-first methodology:

1. Reads field vs lab correctly (FCP→LCP gap diagnostic)
2. Confirms the LCP element per device before prescribing fixes
3. Image/LCP rules — real `<img>`, `fetchpriority="high"`, right-sizing, lazy-load exclusions
4. WP Rocket settings audit — Delay JS exclusion list, Remove Unused CSS, Critical CSS
5. Fonts (Typekit/Adobe `font-display: swap`, Font Awesome)
6. INP / TBT / DOM (`content-visibility`, jQuery Migrate, long tasks)
7. TTFB / server (cache footer, Cloudflare HTML caching)
8. Benchmark comparison against a passing sibling page

**Returns:** Scorecard, root-cause table, prioritized P0/P1/P2 fixes, functionality QA checklist, rollback map, and a "what NOT to chase" list.

**Requirements:**

| Requirement | Details |
|---|---|
| URL | Live page URL (the skill fetches the HTML for structural analysis) |
| PSI data | Attach PageSpeed Insights mobile + desktop — both **field (CrUX)** and **lab (Lighthouse)** — to finalize the scorecard and confirm the LCP element |
| WP Rocket | Settings export (JSON) recommended to verify Delay JS / RUCSS / cache config |

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

## 9. Troubleshooting

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
figma-to-elementor/  gdoc-to-html/  page-audit/   table-compare/  visual-diff/
```

---

## 10. Role Guide

| Role | Primary Skills |
|---|---|
| QA Engineer | `/page-audit` `/table-compare` `/visual-diff` `/content-match` |
| Frontend Developer | `/figma-to-code` `/figma-to-elementor` `/feature-table` `/page-audit` |
| CMS / Content Editor | `/cms-format` `/content-match` `/table-compare` `/gdoc-to-html` |
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
