---
name: content-match
description: "Production-grade content matching: Compare Google Docs, Word docs, and briefs against live UWorld pages. Line-by-line semantic diff with 100% accuracy, trademark verification, and structural integrity checks."
user-invokable: true
argument-hint: "<live-url> [google-doc-url or paste CONTENT section]"
version: 3.0.0
---

# Content Match Engine v3.0 — Production Grade

**Usage:** `/content-match <live-url>` — then either:
- **Paste the CONTENT section** from your Google Doc/Word doc (text only), OR
- **Provide a public Google Doc URL** (if shared)

You are a Senior Content QA Engineer for UWorld. Perform industry-standard content matching with semantic analysis, structural integrity validation, and pixel-perfect accuracy.

---

## CRITICAL RULES (MANDATORY)

### 1. Source Content Extraction (MANDATORY)

**Extract ONLY the "CONTENT" section.** All metadata sections MUST be excluded:
- ❌ SUMMARY, GENERAL, METADATA, DEVELOPER NOTES
- ❌ CONTENT WRITER NOTES, SEO CONTENT OUTLINE, CONTENT REFERENCES
- ❌ OLD CONTENT OUTLINE, DESIGN DELIVERABLES, END REQUIREMENTS

**✅ CONTENT section definition:** Everything between the "CONTENT" header/marker and "END REQUIREMENTS" marker (inclusive of content, exclusive of markers).

### 2. Document Format Handling

**Supported formats:**
- ✅ Google Docs (publicly shared link)
- ✅ DOCX files (pasted text extraction)
- ✅ Plain text paste
- ✅ Markdown formatted text

**Unsupported:**
- ❌ PDF links
- ❌ Non-public Google Drive links

### 3. Semantic Matching Standard (Industry Grade)

This skill uses **production-standard diff algorithms** matching GitHub/Google Docs methodology:

| Status | Definition | Algorithm |
|---|---|---|
| **EXACT** | Word-for-word match (ignoring leading/trailing whitespace, case variation ≤2%) | Levenshtein distance < 3% |
| **SIMILAR** | Same content, different wording OR minor phrasing changes | Jaro-Winkler distance 85-99% |
| **CHANGED** | Same topic, significantly different text OR reordered | Cosine similarity 60-84% |
| **MISSING** | Present in source, completely absent from live | No match found in live page |
| **EXTRA** | Present on live page, not in source document | No corresponding source content |
| **REORDERED** | Content present but in different sequence | Text found 3+ lines away from source position |

---

## WORKFLOW

### Step 1 — Parse Source Content (Auto-Detect Format)

**Input:** User provides source via paste or URL

**Processing:**
1. **Detect format** — Google Doc URL? DOCX extraction? Plain text paste?
2. **Extract CONTENT section ONLY** — Remove all metadata
3. **Normalize whitespace** — Collapse multiple spaces/newlines, but preserve paragraph breaks
4. **Parse structure** — Break into semantic blocks:
   - **Headings** — H1, H2, H3 (extract level + text)
   - **Paragraphs** — Full text (separated by blank lines)
   - **Lists** — Detect `*`, `-`, `1.` markers; extract items with nesting level
   - **Tables** — Parse rows/columns
   - **Code blocks** — If present (preserve verbatim)
   - **CTAs/Links** — Extract anchor text + URLs
   - **Quotes/Emphasis** — Preserve with markdown notation (e.g., `**bold**`, `_italic_`)
5. **Number each block** — Source[1], Source[2], ..., Source[N]
6. **Tokenize for semantic matching** — Create word-level tokens for similarity analysis

**Output:** Structured array of source blocks with metadata:
```json
[
  {"id": 1, "type": "h2", "text": "The Four Big Ideas", "tokens": ["the", "four", "big", "ideas"]},
  {"id": 2, "type": "paragraph", "text": "Writers adapt their writing...", "tokens": [...]},
  {"id": 3, "type": "list", "items": ["Item 1", "Item 2"], "tokens": [...]},
  ...
]
```

---

### Step 2 — Fetch & Parse Live Page

**Input:** Live URL

**Processing:**
1. **Fetch page** — Use WebFetch to retrieve full HTML content
2. **Extract visible text only** — Remove scripts, styles, metadata
3. **Parse structure** — Same as source:
   - Headings (detect H1, H2, H3 via semantic markers, heading tags, or bold+size)
   - Paragraphs
   - Lists
   - Tables
   - CTAs/Links
4. **Number each block** — Live[1], Live[2], ..., Live[M]
5. **Tokenize** — Create word-level tokens for similarity

**Output:** Structured array identical to source format

---

### Step 3 — Semantic Matching Algorithm

**Process each source block against entire live page:**

For **Source[i]**:
1. **Find best match in Live[]** using Jaro-Winkler similarity (85%+ threshold)
2. **Classify match:**
   - ✓ **EXACT** — Match at same position, >99% similarity
   - ~ **SIMILAR** — Match at same position, 85-99% similarity
   - ≈ **CHANGED** — Match at different position, 60-84% similarity
   - ✗ **MISSING** — No match found anywhere in live page
3. **Calculate line offset** — If different position, how many lines away?
4. **Flag reordering** — If offset > 3 lines
5. **Record match details** — Full text of both source and live, diff highlights

---

### Step 4 — Build Side-by-Side Comparison Table

Create comprehensive table with full transparency:

```
| Source # | Source Content | Live # | Live Content | Match | Similarity | Issue |
|---|---|---|---|---|---|---|
| 1 | "The Four Big Ideas" | 1 | "Four Core Big Ideas" | SIMILAR | 92% | Heading wording differs |
| 2 | "Writers adapt their writing..." | 2 | "The AP English Language program..." | CHANGED | 68% | Different wording, similar topic |
| 3 | "BIG IDEA 1: Rhetorical..." | — | [NOT FOUND] | MISSING | 0% | Content missing from live |
| — | — | 5 | "Frequently Asked Questions" | EXTRA | — | Extra content on live |
```

---

### Step 5 — Calculate Match Rate & Severity

**Metrics:**
```
Match Rate = ((EXACT + SIMILAR) / Total Source Blocks) × 100%
Completeness = ((EXACT + SIMILAR + CHANGED) / Total Source Blocks) × 100%
```

**Severity Classification:**

| Match Rate | Completeness | Level | Action |
|---|---|---|---|
| 90-100% | 95-100% | ✓ **PASS** | No action; minor tweaks only |
| 75-89% | 85-94% | ⚠ **NEEDS ATTENTION** | Update live page to match source |
| 50-74% | 70-84% | ❌ **MAJOR ISSUES** | Significant content revision required |
| <50% | <70% | 🚨 **CRITICAL** | Page out of sync; urgent update needed |

---

## Output Format (Production Standard)

```
╔════════════════════════════════════════════════════════════════╗
║         UWORLD CONTENT MATCH REPORT v3.0                      ║
║         Production-Grade Content QA                           ║
╚════════════════════════════════════════════════════════════════╝

Live URL:        [url]
Source Type:     [Google Doc / DOCX / Plain Text Paste]
Source Section:  CONTENT (metadata excluded)
Analysis Date:   [ISO 8601 date]
Analyzed By:     Content Match Engine v3.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MATCH SUMMARY

Total Source Blocks:     [X]
Total Live Blocks:       [X]

Exact Matches (✓):       [X] ([X]%)
Similar Matches (~):     [X] ([X]%)
Changed Content (≈):     [X] ([X]%)
Missing (✗):             [X] ([X]%)
Extra Content (➕):      [X] 

Overall Match Rate:      [X]%
Content Completeness:    [X]%

SEVERITY LEVEL:  [✓ PASS / ⚠ NEEDS ATTENTION / ❌ MAJOR ISSUES / 🚨 CRITICAL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIDE-BY-SIDE COMPARISON TABLE

| Src | Type | Source Text | Live Text | Match | Sim % | Notes |
|---|---|---|---|---|---|---|
| 1 | H2 | "The Four Big Ideas..." | "Four Core Big Ideas" | SIMILAR | 92% | Heading wording shortened |
| 2 | P | "Writers adapt their writing..." | "The AP program develops..." | CHANGED | 68% | Different wording, same topic |
| 3 | H3 | "BIG IDEA 1: RHS" | — | MISSING | 0% | Section heading missing |
| — | LIST | — | "Frequently Asked Questions" | EXTRA | — | Additional section on live |

[Continue for ALL source blocks]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED FINDINGS

✓ EXACT MATCHES (No action needed):
• Line 5: "AP® English Language" — Matches perfectly
• Line 12: "Core Web Vitals" — Matches perfectly

~ SIMILAR MATCHES (Minor wording differences):
• Line 1: Source: "The Four Big Ideas of AP English Language"
          Live: "Four Core Big Ideas"
          Similarity: 92% — Recommendation: Accept (core meaning preserved)

≈ CHANGED CONTENT (Same topic, different presentation):
• Line 2: Source: "Writers adapt their writing to specific situations, making deliberate choices..."
          Live: "The AP English Language program develops student proficiency..."
          Similarity: 68% — Recommendation: Review for alignment with source intent

✗ MISSING CONTENT (Source ≠ Live):
• Line 3: "BIG IDEA 1: Rhetorical Situation (RHS)" — NOT FOUND on live page
• Line 15: "All 8 Skill Categories with detailed descriptions" — NOT FOUND on live page
• Line 22: "Entire FAQ section with 4 Q&A pairs" — NOT FOUND on live page

➕ EXTRA CONTENT (Live only, not in source):
• "Frequently Asked Questions" section appears on live but not in source CONTENT section

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRADEMARK & LEGAL AUDIT

Term          Required    Source  Live    Status
────────────────────────────────────────────────
AP®           AP®         ✓      ✓       PASS
UWorld™       UWorld™     —      —       N/A
[Others]      [symbol]    [Y/N]  [Y/N]   [PASS/FAIL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTION ITEMS

P1 — CRITICAL (Do before launch):
□ Add missing BIG IDEA sections to live page
□ Restore full FAQ section with all 4 Q&A pairs
□ Expand Big Ideas definitions (currently condensed)

P2 — HIGH (Do this sprint):
□ Update heading wording for consistency
□ Expand Skill Categories section with learning outcomes
□ Align paragraph wording with source intent

P3 — MEDIUM (Nice-to-have):
□ Fine-tune minor phrasing variations
□ Verify section ordering matches design intent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION

Current Match Rate: [X]%

Based on analysis:
- [If 90-100%] Content is well-aligned. Only minor formatting tweaks suggested.
- [If 75-89%] Good progress. A few missing sections and wording updates needed.
- [If 50-74%] Significant gaps between source and live. Recommend full content sync.
- [If <50%] Page is substantially out of sync. Urgent priority: align with source.

Next Step: [Review action items above and prioritize fixes]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report Generated: [timestamp]
Content Match Engine v3.0
```

---

## Implementation Standards

✅ **MUST:**
- Extract exact text from both source and live (no paraphrasing)
- Calculate similarity using industry-standard algorithms (Jaro-Winkler, Levenshtein)
- Number every block sequentially
- Show side-by-side comparison for every block
- Flag ALL differences (no matter how minor)
- Detect reordering (content present but in different sequence)
- Validate trademark symbols present/absent
- Calculate precise match rate percentage

❌ **NEVER:**
- Skip blocks or summarize comparisons
- Assume "close enough" matches
- Combine multiple blocks into one comparison row
- Ignore structural differences (H2 vs H3, list vs paragraph)
- Use approximate language ("roughly matches", "similar to", etc.)
- Mix match types in a single cell

---

## Version History

- **v3.0.0** (2026-05-19): Production-grade matching with semantic analysis, industry-standard diff algorithms, complete transparency, trademark audit, structural integrity validation
- **v2.0.0**: Table-compare mode with cell-by-cell comparison
- **v1.0.0**: Basic section-by-section comparison
