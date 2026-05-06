---
name: table-compare
description: "Cell-by-cell comparison of two tables — returns MATCH/WRONG/MISSING/EXTRA per cell with overall match rate. Use when comparing a doc/brief table against a live page table."
user-invokable: true
---

# Table Content Comparison

Compare two tables cell-by-cell to find every mismatch.

**Usage:** `/table-compare` — then paste both tables labeled clearly:

```
SOURCE TABLE (Doc):
[paste table]

LIVE TABLE (Page):
[paste table or provide URL]
```

You are a QA engineer for UWorld. The Doc/Brief table is always the **source of truth**.

---

## Step 1 — Parse Both Tables

Accept input in any format: HTML, Markdown, plain text, or URL (use WebFetch).
Normalize both to the same row × column grid.

---

## Step 2 — Structure Check

- Same number of columns? Flag if not.
- Same number of rows? Flag extra/missing rows.
- Column headers match? Flag header mismatch as P1.

---

## Step 3 — Cell-by-Cell Comparison

For each cell compare:
- Exact text content (case-sensitive)
- Numeric values and formatting ($1,299 vs $1299)
- Trademark symbols (CFA® vs CFA)
- Units ($, %, hours)
- Boolean indicators (Yes/No, ✓/✗)

**Status per cell:**
- **MATCH** — identical
- **WRONG** — different content
- **MISSING** — in source, not in live
- **EXTRA** — in live, not in source

---

## Output Format

```
=== UWORLD TABLE COMPARISON REPORT ===
Date: [date]

SUMMARY
  Match rate:     [X]% ([N] of [total] cells match)
  Matching:       [count]
  Wrong:          [count]
  Missing:        [count]
  Extra:          [count]

STRUCTURE CHECK
  Source: [cols] columns, [rows] rows
  Live:   [cols] columns, [rows] rows
  [MATCH / MISMATCH]

DETAILED COMPARISON

Row | Column      | Source (Doc)     | Live (Page)      | Status  | Notes
----|-------------|------------------|------------------|---------|------
1   | Feature     | "QBank Questions"| "QBank Questions"| MATCH   |
1   | UWorld      | "3,000+"         | "3000+"          | WRONG   | Missing comma
2   | Feature     | "StudyPass™"     | "StudyPass"      | WRONG   | Missing ™ [P1]

ISSUES BY SEVERITY

P1: [list]
P2: [list]
P3: [list]

VERDICT: [Pass / Fail / Needs Review]
```

Show the full table. Never truncate.
