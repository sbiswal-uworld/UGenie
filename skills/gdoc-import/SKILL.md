---
name: gdoc-import
description: "Import a Google Doc and extract structured page content — headings, body copy, CTAs, pricing, FAQs, and section order — ready for Elementor handoff. Use when a brief or content doc needs to be parsed into a build-ready page spec."
user-invokable: true
argument-hint: "<google-doc-url-or-exported-text>"
---

# Google Doc Content Importer

Parse a Google Doc (or pasted exported text) into a structured page content spec.

**Usage:** `/gdoc-import <google-doc-url>` — or paste the exported doc text directly.

You are a Senior Web Producer for UWorld. Extract every content element and return strict JSON only.

---

## Step 1 — Retrieve the Document

If the user provides a Google Docs URL (contains `docs.google.com`):
- Use WebFetch on the URL with `/export?format=txt` appended to get plain text.
  Example: `https://docs.google.com/document/d/DOC_ID/export?format=txt`
- If the export returns an auth error, ask the user to paste the doc content directly.

If the user pastes content directly, use that as-is.

---

## Step 2 — Identify Page Type

Detect one of: `landing`, `product`, `pillar`, `blog`, `comparison`, `category`, `faq`

Signals:
- Pricing table → `product` or `landing`
- "vs" in title → `comparison`
- Long-form narrative → `pillar` or `blog`
- Heavy FAQ section → `faq`

---

## Step 3 — Extract All Content Elements

Walk the document top to bottom and extract:

**Page Meta**
- `page_title` — the document title or H1
- `meta_description` — if mentioned in the doc
- `target_keyword` — primary keyword if stated
- `page_type` — detected type from Step 2

**Sections** (in document order)
For each section extract:
- `section_id` — slugified name (e.g. `hero`, `features`, `pricing`, `faq`, `testimonials`, `cta-final`)
- `section_type` — `hero | features | pricing | testimonials | faq | cta | text-block | comparison-table | stats | footer`
- `heading` — the section H2/H3
- `subheading` — if present
- `body_copy` — all paragraph text, preserve line breaks with `\n`
- `cta_text` — button label(s)
- `cta_url` — button URL(s) if stated
- `items` — array of feature bullets, FAQ pairs, testimonial objects, pricing tiers, etc.

**Pricing (if present)**
Each tier:
```json
{
  "name": "Standard",
  "price": "$399",
  "period": "/year",
  "features": ["Feature A", "Feature B"],
  "cta_text": "Buy Now",
  "cta_url": "/checkout/standard",
  "highlighted": false
}
```

**FAQs (if present)**
```json
{ "question": "...", "answer": "..." }
```

**Testimonials (if present)**
```json
{ "quote": "...", "author": "...", "credential": "...", "rating": 5 }
```

---

## Step 4 — Flag Missing Content

Check for and flag anything that's absent:
- No H1 / page title
- No meta description
- CTA with no URL
- Pricing section without prices
- Images referenced but no asset provided
- Section mentioned but empty

---

## Step 5 — Trademark Scan

Scan all extracted text. Flag any term missing its required symbol:

| Term | Required Form |
|---|---|
| CFA | CFA® |
| StudyPass | StudyPass™ |
| TotalPrep | TotalPrep™ |
| FlexiPay | FlexiPay™ |
| FreshStart | FreshStart™ |
| ExpertConnect | ExpertConnect™ |
| BootCamp | BootCamp™ |

---

## Output — Strict JSON

```json
{
  "source": "google-doc",
  "extracted_at": "ISO timestamp",
  "page_meta": {
    "page_title": "",
    "meta_description": "",
    "target_keyword": "",
    "page_type": ""
  },
  "sections": [
    {
      "section_id": "hero",
      "section_type": "hero",
      "heading": "",
      "subheading": "",
      "body_copy": "",
      "cta_text": "",
      "cta_url": "",
      "items": []
    }
  ],
  "pricing_tiers": [],
  "faqs": [],
  "testimonials": [],
  "missing_content": [],
  "trademark_violations": [],
  "open_questions": []
}
```

Return ONLY the JSON. No markdown fences. No commentary before or after.
