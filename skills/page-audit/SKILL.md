---
name: page-audit
description: Deep single-page SEO audit covering on-page SEO, content quality, technical meta tags, schema, images, performance, responsive design, and HTML/JS code quality. Uses bash+curl+grep for reliable HTML parsing. STRICT ENFORCEMENT MODE - Image analysis table with all 9 columns mandatory on every audit. Trademark check simplified to QA checklist (first mention must have ® or ™). Use when user says "analyze this page", "check page SEO", "single URL", "check this page", or "page analysis".
author: Sangram Biswal
version: 2.5.0
category: seo
user-invokable: true
argument-hint: "<url> [page-type: product|pillar|blog]"
license: MIT
---

# Page Audit & QA

Perform a comprehensive single-page SEO audit. You are a senior web QA engineer for UWorld.

**Usage:** `/page-audit <url> [page-type: product|pillar|blog]`

---

## ⚠️ CRITICAL: ALL RULES ARE MANDATORY AND NON-NEGOTIABLE

This skill has 8 STRICT ENFORCEMENT RULES that MUST be followed on EVERY single audit without exception. These rules cannot be skipped, modified, or ignored:

1. **IMAGE ANALYSIS TABLE** - Must show EVERY image with ALL 9 columns (no exceptions)
2. **FILE SIZES** - Must fetch actual sizes via curl for each image
3. **ALT TEXT** - Must verify and report for every image
4. **DIMENSIONS** - Must extract width/height for every image
5. **LAZY LOADING** - Must check loading attribute for every image
6. **ISSUES COLUMN** - Must populate with P1/P2/P3 severity for each image
7. **OUTPUT FORMAT** - Must follow exact section order and formatting
8. **TRADEMARK TABLE** - Must show all violation counts and % compliance

If these rules are not followed, the report is INCOMPLETE and INVALID. There are NO exceptions.

---

## VALID vs INVALID REPORTS

**REPORT IS VALID IF AND ONLY IF:**
- ✅ IMAGE ANALYSIS section includes complete table with EVERY image on page
- ✅ Image table has all 9 columns populated with actual values (no empty cells)
- ✅ File sizes fetched via curl for each image
- ✅ Alt text column shows actual text or "MISSING"
- ✅ Width/Height columns show actual values or "missing"
- ✅ Loading column shows "lazy" or "not specified"
- ✅ Issues column populated with P1/P2/P3 severity
- ✅ All 8 sections appear in exact order (SEO, Images, Links, Performance, Schema, Content, QA, Responsive, Console, Fixes, Summary)
- ✅ Progress bars use ███░░░ format
- ✅ QA Checklist includes trademark symbol check (first mention of product name)
- ✅ Summary section with top 3 critical issues and top 3 strengths

**REPORT IS INVALID IF:**
- ❌ Image table is missing (only summary provided)
- ❌ Image table incomplete (doesn't show all images on page)
- ❌ Any column in image table has empty cells or placeholders
- ❌ File sizes not fetched (all marked "not specified" without attempting curl)
- ❌ Alt text, Width, Height, Loading, or Issues columns empty/missing
- ❌ Sections appear out of order
- ❌ Progress bars incorrect format
- ❌ Trademark table incomplete or missing counts
- ❌ No Summary section

---

## Overview

This skill audits a single URL across 9 critical dimensions:
1. **On-Page SEO** — title, meta description, H1, heading hierarchy, URL structure, internal/external links
2. **Content Quality** — word count, readability, E-E-A-T signals, freshness
3. **Technical Elements** — viewport, canonical, OG tags (all 4), Twitter Card, hreflang, lang, robots meta
4. **Schema Markup** — JSON-LD detection, validation, type-specific requirements
5. **Images** — alt text (mandatory), format (WebP/AVIF recommended), size, dimensions, lazy loading
6. **Performance** — render-blocking resources, stylesheet count, HTML size, LCP signals, CLS prevention
7. **QA Checklist** — page-type-specific requirements (CTAs, pricing, testimonials, guarantees, etc.)
8. **Responsive Test** — viewport meta, srcset/sizes, media queries, mobile font sizes, touch targets, horizontal scroll risk
9. **Console & Code Quality** — HTML structure errors, deprecated elements, duplicate IDs, missing required attributes, inline JS error patterns, malformed tags

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

## Step 3 — Image Analysis (MANDATORY & COMPREHENSIVE) - STRICT RULES

### CRITICAL REQUIREMENT: IMAGE ANALYSIS TABLE IS NON-NEGOTIABLE

**This section is MANDATORY on EVERY audit. You MUST generate the detailed inventory table showing EVERY single image on the page with ALL required columns. No exceptions. No summaries instead of tables.**

The IMAGE ANALYSIS section MUST include:
1. Total image count in heading: "## IMAGE ANALYSIS (XX total images)"
2. COMPLETE TABLE showing EVERY image with ALL columns below
3. Summary statistics after the table
4. Critical issues list

### 3.1 Extract Complete Image Inventory (ALL IMAGES) - REQUIRED TABLE FORMAT

MANDATORY: Extract **all** image details in one comprehensive table with these exact columns:

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

## Step 7 — Trademark Compliance (For Reference Only - Not Scored in QA Checklist)

For informational audit purposes only. Trademark symbol requirement is now checked in QA Checklist as a simple presence check:
- **Check:** Is at least ONE instance of the primary product name present with its ® or ™ symbol?
- **PASS:** At least one instance found with correct symbol
- **FAIL:** No instances found with correct symbol

Primary product names to check (by division):
- **Finance:** CFA®, FRM®, CFP®
- **Legal:** MCAT®, Bar Exam, NCBE®
- **Medical:** USMLE®, NCLEX®, AAMC®
- **General:** UWorld™, StudyPass™, TotalPrep™, FlexiPay™, FreshStart™, ExpertConnect™, BootCamp™

**Rule:** Check ONLY if the first mention of the product name includes the symbol. If yes = PASS. If no = FAIL. This ensures at minimum, brand protection on the page.

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
| Primary product name includes ® or ™ symbol (first mention) | PASS/FAIL |

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

## Step 10 — Responsive Test

Analyze the HTML source for responsive design signals. Since curl fetches static HTML (no browser rendering), we check structural indicators that predict mobile behaviour.

### 10.1 Viewport & Mobile Meta
```bash
# Viewport meta tag
grep -oP '<meta name="viewport" content="\K[^"]+' /tmp/page.html

# Theme color (mobile browser chrome)
grep -oP '<meta name="theme-color" content="\K[^"]+' /tmp/page.html

# Apple mobile meta tags
grep -i 'apple-mobile-web-app' /tmp/page.html | head -5
```

### 10.2 Responsive Images
```bash
# Images WITH srcset (responsive images)
grep -o '<img[^>]*>' /tmp/page.html | grep -c 'srcset='

# Images WITHOUT srcset (fixed-size risk)
grep -o '<img[^>]*>' /tmp/page.html | grep -cv 'srcset='

# Images with sizes attribute
grep -o '<img[^>]*>' /tmp/page.html | grep -c 'sizes='

# Images using vw units in sizes (fluid responsive)
grep -o 'sizes="[^"]*"' /tmp/page.html | grep -c 'vw'

# Picture elements (art direction responsive)
grep -c '<picture' /tmp/page.html
```

### 10.3 Media Queries & CSS
```bash
# Inline style media queries
grep -o '@media[^{]*{' /tmp/page.html | head -10

# CSS files linked (check each for media attribute)
grep -o '<link[^>]*stylesheet[^>]*>' /tmp/page.html

# Responsive utility classes (Tailwind / Bootstrap signals)
grep -oP 'class="[^"]*"' /tmp/page.html | grep -oP '\b(sm:|md:|lg:|xl:|col-|flex-|grid-)' | sort | uniq -c | sort -rn | head -10
```

### 10.4 Font & Touch Target Checks
```bash
# Inline font-size declarations (flag anything < 14px)
grep -oP 'font-size:\s*\K[0-9]+px' /tmp/page.html | sort -n | head -10

# Viewport-relative font sizes (fluid typography — good)
grep -oP 'font-size:\s*\K[0-9.]+vw' /tmp/page.html | head -5

# Small tap targets — buttons/links with fixed small heights
grep -oP '<(button|a)[^>]*style="[^"]*height:\s*\K[0-9]+px' /tmp/page.html | sort -n | head -10

# Input types (mobile keyboard optimisation)
grep -oP '<input[^>]*type="\K[^"]+' /tmp/page.html | sort | uniq -c | sort -rn
```

### 10.5 Horizontal Scroll Risk
```bash
# Fixed pixel widths wider than typical mobile (>480px)
grep -oP 'width:\s*\K[5-9][0-9]{2,}px|[1-9][0-9]{3,}px' /tmp/page.html | head -10

# Overflow hidden / scroll signals
grep -c 'overflow.*hidden\|overflow-x.*hidden' /tmp/page.html

# Tables without responsive wrapper
grep -c '<table' /tmp/page.html
grep -c 'overflow.*auto\|overflow.*scroll' /tmp/page.html
```

### Responsive Audit Output Table

| Check | Rule | Status |
|---|---|---|
| Viewport meta tag | `width=device-width, initial-scale=1` present | PASS/FAIL |
| Responsive images | `srcset` on all content images | PASS/WARN/FAIL |
| `sizes` attribute | Present on srcset images | PASS/WARN |
| `<picture>` elements | Art direction for hero/key images | PASS/WARN |
| Font sizes | No inline sizes below 14px | PASS/WARN/FAIL |
| Touch targets | Buttons/links ≥44px height (WCAG 2.5.5) | PASS/WARN/FAIL |
| Fixed-width containers | No elements wider than viewport (>480px fixed px) | PASS/WARN/FAIL |
| Tables | Wrapped in overflow container | PASS/WARN/FAIL |
| Horizontal scroll risk | Overflow-x controlled | PASS/WARN/FAIL |
| Mobile input types | `email`, `tel`, `number` used where appropriate | PASS/WARN |

**Severity:**
- Viewport meta missing = **P1** (mobile rendering completely broken)
- Fixed-width containers >480px = **P1** (forces horizontal scroll on mobile)
- Images without srcset = **P2** (serves desktop-sized images to mobile, wastes bandwidth)
- Font sizes <14px inline = **P2** (unreadable on mobile, fails WCAG 1.4.4)
- Touch targets <44px = **P2** (WCAG 2.5.5 failure, poor mobile UX)
- Tables not wrapped = **P3** (possible horizontal scroll on narrow screens)

---

## Step 11 — Console & Code Quality

Detect HTML structure errors, deprecated elements, JS error patterns, and code quality issues — all via static analysis of the raw HTML.

### 11.1 HTML Structure Errors
```bash
# Duplicate IDs (must be unique per HTML spec)
grep -oP 'id="\K[^"]+' /tmp/page.html | sort | uniq -d

# Unclosed common block elements (heuristic check)
open_divs=$(grep -c '<div' /tmp/page.html)
close_divs=$(grep -c '</div>' /tmp/page.html)
echo "Open <div>: $open_divs | Close </div>: $close_divs"

open_sections=$(grep -c '<section' /tmp/page.html)
close_sections=$(grep -c '</section>' /tmp/page.html)
echo "Open <section>: $open_sections | Close </section>: $close_sections"

# Nested anchor tags (invalid HTML — <a> inside <a>)
grep -oP '<a[^>]*>.*?<a' /tmp/page.html | head -5

# Form elements outside <form> tags
grep -c '<input\|<textarea\|<select' /tmp/page.html
grep -c '<form' /tmp/page.html
```

### 11.2 Deprecated / Invalid HTML Elements
```bash
# Deprecated presentational elements
echo "=== DEPRECATED ELEMENTS ===" 
grep -oi '<font\b' /tmp/page.html | wc -l | xargs -I{} echo "<font>: {}"
grep -oi '<center\b' /tmp/page.html | wc -l | xargs -I{} echo "<center>: {}"
grep -oi '<marquee\b' /tmp/page.html | wc -l | xargs -I{} echo "<marquee>: {}"
grep -oi '<blink\b' /tmp/page.html | wc -l | xargs -I{} echo "<blink>: {}"
grep -oi '<strike\b' /tmp/page.html | wc -l | xargs -I{} echo "<strike>: {}"
grep -oi '<frameset\b' /tmp/page.html | wc -l | xargs -I{} echo "<frameset>: {}"

# Deprecated attributes
grep -c 'align="' /tmp/page.html
grep -c 'bgcolor="' /tmp/page.html
grep -c 'border="' /tmp/page.html
grep -c 'cellpadding=\|cellspacing=' /tmp/page.html
```

### 11.3 Missing Required Attributes
```bash
# <img> missing alt attribute entirely
grep -o '<img[^>]*>' /tmp/page.html | grep -cv 'alt='

# <img> with empty alt="" (decorative — acceptable only for spacers)
grep -o '<img[^>]*>' /tmp/page.html | grep -c 'alt=""'

# <input> missing type attribute (defaults to text, may cause UX issues)
grep -o '<input[^>]*>' /tmp/page.html | grep -cv 'type='

# <a> tags missing href (non-functional links)
grep -o '<a [^>]*>' /tmp/page.html | grep -cv 'href='

# <label> elements missing for= attribute
grep -o '<label[^>]*>' /tmp/page.html | grep -cv 'for='

# <button> missing type attribute (defaults to submit — can cause unexpected form submissions)
grep -o '<button[^>]*>' /tmp/page.html | grep -cv 'type='
```

### 11.4 JavaScript Error Patterns
```bash
# Inline event handlers (brittle JS — error-prone pattern)
echo "=== INLINE EVENT HANDLERS ===" 
grep -oc 'onclick=' /tmp/page.html | xargs -I{} echo "onclick: {}"
grep -oc 'onload=' /tmp/page.html | xargs -I{} echo "onload: {}"
grep -oc 'onerror=' /tmp/page.html | xargs -I{} echo "onerror: {}"
grep -oc 'onsubmit=' /tmp/page.html | xargs -I{} echo "onsubmit: {}"

# console.log left in production (debug code not stripped)
grep -c 'console\.log' /tmp/page.html

# JavaScript void(0) pattern (outdated href technique)
grep -c 'href="javascript:void' /tmp/page.html

# document.write usage (blocks rendering, deprecated pattern)
grep -c 'document\.write(' /tmp/page.html

# eval() usage (security risk + performance)
grep -c 'eval(' /tmp/page.html

# Synchronous XHR (blocks main thread)
grep -c 'XMLHttpRequest\|\.open.*false' /tmp/page.html

# Mixed content signals (http:// resources on https:// page)
base_protocol=$(grep -oP 'canonical" href="\K(https?)' /tmp/page.html | head -1)
if [ "$base_protocol" = "https" ]; then
  grep -c 'src="http://' /tmp/page.html
  grep -c 'href="http://' /tmp/page.html
fi
```

### 11.5 Inline Script Quality
```bash
# Count total inline <script> blocks (not src= ones)
grep -c '<script>' /tmp/page.html
grep -c '<script type="text/javascript">' /tmp/page.html

# Scripts in <head> without async/defer (render-blocking)
# Extract head section and check scripts
sed -n '/<head/,/<\/head>/p' /tmp/page.html | grep '<script' | grep -cv 'async\|defer\|type="application/ld+json"'

# Check for common error-prone patterns
grep -c 'undefined\.' /tmp/page.html
grep -c '\.innerHTML\s*=' /tmp/page.html  # XSS risk
```

### Console & Code Quality Output Table

| Check | Found | Severity | Notes |
|---|---|---|---|
| Duplicate IDs | [list] | P1 | Must be unique per HTML spec |
| Unclosed `<div>` tags | [open vs close count] | P1/P2 | Structural break |
| Nested `<a>` tags | [count] | P1 | Invalid HTML |
| Deprecated `<font>` | [count] | P2 | Use CSS instead |
| Deprecated `<center>` | [count] | P2 | Use CSS flexbox/text-align |
| Deprecated `align=` attr | [count] | P2 | Use CSS |
| `<img>` missing `alt=` attr | [count] | P1 | Accessibility failure |
| `<input>` missing `type=` | [count] | P2 | UX + mobile keyboard risk |
| `<a>` missing `href=` | [count] | P2 | Non-functional link |
| `<button>` missing `type=` | [count] | P2 | Accidental form submit |
| `<label>` missing `for=` | [count] | P2 | Accessibility failure |
| `console.log` in production | [count] | P2 | Debug code — strip before deploy |
| `document.write()` | [count] | P1 | Blocks rendering |
| `eval()` usage | [count] | P1 | Security + performance risk |
| Inline `onclick=` handlers | [count] | P2 | Brittle, use addEventListener |
| `javascript:void(0)` hrefs | [count] | P3 | Outdated pattern |
| Mixed content (http on https) | [count] | P1 | Browser blocks, breaks assets |
| Render-blocking head scripts | [count] | P2 | Add async/defer |
| `.innerHTML =` assignments | [count] | P2 | Potential XSS vector |

**Severity Rules:**
- Duplicate IDs = **P1** (CSS/JS targeting breaks; invalid per HTML spec)
- `document.write()` = **P1** (blocks rendering, deprecated)
- `eval()` = **P1** (CSP violation risk, XSS attack surface)
- Mixed content (http on https) = **P1** (browser blocks resources, breaks page)
- Unclosed tags (count mismatch >5) = **P2** (layout breaks in some browsers)
- `console.log` left in = **P2** (performance + exposes logic to users)
- Deprecated elements = **P2** (invalid markup, unpredictable rendering)
- Missing `type=` on `<button>` = **P2** (submits parent form unexpectedly)
- Inline event handlers = **P2** (CSP violations, hard to debug)
- `javascript:void(0)` = **P3** (works but outdated)

---

## Scoring Weights & Formula

| Category | Weight | Max Score |
|---|---|---|
| On-Page SEO | 20% | 20 |
| Content Quality | 20% | 20 |
| Technical Meta Tags | 12% | 20 |
| Schema | 10% | 15 |
| Images | 10% | 15 |
| QA Checklist | 14% | 10 |
| Responsive Test | 10% | 10 |
| Console & Code Quality | 4% | 10 |

**Overall Score = (On-Page × 0.20) + (Content × 0.20) + (Technical × 0.12) + (Schema × 0.10) + (Images × 0.10) + (QA × 0.14) + (Responsive × 0.10) + (Console × 0.04)**

**Note:** Trademark compliance is now checked in QA Checklist (simple presence check for ® or ™ symbol on first mention). No longer scored as separate category.

Range: 0–100

---

## Output Format

**ALL REPORTS MUST FOLLOW THIS EXACT STRUCTURE:**

```
=== UWORLD PAGE AUDIT REPORT ===
URL: [url]
Date: [date]
Page Type: [Hub / Pillar Page / Product / Blog] ([description])

OVERALL SCORE: XX/100

SECTION SCORES:
  On-Page SEO:        XX/20   [progress bar with ███░░░]
  Content Quality:    XX/20   [progress bar]
  Technical:          XX/20   [progress bar]
  Schema:             XX/15   [progress bar]
  Images:             XX/15   [progress bar]
  QA Checklist:       XX/10   [progress bar]
  Responsive Test:    XX/10   [progress bar]
  Console & Code:     XX/10   [progress bar]

---

## SEO ANALYSIS

| Check | Rule | Value | Status |
|---|---|---|---|
| Title tag | 50–70 chars, keyword-rich | "[title]" (XX chars) | PASS/FAIL/WARN |
| Meta description | 150–165 chars, compelling | "[description]" (XX chars) | PASS/FAIL |
| H1 count | Exactly 1 | X H1 found | PASS/FAIL |
| H1 content | Keyword-rich, matches intent | "[h1 text]" | PASS/FAIL |
| H2–H6 hierarchy | Logical, no skipped levels | XX H2s, XX H3s | PASS/FAIL |
| Canonical | Present, self-ref or correct | [URL] | PASS/FAIL |
| Lang attribute | <html lang="en"> | lang="[lang]" | PASS/FAIL |
| Viewport | Standard mobile meta | Present | PASS/FAIL |
| OG: title | User-facing, not staging | "[og:title]" | PASS/FAIL |
| OG: description | Present, compelling | [status] | PASS/FAIL |
| OG: image | Absolute URL | [status] | PASS/FAIL |
| OG: url | Matches canonical | [status] | PASS/FAIL |
| Twitter card | twitter:card present | [value] | PASS/FAIL |
| Meta robots | index, follow or block | [value] | PASS/FAIL |
| URL structure | Short, descriptive | [URL] | PASS/FAIL |

---

## IMAGE ANALYSIS (XX total images)

**MANDATORY TABLE: Complete Inventory of ALL Images**

| # | Filename/Source | Format | Size (KB) | Alt Text | Width | Height | Loading | Issues |
|---|---|---|---|---|---|---|---|---|
| 1 | [src basename] | [jpg/png/webp/svg/gif/avif] | [KB or 'not specified'] | [text or MISSING] | [px or 'missing'] | [px or 'missing'] | [lazy/not specified] | [P1/P2 flags] |
| 2 | [next image] | ... | ... | ... | ... | ... | ... | ... |
| ... | (continue for ALL images on page) | ... | ... | ... | ... | ... | ... | ... |

**CRITICAL ENFORCEMENT RULES FOR IMAGE TABLE:**
- MUST show EVERY single <img> tag found on page (no exceptions, no filtering)
- MUST include all 9 columns: #, Filename, Format, Size, Alt, Width, Height, Loading, Issues
- MUST get file size via curl -sI for each image URL (not just "not specified")
- MUST populate Alt Text column with actual alt attribute value or "MISSING" if absent
- MUST populate Width/Height with actual attribute values or "missing" if absent
- MUST populate Loading with "lazy" if loading="lazy" present, else "not specified"
- MUST flag all issues in Issues column using P1/P2/P3 severity
- MUST include row for EVERY image, in order of appearance

**After Table - Summary Statistics:**
- **Total images:** XX
- **Images with alt text:** XX/XX (XX%)
- **Images MISSING alt text:** XX (P1 failures)
- **WebP/AVIF format:** XX (XX%)
- **PNG/JPG format:** XX (P2 flags)
- **Dimensions present:** XX
- **Dimensions missing:** XX (P2 flags)
- **Lazy loading detected:** XX
- **Format status:** [optimized | needs WebP conversion | CRITICAL OVERSIZED]

**Critical Issues Section (required):**
- List ALL P1 issues first (oversized images >500KB, missing alt text, etc.)
- List ALL P2 issues second (missing dimensions, no lazy loading, etc.)
- Include specific details: filename, size, impact, fix required

---

## LINK ANALYSIS (XXX total)

| Type | Count | Target="_blank" | rel="noopener noreferrer" | Issues |
|---|---|---|---|---|
| Internal | XX | [count] | N/A | [issues] |
| External | XX | [count] | [count] | **P2: [count] missing security attributes** |
| [Other type] | XX | [count] | [count] | [issues] |

> **Pattern:** [Summary of link security findings]

---

## PERFORMANCE

| Check | Rule | Status |
|---|---|---|
| Render-blocking scripts | No `<script src>` in `<head>` without `async`/`defer` | PASS/FAIL |
| Stylesheet count | ≤5 external | PASS/FAIL |
| HTML file size | <200KB | PASS/FAIL — [actual size] |
| LCP image preload | `<link rel="preload" as="image">` | PASS/FAIL |
| Image dimensions | Width + height on all | PASS/FAIL |
| Lazy loading | Below-fold images lazy | PASS/FAIL |

---

## SCHEMA / STRUCTURED DATA

**Schemas Found:**
1. **[Schema Type 1]** — [status] ✓
2. **[Schema Type 2]** — [status] ✓

**Missing:**
- **[Schema Type 3]** — [reason]
- **[Schema Type 4]** — [reason]

**Assessment:** XX/15 — [summary]

---

## CONTENT QUALITY

| Metric | Value | Status |
|---|---|---|
| Word count | [count] | PASS/FAIL |
| Readability | [grade level] | PASS/FAIL |
| Keyword usage | [density] | PASS/FAIL |
| E-E-A-T signals | [indicators] | PASS/FAIL |
| Freshness | [publish/update dates] | PASS/FAIL |
| Structure | [assessment] | PASS/FAIL |

---

## QA CHECKLIST

**All Pages:**
| Item | Status |
|---|---|
| CTA button present | PASS/FAIL |
| Footer copyright year | PASS/FAIL |
| Privacy Policy link | PASS/FAIL |
| Terms of Use link | PASS/FAIL |
| Primary product name includes ® or ™ symbol (first mention) | PASS/FAIL |

**Hub/Pillar Pages:**
| Item | Status |
|---|---|
| Author byline + credentials | PASS/FAIL |
| Publish date | PASS/FAIL |
| Table of contents | PASS/FAIL |
| Related articles/links | PASS/FAIL |

---

## RESPONSIVE TEST

| Check | Rule | Status |
|---|---|---|
| Viewport meta tag | `width=device-width, initial-scale=1` | PASS/FAIL |
| Responsive images | `srcset` on content images | PASS/FAIL |
| Font sizes | No inline <14px | PASS/FAIL |
| Touch targets | ≥44px height (WCAG 2.5.5) | PASS/FAIL |
| Fixed-width containers | No >480px fixed width | PASS/FAIL |
| Tables | Wrapped in overflow | PASS/FAIL |

---

## CONSOLE & CODE QUALITY

| Issue | Count | Severity | Notes |
|---|---|---|---|
| Duplicate IDs | XX | P1/P2 | [list IDs] |
| Unclosed tags | [count diff] | P1/P2 | [details] |
| Deprecated elements | XX | P2 | [list] |
| Missing required attrs | XX | P1/P2 | [details] |
| Render-blocking scripts | XX | P1 | [details] |
| External links missing rel | XX | P2 | [details] |

---

## PRIORITIZED FIX LIST

### P1 — CRITICAL (Fix Immediately)

**1. [ISSUE TITLE]**
- Current: [what exists]
- **Fix:** [specific action with example code if applicable]
- **Impact:** XX–XX% improvement
- **Effort:** X hours

**2. [ISSUE TITLE]**
- Description with details
- **Fix:** [specific steps]
- **Impact:** [metric]
- **Effort:** [time]

### P2 — IMPORTANT (Fix Within 1 Week)

**1. [ISSUE TITLE]**
- Description
- **Impact:** [metric]
- **Effort:** [time]

### P3 — MINOR (Fix Within 1 Month)

**1. [ISSUE TITLE]**
- Description
- **Impact:** [metric]

---

## SUMMARY

The [page type] scores **XX/100** — [2-3 sentence assessment of strengths and weaknesses].

**Key differentiator:** [Notable finding vs. similar pages]

**Top 3 Critical Issues:**
1. [Issue 1 with impact]
2. [Issue 2 with impact]
3. [Issue 3 with impact]

**Top 3 Strengths:**
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

**Combined P1 fixes are projected to yield:** +XX% organic visibility improvement, +XX% social CTR gain, +XX% conversion improvement

**Timeline:** P1 (1-3 days) + P2 (4-7 days) = 2 weeks for core fixes
```

**KEY FORMATTING RULES (MANDATORY - NO EXCEPTIONS):**

1. ✅ Start with `=== UWORLD PAGE AUDIT REPORT ===` header
2. ✅ Include Overall Score with visual progress bars using `███░░░` format
3. ✅ All 9 sections in this exact order: SEO → Images → Links → Performance → Schema → Trademark → Content → QA → Responsive → Console → Fixes → Summary
4. ✅ IMAGE ANALYSIS section MUST include complete table showing EVERY image with all 9 columns
5. ✅ Image table columns are: # | Filename/Source | Format | Size (KB) | Alt Text | Width | Height | Loading | Issues
6. ✅ Each image row MUST be populated with actual values (no placeholders or empty cells)
7. ✅ File sizes MUST be fetched via curl -sI (not estimated or guessed)
8. ✅ Alt text MUST show actual content or "MISSING" if absent (not "N/A" or blank)
9. ✅ Width/Height MUST show actual values or "missing" if absent (not "N/A")
10. ✅ Loading MUST show "lazy" or "not specified" (not "N/A" or blank)
11. ✅ Issues MUST be populated with P1/P2/P3 severity or "None"
12. ✅ Use markdown tables for structured data
13. ✅ Include specific values (char counts, percentages, file sizes)
14. ✅ Use PASS/FAIL/WARN status labels
15. ✅ P1/P2/P3 severity classification with effort estimates
16. ✅ Code examples in fixes (wrapped in backticks)
17. ✅ Impact metrics for each fix
18. ✅ Always include "SUMMARY" at end with key takeaways

**IF ANY OF RULES 4-11 ARE NOT FOLLOWED, THE REPORT IS INVALID AND INCOMPLETE.**

---

## Error Handling

| Scenario | Action |
|---|---|
| URL unreachable (404, DNS failure, connection refused) | Report error clearly with status code. Do not guess content. Suggest user verify URL and try again. |
| Page requires authentication (401/403) | Report page is behind authentication. Suggest providing rendered HTML directly or a publicly accessible URL. |
| JavaScript-rendered content (empty body in HTML) | Note that key content may be CSR. Analyze available HTML and flag results as potentially incomplete. Suggest browser-rendered snapshot if available. |
| curl connection timeout | Retry with longer timeout or check if domain is blocked. Some domains may require user-agent headers: `curl -s -A "Mozilla/5.0" URL` |
| **IMAGE TABLE INCOMPLETE** | **CRITICAL: If image table is missing any images, the report is INVALID. Use bash grep to extract EVERY <img> tag. Example: `grep -o '<img[^>]*>' file.html` — guaranteed to find every image. Re-run extraction and ensure table shows all images.** |
| Image file size unavailable | Get size via curl -sI. If HEAD request fails, note "not specified" in Size column. Do NOT skip the column - it must be populated. |
| Images not detected | Use bash grep to extract ALL img tags: `grep -o '<img[^>]*>' file.html \| nl` — guaranteed to find every image with attributes. If grep returns 0 images, verify page loaded correctly. |
| Malformed HTML | Bash grep is resilient to broken HTML. It will extract partial matches. Continue analysis with available data and note limitations in report. Do NOT omit the image table if HTML is malformed. |
| Large pages with 100+ images | Image table MUST still show every image, even if page has 100+ images. No exceptions, no "see attached file" - table must be in report. If too large, this is a finding to report (page bloat issue). |

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

## STRICT ENFORCEMENT - NON-NEGOTIABLE RULES

These rules are MANDATORY on EVERY audit. Failure to follow these results in incomplete/invalid reports.

1. **IMAGE ANALYSIS TABLE IS MANDATORY**
   - MUST include complete table showing EVERY image on page
   - MUST have all 9 columns: #, Filename, Format, Size, Alt, Width, Height, Loading, Issues
   - NO exceptions - even if page has 100+ images, table must show all
   - NO "summary instead of table" - table is the primary deliverable

2. **FILE SIZES MUST BE FETCHED**
   - Use curl -sI to get actual file size for each image URL
   - Flag images >500KB as P1 (critical)
   - Flag images 200-500KB as P2 (warning)
   - If curl fails, still mark as "not specified" but note in issues

3. **ALT TEXT MUST BE VERIFIED**
   - Check every <img> tag for alt attribute
   - "MISSING" = no alt attribute at all (P1)
   - Empty alt="" = acceptable only for decorative images (flag if content image)
   - Actual text = show first 40 characters

4. **DIMENSIONS MUST BE EXTRACTED**
   - Extract width and height from every <img> tag
   - "missing" = either width OR height not present (P2 - CLS risk)
   - Both present = show as "XXpx"

5. **LAZY LOADING MUST BE CHECKED**
   - "lazy" = loading="lazy" attribute present
   - "not specified" = no loading attribute (P2 for below-fold images)
   - Report all non-lazy images on page

6. **ISSUES COLUMN MUST BE POPULATED**
   - Every image must have issues column entry or "None"
   - Use P1/P2/P3 severity labels
   - Examples: "P1: No alt text", "P2: Missing dims", "P2: Not lazy"

7. **OUTPUT FORMAT MUST BE FOLLOWED EXACTLY**
   - Header must include total image count: "## IMAGE ANALYSIS (XX total images)"
   - All sections must appear in order (SEO → Images → Links → Performance → Schema → Trademark → Content → QA → Responsive → Console → Fixes → Summary)
   - Progress bars must use ███░░░ format
   - Section scores must have exact format

8. **TRADEMARK COMPLIANCE TABLE MUST SHOW VIOLATIONS**
   - Must scan ALL text for trademark terms
   - Must count both bare instances and instances with symbols
   - Must calculate % compliance
   - Must flag every bare instance as P1 or P1 CRITICAL

---

## Version History

- **v2.5.0** (2026-05-18): TRADEMARK SIMPLIFICATION UPDATE - Trademark compliance moved from separate scoring section to QA Checklist. Simplified check: if primary product name has ® or ™ symbol on first mention = PASS. Removed detailed trademark violation tracking. Scoring weights adjusted: On-Page 20%, Content 20%, Technical 12%, Schema 10%, Images 10%, QA 14%, Responsive 10%, Console 4%. Trademark no longer separate category (now part of QA checklist).

- **v2.4.0** (2026-05-18): STRICT ENFORCEMENT UPDATE - All rules are now mandatory and non-negotiable. Image Analysis table MUST show every image with all 9 columns. File sizes MUST be fetched via curl. Alt text, dimensions, and lazy loading MUST be verified for every image. No exceptions for large pages (100+ images). Output format enforcement: 9 mandatory sections in exact order, progress bars required, signature footer required. Trademark compliance table must show all violations with %. Every audit must follow these rules without exception.

- **v2.3.0** (2026-05-18): Updated Output Format to use CLEAN PLAIN-TEXT only (no markdown). All reports now use ASCII dividers, plain-text tables, and symbol indicators (✓/⚠️/❌). Removes markdown formatting issues for universal readability across all editors/viewers. Output saved as `.txt` files with structured sections.
- **v2.2.0** (2026-05-18): Added Step 10 Responsive Test (viewport meta, srcset/sizes coverage, media queries, font sizes, touch targets, horizontal scroll risk). Added Step 11 Console & Code Quality (duplicate IDs, unclosed tags, deprecated elements, missing required attributes, JS error patterns — console.log, document.write, eval, mixed content, inline handlers). Updated scoring to 9 dimensions; weights rebalanced to 100%.
- **v2.1.0** (2026-05-14): Switched from WebFetch to bash+curl+grep HTML parsing for reliable metadata extraction. Added comprehensive bash scripts for image inventory with file size detection. Improved accuracy of alt text, dimensions, and lazy loading detection. Enhanced image analysis to extract ALL images with complete details. Better error handling for timeout/connection issues.
- **v2.0.0** (2026-05-13): Complete image analysis methodology with mandatory alt text, comprehensive checklist coverage, detailed scoring weights, improved error handling, common findings reference
- **v1.9.9** (prior): Initial version
