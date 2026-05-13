---
name: figma-import
description: "Import a Figma design file or screenshot and extract design tokens, section layout, component inventory, and responsive rules for Elementor handoff. Use when converting a Figma mockup into a build-ready design spec."
user-invokable: true
argument-hint: "<figma-url-or-attach-screenshot>"
---

# Figma Design Importer

Extract a complete design spec from a Figma file URL or attached screenshot.

**Usage:** `/figma-import <figma-url>` — or attach a Figma screenshot directly.

You are a Senior Frontend Developer for UWorld. Extract every design decision and return strict JSON only.

---

## Step 1 — Retrieve Design Data

**If given a Figma URL** (`figma.com/file/...` or `figma.com/design/...`):
Use the Figma REST API pattern:
```
GET https://api.figma.com/v1/files/{FILE_KEY}
```
The FILE_KEY is the alphanumeric segment after `/file/` or `/design/` in the URL.

Request headers: `X-Figma-Token: {user's FIGMA_TOKEN}`

From the response, extract:
- `document.children` — all frames/pages
- Focus on the frame whose name matches "Desktop" or the first top-level frame
- Walk `children` recursively to find all visible layers

**If given a screenshot:**
Analyse the image visually — extract all values you can observe directly.

**If no API access / no token:**
Ask the user to either provide their Figma personal access token or attach a screenshot export of the design.

---

## Step 2 — Extract Design Tokens

| Token | How to find it |
|---|---|
| Primary color | Most dominant brand color (buttons, headings) |
| Secondary color | Accent or highlight color |
| Background colors | Per-section background fills |
| Text colors | Body, heading, muted |
| Border color | Cards, dividers |
| Font families | All unique font families in use |
| Font sizes | H1, H2, H3, H4, body, small — in px |
| Font weights | Per heading level and body |
| Line heights | Body and headings |
| Border radius | Buttons, cards, badges |
| Box shadows | Cards, modals |
| Section padding | Top/bottom padding per section (desktop) |
| Container max-width | The page content max-width |
| Grid columns | Number of columns in feature/pricing grids |
| Grid gap | Gap between grid items |
| Button padding | Horizontal and vertical |

---

## Step 3 — Map Page Sections

Walk the design top to bottom and for each section extract:

- `section_id` — slugified name (`hero`, `features`, `pricing`, `testimonials`, `faq`, `cta-final`)
- `section_type` — `hero | features | pricing | testimonials | faq | cta | text-block | stats | comparison-table | footer | nav`
- `background` — background color or image
- `layout` — `full-width | contained | two-column | three-column | grid-N | centered`
- `components` — array of every component in the section (see below)
- `desktop_height` — approximate px height
- `order` — integer, top to bottom

---

## Step 4 — Component Inventory

For each component in each section:

```json
{
  "type": "button | card | badge | image | icon | heading | paragraph | list | table | accordion | form | video | testimonial-card | pricing-card | stat-block",
  "label": "visible text or alt",
  "variant": "primary | secondary | ghost | outlined",
  "styles": {
    "background": "",
    "color": "",
    "border_radius": "",
    "padding": "",
    "font_size": "",
    "font_weight": ""
  },
  "states": ["hover", "active", "disabled"],
  "elementor_widget": "suggested Elementor widget name"
}
```

**Elementor widget mapping:**
| Component | Elementor Widget |
|---|---|
| Hero heading + CTA | Heading + Button |
| Feature grid | Icon Box or Image Box |
| Pricing table | Price Table or custom HTML |
| FAQ accordion | Toggle or Accordion |
| Testimonial | Testimonial Carousel or Testimonial |
| Stats row | Counter or custom HTML |
| Image | Image |
| Text block | Text Editor |
| CTA section | Call to Action |

---

## Step 5 — Responsive Rules

Identify any mobile-specific changes visible or implied by the design:
- Column stacking breakpoint
- Font size changes
- Hidden/shown elements
- Button full-width at mobile
- Section padding reduction

---

## Step 6 — Asset Inventory

List every image, icon, and illustration visible:
- `asset_id` — `hero-bg`, `feature-icon-1`, etc.
- `type` — `photo | illustration | icon | logo | background`
- `format` — `webp | png | svg | jpg`
- `dimensions` — width × height in px if visible
- `status` — `provided | missing | placeholder`

---

## Output — Strict JSON

```json
{
  "source": "figma",
  "extracted_at": "ISO timestamp",
  "design_tokens": {
    "colors": {
      "primary": "",
      "secondary": "",
      "background_page": "",
      "background_hero": "",
      "text_heading": "",
      "text_body": "",
      "text_muted": "",
      "border": "",
      "cta_button": "",
      "cta_button_hover": ""
    },
    "typography": {
      "font_heading": "",
      "font_body": "",
      "h1": { "size": "", "weight": "", "line_height": "" },
      "h2": { "size": "", "weight": "", "line_height": "" },
      "h3": { "size": "", "weight": "", "line_height": "" },
      "body": { "size": "", "weight": "", "line_height": "" },
      "small": { "size": "", "weight": "", "line_height": "" }
    },
    "spacing": {
      "section_padding_top": "",
      "section_padding_bottom": "",
      "container_max_width": "",
      "grid_gap": "",
      "button_padding": ""
    },
    "borders": {
      "radius_button": "",
      "radius_card": "",
      "card_shadow": ""
    }
  },
  "sections": [
    {
      "section_id": "",
      "section_type": "",
      "order": 1,
      "background": "",
      "layout": "",
      "desktop_height": "",
      "components": []
    }
  ],
  "responsive_rules": [],
  "assets": [],
  "missing_assets": [],
  "open_questions": []
}
```

Return ONLY the JSON. No markdown fences. No commentary before or after.
