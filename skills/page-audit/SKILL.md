---
name: page-audit
description: "Full UWorld page QA audit — SEO, images, links, schema, trademark compliance, and prioritized fix list. Use when asked to audit a page, check a URL, or run QA."
user-invokable: true
argument-hint: "<url> [product|pillar|blog]"
---

# Page Audit & QA

Perform a comprehensive page audit on the URL provided. You are a senior web QA engineer for UWorld.

**Usage:** `/page-audit <url> [page-type: product|pillar|blog]`

---

## Step 1 — Fetch & Parse

Use the WebFetch tool to retrieve the full HTML of the page at the URL provided by the user.
Extract: title tag, meta description, canonical URL, lang attribute, viewport meta, OG tags,
all headings (H1–H6), all images, all links (internal and external), all `<script>` and
`<link rel="stylesheet">` tags, all JSON-LD blocks, and full visible text.

---

## Step 2 — SEO Analysis

Check each item and mark PASS / FAIL / WARN:

| Check | Rule |
|---|---|
| Title tag | Present, 50–70 characters |
| Meta description | Present, 100–165 characters |
| H1 count | Exactly 1 H1 on the page |
| Canonical | Present, matches page URL |
| Lang attribute | `<html lang="en">` present |
| Viewport | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| OG: title | Present and non-empty |
| OG: description | Present and non-empty |
| OG: image | Present, absolute URL |
| OG: url | Present, matches canonical |
| Twitter card | `<meta name="twitter:card">` present |

---

## Step 3 — Image Analysis

For every `<img>` tag build a table:

| Filename | Format | Alt Text | Lazy Load | Width/Height | Issue |
|---|---|---|---|---|---|

Rules:
- Format must be WebP or AVIF (flag JPG/PNG as P2)
- Alt text must be present and descriptive
- `loading="lazy"` required (first 2 images may skip)
- `width` and `height` attributes must both be present

---

## Step 4 — Link Analysis

Classify each `<a>` as internal or external.

- External: must have `target="_blank"` AND `rel="noopener noreferrer"` → flag missing as P2
- Internal: must NOT have `target="_blank"` → flag any that do as P2

---

## Step 5 — Performance Checks

| Check | Rule |
|---|---|
| Render-blocking scripts | No `<script>` in `<head>` without `async` or `defer` |
| Stylesheet count | Flag if more than 5 external CSS files |
| HTML size | Warn if raw HTML exceeds 200KB |

---

## Step 6 — Schema / Structured Data

Parse every `<script type="application/ld+json">` block.

- At least 1 JSON-LD block required
- BreadcrumbList required on product and pillar pages
- FAQPage required if page has a FAQ section
- Course/Product schema required on course pages

---

## Step 7 — Trademark Compliance

Scan all visible text for these terms and verify the correct symbol is attached:

| Term | Required Form |
|---|---|
| CFA | CFA® |
| StudyPass | StudyPass™ |
| TotalPrep | TotalPrep™ |
| FlexiPay | FlexiPay™ |
| FreshStart | FreshStart™ |
| ExpertConnect | ExpertConnect™ |
| BootCamp | BootCamp™ |

Flag every instance without its symbol as P1.

---

## Step 8 — Page-Type QA Checklist

**All pages:** CTA button, footer copyright year, Privacy Policy link, Terms of Use link

**Product pages:** Price displayed, Buy/Enroll CTA, testimonials, money-back guarantee, features list

**Pillar/Blog pages:** Author byline, publish date, table of contents (if >1500 words), related articles

---

## Output Format

```
=== UWORLD PAGE AUDIT REPORT ===
URL: [url]
Date: [date]
Page Type: [detected type]

OVERALL SCORE: [0-100] / 100

SECTION SCORES:
  SEO:         [score]/20
  Images:      [score]/15
  Links:       [score]/15
  Performance: [score]/15
  Schema:      [score]/15
  Trademark:   [score]/10
  QA Checklist:[score]/10

SEO ANALYSIS
[table with PASS/FAIL/WARN per check]

IMAGE ANALYSIS ([count] images)
[full image table]

LINK ANALYSIS
[table — show only rows with issues unless total < 20]

PERFORMANCE
[table of checks]

SCHEMA
[types found + missing types]

TRADEMARK COMPLIANCE
[list every violation OR "No trademark violations found."]

QA CHECKLIST
[checklist with PASS/FAIL/WARN]

PRIORITIZED FIX LIST

P1 — CRITICAL:
1. [issue] → [fix]

P2 — IMPORTANT:
1. [issue] → [fix]

P3 — MINOR:
1. [issue] → [fix]
```
