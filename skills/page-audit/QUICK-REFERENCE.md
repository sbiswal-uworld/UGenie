# Page Audit Skill — Quick Reference Guide

## TL;DR — What Changed

**Old approach (v2.0.0):** WebFetch → markdown conversion → metadata loss 😞
**New approach (v2.1.0):** curl → bash grep → complete HTML parsing ✅

---

## Quick Start

### 1. Run Full Page Audit
```bash
/page-audit https://example.com/page product
```

Output:
- **Overall Score:** 0–100 (weighted across 7 categories)
- **Section Scores:** On-Page SEO, Content, Technical, Schema, Images, Trademark, QA
- **Detailed Analysis:** Tables for each audit dimension
- **Complete Image Inventory:** ALL images with sizes, alt text, dimensions
- **Prioritized Fixes:** P1 (critical), P2 (important), P3 (minor)

---

## Key Improvements in v2.1.0

### Better Image Analysis
**Previously:**
```
- Total images: 28
- Images with alt text: ~20 (estimate)
- Image sizes: "not specified"
- Missing dimensions: Unknown
```

**Now:**
```
| # | Filename | Format | Size (KB) | Alt Text | Width | Height | Loading | Issues |
|---|----------|--------|-----------|----------|-------|--------|---------|--------|
| 1 | logo.webp | WebP | 3 | Logo | 273 | 43 | not specified | ✓ PASS |
| 2 | hero.webp | WebP | 74 | **MISSING** | 1200 | 675 | not specified | **P1: No alt** |
| 3-28 | ... | ... | ... | ... | ... | ... | ... | ... |
```

**What you get:**
- ✅ File size in KB (identifies bloated images)
- ✅ Exact image count (no missed images)
- ✅ Alt text status (P1 if missing)
- ✅ Width/height validation (prevents CLS)
- ✅ Lazy loading check (performance impact)

### Better Metadata Extraction
**Accurately extracts:**
- Title tag (not converted to markdown)
- Meta description (not corrupted)
- Canonical URL (not lost)
- All OG tags (og:title, og:description, og:image, og:url)
- Twitter Card meta
- JSON-LD schema types
- HTML lang attribute
- Viewport settings

### Better Link Analysis
**Detects:**
- All internal links (count + structure)
- All external links (security risk assessment)
- Missing `target="_blank"` on external links
- Missing `rel="noopener noreferrer"` (security issue)

### Better Performance Analysis
**Reports:**
- Exact HTML file size (identifies bloat)
- Script count (render-blocking risk)
- CSS file count (network impact)
- Image lazy loading percentage
- File size breakdown by image

---

## How the Bash Parsing Works

### Step 1: Fetch Raw HTML
```bash
curl -s "URL" > /tmp/page.html
```

### Step 2: Extract Metadata
```bash
# Title
grep -oP '<title>\K[^<]+' /tmp/page.html

# Description
grep -oP '<meta name="description" content="\K[^"]+' /tmp/page.html

# Canonical
grep -oP '<link rel="canonical" href="\K[^"]+' /tmp/page.html

# OG tags
grep 'property="og:' /tmp/page.html | grep -E 'og:(title|description|image|url)'
```

### Step 3: Extract Images with Sizes
```bash
# Count images
grep -c '<img' /tmp/page.html

# Extract all img tags
grep -o '<img[^>]*>' /tmp/page.html | nl

# Get file sizes
curl -sI "IMAGE_URL" 2>/dev/null | grep -i 'content-length'
```

### Step 4: Analyze Images
For each image:
1. Get src → filename → format
2. Curl -I to get file size
3. Check for alt attribute
4. Check for width/height
5. Check for loading="lazy"
6. Flag issues (P1/P2)

---

## What Gets Reported Now

### 1. Complete Image Inventory Table
All images listed with:
- Filename (truncated for readability)
- Format (WebP, PNG, JPG, SVG, etc.)
- File size in KB (with P1/P2 flags if oversized)
- Alt text (or **MISSING** flag)
- Width & height (or **missing** flag)
- Loading attribute (lazy or not specified)
- Issues (P1 CRITICAL, P2 IMPORTANT, etc.)

### 2. Image Summary Statistics
```
IMAGE SUMMARY:
- Total images: 28
- Images with alt text: 25 (89%)
- Images MISSING alt text: 3 (P1 CRITICAL)
- WebP/AVIF format: 26 (93% modern)
- PNG/JPG format: 2 (7% legacy)
- Dimensions present: 28/28 (100%)
- Dimensions missing: 0
- Lazy loading detected: 18/28 (64%)
- Format optimization: GOOD (93% WebP)
```

### 3. File Size Breakdown
```
Size Distribution:
├─ < 10 KB:   12 images (ultra-light)
├─ 10-50 KB:  8 images (good)
├─ 50-100 KB: 5 images (moderate)
├─ 100+ KB:   3 images (needs optimization)
```

### 4. Specific Issues by Image
```
Image #2: cropped-logo.webp
- Size: 3 KB ✓
- Alt: **MISSING** ✗ P1 CRITICAL
- Dimensions: 274 × 43 ✓
- Issues: Add alt="UWorld Grad School Logo"

Image #22: L91304.webp (testimonial)
- Size: 155 KB ✓
- Alt: **MISSING** ✗ P1 CRITICAL
- Dimensions: **missing** ✗ P2
- Issues: Add alt text + width/height attributes
```

---

## Typical Audit Timeline

### Quick Audit (10 minutes)
- Fetch page
- Extract core metadata
- Count images & identify missing alt text
- Check page size & script count
- Generate quick summary

### Standard Audit (30 minutes)
- Full metadata extraction
- Complete image inventory (all images with sizes)
- Link analysis (internal/external + security)
- Schema detection
- Content quality assessment
- Performance checks
- Trademark compliance scan

### Comprehensive Audit (60 minutes)
- Everything above +
- Detailed heading hierarchy
- Every link reviewed for descriptive text
- Content word count & readability
- E-E-A-T signal analysis
- QA checklist (page-type specific)
- Prioritized fix list (P1/P2/P3)
- Expected ROI calculations

---

## Common Issues Identified

### P1 — CRITICAL (Fix Immediately)
- ❌ Missing alt text (accessibility + SEO)
- ❌ HTML > 500 KB (performance bloat)
- ❌ Trademark symbols missing (legal risk)
- ❌ No schema markup (blocks rich results)

### P2 — IMPORTANT (Fix Within 1 Week)
- ⚠ Images missing dimensions (CLS risk)
- ⚠ Images > 200 KB (optimize compression)
- ⚠ Missing lazy loading (LCP performance)
- ⚠ External links without rel="noopener" (security)

### P3 — MINOR (Fix Within 1 Month)
- 📝 No copyright year (legal polish)
- 📝 Generic OG title (social CTR)
- 📝 No author credentials (E-E-A-T)

---

## Real-World Example: MCAT Prep Course

**Audit of:** https://gradschool.uworld.com/mcat/prep-course/

### Results
```
OVERALL SCORE: 68/100

CRITICAL FINDINGS:
1. MCAT trademark: 196 instances missing ® symbol (P1)
2. HTML bloat: 848 KB (4.2× over limit) (P1)
3. Missing alt text: 2 images (P1)
4. Missing dimensions: 5 images (P2)
5. Lazy loading: Only 45% of images (P2)

IMAGE INVENTORY:
- Total: 24 images
- WebP: 24/24 (100% ✓)
- With alt: 22/24 (92%)
- Missing alt: 2 (P1)
- Missing dimensions: 5 (P2)
- Lazy loaded: 14/24 (58%)

QUICK FIXES (30 minutes):
✓ Add 1 testimonial (+2–4% conversion)
✓ Add alt text to 2 images (+3–5% SEO)
✓ Add dimensions to 5 images (eliminate CLS)
✓ Promote money-back guarantee (+3–8% conversion)

IMPACT:
- 25–35% organic visibility improvement
- 5–12% conversion rate increase
- Eliminated Core Web Vitals issues
- Legal trademark compliance
```

---

## Tips for Using the Skill

1. **Always check the image inventory table** — It shows which images have issues
2. **Review P1 issues first** — These are blocking visibility/accessibility
3. **File sizes matter** — Large images impact Core Web Vitals significantly
4. **Alt text is mandatory** — Every image must have descriptive alt text
5. **Dimensions prevent CLS** — Always include width + height attributes
6. **Lazy loading saves LCP** — Apply to images below the fold

---

## Questions?

For detailed implementation guidance, see:
- `SKILL.md` — Full methodology and rules
- `CHANGELOG.md` — What's new in v2.1.0
- Real examples from recent audits (AP Biology, MCAT courses)
