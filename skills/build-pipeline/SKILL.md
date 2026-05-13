---
name: build-pipeline
description: "Full Figma + Google Docs → Elementor page build pipeline. Orchestrates gdoc-import, figma-import, spec normalization, elementor-build, and QA in one command. Use when you have both a Figma mockup and a Google Doc brief and want a complete Elementor page package."
user-invokable: true
argument-hint: "<gdoc-url> <figma-url>"
---

# Full Page Build Pipeline

Orchestrate the complete workflow: Google Doc brief + Figma mockup → normalized spec → Elementor page → QA report.

**Usage:** `/build-pipeline <google-doc-url> <figma-url>`

Alternatively: provide one or both as attachments/pasted content.

You are a Senior Web Producer for UWorld running an automated page build pipeline. Be systematic. Complete every stage before moving to the next.

---

## STAGE 1 — Content Extraction (Google Docs)

Run the full `/gdoc-import` process on the Google Doc URL or pasted content:

1. Fetch or receive the document content
2. Detect page type
3. Extract all sections with heading, body copy, CTAs, pricing, FAQs, testimonials
4. Flag missing content and trademark violations
5. Output: `content_spec` JSON object

Report to user:
```
✓ STAGE 1 COMPLETE — Content Extraction
  Page type: {page_type}
  Sections found: {count}
  Missing items: {count}
  Trademark flags: {count}
```

---

## STAGE 2 — Design Extraction (Figma)

Run the full `/figma-import` process on the Figma URL or attached screenshot:

1. Retrieve file data via Figma API or analyse screenshot
2. Extract design tokens (colors, typography, spacing, borders)
3. Map all sections with layout and component inventory
4. Identify responsive rules
5. Inventory all assets
6. Output: `design_spec` JSON object

Report to user:
```
✓ STAGE 2 COMPLETE — Design Extraction
  Sections found: {count}
  Design tokens extracted: {count}
  Missing assets: {count}
  Open questions: {count}
```

---

## STAGE 3 — Spec Normalization

Merge `content_spec` and `design_spec` into a single `page_spec`:

**Merge rules:**
- For each section in `content_spec.sections`, find the matching section in `design_spec.sections` by `section_type` and `order`
- Attach `design_tokens` and `layout` from design to each content section
- Attach `components` array from design to each content section
- If a content section has no matching design section → flag as `design_missing`
- If a design section has no matching content section → flag as `content_missing`
- Merge `pricing_tiers`, `faqs`, `testimonials` from content with component styles from design
- Set `page_meta` from content, append design token summary

**Output `page_spec`:**

```json
{
  "page_meta": {
    "page_title": "",
    "meta_description": "",
    "target_keyword": "",
    "page_type": "",
    "build_date": ""
  },
  "design_tokens": { ... },
  "sections": [
    {
      "section_id": "",
      "section_type": "",
      "order": 1,
      "heading": "",
      "subheading": "",
      "body_copy": "",
      "cta_text": "",
      "cta_url": "",
      "items": [],
      "layout": "",
      "background": "",
      "components": [],
      "status": "ready | design_missing | content_missing"
    }
  ],
  "pricing_tiers": [],
  "faqs": [],
  "testimonials": [],
  "assets": [],
  "missing_content": [],
  "missing_design": [],
  "trademark_violations": [],
  "open_questions": []
}
```

Report to user:
```
✓ STAGE 3 COMPLETE — Spec Normalization
  Sections matched: {count}
  Design missing: {count} sections
  Content missing: {count} sections
  Ready to build: {count} sections
```

If `open_questions` is non-empty, list them and ask the user:
> "The following items need clarification before building. You can answer now or type SKIP to build with placeholders."

Wait for user response or SKIP before proceeding.

---

## STAGE 4 — Elementor Build

Run the full `/elementor-build both` process on the merged `page_spec`:

1. Generate CSS custom properties from design tokens
2. Build each section's HTML using content + design values
3. Apply responsive CSS
4. Output Elementor widget checklist
5. Output developer handoff notes

**HTML Output filename convention:** `{page_type}-{target_keyword-slugified}-elementor.html`

Report to user:
```
✓ STAGE 4 COMPLETE — Elementor Build
  Sections built: {count}
  HTML file: {filename}
  Sections needing placeholder images: {count}
```

---

## STAGE 5 — QA Pre-Flight

Run automated QA checks before handing off:

**Content QA:**
- [ ] Every section from brief has a matching built section
- [ ] All CTA buttons have text and URL
- [ ] All prices match the brief exactly
- [ ] No Lorem Ipsum placeholder text remains
- [ ] Trademark symbols present (CFA®, StudyPass™, etc.)
- [ ] Meta title and description populated
- [ ] H1 appears exactly once

**Design QA:**
- [ ] All CSS custom properties match extracted design tokens
- [ ] Section order matches Figma layout order
- [ ] Hero background color matches design
- [ ] Button styles match design (color, radius, padding)
- [ ] Mobile responsive rules applied
- [ ] Pricing highlighted tier styled correctly

**Elementor QA:**
- [ ] Widget checklist covers every section
- [ ] No sections marked `design_missing` in built output
- [ ] Developer handoff notes include all missing assets

**Score each category 0–100%.**

---

## STAGE 6 — Final Package

Deliver the complete build package:

```
=== UWORLD PAGE BUILD PACKAGE ===
Page: {page_title}
Type: {page_type}
Target Keyword: {target_keyword}
Build Date: {date}

OVERALL READINESS: {X}%

DELIVERABLES:
1. page_spec.json         — normalized content + design spec
2. {filename}.html        — Elementor preview HTML
3. elementor-checklist    — step-by-step widget build guide
4. developer-handoff      — CSS tokens, fonts, missing assets
5. qa-report              — pre-flight check results

NEXT STEPS:
1. Resolve {count} open questions (listed below)
2. Provide {count} missing assets (listed below)
3. Import HTML into Elementor as a template
4. Follow the Elementor Build Checklist
5. After going live, run: /visual-diff <live-url>
6. After going live, run: /content-match <live-url>
7. After going live, run: /page-audit <live-url>

OPEN QUESTIONS:
{open_questions}

MISSING ASSETS:
{missing_assets}

TRADEMARK VIOLATIONS TO FIX:
{trademark_violations}
```

---

## Error Handling

- If Stage 1 fails (Doc auth error): ask user to paste content directly, continue with Stage 2
- If Stage 2 fails (Figma auth error): ask user to attach screenshot, extract visually
- If a section is `content_missing`: build the section structure with `[CONTENT NEEDED]` placeholders
- If a section is `design_missing`: build using UWorld brand defaults, flag in QA

Never stop the pipeline on a single failure. Always build what you can and flag what's missing.
