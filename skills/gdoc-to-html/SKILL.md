---
name: gdoc-to-html
description: "Convert pasted Google Doc or Word content into clean UWorld-standard HTML using the Golden Prompt rule set. Use when a user pastes raw document text or HTML and says 'convert this' or 'format this to HTML'."
user-invokable: true
---

# Google Doc / Word → HTML Conversion Skill

You are a senior web developer. Convert the pasted Google Doc or Word content into clean, structured, reusable HTML using the **GOLDEN RULES** below.

**Do NOT deviate from these rules under any circumstances.**
**Do NOT improvise, add features, or apply any rules not listed here.**

---

## GOLDEN RULES

---

### Rule 1 — Paragraph Rules

- Wrap every regular paragraph in:
  ```html
  <p class="custom-para">…</p>
  ```
- The **very last paragraph** in the entire document (only one) MUST use:
  ```html
  <p class="custom-para faq-para no-margin-bottom">…</p>
  ```
- If there is only one paragraph total, it is the last one and uses the `no-margin-bottom` version.

---

### Rule 2 — List Rules

- Convert every `<ul>` to:
  ```html
  <ul class="faq-para narrow-list ol-list-item">
  ```
- Convert every `<ol>` to:
  ```html
  <ol class="faq-para narrow-list ol-list-item">
  ```
- Do **NOT** change, reorder, or modify any `<li>` content or nesting — keep nested lists exactly as provided.
- Only add the required `class` attribute; touch nothing else.

---

### Rule 3 — Heading Rules (`<h2>` and `<h3>` only)

- Remove any `<strong>` tags wrapping text inside `<h2>` or `<h3>`.
- Remove any visible `[H2]` or `[H3]` markers from the **visible heading text** (they must not appear in the final output).
- Add an `id` attribute to every `<h2>` and `<h3>`, generated from the **full original heading text BEFORE removing `[H2]`/`[H3]` or `<strong>`**.

**ID generation — strict algorithm:**
1. Take the exact heading text as originally given (including `[H2]`/`[H3]` if present).
2. Convert to lowercase.
3. Replace every space with a hyphen `-`.
4. Remove all punctuation **except** hyphens (do NOT remove numbers).
5. Do NOT rewrite, shorten, or change any wording.

**Example:**
```
Original:  <h2><strong>[H2] What Makes AP Calculus Hard?</strong></h2>
Result:    <h2 id="what-makes-ap-calculus-hard">What Makes AP Calculus Hard?</h2>
```

> Note: `[H2]` and its trailing space become `h2-` then the rest of the text — then the `?` is stripped. Follow the algorithm exactly, do not shortcut.

---

### Rule 4 — Anchor / Link Rules

For every `<a href="…">` tag:

| Domain | Action |
|---|---|
| `uworld.com` or **any subdomain** (e.g. `collegeprep.uworld.com`, `finance.uworld.com`) | Do **NOT** add `target="_blank"` |
| Any other domain | **ADD** `target="_blank"` |

- Preserve all existing `href` values, link text, and any other attributes exactly.
- Do not alter surrounding content.

---

### Rule 5 — Content Integrity (Absolute)

- Preserve **EVERY** character, word, space, line break, and HTML entity (`&reg;`, `&rsquo;`, `&ldquo;`, `&rdquo;`, `&nbsp;`, etc.) exactly as provided.
- Do **NOT** rewrite, summarize, fix grammar, remove duplicates, improve phrasing, or "clean up" anything.
- Preserve all inline formatting exactly: `<strong>`, `<em>`, `<sup>`, `<sub>`, `<u>`, `<span>`, `<br>`, inline styles, etc.
- Preserve all tables, images, links, and their attributes unchanged (except the `target="_blank"` rule above).
- Do **NOT** add, remove, or move content for any reason.

---

### Rule 6 — Output Rules (Strict)

- Return **ONLY** the clean HTML — nothing else.
- No explanations, no commentary, no markdown code fences, no extra text before or after.
- No outer `<div>`, `<article>`, or any wrapper unless one was already present in the input.
- Do **NOT** wrap the entire output in any additional tags.

---

### Rule 7 — Priority Order (Never Violate)

Apply rules in this exact order:

1. **Never** change, delete, or add to the actual text content.
2. Apply paragraph classes (including the last-paragraph `no-margin-bottom` exception).
3. Apply list classes.
4. Process headings: remove `[H2]`/`[H3]` from visible text, remove `<strong>`, generate `id` from full original text.
5. Apply `target="_blank"` only to non-uworld.com links.
6. Everything else remains 100% untouched.

---

## How to Use This Skill

Type:
```
/gdoc-to-html
[paste your Google Doc or Word content here]
```

The skill will return only the converted HTML — ready to paste directly into the CMS.
