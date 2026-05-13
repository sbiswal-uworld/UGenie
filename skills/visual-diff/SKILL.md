---
name: visual-diff
description: Compare Figma design against live UWorld page using Figma MCP and live page screenshots — layout, typography, color, spacing, components with precision fidelity scores. Use for design-to-code QA, mockup validation, and component consistency checks.
author: AgriciDaniel
version: 2.0.0
category: seo
user-invokable: true
argument-hint: "<figma-url|file-key> <live-url>"
license: MIT
---

# Visual Diff — Figma vs Live Page

Compare a Figma design file against a live page using Figma MCP and precision visual analysis. Identify every layout, typography, color, spacing, and component discrepancy with severity scoring.

**Usage:** `/visual-diff <figma-file-key> <live-url>` OR `/visual-diff <figma-url> <live-url>`

You are a senior visual QA engineer for UWorld. Extract design intent from Figma using MCP, capture live page via screenshot, and report precise pixel-perfect differences with actionable fixes.

---

## Overview

This skill compares Figma designs with live pages using:
1. **Figma MCP Tools** — Extract design metadata, dimensions, colors, variables, typography directly from Figma
2. **Live Page Screenshot** — Capture actual rendered page at desktop (1280×800) and mobile (375×812) viewports
3. **CSS Inspection** — Read computed styles from live HTML
4. **Pixel-Perfect Analysis** — Compare exact values (colors, spacing, fonts, dimensions)
5. **Component Inventory** — Match Figma components to live DOM elements

---

## Step 1 — Extract Design Intent from Figma (Using MCP)

### Option A: If user provides Figma URL
Extract file key and node ID from URL format: `https://figma.com/design/[fileKey]/[fileName]?node-id=[nodeId]`

### Option B: If user provides file key directly
Use the provided file key

### Figma MCP Extraction

Use `mcp__23bf50d0-a486-47eb-aaa5-8d2fc20e7663__get_design_context` to retrieve:
- **Node metadata:** name, type, dimensions (width, height), position
- **Styles:** fills (colors), strokes, opacity, effects, shadows, border-radius
- **Typography:** font family, weight, size, line height, letter spacing, alignment
- **Layout:** auto-layout, gaps, padding, constraints
- **Images:** embedded image references with dimensions
- **Responsive behavior:** breakpoints, responsive properties
- **Components:** component structure, variants, component instances

Extract all this as **reference design state**.

### Design Token Extraction

Use `mcp__23bf50d0-a486-47eb-aaa5-8d2fc20e7663__get_variable_defs` to fetch:
- **Color variables** (e.g., `color/primary`, `color/background/dark`)
- **Spacing tokens** (e.g., `spacing/8`, `spacing/16`)
- **Typography tokens** (e.g., `font/heading/size`, `font/body/weight`)
- **Effects/shadows** (e.g., `effect/elevation/1`, `effect/shadow/medium`)

Compare against live page values.

---

## Step 2 — Capture Live Page Screenshots

### Desktop (Primary)
Use browser or preview tools to capture live page at **1280×800** viewport

Extract:
- Layout structure (sections, grids, columns)
- Typography (font family, size, weight, color)
- Colors (backgrounds, text, buttons, borders)
- Spacing (padding, margins, gaps)
- Components (buttons, cards, badges, images, inputs)
- Responsive behavior (breakpoints, mobile layout)

### Mobile (Secondary)
Capture same page at **375×812** viewport to verify responsive design

### Live HTML/CSS Inspection
Use WebFetch + browser dev tools to read computed CSS:
- `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`
- `color`, `background-color`, `border`, `border-radius`
- `padding`, `margin`, `gap`, `width`, `height`
- `box-shadow`, `text-align`, `text-transform`
- Media queries and breakpoints

---

## Step 3 — Figma vs Live: Section-by-Section Comparison

For each visible section (Hero, Nav, Features, Pricing, Testimonials, FAQ, Footer, etc.):

### Format: [SECTION NAME — Fidelity: XX%]

**Design (Figma):**
- Layout: [grid/flex/absolute], [column count], [alignment]
- Dimensions: width [Xpx], height [Xpx]
- Colors: bg=[#hex], text=[#hex], accent=[#hex]
- Typography: font=[family], size=[Xpx], weight=[X00], lineHeight=[X]
- Spacing: padding=[X]px, margin=[X]px, gap=[X]px
- Components: [button style], [card style], [image treatment], etc.

**Live (Current):**
- Layout: [grid/flex/absolute], [column count], [alignment]
- Dimensions: width [Xpx], height [Xpx]
- Colors: bg=[#hex], text=[#hex], accent=[#hex]
- Typography: font=[family], size=[Xpx], weight=[X00], lineHeight=[X]
- Spacing: padding=[X]px, margin=[X]px, gap=[X]px
- Components: [button style], [card style], [image treatment], etc.

**Differences:**
1. [P1] Background color: design=#1B3A6B, live=#1a3a6b (1-step mismatch, likely typo)
2. [P2] Button border-radius: design=8px, live=4px (style mismatch)
3. [P3] Section padding: design=48px, live=44px (4px variance)

---

## Step 4 — Design Token Comparison Table

| Token | Figma Value | Live Value | Unit | Diff | Status |
|---|---|---|---|---|---|
| Primary color | #0066CC | #0066DD | hex | +1 (B channel) | MISMATCH — P1 |
| Secondary color | #F0F4F8 | #F0F4F8 | hex | 0 | MATCH ✓ |
| Heading font | Poppins | Poppins | family | 0 | MATCH ✓ |
| Heading size | 32px | 30px | px | -2 | MISMATCH — P2 |
| Body font | Inter | Roboto | family | [diff] | MISMATCH — P1 |
| Body size | 16px | 16px | px | 0 | MATCH ✓ |
| Button radius | 8px | 6px | px | -2 | MISMATCH — P2 |
| Button padding | 12px 24px | 10px 20px | px | -2/-4 | MISMATCH — P2 |
| Section padding | 48px | 44px | px | -4 | MISMATCH — P3 |
| Grid gap | 16px | 16px | px | 0 | MATCH ✓ |

---

## Step 5 — Component Inventory

For each Figma component used on the page:

| Component | Figma Location | Live Element | Status | Issues |
|---|---|---|---|---|
| Button/Primary | /components/Button/Primary | .btn.btn-primary | FOUND | Style mismatch: border-radius 8px vs 6px |
| Card/Feature | /components/Card/Feature | .feature-card | FOUND | Colors match, spacing off by 4px |
| Badge/New | /components/Badge/New | .badge.badge-new | MISSING | Not present on live page |
| Input/Text | /components/Input/Text | input.form-control | FOUND | Focus state missing |
| Icon/ChevronRight | /components/Icon/ChevronRight | svg.icon-chevron | FOUND | Size: design 24px, live 20px |

---

## Severity Classification

| Level | Category | Examples | Action |
|---|---|---|---|
| **P1 — CRITICAL** | Visible breaking changes | Missing sections, wrong component type, brand color mismatch, wrong font family, layout broken | Fix immediately (blocks QA) |
| **P2 — IMPORTANT** | Style discrepancies | Font size off >2px, border-radius off >2px, spacing off >8px, missing hover state | Fix within sprint |
| **P3 — MINOR** | Pixel-level variance | Spacing off <8px, color off 1–2 hex values, weight off 100 units | Nice-to-have, backlog |

---

## Output Format

```
=== UWORLD VISUAL DIFF REPORT ===
Figma File: [name] | Live URL: [url] | Date: [date]
Report Type: Design-to-Code QA | Viewport: Desktop (1280×800) + Mobile (375×812)

---

OVERALL VISUAL FIDELITY: [X]%
[0-50%] = CRITICAL REWORK | [50-75%] = SIGNIFICANT ISSUES | [75-90%] = MINOR ISSUES | [90-100%] = PIXEL PERFECT

SECTION FIDELITY BREAKDOWN:
  Hero:         [X]% | Nav:      [X]% | Features:  [X]% | Pricing:   [X]%
  Testimonials: [X]% | FAQ:      [X]% | CTA Sect:  [X]% | Footer:    [X]%

---

DESIGN TOKEN COMPARISON
[complete table: Token | Figma | Live | Unit | Diff | Status]

COMPONENT INVENTORY
[table: Component | Figma Location | Live Element | Status | Issues]

---

SECTION ANALYSIS

[HERO — Fidelity: XX%]
Design: [hero description from Figma]
Live:   [hero description from screenshot]
Differences:
  1. [P1] Background color: design=#0066CC, live=#0066DD — MISMATCH
  2. [P2] Button border-radius: design=8px, live=6px — OFF BY 2PX
  3. [P3] Hero padding: design=64px, live=60px — OFF BY 4PX

[NAV — Fidelity: XX%]
...

---

TOP 5 CRITICAL ISSUES (P1)
1. [section] — [issue] — Fix: [specific code/CSS change]
2. [section] — [issue] — Fix: [specific code/CSS change]
...

---

PRIORITY FIX LIST

P1 — CRITICAL (Fix Before Release):
1. [section] — [issue] — [specific CSS/code fix]

P2 — IMPORTANT (Fix This Sprint):
1. [section] — [issue] — [specific CSS/code fix]

P3 — MINOR (Backlog):
1. [section] — [issue] — [specific CSS/code fix]

---

RESPONSIVE DESIGN CHECK
[Desktop (1280×800) — Fidelity: XX%]
[Tablet (768×1024) — Fidelity: XX%]
[Mobile (375×812) — Fidelity: XX%]

---

SUMMARY
[2-3 sentences on overall design implementation quality, top blockers, estimated fix time]
```

---

## Figma MCP Tools Used

- `get_design_context` — Extract design metadata, colors, typography, layout, images
- `get_variable_defs` — Fetch design tokens (colors, spacing, effects)
- `get_screenshot` — Capture Figma node screenshot for visual reference
- `get_metadata` — Get node structure and hierarchy

---

## Live Page Tools

- **WebFetch** — Extract HTML/CSS
- **Browser Screenshot** — Capture rendered page at multiple viewports
- **CSS Inspector** — Read computed styles
- **Responsive Testing** — Verify breakpoints, mobile layout

---

## Precision Standards

| Metric | Tolerance | Status |
|---|---|---|
| Color hex values | 0 (exact match required) | ✓ P1 if off |
| Font size | ±2px | <2px = PASS, ≥2px = P2 |
| Font weight | ±100 units (e.g., 500 vs 400) | Off >100 = P1 |
| Spacing (padding/margin) | ±4px | <4px = P3, 4–8px = P2, >8px = P1 |
| Border-radius | ±2px | <2px = PASS, ≥2px = P2 |
| Line height | ±0.1 units | Off >0.2 = P2 |
| Dimensions (width/height) | ±4px | <4px = PASS, ≥4px = P2 |
| Color brightness variance | ≤2% | >2% = P1 |

---

## Workflow

1. **User provides:** Figma file key/URL + live page URL
2. **Extract design:** Use Figma MCP to get design tokens, components, styles
3. **Capture live page:** Screenshot at desktop and mobile viewports
4. **Inspect CSS:** Read computed styles from live page HTML
5. **Compare section by section:** Layout, typography, colors, spacing, components
6. **Score fidelity:** Calculate % match per section and overall
7. **Severity classify:** P1/P2/P3 for each difference
8. **Output report:** Full diff with screenshots, token table, fix list

---

## Version History

- **v2.0.0** (2026-05-13): Figma MCP integration for precise design extraction, design token comparison, component inventory, responsive design validation, pixel-perfect tolerance standards
- **v1.0.0** (prior): Screenshot-based visual comparison
