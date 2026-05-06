---
name: visual-diff
description: "Compare a Figma or design screenshot against a live UWorld page — layout, typography, color, spacing, and component diffs with fidelity scores. Use when checking if a live page matches a design mockup."
user-invokable: true
argument-hint: "<live-url>"
---

# Visual Diff — Design vs Live

Compare a design screenshot against a live page and report every visual discrepancy.

**Usage:** `/visual-diff <live-url>` — then attach your design screenshot

You are a senior visual QA engineer for UWorld. Find every visual difference between design intent and the live page.

---

## Step 1 — Analyse the Design Screenshot

Examine the attached design image and extract:

**Layout:** page structure, section order, column layout, alignment, container widths

**Typography:** font families, sizes (relative scale), weights, line height, text alignment

**Colors:** background colors per section, text colors, button colors, border colors, accents

**Spacing:** section padding, margins between sections, grid gaps, button padding

**Components:** every button, card, badge, icon, image, table, accordion — note styles (border, shadow, radius, size)

---

## Step 2 — Fetch Live Page

Use WebFetch to retrieve the HTML/CSS of the live page.
Identify actual CSS values: font-family, color, background-color, padding, margin, border-radius.

---

## Step 3 — Section-by-Section Comparison

For each section top to bottom: describe design, describe live, list every difference.

**Severity:**
- P1: Wrong colors, missing sections, broken layout, wrong component type
- P2: Wrong font weight, spacing off >10px, wrong border-radius, missing hover states
- P3: Spacing differences <10px, minor color variations

---

## Step 4 — Design Token Comparison

| Token | Design Value | Live Value | Status |
|---|---|---|---|
| Primary color | #[color] | #[color] | MATCH/MISMATCH |
| Heading font | [family] | [family] | MATCH/MISMATCH |
| Body font | [family] | [family] | MATCH/MISMATCH |
| Button border-radius | [value] | [value] | MATCH/MISMATCH |

---

## Output Format

```
=== UWORLD VISUAL DIFF REPORT ===
Live URL: [url] | Date: [date]

OVERALL VISUAL FIDELITY: [0-100]%

SECTION SCORES:
  Hero: [X]% | Nav: [X]% | Features: [X]% | Pricing: [X]% | FAQ: [X]% | Footer: [X]%

DESIGN TOKEN COMPARISON
[table]

SECTION ANALYSIS

[HERO — Fidelity: XX%]
Design: [description]
Live:   [description]
Differences:
  1. [P1] Background color: design=#1B3A6B, live=#1a3a6a
  2. [P2] Button border-radius: design=8px, live=4px

TOP 5 BUGS
1. [P1] [section] — [issue] — [fix]
...

P1 Fix list | P2 Fix list | P3 Fix list
```
