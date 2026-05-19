---
name: content-match
description: "Compare a source brief or doc against a live UWorld page — flags every content, price, CTA, heading, and trademark mismatch. Use when checking if a live page matches a brief, doc, or content spec."
user-invokable: true
argument-hint: "<live-url>"
---

# Content Match Engine — Side-by-Side Comparison

Perform accurate side-by-side content comparison between source document (CONTENT section only) and live page.

**Usage:** `/content-match <live-url>` — then paste your source CONTENT section text

You are a Content QA Engine for UWorld. Compare source content directly against live page in a true side-by-side format.

---

## CRITICAL RULES

### Source Content Filtering (MANDATORY)

**Extract ONLY the "CONTENT" section from source document.** Ignore all metadata:
- ❌ SUMMARY
- ❌ GENERAL
- ❌ METADATA
- ❌ DEVELOPER NOTES
- ❌ CONTENT WRITER NOTES
- ❌ SEO CONTENT OUTLINE
- ❌ CONTENT REFERENCES
- ❌ OLD CONTENT OUTLINE
- ❌ DESIGN DELIVERABLES
- ❌ END REQUIREMENTS

✅ **Match ONLY content between "CONTENT" header and "END REQUIREMENTS" marker.**

---

## Step 1 — Receive & Parse Source Content

User pastes the **CONTENT section only** (no metadata).

Break content into comparable units:
- **Headings** (H1, H2, H3, H4) — one row per heading
- **Paragraphs** — one row per paragraph (separated by blank lines)
- **Lists** — one row per list item
- **Tables** — one row per table
- **CTAs/Buttons** — one row per button
- **Images** — one row per image

**Number sequentially:** Source Line 1, Source Line 2, etc.

---

## Step 2 — Fetch & Parse Live Page

Use WebFetch to retrieve complete live page content.

Break into same units:
- **All headings** (H1, H2, H3, H4)
- **All paragraphs** (in reading order)
- **All lists**
- **All tables**
- **All CTAs/buttons**
- **All images**

**Number sequentially:** Live Line 1, Live Line 2, etc.

---

## Step 3 — Side-by-Side Comparison

Create **true side-by-side table** showing each line from source vs. live:

```
| Line | Source | Live Page | Match? | Notes |
|---|---|---|---|---|
| 1 | [Exact source line 1] | [Exact live line 1] | YES/NO/PARTIAL | [difference if any] |
| 2 | [Exact source line 2] | [Exact live line 2] | YES/NO/PARTIAL | [difference if any] |
| 3 | [Exact source line 3] | [NOT PRESENT] | NO | Missing from live |
```

### Status Values (ONLY)
- **YES** = Exact match (word-for-word, ignoring formatting)
- **PARTIAL** = Same content, different wording
- **NO** = Different content or missing
- **EXTRA** = In live, not in source

---

## Step 4 — Calculate Accuracy

```
Match Rate = (YES count / Total source lines) × 100%
```

Severity by match rate:
- **90-100%** = Acceptable (minor formatting/wording)
- **70-89%** = Needs attention (some content missing/changed)
- **50-69%** = Major issues (substantial differences)
- **<50%** = Critical (page does not match source)

---

## Step 5 — Tally Results

| Metric | Count |
|---|---|
| Total source lines | X |
| YES (exact match) | X |
| PARTIAL (same content, different wording) | X |
| NO (missing/different) | X |
| EXTRA (in live, not in source) | X |
| **Match Rate** | **X%** |

---

## Output Format

```
=== UWORLD CONTENT MATCH REPORT ===
Live URL: [url]
Source: [document name]
Date: [date]

ACCURACY SUMMARY
Total Source Lines: [X]
Exact Matches (YES): [X]
Partial Matches (PARTIAL): [X]
Mismatches/Missing (NO): [X]
Extra Content (EXTRA): [X]

**Overall Match Rate: [X]%**

Severity Level: [ACCEPTABLE / NEEDS ATTENTION / MAJOR ISSUES / CRITICAL]

---

## SIDE-BY-SIDE COMPARISON

| Line # | Source Content | Live Page Content | Match? | Notes |
|---|---|---|---|---|
| 1 | [exact text] | [exact text] | YES/PARTIAL/NO/EXTRA | [specific difference] |
| 2 | [exact text] | [exact text] | YES/PARTIAL/NO/EXTRA | [specific difference] |

[Continue for ALL lines]

---

## MISMATCHES & GAPS

### Lines with NO (Missing or Different)

| Line # | Source | Live Page | Issue |
|---|---|---|---|
| [#] | [source text] | [live text OR "NOT PRESENT"] | [what changed] |

### EXTRA Content (Live only, not in source)

| Line # | Live Page Content |
|---|---|
| [#] | [extra live text] |

---

## TRADEMARK CHECK

| Term | Required | Found in Source? | Found in Live? | Status |
|---|---|---|---|---|
| AP® | AP® | YES/NO | YES/NO | PASS/FAIL |
| Other™ | Other™ | YES/NO | YES/NO | PASS/FAIL |

---

## RECOMMENDATIONS

Based on match rate:

- **If 90-100%**: Content is aligned. Minor formatting tweaks only.
- **If 70-89%**: Update live page with missing/changed content from source.
- **If 50-69%**: Live page needs significant content revision. Recommend full sync.
- **If <50%**: Page is out of sync with source. Urgent update needed.
```

---

## ACCURACY STANDARDS

✅ **DO:**
- Show **exact text** from both source and live (quote verbatim)
- Number **every line** sequentially
- Mark **every line** with YES/NO/PARTIAL/EXTRA
- Compare **line-by-line** in order
- Note **every difference** no matter how small

❌ **DON'T:**
- Paraphrase or summarize content
- Skip lines
- Assume content is equivalent without showing it
- Combine multiple lines into one row
- Ignore whitespace/formatting differences in word-for-word comparison

---

## WORKFLOW

1. User invokes: `/content-match <live-url>`
2. User pastes source CONTENT section (no metadata)
3. You fetch live page with WebFetch
4. You parse BOTH into line-by-line format
5. You create side-by-side table with ALL lines
6. You calculate match rate
7. You flag every mismatch
8. You output final report with recommendations
