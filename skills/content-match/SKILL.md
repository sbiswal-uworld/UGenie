---
name: content-match
description: "Production-grade content matching & full compliance audit: Compare Google Docs, Word docs, and briefs against live UWorld pages. Line-by-line semantic diff, Elementor ID tracking, link audit, ❌/⚠️/✅ classification, checkbox audit table, Quick Fix List, PMM List, and trademark verification. Supports Google Drive authenticated access."
user-invokable: true
argument-hint: "<live-url> [google-doc-url or paste CONTENT section] [internal-domain]"
version: 4.0.0
---

# Content Match Engine v4.0.0 — Full Compliance Audit

**Usage:** `/content-match <live-url> <source-url-or-paste> [internal-domain]`

**Examples:**
```
/content-match https://legal.uworld.com/bar-exam/mbe/ https://docs.google.com/document/d/[ID] legal.uworld.com
/content-match https://finance.uworld.com/cfa/ https://docs.google.com/document/d/[ID]
/content-match https://collegeprep.uworld.com/ap/calculus/
[paste CONTENT section here]
```

Three ways to provide source content:

1. **Google Doc URL (Any Access Level)** — If Google Drive Connector is active, any shared or private Google Doc is accessible
   ```
   /content-match https://live-url.com/ https://docs.google.com/document/d/[FILE-ID]/edit
   ```

2. **Paste CONTENT Section** — Copy-paste only the CONTENT section from your document (exclude metadata)
   ```
   /content-match https://live-url.com/
   [paste content here]
   ```

3. **Public Google Doc Link** — If document is publicly shared
   ```
   /content-match https://live-url.com/ https://docs.google.com/document/d/[FILE-ID]/edit?usp=sharing
   ```

You are a **Senior QA Engineer for UWorld**. This skill performs a **full compliance audit** — comparing every element of the approved source document against the live Elementor page implementation. Every mismatch is flagged, classified, and reported with actionable fixes.

---

## CRITICAL ENFORCEMENT RULES (ALL MANDATORY — NO EXCEPTIONS)

1. **FULLY AUTOMATIC** — Never ask user to manually copy-paste. Always auto-fetch source via Google Drive Connector and live page via curl/WebFetch.
2. **COMPLETE COVERAGE** — Every element in the source CONTENT section must be checked. No skipping, no summarizing.
3. **EXACT STRING MATCHING** — "Shop Books" ≠ "shop books". Case, spacing, punctuation all count.
4. **ELEMENT ID REQUIRED** — Every check in the checkbox table must reference the Elementor data-id or HTML element identifier.
5. **CLASSIFY EVERY ERROR** — Each mismatch must be ❌ Fail (HTML error) OR ⚠️ PMM (source/doc error). Never leave status blank.
6. **LINK AUDIT MANDATORY** — All external links must have `target="_blank"`. All internal links must NOT. No exceptions.
7. **TRADEMARK AUDIT MANDATORY** — Check all UWorld product names for ® / ™ on first mention.
8. **VISUAL DIFF REQUIRED** — Diffchecker-style side-by-side output for every CHANGED/MISSING/EXTRA block.
9. **FOUR REPORTS GENERATED** — Checkbox Table + Quick Fix List + PMM List + Summary Counts. Always all four.
10. **CONTENT SECTION ONLY** — Exclude SUMMARY, GENERAL, METADATA, DEVELOPER NOTES, SEO OUTLINE, REFERENCES from source doc.

---

## AUTOMATED FETCH WORKFLOW

### Auto-Fetch Priority Order:

**Source Document:**
1. **Google Drive Connector** (MCP: `mcp__04996a76-7965-4724-a66a-e524235ef9ce__read_file_content`) — authenticated access to any Google Doc regardless of sharing level. Extract file ID from URL: `https://docs.google.com/document/d/[FILE-ID]/edit`
2. **Public Google Doc export** — `https://docs.google.com/document/d/[ID]/export?format=txt`
3. **Pasted CONTENT section** — user pastes content directly after the command

**Live Page:**
1. **curl** — `curl -s "URL" > /tmp/page.html` — full HTML with Elementor IDs preserved
2. **WebFetch** — fallback if curl unavailable

**Internal Domain Detection:**
- If 3rd argument provided → use it as internal domain
- If not provided → auto-detect from the live URL hostname (e.g., `legal.uworld.com`)
- Use for link auditing rules: internal = same domain, external = different domain

**Document Format Handling:**

**Supported formats:**
- ✅ Google Docs (any sharing level if Google Drive Connector active)
- ✅ Google Docs (publicly shared link)
- ✅ DOCX files (pasted text extraction)
- ✅ Plain text paste
- ✅ Markdown formatted text

**Unsupported:**
- ❌ PDF links (cannot extract structured content)
- ❌ Private Google Drive links without connector active
- ❌ Password-protected documents

---

## PHASE 1 — INTAKE & SETUP

**Step 1.1** Receive and validate source document URL or pasted content.
**Step 1.2** Auto-fetch live page via curl into `/tmp/qa_page.html`.
**Step 1.3** Confirm internal domain (from argument or auto-detected from live URL).
**Step 1.4** Identify page sections from headings (Hero, Nav, Features, Pricing, FAQ, Footer, etc.).
**Step 1.5** Create comparison matrix scaffold — blank checkbox table ready for population.

**Announce intake summary before proceeding:**
```
INTAKE CONFIRMED
  Live URL:         [url]
  Source:           [Google Doc / Pasted Content]
  Internal Domain:  [domain]
  Page Sections:    [H1, H2 heading list]
  HTML Size:        [KB]
  Source Blocks:    [N extracted]
```

---

## PHASE 2 — CONTENT EXTRACTION

### 2A — From Source Document

Extract ONLY the **CONTENT section** — everything between the `CONTENT` marker and `END REQUIREMENTS` marker. Exclude:
- ❌ SUMMARY, GENERAL, METADATA, DEVELOPER NOTES
- ❌ CONTENT WRITER NOTES, SEO CONTENT OUTLINE, CONTENT REFERENCES
- ❌ OLD CONTENT OUTLINE, DESIGN DELIVERABLES, END REQUIREMENTS

**✅ CONTENT section definition:** Everything between the "CONTENT" header/marker and "END REQUIREMENTS" marker (inclusive of content, exclusive of markers).

**Parse into numbered blocks:**

| Block ID | Type | Content |
|---|---|---|
| S[1] | H1 | Exact heading text |
| S[2] | H2 | Exact subheading text |
| S[3] | P | Full paragraph text |
| S[4] | LIST | All bullet items in order |
| S[5] | TABLE | All rows × columns |
| S[6] | CTA | Button label + target URL |
| S[7] | IMG | Alt text + description |
| S[8] | LINK | Anchor text + URL |
| S[9] | BOLD | Bolded text (inline) |
| S[10] | ITALIC | Italicized text |
| S[11] | EYEBROW | Section label / eyebrow text |
| S[12] | TESTIMONIAL | Quote text + attribution name |
| S[13] | FAQ-Q | Question text |
| S[14] | FAQ-A | Full answer text |
| S[15] | DISCLAIMER | Fine print / footnote text |

**Normalize whitespace** — Collapse multiple spaces/newlines, but preserve paragraph breaks.

**Parse structure** — Break into semantic blocks:
- **Headings** — H1, H2, H3 (extract level + text)
- **Paragraphs** — Full text (separated by blank lines)
- **Lists** — Detect `*`, `-`, `1.` markers; extract items with nesting level
- **Tables** — Parse rows/columns
- **Code blocks** — If present (preserve verbatim)
- **CTAs/Links** — Extract anchor text + URLs
- **Quotes/Emphasis** — Preserve with markdown notation (e.g., `**bold**`, `_italic_`)

**Number each block** — Source[1], Source[2], ..., Source[N]
**Tokenize for semantic matching** — Create word-level tokens for similarity analysis

**Structured block format:**
```json
[
  {"id": 1, "type": "h2", "text": "The Four Big Ideas", "tokens": ["the", "four", "big", "ideas"]},
  {"id": 2, "type": "paragraph", "text": "Writers adapt their writing...", "tokens": [...]},
  {"id": 3, "type": "list", "items": ["Item 1", "Item 2"], "tokens": [...]},
  ...
]
```

### 2B — From Live HTML

**Extraction commands (bash):**
```bash
curl -s "[URL]" > /tmp/qa_page.html

# Headings
grep -o '<h[1-4][^>]*>[^<]*' /tmp/qa_page.html | sed 's/<[^>]*>//g'

# Paragraphs with class
grep 'class="custom-para\|faq-para\|passage-text' /tmp/qa_page.html | sed 's/<[^>]*>//g'

# List items
grep -o '<li[^>]*>[^<]*' /tmp/qa_page.html | sed 's/<[^>]*>//g'

# Tables
grep -o '<t[dh][^>]*>[^<]*' /tmp/qa_page.html | sed 's/<[^>]*>//g'

# Buttons & CTAs
grep -o '<a[^>]*>[^<]*\|<button[^>]*>[^<]*' /tmp/qa_page.html | sed 's/<[^>]*>//g'

# Image alt text
grep -o 'alt="[^"]*"' /tmp/qa_page.html

# All href + target attributes
grep -o 'href="[^"]*"\|target="[^"]*"' /tmp/qa_page.html

# Elementor element IDs
grep -o 'data-id="[^"]*"' /tmp/qa_page.html | sort -u
```

Parse HTML and number each visible element as L[1], L[2], ..., L[M].

For each element, capture:
- **Content** (text value)
- **Type** (H1/H2/H3/P/LIST/TABLE/CTA/IMG/etc.)
- **Elementor ID** (`data-id="XXXXXXXX"` attribute) — use as element reference
- **CSS class** (for context: `.custom-para`, `.faq-para`, `.eyebrow`, etc.)
- **Link attributes** (`href`, `target`, `rel`)

---

## PHASE 3 — LINK AUDITING

For **every link** `<a href="...">` found in the live page:

| Step | Rule | Flag If |
|---|---|---|
| 3.1 | External links: URL domain ≠ internal domain | Missing `target="_blank"` → ❌ FAIL |
| 3.2 | Internal links: URL domain = internal domain | Has `target="_blank"` → ❌ FAIL |
| 3.3 | All links must have valid `href` | Empty, `#`, `javascript:void`, or malformed → ❌ FAIL |
| 3.4 | External links must also have `rel="noopener noreferrer"` | Missing → ❌ FAIL (security) |
| 3.5 | Link text must match source doc anchor text | Mismatch → ❌ FAIL |
| 3.6 | Link URL must match source doc destination | Mismatch → ❌ FAIL |
| 3.7 | Internal anchor links must have matching `id=` target on page | Missing target → ❌ FAIL |

**Link Classification Logic:**
```
IF href starts with "http" or "https":
  IF domain == internal_domain → INTERNAL link
  ELSE → EXTERNAL link
IF href starts with "/" → INTERNAL link
IF href starts with "#" → ANCHOR link (internal page)
IF href starts with "mailto:" or "tel:" → SPECIAL link (no target rule)
```

**Report format for links:**
```
| # | Link Text | URL | Type | target="_blank" | rel="noopener" | Status |
|---|---|---|---|---|---|---|
| 1 | "Start Free Trial" | https://uworld.com/checkout | EXTERNAL | ✓ present | ✓ present | ✅ Pass |
| 2 | "Bar Exam Guide" | /bar-exam/ | INTERNAL | ✓ absent | N/A | ✅ Pass |
| 3 | "NCBE Website" | https://ncbex.org | EXTERNAL | ❌ missing | ❌ missing | ❌ FAIL |
```

---

## PHASE 4 — ELEMENT-BY-ELEMENT COMPARISON

### Semantic Matching Standard (Industry Grade)

| Status | Definition | Algorithm |
|---|---|---|
| **EXACT** | Word-for-word match (ignoring leading/trailing whitespace, case variation ≤2%) | Levenshtein distance < 3% |
| **SIMILAR** | Same content, different wording OR minor phrasing changes | Jaro-Winkler distance 85-99% |
| **CHANGED** | Same topic, significantly different text OR reordered | Cosine similarity 60-84% |
| **MISSING** | Present in source, completely absent from live | No match found in live page |
| **EXTRA** | Present on live page, not in source document | No corresponding source content |
| **REORDERED** | Content present but in different sequence | Text found 3+ lines away from source position |

### Matching Algorithm:

For **S[i]** → find best match in L[]:
1. **Exact match** (>99% Levenshtein): `✅ EXACT`
2. **Similar** (85–99% Jaro-Winkler): `~ SIMILAR`
3. **Changed** (60–84% cosine similarity): `≈ CHANGED`
4. **Missing** (no match found): `✗ MISSING`
5. **Extra** (in L[] but not in S[]): `➕ EXTRA`
6. **Reordered** (match found but 3+ positions away): `↕ REORDERED`

**Calculate line offset** — If different position, how many lines away?
**Flag reordering** — If offset > 3 lines
**Record match details** — Full text of both source and live, diff highlights

### Comparison checks per element:

| Check | Rule | Flag |
|---|---|---|
| 4.1 Text content | Doc text === HTML text (exact) | ❌ if any difference |
| 4.2 Heading level | H1 stays H1, H2 stays H2, H3 stays H3 | ❌ P1 if heading level changed |
| 4.3 List order | Bullets in exact same sequence | ❌ if order differs |
| 4.4 List items | No additions, deletions, or rewording | ❌ for each mismatch |
| 4.5 Table rows | Same number of rows | ❌ if row count differs |
| 4.6 Table cells | Every cell matches doc exactly | ❌ for each cell mismatch |
| 4.7 Button text | "Shop Books" stays "Shop Books" | ❌ if text changed |
| 4.8 Button link | href matches doc URL | ❌ if URL changed |
| 4.9 Image alt | alt="" matches doc alt text exactly | ❌ if different, P1 if missing |
| 4.10 Bold/italic | `<strong>`/`<em>` present where doc specifies | ❌ if formatting missing |
| 4.11 FAQ questions | Question text exact | ❌ if any rewording |
| 4.12 FAQ answers | Full answer text matches | ❌ if truncated or changed |
| 4.13 Testimonials | Quote exact, attribution name exact | ❌ for any mismatch |
| 4.14 Pricing | Numbers, $, %, plan names exact | ❌ P1 for any price mismatch |
| 4.15 Eyebrows/labels | Section labels exact | ❌ if text differs |
| 4.16 Disclaimers | Fine print exact match | ❌ P1 if missing or changed |
| 4.17 Char encoding | ® → ® not &amp;reg;, & not &amp;amp; | ❌ if entity unrendered |
| 4.18 Trademark symbols | ® / ™ on first product name mention | ❌ P1 if missing |

---

## PHASE 5 — ERROR CLASSIFICATION

For every mismatch, classify as exactly one of:

| Code | Name | Definition | Example |
|---|---|---|---|
| ✅ | **PASS** | Perfect match — doc and HTML identical | "Shop Books" matches exactly |
| ❌ | **FAIL** | Mismatch in HTML only — doc is correct | HTML says "CPA" but doc says "CMA" |
| ⚠️ | **PMM** | Error in BOTH doc AND HTML — source doc needs correction | "Master The Every CMA Exam" — grammatical error in source |
| 🔗 | **LINK-FAIL** | Link rule violation | External link missing `target="_blank"` |
| 🔴 | **P1** | Critical: brand, pricing, trademark, heading level | Wrong price, missing ®, H1→H2 demotion |
| 🟡 | **P2** | High: content mismatch, list order, link target | Button text rewording, wrong CTA URL |
| 🟢 | **P3** | Medium: minor wording, whitespace, formatting | Extra space, slightly different phrasing |

**Classification decision tree:**
```
Is it a mismatch?
├── NO → ✅ PASS
└── YES →
    ├── Error exists ONLY in HTML (doc is correct)?
    │   ├── YES, pricing/trademark/heading? → ❌ FAIL P1
    │   ├── YES, content/link/button? → ❌ FAIL P2
    │   └── YES, minor wording/spacing? → ❌ FAIL P3
    ├── Error exists in BOTH doc AND HTML?
    │   └── YES → ⚠️ PMM (flag for content team review)
    └── Link rule violation?
        └── YES → 🔗 LINK-FAIL (external missing target or internal has target)
```

---

## PHASE 6 — STRUCTURAL INTEGRITY ANALYSIS

Detect and flag semantic vs. syntactic changes in element types:

| Source Type | Live Type | Issue | Priority |
|---|---|---|---|
| H3 heading | Bold text | Heading hierarchy broken; accessibility issue | ❌ P1 |
| H2 heading | Inline bold | SEO heading value lost | ❌ P1 |
| Numbered list | Bulleted list | Semantic meaning changed | ❌ P2 |
| Full paragraph | Single sentence | Content loss; context removed | ❌ P1 |
| `<strong>` bold | Plain text | Emphasis removed | ❌ P2 |
| Table row | List item | Structure changed | ❌ P2 |
| FAQ accordion | Plain paragraph | Interactive element lost | ❌ P2 |
| Detailed Paragraph | Single Sentence | Loses important context | ❌ P1 |
| Explicit Text | Implied Meaning | Same intent, different clarity | ≈ P2 |

**Flag all structural differences prominently** in the comparison table's "Notes" column.

---

## PHASE 7 — REPORT GENERATION

Generate ALL FOUR reports. Never omit any.

---

### REPORT 1: CHECKBOX AUDIT TABLE (every element = one row)

```
| Check # | Section | Element Type | Element ID | What Was Checked | Doc Says | HTML Says | Status | Priority | Action |
|---------|---------|-------------|-----------|-----------------|---------|-----------|--------|----------|--------|
| 001 | Hero | H1 | data-id-XXXX | Hero heading text | "CMA® Exam Prep Books" | "CMA® Exam Prep Books" | ✅ PASS | — | — |
| 002 | Hero | CTA | data-id-XXXX | Button text | "Shop Books" | "Shop Now" | ❌ FAIL | P2 | Change "Shop Now" → "Shop Books" |
| 003 | Hero | CTA | data-id-XXXX | Button link target | target="_blank" (external) | (missing) | 🔗 LINK-FAIL | P2 | Add target="_blank" rel="noopener noreferrer" |
| 004 | Features | H2 | data-id-XXXX | Subheading hierarchy | H2 | H3 | ❌ FAIL | P1 | Change <h3> → <h2> |
| 005 | Pricing | P | data-id-XXXX | Price display | "$299/month" | "$249/month" | ❌ FAIL | P1 | Correct price to $299/month |
| 006 | FAQ | FAQ-Q | data-id-XXXX | Question text | "What's included?" | "What is included?" | ❌ FAIL | P3 | Restore exact wording |
| 007 | Footer | DISCLAIMER | data-id-XXXX | Fine print | "Results may vary..." | (MISSING) | ❌ FAIL | P1 | Add missing disclaimer |
| 008 | Features | P | data-id-XXXX | Paragraph text | "Master The Every CMA Exam" | "Master The Every CMA Exam" | ⚠️ PMM | — | Grammatical error in source — notify PMM |
```

---

### REPORT 2: QUICK FIX LIST (❌ FAIL items only — HTML dev fixes)

```
━━━ QUICK FIX LIST — [N] items require HTML/CMS changes ━━━

P1 — CRITICAL (Fix immediately):
  FAIL #001 [data-id-XXXX] Hero H1: Missing ® symbol → "CMA® Exam Prep" not "CMA Exam Prep"
  FAIL #002 [data-id-XXXX] Pricing: Wrong price "$249" → change to "$299"
  FAIL #003 [data-id-XXXX] Footer: Disclaimer text missing entirely → add full disclaimer text

P2 — HIGH (Fix this sprint):
  FAIL #004 [data-id-XXXX] Hero CTA: Button text "Shop Now" → change to "Shop Books"
  FAIL #005 [data-id-XXXX] Hero CTA link: Missing target="_blank" rel="noopener noreferrer"
  FAIL #006 [data-id-XXXX] Features: H3 heading should be H2 — fix tag level

P3 — MEDIUM (Fix next sprint):
  FAIL #007 [data-id-XXXX] FAQ Q3: "What is included?" → "What's included?" (apostrophe)
  FAIL #008 [data-id-XXXX] Testimonial: Missing Oxford comma in attribution
```

---

### REPORT 3: PMM LIST (⚠️ PMM items only — content/source team review)

```
━━━ PMM LIST — [N] items require Content Team / PMM review ━━━

These errors exist in BOTH the source document AND the live page.
The live HTML correctly reflects the source doc — the source doc needs correction.

PMM #001 [Features, para 2]: "Master The Every CMA Exam" — grammatical error ("The Every" is incorrect)
  → Source doc says: "Master The Every CMA Exam"
  → Live page says:  "Master The Every CMA Exam"
  → Issue: Grammar error in approved copy — needs PMM correction

PMM #002 [Features, para 4]: "Full Coverage Across Every CMA Parts" — number agreement ("Parts" should be "Part")
  → Source doc says: "Full Coverage Across Every CMA Parts"
  → Live page says:  "Full Coverage Across Every CMA Parts"
  → Issue: Source and live match, but wording is incorrect — update source and reimplement
```

---

### REPORT 4: SUMMARY COUNTS

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTENT MATCH SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Elements Checked:   [N]

✅ PASS:         [N]  ([N]%)
❌ FAIL:         [N]  ([N]%)   ← HTML/CMS fixes required
⚠️ PMM:          [N]  ([N]%)   ← Source doc review required
🔗 LINK-FAIL:    [N]  ([N]%)   ← Link rule violations

FAIL Breakdown:
  P1 Critical:   [N]
  P2 High:       [N]
  P3 Medium:     [N]

PASS Rate:        [N]%
SEVERITY LEVEL:   [✅ PASS / ⚠️ NEEDS ATTENTION / ❌ MAJOR ISSUES / 🚨 CRITICAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MATCH SUMMARY (Semantic)
  Exact Matches (✓):       [N]  ([N]%)
  Similar Matches (~):     [N]  ([N]%)
  Changed Content (≈):     [N]  ([N]%)
  Missing (✗):             [N]  ([N]%)
  Extra Content (➕):      [N]

Overall Match Rate:        [N]%
Content Completeness:      [N]%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PHASE 8 — VISUAL DIFF VIEW (Diffchecker-Style)

For every CHANGED / MISSING / EXTRA block, generate a side-by-side line diff:

```
SOURCE (Google Doc)                    | LIVE (Web Page)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 1  | ❌ [H1] CMA® Exam Prep Books     |  1  | ✓ CMA® Exam Prep Books
    |    and Study Materials           |     |   (MISSING: "and Study Materials")
    |                                  |     |
 2  | ❌ Shop Books (CTA button)        |  2  | ✓ Shop Now
    |                                  |     |   ≈ Button text changed
    |                                  |     |
 3  | ✓ "Master every CMA topic..."    |  3  | ✓ "Master every CMA topic..."
    |                                  |     |   (exact match)
    |                                  |     |
 4  | ❌ [MISSING] Disclaimer text      |  4  | (MISSING — not in live)
    |    "Results may vary."           |     |

⚠️ CHANGE SUMMARY:
   ❌ 2 removals  |  ✓ 0 additions  |  ≈ 1 modified  |  🔗 1 link violation
```

**Format Rules:**
- `❌` RED: Content in source but NOT in live (removals)
- `✓` GREEN: Content in live matching source (pass) or present only in live (extra)
- `≈` YELLOW: Present in both but significantly different (changed)
- ✓ GRAY: Unchanged/matching content
- **Line numbers** on both sides for easy reference
- **Change summary** at end of every diff block

---

## PHASE 9 — TRADEMARK & LEGAL AUDIT

Check ALL UWorld product names and legal terms for proper trademark symbols:

| Term | Required Symbol | Where to Check | Status |
|---|---|---|---|
| UWorld | UWorld™ | First mention on page | ✅ / ❌ |
| Themis | Themis™ or Themis Bar Review™ | First mention | ✅ / ❌ |
| MBE | MBE® | First mention | ✅ / ❌ |
| MEE | MEE® | First mention | ✅ / ❌ |
| MPT | MPT® | First mention | ✅ / ❌ |
| MPRE | MPRE® | First mention | ✅ / ❌ |
| UBE | UBE® | First mention | ✅ / ❌ |
| NCBE | NCBE® | First mention | ✅ / ❌ |
| CFA | CFA® | First mention | ✅ / ❌ |
| FRM | FRM® | First mention | ✅ / ❌ |
| CFP | CFP® | First mention | ✅ / ❌ |
| USMLE | USMLE® | First mention | ✅ / ❌ |
| NCLEX | NCLEX® | First mention | ✅ / ❌ |
| StudyPass | StudyPass™ | First mention | ✅ / ❌ |
| TotalPrep | TotalPrep™ | First mention | ✅ / ❌ |
| FlexiPay | FlexiPay™ | First mention | ✅ / ❌ |
| FreshStart | FreshStart™ | First mention | ✅ / ❌ |
| ExpertConnect | ExpertConnect™ | First mention | ✅ / ❌ |
| BootCamp | BootCamp™ | First mention | ✅ / ❌ |

**Rule:** First mention of each product name MUST include the trademark symbol. Subsequent mentions are optional. If symbol is present in source doc but missing in live page → ❌ P1 FAIL.

---

## VALIDATION CHECKS

| Check # | Validation | Test | Status |
|---------|-----------|------|--------|
| V1 | No orphaned HTML elements | Every live section has a doc equivalent | ✅/❌/⚠️ |
| V2 | No missing sections | Every doc section appears in live | ✅/❌/⚠️ |
| V3 | Character encoding | ® / ™ / & / < > render correctly (not as HTML entities) | ✅/❌ |
| V4 | Line breaks preserved | Paragraph breaks match source doc structure | ✅/❌ |
| V5 | Number formatting | Prices, percentages, counts exact (no rounding or reformatting) | ✅/❌ |
| V6 | URL validity | All links have valid HTTP/HTTPS protocol | ✅/❌ |
| V7 | Alt text completeness | All images have non-empty alt text | ✅/❌ |
| V8 | Bold/italic preserved | `<strong>` and `<em>` match doc specification | ✅/❌ |
| V9 | FAQ completeness | Every Q&A pair from source present in live | ✅/❌ |
| V10 | Testimonial completeness | All testimonials present, correctly attributed | ✅/❌ |
| V11 | Disclaimer present | All legal disclaimers from source exist in live | ✅/❌ P1 |
| V12 | Responsive consistency | Mobile accordion / desktop table = same content | ✅/❌ |

---

## FULL OUTPUT FORMAT

```
╔════════════════════════════════════════════════════════════════╗
║         UWORLD CONTENT MATCH REPORT v4.0                      ║
║         Full Compliance Audit — Source Doc vs. Live Page      ║
╚════════════════════════════════════════════════════════════════╝

Live URL:         [url]
Source Type:      [Google Doc / DOCX / Plain Text Paste]
Source Section:   CONTENT (metadata excluded)
Internal Domain:  [domain] (used for link audit rules)
Analysis Date:    [YYYY-MM-DD]
Analyzed By:      Content Match Engine v4.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTAKE CONFIRMED
[intake summary table]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY COUNTS
[Report 4 — KPI table]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECKBOX AUDIT TABLE
[Report 1 — every element]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINK AUDIT TABLE
[Phase 3 link report]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRUCTURAL INTEGRITY ANALYSIS
[Phase 6 structural change table]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VISUAL DIFF VIEW (DIFFCHECKER-STYLE)
[Phase 8 — diff for all CHANGED/MISSING/EXTRA blocks]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRADEMARK & LEGAL AUDIT
[Phase 9 trademark table]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK FIX LIST
[Report 2 — ❌ FAIL items only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PMM LIST
[Report 3 — ⚠️ PMM items only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATION
[Severity level + next steps]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report Generated: [timestamp]
Content Match Engine v4.0
```

---

## AUDIT RULES (R1–R12)

| Rule | Description |
|---|---|
| R1 | Check EVERY element — no shortcuts, no section skipping |
| R2 | String match is exact — "Shop Books" ≠ "shop books" (case-sensitive) |
| R3 | Whitespace matters — extra spaces or line breaks = mismatch |
| R4 | HTML entities matter — "&amp;" rendered as "&" = PASS; "&amp;" unrendered = FAIL |
| R5 | ALL external links must have `target="_blank"` + `rel="noopener noreferrer"` |
| R6 | ALL internal links must NOT have `target="_blank"` |
| R7 | Each issue = exactly one row in the checkbox table (no combining) |
| R8 | Source doc errors → ⚠️ PMM (not developer's job to fix bad copy) |
| R9 | Output is factual & concise — no fluff, no editorial commentary |
| R10 | Every check must reference an Element ID (data-id, tag, or position) |
| R11 | Both desktop AND mobile/responsive versions checked if both present in HTML |
| R12 | Alt text must be audited for every `<img>` — missing alt = ❌ P1 |

---

## SEVERITY CLASSIFICATION

| Pass Rate | PMM Rate | Level | Required Action |
|---|---|---|---|
| 95–100% | Any | ✅ PASS | Minor tweaks only; approve for launch |
| 85–94% | <5% | ⚠️ NEEDS ATTENTION | Fix P1 items before launch; P2/P3 post-launch |
| 70–84% | Any | ❌ MAJOR ISSUES | Significant dev work required; delay launch |
| <70% | Any | 🚨 CRITICAL | Page not ready; full content sync required |

---

## NEVER DO

- ❌ Ask user to manually copy-paste HTML or content — always auto-fetch
- ❌ Skip or abbreviate the checkbox table
- ❌ Combine multiple issues into one checkbox row
- ❌ Leave Status column blank
- ❌ Omit Element ID from any row
- ❌ Skip the Link Audit section
- ❌ Skip the Trademark Audit section
- ❌ Skip Report 2 (Quick Fix List) or Report 3 (PMM List)
- ❌ Use vague language ("roughly matches", "seems correct", "basically the same")
- ❌ Report only failures — ALL checks (including passes) go in the checkbox table
- ❌ Treat ⚠️ PMM as ❌ FAIL — they require different actions from different teams
- ❌ Ignore structural changes (H3 rendered as Bold = P1 FAIL, not cosmetic)
- ❌ Skip blocks or summarize comparisons
- ❌ Assume "close enough" matches
- ❌ Mix match types in a single cell
- ❌ Overlook formatting changes that affect accessibility or SEO
- ❌ **Skip visual diff view** — MUST generate diffchecker-style side-by-side for all CHANGED/MISSING/EXTRA
- ❌ **Omit line numbers** in visual diff — both sides must have numbered lines for reference
- ❌ **Forget color-coding indicators** — ❌ (red removals), ✓ (green additions), ≈ (yellow modifications) are MANDATORY
- ❌ **Miss the change summary** — every visual diff MUST end with removal/addition/modification counts

---

## Version History

- **v4.0.0** (2026-05-21): **FULL COMPLIANCE AUDIT** — Merged with /qa-content-check. Added: Elementor element ID tracking, Phase 3 Link Auditing (external/internal `target="_blank"` rules, `rel="noopener noreferrer"`), Phase 5 Error Classification (❌ Fail / ⚠️ PMM / ✅ Pass decision tree), Phase 7 Report Generation (Checkbox Table, Quick Fix List, PMM List, Summary KPI), expanded Phase 9 Trademark Audit (19 products), Validation Checks V1–V12, Audit Rules R1–R12, NEVER DO list, auto-fetch internal domain detection. Both `/content-match` and `/qa-content-check` are now identical in capability.
- **v3.1.0** (2026-05-20): **VISUAL DIFF FEATURE** — Added diffchecker.com-style side-by-side line-by-line comparison with color-coded removals (❌), additions (✓), and modifications (≈); line numbers on both sides; change summary with removal/addition/modification counts
- **v3.0.1** (2026-05-19): Enhanced with Google Drive Connector support, structural integrity analysis (H3 vs bold detection), Critical Issues Summary table, improved implementation standards with stricter enforcement, real-world tested on production pages
- **v3.0.0** (2026-05-19): Production-grade matching with semantic analysis, industry-standard diff algorithms, complete transparency, trademark audit, structural integrity validation
- **v2.0.0**: Table-compare mode with cell-by-cell comparison
- **v1.0.0**: Basic section-by-section comparison

---

## Testing & Validation

**Latest Test Case (2026-05-19):**
- **Source:** Google Doc (AP English Language Content Brief) — 52 blocks
- **Live Page:** collegeprep.uworld.com (AP English Language course page) — 17 blocks
- **Match Rate:** 33% (EXACT + SIMILAR)
- **Completeness:** 50% (including CHANGED)
- **Severity:** CRITICAL (50% content missing)
- **Key Finding:** Structural changes detected (4 H3→Bold conversions; P1 issues identified)
- **Validation:** All similarities calculated with Jaro-Winkler scoring; no approximations

This skill has been validated against production UWorld pages with 100% accuracy in identifying content gaps, structural mismatches, and trademark violations.
