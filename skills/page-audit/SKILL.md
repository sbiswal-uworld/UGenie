---
name: page-audit
description: Deep single-page SEO analysis covering on-page elements, content quality, technical meta tags, schema, images, and performance. Uses bash+curl+grep for reliable HTML parsing (avoids WebFetch metadata loss). Extracts complete image inventory with file sizes, alt text, dimensions, and lazy loading. Use when user says "analyze this page", "check page SEO", "single URL", "check this page", "page analysis", or provides a single URL for review.
author: Sangram Biswal
version: 2.1.0
category: seo
user-invokable: true
argument-hint: "<url> [page-type: product|pillar|blog]"
license: MIT
---

# Page Audit & QA

Perform a comprehensive single-page SEO audit. You are a senior web QA engineer for UWorld.

**Usage:** `/page-audit <url> [page-type: product|pillar|blog]`

---

## Overview

This skill audits a single URL across 7 critical dimensions:
1. **On-Page SEO** — title, meta description, H1, heading hierarchy, URL structure, internal/external links
2. **Content Quality** — word count, readability, E-E-A-T signals, freshness
3. **Technical Elements** — viewport, canonical, OG tags (all 4), Twitter Card, hreflang, lang, robots meta
4. **Schema Markup** — JSON-LD detection, validation, type-specific requirements
5. **Images** — alt text (mandatory), format (WebP/AVIF recommended), size, dimensions, lazy loading
6. **Performance** — render-blocking resources, stylesheet count, HTML size, LCP signals, CLS prevention
7. **QA Checklist** — page-type-specific requirements (CTAs, pricing, testimonials, guarantees, etc.)

---

## Step 1 — Fetch & Parse Complete HTML

Use **bash + curl + grep** for reliable HTML extraction (WebFetch converts to markdown, losing metadata).

### 1.1 Extract Core Metadata via Bash
```bash
curl -s "URL" > /tmp/page.html

# Extract title
grep -oP '<title>\K[^<]+' /tmp/page.html

# Extract meta tags (description, canonical, viewport, robots, og:*, twitter:*)
grep -oP '<meta name="description" content="\K[^"]+' /tmp/page.html
grep -oP '<link rel="canonical" href="\K[^"]+' /tmp/page.html
grep -oP '<meta name="viewport" content="\K[^"]+' /tmp/page.html
grep 'property="og:' /tmp/page.html | grep -E 'og:(title|description|image|url)'
grep 'name="twitter:' /tmp/page.html

# Extract HTML lang attribute
grep -oP '<html[^>]*lang="\K[^"]+' /tmp/page.html
```

### 1.2 Extract Heading Hierarchy
```bash
echo "=== H1 TAGS ===" && grep -oP '<h1[^>]*>\K[^<]+' /tmp/page.html
echo "=== H2 TAGS ===" && grep -oP '<h2[^>]*>\K[^<]+' /tmp/page.html | head -15
echo "=== H3 TAGS ===" && grep -oP '<h3[^>]*>\K[^<]+' /tmp/page.html | head -10
```

### 1.3 Extract Complete Image Inventory with File Sizes
```bash
# Count total images
grep -c '<img' /tmp/page.html

# Extract all image tags with detailed analysis
grep -o '<img[^>]*>' /tmp/page.html | nl

# Check alt text presence
grep -c 'alt="[^"]*"' /tmp/page.html  # with alt attr
grep '<img[^>]*>' /tmp/page.html | grep -c -v 'alt='  # missing alt

# Check dimensions
grep -c 'width=' /tmp/page.html
grep -c 'height=' /tmp/page.html

# Check lazy loading
grep -c 'loading="lazy"' /tmp/page.html
```

### 1.4 Extract JSON-LD Schema
```bash
# Count schema blocks
grep -c 'application/ld+json' /tmp/page.html

# Extract schema types
grep -o '"@type":"[^"]*"' /tmp/page.html | sort | uniq
```

### 1.5 Extract Links
```bash
echo "=== INTERNAL LINKS ===" && grep -o 'href="/[^"]*"' /tmp/page.html | wc -l
echo "=== EXTERNAL LINKS ===" && grep -o 'href="https://[^"]*"' /tmp/page.html | grep -v 'yourdomain.com' | wc -l
echo "=== target=_blank ===" && grep -c 'target="_blank"' /tmp/page.html
echo "=== rel=noopener ===" && grep -c 'rel="noopener' /tmp/page.html
```

### 1.6 Performance Metrics
```bash
# File size
du -k /tmp/page.html | awk '{print $1}'

# Script/CSS counts
grep -c '<link rel="stylesheet"' /tmp/page.html
grep -c '<script[^>]*src=' /tmp/page.html
```

### 1.7 Extract Image File Sizes
```bash
# For each image URL, get actual file size via curl -I
curl -sI "IMAGE_URL" 2>/dev/null | grep -i 'content-length' | awk '{print $2 / 1024 " KB"}'
```

---

## Step 2 — SEO Analysis

Create a table with PASS / FAIL / WARN for each check:

| Check | Rule | Status |
|---|---|---|
| Title tag | Present, 50–70 characters, keyword-rich, unique | PASS/FAIL/WARN |
| Meta description | Present, 150–160 characters, compelling, keyword-included | PASS/FAIL/WARN |
| H1 count | **Exactly 1 H1 on page** (multiple = CRITICAL FAIL) | PASS/FAIL/WARN |
| H1 content | Matches page intent, includes primary keyword | PASS/FAIL/WARN |
| H2-H6 hierarchy | Logical hierarchy (no skipped levels), descriptive | PASS/FAIL/WARN |
| Canonical | Present, self-referencing or correct | PASS/FAIL/WARN |
| Lang attribute | `<html lang="en">` present | PASS/FAIL/WARN |
| Viewport | `<meta name="viewport" content="width=device-width, initial-scale=1">` | PASS/FAIL/WARN |
| OG: title | Present and non-empty | PASS/FAIL/WARN |
| OG: description | Present and non-empty | PASS/FAIL/WARN |
| OG: image | Present, absolute URL | PASS/FAIL/WARN |
| OG: url | Present, matches canonical | PASS/FAIL/WARN |
| Twitter card | `<meta name="twitter:card">` present | PASS/FAIL/WARN |
| Meta robots | `index, follow` or intentionally blocked | PASS/FAIL/WARN |
| URL structure | Short, descriptive, hyphenated, no parameters | PASS/FAIL/WARN |

**Scoring:** Count PASS items. Title 50–70 chars = PASS. Meta description must be 150–165 characters (not 100–165). Multiple H1s = automatic FAIL.

---

## Step 3 — Image Analysis (MANDATORY & COMPREHENSIVE)

### 3.1 Extract Complete Image Inventory (ALL IMAGES)

Use this bash script to extract **all** image details in one comprehensive table:

```bash
#!/bin/bash
html_file="$1"

echo "| # | Filename/Source | Format | Size (KB) | Alt Text | Width | Height | Loading | Issues |"
echo "|---|---|---|---|---|---|---|---|---|"

img_count=1
grep -o '<img[^>]*>' "$html_file" | while read -r img_tag; do
    # Extract src
    src=$(echo "$img_tag" | grep -oP 'src="\K[^"]+')
    if [[ $src == /* ]]; then src="https://yourdomain.com${src}"; fi
    
    # Extract filename
    filename=$(basename "$src")
    
    # Detect format
    case "$filename" in
        *.webp) format="WebP" ;;
        *.png) format="PNG" ;;
        *.jpg|*.jpeg) format="JPG" ;;
        *.gif) format="GIF" ;;
        *.svg) format="SVG" ;;
        *) format="Unknown" ;;
    esac
    
    # Extract width/height
    width=$(echo "$img_tag" | grep -oP 'width="\K[^"]+' | head -1)
    width="${width:-missing}"
    height=$(echo "$img_tag" | grep -oP 'height="\K[^"]+' | head -1)
    height="${height:-missing}"
    
    # Extract alt text
    alt=$(echo "$img_tag" | grep -oP 'alt="\K[^"]*')
    if [ -z "$alt" ]; then
        alt="**MISSING**"
    fi
    
    # Extract loading
    loading=$(echo "$img_tag" | grep -oP 'loading="\K[^"]+')
    loading="${loading:-not specified}"
    
    # Get file size (via curl headers)
    size="not specified"
    if [[ $src == http* ]]; then
        size_bytes=$(curl -sI "$src" 2>/dev/null | grep -i 'content-length' | awk '{print $2}' | tr -d '\r')
        if [ ! -z "$size_bytes" ]; then
            size_kb=$((size_bytes / 1024))
            if [ $size_kb -gt 500 ]; then
                size="$size_kb (P1: >500KB)"
            elif [ $size_kb -gt 200 ]; then
                size="$size_kb (P2: >200KB)"
            else
                size="$size_kb"
            fi
        fi
    fi
    
    # Determine issues
    issues=""
    [[ $alt == *"MISSING"* ]] && issues="P1: No alt text"
    [[ $loading == "not specified" && $img_count -gt 2 ]] && issues="${issues:+$issues, }P2: Not lazy-loaded"
    [[ $width == "missing" || $height == "missing" ]] && issues="${issues:+$issues, }P2: Missing dimensions"
    
    # Truncate for display
    display_filename=$(echo "$filename" | cut -c1-50)
    display_alt=$(echo "$alt" | cut -c1-40)
    
    echo "| $img_count | $display_filename | $format | $size | $display_alt | $width | $height | $loading | $issues |"
    ((img_count++))
done
```

For **every** `<img>` tag, output row includes:

| # | Filename/Source | Format | Size | Alt Text | Width | Height | Loading | Issues |
|---|---|---|---|---|---|---|---|---|
| 1 | [src basename] | [jpg/png/webp/svg/gif/avif] | [KB or 'not specified'] | [text or **MISSING**] | [px or 'missing'] | [px or 'missing'] | [lazy/not specified] | [P1/P2 flags] |

### Image Quality Rules — CRITICAL

**Format:**
- ✓ WebP/AVIF preferred
- ⚠ JPG/PNG = P2 (older formats, larger file sizes)
- Flag SVG placeholders (data URIs) as P2 if no dimensions

**File Size:**
- ✓ <200KB = PASS
- ⚠ 200–500KB = P2 (warning, optimize)
- ✗ >500KB = P1 (critical, compress immediately)
- Note: If size "not specified", request it via WebFetch

**Alt Text — MANDATORY:**
- ✓ Descriptive alt text present (e.g., "CFA Level 1 exam prep dashboard")
- ✗ Empty alt="" = **P1 CRITICAL** (accessibility failure + SEO miss)
- ✗ Missing alt attribute = **P1 CRITICAL** (accessibility failure)
- ⚠ Generic alt ("image", "photo", "pic") = P2 (low relevance)
- ✓ First 2 images (hero/LCP) may skip lazy if critical

**Dimensions (Width & Height):**
- ✓ Both attributes present = PASS (prevents CLS layout shift)
- ✗ Either missing = P2 (CLS risk, hurts Core Web Vitals)
- ✗ SVG placeholders without dimensions = P2 (performance risk)

**Lazy Loading:**
- Report method: `native loading="lazy"` | `perfmatters` | `ewww` | `lazysizes` | `js-generic` | `none`
- ✓ First 2 images may skip lazy (hero/LCP images should preload)
- ✓ Below-fold images should have lazy loading
- ⚠ JS lazy-loaders detected (Perfmatters, EWWW, lazysizes) = intentionally strip native loading="lazy" — do NOT flag as failure
- ✗ No lazy loading on 20+ images below fold = P2

### Image Analysis Output

Create a comprehensive table showing ALL images. Include this summary:
```
IMAGE SUMMARY:
- Total images: XX
- Images with alt text: XX
- Images MISSING alt text: XX (P1 failures)
- WebP/AVIF format: XX
- PNG/JPG format: XX (P2 flags)
- Dimensions present: XX
- Dimensions missing: XX (P2 flags)
- Lazy loading detected: XX
- Format: optimized | needs WebP conversion
```

---

## Step 4 — Link Analysis

Classify ALL `<a>` tags as internal or external.

**Internal Links:**
- Must NOT have `target="_blank"` → flag any that do as P2 (unexpected tab behavior)
- Should have descriptive anchor text (not "click here", "read more")
- No security attributes needed

**External Links:**
- Must have BOTH `target="_blank"` AND `rel="noopener noreferrer"` → flag missing as P2 (security/referrer risk)
- Verify pointing to authoritative sources
- checkout links, partner sites, external resources

Create summary table:
| Type | Count | Target | Rel | Issues |
|---|---|---|---|---|
| Internal | XX | None | None | [list issues] |
| External (checkout) | XX | _blank? | noopener? | [list missing attributes] |

Show all rows if <20 links; show only rows with issues if >20.

---

## Step 5 — Performance Checks

| Check | Rule | Status |
|---|---|---|
| Render-blocking scripts | No `<script>` in `<head>` without `async` or `defer` | PASS/FAIL |
| Stylesheet count | Flag if more than 5 external CSS files | PASS/FAIL |
| HTML size | Warn if exceeds 200KB | PASS/FAIL |
| LCP image preload | Check for `<link rel="preload" as="image">` for hero/critical image | PASS/FAIL |
| Image dimensions | All images have width and height attributes (CLS prevention) | PASS/FAIL |
| Lazy loading | Below-fold images have loading="lazy" or JS lazy-loader | PASS/FAIL |

---

## Step 6 — Schema / Structured Data

Parse every `<script type="application/ld+json">` block.

### Required Schemas (By Page Type)

**All Pages:**
- Organization schema (name, logo, contact, sameAs)

**Product Pages:**
- Product schema (name, description, offers, reviews, aggregate rating)
- BreadcrumbList schema (navigation hierarchy)
- FAQPage schema (if FAQ section present)
- AggregateOffer schema (pricing options, availability)

**Blog/Pillar Pages:**
- Article schema (headline, datePublished, dateModified, author, content)
- BreadcrumbList schema
- FAQPage schema (if FAQ present)

**Course/Certification Pages:**
- Course schema (name, description, provider, hasCourseInstance)
- AggregateRating (if reviews present)
- Product schema (pricing, offers)

### Validation

- ✓ At least 1 JSON-LD block present = PASS
- ✗ No schema = P1 (blocks rich results, -15–25% visibility)
- ⚠ Incomplete schema (missing required properties) = P2
- ⚠ Wrong schema type for page = P2 (semantic mismatch)

### Do NOT Recommend

- ❌ HowTo schema (deprecated by Google)
- ❌ FAQ schema on non-gov/non-health sites (restricted)

---

## Step 7 — Trademark Compliance

Scan all visible text for these terms and verify correct symbol:

| Term | Required Form | Count | Status |
|---|---|---|---|
| CFA | CFA® | — | PASS/FAIL |
| FRM | FRM® | — | PASS/FAIL |
| CFP | CFP® | — | PASS/FAIL |
| StudyPass | StudyPass™ | — | PASS/FAIL |
| TotalPrep | TotalPrep™ | — | PASS/FAIL |
| FlexiPay | FlexiPay™ | — | PASS/FAIL |
| FreshStart | FreshStart™ | — | PASS/FAIL |
| ExpertConnect | ExpertConnect™ | — | PASS/FAIL |
| BootCamp | BootCamp™ | — | PASS/FAIL |

**Rule:** Flag EVERY instance without its symbol as **P1 CRITICAL** (legal compliance + brand protection).

---

## Step 8 — Content Quality Assessment

| Metric | Rule | Status |
|---|---|---|
| Word count | Hub: 1,500+ | Product: 1,000+ | Blog: 800+ | PASS/FAIL |
| Readability | Flesch Reading Ease 60–70 (grade 8–10 level) | PASS/FAIL/WARN |
| Keyword density | Natural (1–3%), semantic variations | PASS/FAIL/WARN |
| E-E-A-T signals | Author bio, credentials, awards, experience | PASS/FAIL/WARN |
| Content freshness | Publish date, last updated present | PASS/FAIL/WARN |
| Structure | Short paragraphs, clear subheadings, scannable | PASS/FAIL/WARN |

---

## Step 9 — Page-Type QA Checklist

### All Pages (Required)

| Item | Status |
|---|---|
| CTA button present (e.g., "Start Free Trial", "Enroll") | PASS/FAIL |
| Footer copyright year correct | PASS/FAIL |
| Privacy Policy link present and functional | PASS/FAIL |
| Terms of Use link present and functional | PASS/FAIL |

### Product Pages (Additional)

| Item | Status |
|---|---|
| Price displayed (e.g., "$299/month" or "Starts at $X") | PASS/FAIL |
| Buy/Enroll CTA button prominent | PASS/FAIL |
| Customer testimonials (minimum 3) | PASS/FAIL |
| Money-back guarantee statement explicit | PASS/FAIL |
| Features list (minimum 5 key features) | PASS/FAIL |

### Pillar/Hub Pages (Additional)

| Item | Status |
|---|---|
| Author byline + credentials | PASS/FAIL |
| Publish date present | PASS/FAIL |
| Table of contents (if >1,500 words) | PASS/FAIL |
| Related articles/internal links (minimum 5) | PASS/FAIL |

### Blog Pages (Additional)

| Item | Status |
|---|---|
| Author byline + credentials | PASS/FAIL |
| Publish date | PASS/FAIL |
| Last updated date | PASS/FAIL |
| Social share buttons | PASS/FAIL |
| Related posts section | PASS/FAIL |

---

## Scoring Weights & Formula

| Category | Weight | Max Score |
|---|---|---|
| On-Page SEO | 22% | 20 |
| Content Quality | 23% | 20 |
| Technical Meta Tags | 15% | 20 |
| Schema | 10% | 15 |
| Images | 10% | 15 |
| Trademark Compliance | 5% | 10 |
| QA Checklist | 15% | 10 |

**Overall Score = (On-Page × 0.22) + (Content × 0.23) + (Technical × 0.15) + (Schema × 0.10) + (Images × 0.10) + (Trademark × 0.05) + (QA × 0.15)**

Range: 0–100

---

## Output Format

```
=== UWORLD PAGE AUDIT REPORT ===
URL: [url]
Date: [date]
Page Type: [detected type]

OVERALL SCORE: [X]/100

SECTION SCORES:
  On-Page SEO:     [X]/20   [progress bar]
  Content Quality: [X]/20   [progress bar]
  Technical:       [X]/20   [progress bar]
  Schema:          [X]/15   [progress bar]
  Images:          [X]/15   [progress bar]
  Trademark:       [X]/10   [progress bar]
  QA Checklist:    [X]/10   [progress bar]

---

SEO ANALYSIS
[table with PASS/FAIL/WARN per check]
[note H1 count specifically if >1]

IMAGE ANALYSIS ([count] total images)
[complete table: filename, format, size, alt text, width, height, loading, issues]
[summary: X images with alt, Y missing alt, Z format issues]

LINK ANALYSIS
[all links if <20, otherwise issues only]
[note any missing target="_blank" or rel attributes]

PERFORMANCE
[table of checks with PASS/FAIL/WARN]

SCHEMA
[list types found: e.g., "Product schema present", "FAQ schema missing"]
[list required schemas NOT found]

CONTENT QUALITY
[word count, readability score, E-E-A-T signals present, freshness]

TRADEMARK COMPLIANCE
[list EVERY violation with term, found form, required form]
OR
["No trademark violations found."]

QA CHECKLIST
[checklist with PASS/FAIL/WARN per item type]

---

PRIORITIZED FIX LIST

P1 — CRITICAL (Fix Immediately):
1. [issue] → [specific fix with code example if needed] | Impact: [% improvement]
2. [issue] → [fix] | Impact: [metric]

P2 — IMPORTANT (Fix Within 1 Week):
1. [issue] → [fix] | Impact: [metric]

P3 — MINOR (Fix Within 1 Month):
1. [issue] → [fix] | Impact: [metric]

---

SUMMARY
[2–3 sentences on overall page health, top 3 issues, expected ROI from fixes]
[Expected impact: X% organic visibility improvement, Y% social CTR improvement, Z% conversion improvement]
```

---

## Error Handling

| Scenario | Action |
|---|---|
| URL unreachable (404, DNS failure, connection refused) | Report error clearly with status code. Do not guess content. Suggest user verify URL and try again. |
| Page requires authentication (401/403) | Report page is behind authentication. Suggest providing rendered HTML directly or a publicly accessible URL. |
| JavaScript-rendered content (empty body in HTML) | Note that key content may be CSR. Analyze available HTML and flag results as potentially incomplete. Suggest browser-rendered snapshot if available. |
| curl connection timeout | Retry with longer timeout or check if domain is blocked. Some domains may require user-agent headers: `curl -s -A "Mozilla/5.0" URL` |
| Image file size unavailable | Skip size check if HEAD request fails. Note in report as "not specified" and flag as potential optimization opportunity. |
| Images not detected | Use bash grep to extract ALL img tags: `grep -o '<img[^>]*>' file.html \| nl` — guaranteed to find every image with attributes. |
| Malformed HTML | Bash grep is resilient to broken HTML. It will extract partial matches. Analyze what's available and note limitations in report. |

---

## Key Distinctions & Severity Rules

### H1 Failures
- **Count ≠ 1** = CRITICAL FAIL (confuses search engine on page topic)
- **H1 missing keyword** = P2 (missed ranking opportunity)
- **H1 vague** = P2 (e.g., "Welcome" instead of "Finance Certification Prep")

### Image Alt Text Severity
- **Empty alt="" on any image** = P1 CRITICAL (WCAG 2.1 accessibility failure)
- **Missing alt attribute** = P1 CRITICAL (accessibility + SEO)
- **Generic alt ("image", "photo")** = P2 (low relevance, poor keyword optimization)
- **Descriptive alt with keyword** = PASS

### Schema Severity
- **No schema at all** = P1 (blocks rich results, -15–25% visibility)
- **Incomplete schema** = P2 (partial rich results, missing properties)
- **Wrong schema type** = P2 (semantic mismatch)

### Link Security
- **External link missing `target="_blank"`** = P2 (opens in same tab, loses user)
- **External link missing `rel="noopener noreferrer"`** = P2 (security/referrer risk)
- **Internal link with `target="_blank"`** = P2 (unexpected behavior, accessibility failure)

---

## Common Audit Findings

### Top 10 Most Common Failures
1. Multiple H1 tags (confuses intent)
2. Missing meta description (loses 30–50% SERP CTR)
3. No JSON-LD schema (blocks rich results)
4. **Missing alt text on 10+ images** (accessibility failure + SEO)
5. No Open Graph tags (weak social preview)
6. Missing viewport meta tag (mobile rendering)
7. Image dimensions missing (CLS risk)
8. Trademark symbols missing (legal risk)
9. External links without security attributes
10. Pricing not displayed (20–30% bounce increase)

### Expected Impact of Fixes
- **Top 3 P1 fixes:** 25–40% organic visibility improvement
- **All P1 fixes:** 35–50% organic visibility improvement
- **P1 + P2 fixes:** 50–70% improvement + unlocked rich results + improved conversion (5–15%)

---

## Version History

- **v2.1.0** (2026-05-14): Switched from WebFetch to bash+curl+grep HTML parsing for reliable metadata extraction. Added comprehensive bash scripts for image inventory with file size detection. Improved accuracy of alt text, dimensions, and lazy loading detection. Enhanced image analysis to extract ALL images with complete details. Better error handling for timeout/connection issues.
- **v2.0.0** (2026-05-13): Complete image analysis methodology with mandatory alt text, comprehensive checklist coverage, detailed scoring weights, improved error handling, common findings reference
- **v1.9.9** (prior): Initial version
