# UGenie — UWorld WebGenie Skills
### Claude Code Slash Commands for the UWorld Web Team

---

## What Is It?

UGenie is a set of **8 production-ready Claude Code slash commands** built specifically for the UWorld web team. Instead of manually formatting HTML, hunting down design tokens, or diff-checking tables row by row — you type one command and Claude does it in seconds.

No extra API key. No extra subscription. Works instantly on every team member's machine.

---

## How It Improves Productivity

| Without UGenie | With UGenie |
|---|---|
| Manually audit a page for SEO, images, broken links | `/page-audit <url>` — full structured report in seconds |
| Pixel-check Figma design vs live site by eye | `/visual-diff <url>` — scored diff report per section |
| Hand-format raw CMS HTML to UWorld standard | `/cms-format` — paste, done |
| Compare a content brief against a live page manually | `/content-match <url>` — every mismatch flagged with severity |
| Build Elementor JSON from a Figma design manually | `/figma-to-elementor` — MCP extracts tokens, JSON built automatically |
| Copy-check comparison tables cell by cell | `/table-compare` — MATCH / WRONG / MISSING per cell |
| Write HTML/React from a design screenshot | `/figma-to-code` — production-ready code output |
| Build feature comparison tables from scratch | `/feature-table` — desktop + mobile HTML in one shot |

---

## The 8 Skills

| Command | Who Uses It | What It Does |
|---|---|---|
| `/page-audit` | QA Engineers | Full SEO, images, links, and schema audit on any URL |
| `/cms-format` | CMS / Content | Converts raw CMS HTML to UWorld golden standard |
| `/content-match` | Content / QA | Compares brief vs live page, flags every discrepancy |
| `/visual-diff` | QA / Dev | Scores Figma design vs live page section by section |
| `/table-compare` | QA / Content | Cell-by-cell comparison with MATCH / WRONG / MISSING |
| `/figma-to-code` | Developers | Design screenshot → production HTML / React / Tailwind |
| `/figma-to-elementor` | Developers | Figma URL → Elementor JSON (**Figma MCP required**) |
| `/feature-table` | Developers | Generates UWorld-standard comparison table HTML |

---

## `/figma-to-elementor` — How to Use

> **Connecting Figma MCP to Elementor is mandatory** before running this skill.

**Trigger phrase:**
```
Implement this design from Figma.
@https://www.figma.com/design/<fileKey>/...?node-id=<nodeId>
```

The skill automatically extracts all design tokens via Figma MCP, builds the full Elementor JSON bottom-up, runs a pre-flight checklist, and saves the file ready to import into WordPress.

---

## Run It Directly in Claude

Open Claude and paste any of these to run the skill immediately:

```
/page-audit https://uworld.com
```
```
/figma-to-elementor
Implement this design from Figma.
@https://www.figma.com/design/...
```
```
/visual-diff https://uworld.com
[attach Figma screenshot]
```

Or open the artifact directly in Claude:
**[Open UGenie Skills in Claude](https://claude.ai/artifacts/YOUR_ARTIFACT_LINK)**
> *(Replace with your shared Claude artifact link)*

---

## Links

| Resource | Link |
|---|---|
| GitHub Repository | [github.com/sbiswal-uworld/UGenie](https://github.com/sbiswal-uworld/UGenie) |
| Demo Video | [Watch on Google Drive](YOUR_DEMO_VIDEO_DRIVE_LINK) |
| All Assets (Drive) | [UGenie Assets Folder](YOUR_ASSETS_DRIVE_LINK) |

---

## Install in 3 Steps

```bash
git clone https://github.com/sbiswal-uworld/UGenie.git
cd UGenie
bash install.sh
```

Type `/` in Claude Code — all 8 commands appear instantly.

---

*Built for the UWorld web team · Powered by [Claude Code](https://claude.ai/code)*
