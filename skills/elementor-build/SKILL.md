---
name: elementor-build
description: "Generate a production-ready Elementor page from a page spec JSON — outputs section HTML, Elementor widget structure, CSS custom properties, and a developer handoff checklist. Use after gdoc-import and figma-import have produced a combined page spec."
user-invokable: true
argument-hint: "[html|json|both]"
---

# Elementor Page Builder

Generate a complete Elementor-ready page from a combined page spec.

**Usage:** `/elementor-build [html|json|both]` — then paste your page spec JSON (output from `/build-pipeline` or manually combined `/gdoc-import` + `/figma-import` output).

Default output is `both` (HTML preview + Elementor widget checklist).

You are a Senior WordPress/Elementor developer for UWorld. Output production-ready code only.

---

## Step 1 — Parse the Page Spec

Accept JSON with this structure (produced by `/gdoc-import` + `/figma-import` merged):

```json
{
  "page_meta": { ... },
  "design_tokens": { ... },
  "sections": [ { "section_id": "", "section_type": "", "heading": "", "body_copy": "", "components": [], "layout": "" } ],
  "pricing_tiers": [],
  "faqs": [],
  "testimonials": []
}
```

If the spec is missing design tokens, fall back to UWorld brand defaults:
- Primary: `#1B3A6B`
- Accent: `#0066CC`
- Text: `#1A1A1A`
- Font: `DM Sans, sans-serif`
- Section padding: `80px 0`
- Container: `1200px`

---

## Step 2 — Generate CSS Custom Properties

Output a `<style>` block with every design token as a CSS variable:

```css
:root {
  --color-primary: #1B3A6B;
  --color-accent: #0066CC;
  --color-bg: #FFFFFF;
  --color-text: #1A1A1A;
  --color-muted: #6B7280;
  --color-border: #E5E7EB;
  --font-heading: 'DM Sans', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --size-h1: 48px;
  --size-h2: 36px;
  --size-h3: 24px;
  --size-body: 16px;
  --weight-heading: 700;
  --radius-button: 8px;
  --radius-card: 12px;
  --shadow-card: 0 4px 20px rgba(0,0,0,0.08);
  --section-padding: 80px 0;
  --container-width: 1200px;
}
```

---

## Step 3 — Build Each Section

For each section in `sections[]`, generate the HTML block AND the Elementor widget spec.

### Section Type Rules

**hero**
```html
<section class="uw-section uw-hero" style="background: var(--color-hero-bg, var(--color-primary));">
  <div class="uw-container">
    <div class="uw-hero__content">
      <h1 class="uw-hero__heading">{heading}</h1>
      <p class="uw-hero__sub">{subheading}</p>
      <a href="{cta_url}" class="uw-btn uw-btn--primary">{cta_text}</a>
    </div>
  </div>
</section>
```
Elementor: Section → Inner Section → Heading widget + Text Editor widget + Button widget

**features** (2–4 columns)
```html
<section class="uw-section uw-features">
  <div class="uw-container">
    <h2 class="uw-section__heading">{heading}</h2>
    <div class="uw-grid uw-grid--{cols}">
      {items.map → <div class="uw-feature-card">
        <div class="uw-feature-card__icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>}
    </div>
  </div>
</section>
```
Elementor: Section → Icon Box widget (repeat per feature)

**pricing**
```html
<section class="uw-section uw-pricing">
  <div class="uw-container">
    <h2 class="uw-section__heading">{heading}</h2>
    <div class="uw-pricing-grid">
      {pricing_tiers.map → <div class="uw-pricing-card {highlighted ? 'uw-pricing-card--featured' : ''}">
        <div class="uw-pricing-card__name">{name}</div>
        <div class="uw-pricing-card__price">{price}<span>{period}</span></div>
        <ul class="uw-pricing-card__features">
          {features.map → <li>{feature}</li>}
        </ul>
        <a href="{cta_url}" class="uw-btn {highlighted ? 'uw-btn--primary' : 'uw-btn--outline'}">{cta_text}</a>
      </div>}
    </div>
  </div>
</section>
```
Elementor: Price Table widget per tier, OR custom HTML widget for full control

**testimonials**
```html
<section class="uw-section uw-testimonials">
  <div class="uw-container">
    <h2 class="uw-section__heading">{heading}</h2>
    <div class="uw-testimonials-grid">
      {testimonials.map → <div class="uw-testimonial-card">
        <div class="uw-testimonial-card__stars">{"★".repeat(rating)}</div>
        <blockquote class="uw-testimonial-card__quote">"{quote}"</blockquote>
        <cite class="uw-testimonial-card__author">— {author}, {credential}</cite>
      </div>}
    </div>
  </div>
</section>
```
Elementor: Testimonial Carousel widget

**faq**
```html
<section class="uw-section uw-faq">
  <div class="uw-container uw-container--narrow">
    <h2 class="uw-section__heading">{heading}</h2>
    <div class="uw-accordion">
      {faqs.map → <div class="uw-accordion__item">
        <button class="uw-accordion__trigger" aria-expanded="false">{question}</button>
        <div class="uw-accordion__body"><p>{answer}</p></div>
      </div>}
    </div>
  </div>
</section>
```
Elementor: Toggle or Accordion widget

**cta**
```html
<section class="uw-section uw-cta" style="background: var(--color-primary);">
  <div class="uw-container uw-container--centered">
    <h2 class="uw-cta__heading">{heading}</h2>
    <p class="uw-cta__sub">{body_copy}</p>
    <a href="{cta_url}" class="uw-btn uw-btn--white">{cta_text}</a>
  </div>
</section>
```
Elementor: Call to Action widget

**stats**
```html
<section class="uw-section uw-stats">
  <div class="uw-container">
    <div class="uw-stats-row">
      {items.map → <div class="uw-stat">
        <span class="uw-stat__number">{value}</span>
        <span class="uw-stat__label">{label}</span>
      </div>}
    </div>
  </div>
</section>
```
Elementor: Counter widget per stat

---

## Step 4 — Responsive CSS

Append a mobile block for every section:

```css
@media (max-width: 768px) {
  .uw-hero__heading { font-size: calc(var(--size-h1) * 0.6); }
  .uw-grid--3, .uw-grid--4 { grid-template-columns: 1fr; }
  .uw-pricing-grid { grid-template-columns: 1fr; }
  .uw-btn { width: 100%; text-align: center; }
  .uw-section { padding: 48px 20px; }
}
```

---

## Step 5 — Elementor Widget Checklist

Output a numbered checklist mapping each section to its Elementor implementation steps:

```
ELEMENTOR BUILD CHECKLIST
=========================
□ 1. [Hero] Create new Section → set background color #1B3A6B
      Add Inner Section (1 column)
      Add Heading widget → paste H1 text → set color white, size 48px
      Add Text Editor widget → paste subheading
      Add Button widget → label: "Start Free Trial" → link: /start
      Style button: background #0066CC, radius 8px, padding 14px 32px

□ 2. [Features] Create new Section → white background
      Add Heading widget → H2 text → center-align
      Add Inner Section (3 columns)
      Add Icon Box widget to each column → icon, title, description

[continue for every section]
```

---

## Step 6 — Developer Handoff Notes

```
DEVELOPER HANDOFF
=================
Page: {page_title}
Target Keyword: {target_keyword}
Page Type: {page_type}

CSS FILE: Copy all --custom properties into your theme's global CSS or
          Elementor → Site Settings → Custom CSS

FONTS: Add to WordPress → Appearance → Editor → theme.json or
       Elementor → Site Settings → Typography

MISSING BEFORE BUILD:
{missing_content}

TRADEMARK REVIEW REQUIRED:
{trademark_violations}

QA STEPS AFTER BUILD:
1. Run /visual-diff against Figma screenshot
2. Run /content-match against live URL
3. Run /page-audit for SEO + trademark check
```

---

## Output

If mode is `html`: output the full HTML file (DOCTYPE to closing body tag), CSS variables embedded in `<style>` in `<head>`.

If mode is `json`: output the Elementor widget structure as JSON (section → column → widget hierarchy).

If mode is `both` (default): output HTML first, then the ELEMENTOR BUILD CHECKLIST, then DEVELOPER HANDOFF.

No markdown fences. No commentary before or after the output.
