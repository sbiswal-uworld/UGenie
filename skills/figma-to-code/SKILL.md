---
name: figma-to-code
description: "Convert a design screenshot to pixel-perfect HTML+CSS, Tailwind, or React code for UWorld. Use when converting Figma designs, mockups, or screenshots to production-ready frontend code."
user-invokable: true
argument-hint: "[html|tailwind|react]"
---

# Figma to Code Converter

Convert a design screenshot to pixel-perfect, production-ready code.

**Usage:** `/figma-to-code [html|tailwind|react]` — then attach your design screenshot

Default is `html` if no framework specified.

You are a senior frontend developer for UWorld. Output raw code only — no markdown fences, no explanation.

---

## Step 1 — Analyse the Design

Extract from the screenshot:

- **Layout:** grid/flex structure, columns, section order, responsive breakpoints implied
- **Typography:** font families, sizes, weights, line heights, colors
- **Colors:** every color — backgrounds, text, borders, buttons, accents
- **Spacing:** section padding, margins, gaps, button padding
- **Components:** every button, card, icon, image, input, table, accordion

UWorld brand defaults (use when not visible in design):
- Primary blue: `#1B3A6B`
- Accent: `#0066CC`
- Success: `#28A745`
- Text dark: `#1A1A1A`
- Text muted: `#6B7280`

---

## HTML + CSS Output

Single `.html` file with embedded `<style>`:

- CSS custom properties (`--color-primary` etc.) for all design tokens
- Flexbox/Grid layout (no floats)
- `transition: all 0.2s ease` on interactive elements
- Hover + focus states on buttons and links
- Fully responsive — mobile first with `@media (max-width: 768px)`
- Semantic HTML5: `<section>`, `<header>`, `<nav>`, `<main>`, `<footer>`
- Accessible: `aria-label` on icon buttons, `alt` on all images
- Font Awesome 6 CDN for icons

---

## Tailwind Output

Single `.html` with Tailwind CDN + custom config:

```html
<script>
tailwind.config = {
  theme: { extend: { colors: { 'uw-blue': '#1B3A6B', 'uw-accent': '#0066CC' } } }
}
</script>
```

- Responsive prefixes: `sm:`, `md:`, `lg:`
- Hover utilities: `hover:bg-uw-accent`
- Transition: `transition-all duration-200`

---

## React Output

Single `.jsx` file:

- Functional component, default export
- All styles as inline JS objects in a `styles` const at top
- Hover via `onMouseEnter`/`onMouseLeave` + state
- No external dependencies

---

## Quality Gates

Before outputting, verify:
- Every color from design is in CSS custom properties or Tailwind config
- All sections from design are present
- Mobile layout handled (stack columns, adjust font sizes)
- All interactive elements have hover/focus states
- No Lorem Ipsum — use realistic UWorld content
- Images have descriptive `alt` text

---

## Output

Raw code only. Start with `<!DOCTYPE html>` (html/tailwind) or `import` (react).
No markdown fences. No explanation before or after.
