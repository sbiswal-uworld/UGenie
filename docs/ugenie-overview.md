# UGenie — UWorld WebGenie Skills
### Claude Code Slash Commands for the UWorld Web Development Team

---

## What Is It?

UGenie is a set of **9 production-ready Claude Code slash commands** built specifically for the UWorld web team. Instead of manually formatting HTML, hunting down design tokens, or diff-checking tables row by row — you type one command and Claude does it in seconds.

No extra API key. No extra subscription. Works instantly on every team member's machine.

---

## How It Improves Productivity

| Without UGenie | With UGenie |
|---|---|
| Manually audit a page for SEO, images, broken links | `/page-audit <url>` — full structured report in seconds |
| Pixel-check Figma design vs live site by eye | `/visual-diff <figma-url> <live-url>` — scored diff report per section |
| Hand-format raw CMS HTML to UWorld standard | `/cms-format` — paste, done |
| Compare a content brief against a live page manually | `/content-match <url>` — line-by-line semantic diff with match rate % |
| Build Elementor JSON from a Figma design manually | `/figma-to-elementor` — MCP extracts tokens, JSON built automatically |
| Copy-check comparison tables cell by cell | `/table-compare` — MATCH / WRONG / MISSING per cell |
| Write HTML/React from a design screenshot | `/figma-to-code` — production-ready code output |
| Build feature comparison tables from scratch | `/feature-table` — desktop + mobile HTML in one shot |
| Format Google Doc / Word content to UWorld HTML | `/gdoc-to-html` — applies Golden Rule Set, paste-ready output |

---

## The 9 Skills

| Command | Version | Who Uses It | What It Does | Requires |
|---|---|---|---|---|
| `/page-audit` | v2.5.0 | QA Engineers | Full SEO + QA audit across 9 dimensions — scored /100 with P1/P2/P3 fix list | — |
| `/cms-format` | — | CMS / Content | Converts raw CMS questions to UWorld production-ready HTML format | — |
| `/content-match` | v3.0.1 | Content / QA | Line-by-line semantic diff — brief vs live page with match rate % and trademark check | **Google Drive MCP** |
| `/visual-diff` | v2.0.0 | QA / Dev | Pixel-perfect Figma vs live comparison — fidelity scores per section | **Figma MCP** |
| `/table-compare` | — | QA / Content | Cell-by-cell comparison with MATCH / WRONG / MISSING / EXTRA | — |
| `/figma-to-code` | — | Developers | Design screenshot → production HTML / React / Tailwind | — |
| `/figma-to-elementor` | — | Developers | Figma URL → Elementor JSON, importable into WordPress | **Figma MCP** |
| `/feature-table` | — | Developers / CMS | Generates UWorld comparison table HTML — desktop + mobile accordion | — |
| `/gdoc-to-html` | — | CMS / Content | Google Doc / Word content → UWorld-standard HTML using the Golden Rule Set | — |

---

## Skills That Require External Connectors

Two skills need external MCP connectors configured before use:

### `/content-match` — Requires Google Drive MCP

> ⚠️ **Google Drive MCP must be connected** to read Google Docs directly via URL.
> Without it, paste the CONTENT section text manually instead.

**What it does (v3.0.1):**
- Extracts the **CONTENT section only** — automatically ignores metadata (SUMMARY, DEVELOPER NOTES, SEO OUTLINE, DESIGN DELIVERABLES, etc.)
- Parses both source and live page into semantic blocks (headings, paragraphs, lists, CTAs, tables)
- Runs **line-by-line semantic diff** using Jaro-Winkler + Levenshtein similarity scoring
- Returns a full side-by-side comparison table with match status and similarity % per line

**Match statuses:** `EXACT` / `SIMILAR` / `CHANGED` / `MISSING` / `EXTRA` / `REORDERED`

**Severity levels:**
| Match Rate | Level |
|---|---|
| 90–100% | ✅ PASS |
| 75–89% | ⚠️ NEEDS ATTENTION |
| 50–74% | ❌ MAJOR ISSUES |
| < 50% | 🚨 CRITICAL |

```
/content-match https://finance.uworld.com/cfa/level-1/
[paste CONTENT section here]
```

---

### `/visual-diff` — Requires Figma MCP

> ⚠️ **Figma MCP must be connected** and `FIGMA_ACCESS_TOKEN` must be configured.
> The skill will not proceed without an active Figma MCP connection.

**What it does (v2.0.0):**
- Extracts all design tokens from Figma via `get_design_context` — colors, spacing, fonts, shadows, border-radius
- Captures live page screenshots at desktop (1280×800) and mobile (375×812) viewports
- Compares Figma values vs live computed CSS section by section
- Returns fidelity % per section, a Design Token Comparison Table, and a Component Inventory

**Precision tolerance standards:**
| Metric | P1 if... | P2 if... |
|---|---|---|
| Color hex values | Any difference | — |
| Font size | Off > 4px | Off 2–4px |
| Spacing (padding/margin) | Off > 8px | Off 4–8px |
| Border-radius | Off > 4px | Off 2–4px |

```
/visual-diff https://www.figma.com/design/AbCdEf123456/...?node-id=1-2 https://finance.uworld.com/cfa/
```

**To get a Figma access token:** Figma → Account Settings → Security → Personal access tokens

---

### `/figma-to-elementor` — Requires Figma MCP

> ⚠️ **Figma MCP must be connected** and `FIGMA_ACCESS_TOKEN` must be configured.

**Trigger phrase:**
```
Implement this design from Figma.
@https://www.figma.com/design/<fileKey>/...?node-id=<nodeId>
```

The skill automatically extracts all design tokens via Figma MCP, builds the full Elementor JSON bottom-up, runs a 15-point pre-flight checklist, and saves the file ready to import into WordPress.

---

## `/page-audit` — What's New in v2.5.0

The page audit skill now covers **9 dimensions** (up from 7):

| Dimension | Weight | What It Checks |
|---|---|---|
| On-Page SEO | 20% | Title, meta description, H1, headings, canonical, OG tags, Twitter Card |
| Content Quality | 20% | Word count, readability, E-E-A-T signals, freshness |
| Technical | 12% | Viewport, canonical, hreflang, robots meta |
| Schema Markup | 10% | JSON-LD detection and type-specific validation |
| Images | 10% | Alt text, format, file size (via curl), dimensions, lazy loading |
| QA Checklist | 14% | CTAs, footer year, Privacy/Terms links, trademark symbol check |
| Responsive Test | 10% | Viewport meta, srcset, font sizes, touch targets, fixed-width containers |
| Console & Code Quality | 4% | Duplicate IDs, deprecated elements, JS error patterns |

**Strict enforcement:** Every audit report must include a complete image inventory table with all 9 columns for every image on the page. Reports without the full image table are considered invalid.

---

## Run It Directly in Claude Code

Type `/` in Claude Code to see all 9 commands. Examples:

```
/page-audit https://finance.uworld.com/cfa/level-1/courses/
```
```
/content-match https://finance.uworld.com/cfa/level-1/
[paste CONTENT section here]
```
```
/visual-diff https://www.figma.com/design/... https://finance.uworld.com/cfa/
```
```
/gdoc-to-html
[paste Google Doc content here]
```

---

## Links

| Resource | Link |
|---|---|
| GitHub Repository | [github.com/sbiswal-uworld/UGenie](https://github.com/sbiswal-uworld/UGenie) |
| Demo Video | [Watch on Google Drive](https://drive.google.com/file/d/18cSRBRn0QGqgeIUbRLZX28kUFU8Yfaby/view?usp=drive_link) |
| Figma to Elementor Assets | [Open Google Drive Folder](https://drive.google.com/drive/folders/1bIlt2G6ZKZ0a2tWTOUGqjvL8lu4F8ydt) |

---

## Install in 3 Steps

```bash
git clone https://github.com/sbiswal-uworld/UGenie.git
cd UGenie
bash install.sh
```

Type `/` in Claude Code — all 9 commands appear instantly.

---

## Version History

| Version | Skill | What Changed |
|---|---|---|
| v3.0.1 | `/content-match` | Production-grade semantic matching — Jaro-Winkler + Levenshtein diff, 6 match statuses, Google Drive MCP support |
| v2.5.0 | `/page-audit` | Trademark check moved to QA checklist, scoring rebalanced, strict enforcement mode |
| v2.0.0 | `/visual-diff` | Full Figma MCP integration — design token comparison, component inventory, pixel-perfect tolerance |
| v1.0.0 | All | Initial release — 9 skills, dual-directory install |

---

*Built for the UWorld web team · Powered by [Claude Code](https://claude.ai/code)*
