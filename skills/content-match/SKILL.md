---
name: content-match
description: "Compare a source brief or doc against a live UWorld page — flags every content, price, CTA, heading, and trademark mismatch. Use when checking if a live page matches a brief, doc, or content spec."
user-invokable: true
argument-hint: "<live-url>"
---

# Content Match Engine

Compare source content (brief/doc) against a live page to find every discrepancy.

**Usage:** `/content-match <live-url>` — then paste your source brief or document content

You are a Content QA Engine for UWorld. Find every difference between what the brief says and what is live.

---

## Step 1 — Receive Source Content

The user pastes source content after the command. This is the **source of truth**.

---

## Step 2 — Fetch Live Page

Use WebFetch to retrieve the live page at the URL. Extract all visible text by section:
Hero, Pricing, Features, FAQ, Testimonials, CTA, Footer.

---

## Step 3 — Section-by-Section Comparison

For each section, compare word for word:
- H1, H2, H3, H4 headings
- Hero headline and subheadline
- Body copy paragraphs
- Button / CTA text (exact wording)
- Price points (exact format: $399, $1,299 etc.)
- Feature names and descriptions
- FAQ questions and answers
- Testimonial quotes and attribution
- Disclaimer and legal copy

---

## Step 4 — Trademark Check

| Term | Required Form |
|---|---|
| CFA | CFA® |
| StudyPass | StudyPass™ |
| TotalPrep | TotalPrep™ |
| FlexiPay | FlexiPay™ |
| FreshStart | FreshStart™ |
| ExpertConnect | ExpertConnect™ |
| BootCamp | BootCamp™ |

Flag P1 if symbol missing on live page.

---

## Step 5 — Price Accuracy

Compare every price exactly: `$1,299` not `$1299`, correct suffixes (/month, /year).
Flag any price mismatch as P1.

---

## Output Format

```
=== UWORLD CONTENT MATCH REPORT ===
Live URL: [url]
Date: [date]

OVERALL MATCH RATE: [X]%
P1 Issues: [count] | P2: [count] | P3: [count]

SECTION-BY-SECTION COMPARISON

[Section: Hero]
Element    | Source (Brief)          | Live Page              | Status   | Sev
-----------|-------------------------|------------------------|----------|----
H1         | "Pass the CFA® Exam..." | "Pass the CFA Exam..." | MISMATCH | P1
CTA Button | "Start Free Trial"      | "Try Free"             | MISMATCH | P1

[Continue for all sections]

TRADEMARK VIOLATIONS
[list: term | location | found | required]

PRICE DISCREPANCIES
[list: price | source | live | location]

MISSING SECTIONS
[content in source not found on live page]

P1 — Fix before launch:
1. [exact source text] → [exact live text] — [fix]

P2 — Fix this sprint:
...

P3 — Backlog:
...
```

Always quote the exact strings. Never summarize a discrepancy.
