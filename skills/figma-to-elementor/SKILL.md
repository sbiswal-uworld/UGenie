---
name: figma-to-elementor
description: "Convert Figma designs to pixel-perfect Elementor JSON for UWorld. Use when user says 'Implement this design from Figma' and provides a Figma URL. Requires Figma MCP connection."
user-invokable: true
argument-hint: "@https://www.figma.com/design/..."
---

# Figma → Elementor JSON Conversion Skill

Convert a Figma design to a pixel-perfect Elementor JSON file importable into WordPress.

**Trigger:** `Implement this design from Figma. @https://www.figma.com/design/...`

> **MANDATORY PREREQUISITE:** The Figma MCP must be connected before running this skill.
> Without it, design tokens (colors, spacing, fonts, shadows) cannot be accurately extracted.
> Verify the connection by running `get_design_context` — if it fails, stop and ask the user to connect Figma MCP.

**Output directory:** `C:\Users\sbiswal\Downloads\Productivity Tool\Elementor JSON Exports\`

---

## Step 1 — Extract Figma File Key & Node ID

Parse the provided Figma URL:
- `https://www.figma.com/design/<fileKey>/...?node-id=<nodeId>`
- Call `get_design_context` with `fileKey` + `nodeId` via Figma MCP
- Extract every design token: hex colors, px values, font sizes, weights, letter-spacing, line-height, gap, padding, margin, border-radius, box-shadows, gradients

If a value is not visible or readable, zoom in or call `get_screenshot` — **never use placeholder values**.

---

## Step 2 — Core Principles

- **Pixel-perfect accuracy** — extract exact values from Figma, no approximations
- **Never skip a container** — every Figma group/frame = one Elementor container
- **Ignore the top navbar** — convert only sections below it
- **Match live site JSON structure** — file format, key order, and field names must match real UWorld exports
- **No placeholder values** — use Figma MCP to get any missing values

---

## Step 3 — File Structure

```json
{
  "content": [
    {
      "id": "abc12345",
      "settings": { },
      "elements": [ ],
      "isInner": false,
      "elType": "container"
    }
  ]
}
```

**No `version`, `title`, or `type` at top level.** Live site exports only use `{"content": [...]}`.

**Key order in every object:**
1. `id`
2. `settings`
3. `elements`
4. `isInner` ← always at END
5. `elType` ← always at END (+ `widgetType` for widgets)

---

## Step 4 — Container Settings Template

```json
{
  "id": "abc12345",
  "settings": {
    "flex_direction": "row",
    "flex_justify_content": "center",
    "flex_align_items": "center",
    "flex_gap": { "unit": "px", "size": 16, "sizes": [], "column": "16", "row": "16", "isLinked": true },
    "flex_gap_tablet": { "unit": "px", "size": "", "sizes": [], "column": "", "row": "", "isLinked": true },
    "flex_gap_mobile": { "unit": "px", "size": "", "sizes": [], "column": "", "row": "", "isLinked": true },
    "padding": { "unit": "em", "top": "5", "right": "1", "bottom": "1", "left": "1", "isLinked": false },
    "padding_tablet": { "unit": "em", "top": "4", "right": "1", "bottom": "1", "left": "1", "isLinked": false },
    "padding_mobile": { "unit": "em", "top": "3", "right": "1", "bottom": "1", "left": "1", "isLinked": false },
    "margin": { "unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": false },
    "background_background": "classic",
    "background_color": "#ffffff",
    "css_classes": "section-name",
    "custom_css": "/* section-scoped CSS */",
    "_offset_x": { "unit": "px", "size": "0", "sizes": [] },
    "_offset_x_end": { "unit": "px", "size": "0", "sizes": [] },
    "_offset_y": { "unit": "px", "size": "0", "sizes": [] },
    "_offset_y_end": { "unit": "px", "size": "0", "sizes": [] }
  },
  "elements": [],
  "isInner": false,
  "elType": "container"
}
```

**DO NOT use:** `_element_width`, `_element_flex`, `_element_max_width`, `_element_custom_width`

---

## Step 5 — Layout & Width Rules

| Figma | Elementor |
|---|---|
| Horizontal auto layout | `flex_direction: "row"` |
| Vertical auto layout | `flex_direction: "column"` |
| Fill container | `width: { "unit": "%", "size": 100 }` |
| Fixed % column | `width: { "unit": "%", "size": 50 }` + `width_tablet` + `width_mobile` |
| Max-width centered | `boxed_width: { "unit": "px", "size": 1100 }` |
| Content width full | `content_width: "full"` |

`flex_wrap: "nowrap"` on main rows. Only `"wrap"` on small button groups.

---

## Step 6 — Typography (Font: Proxima Nova)

| Usage | Size | Weight | Line-height |
|---|---|---|---|
| Hero H1 | 44px | 600 | 1.2em |
| Section H2 | 36px | 700 | 44px |
| Feature H2 | 32px | 700 | 40px |
| Callout label | 20px | 600 | 26px |
| Subtitle | 24px | 500 | 32px |
| Body | 16px | 400 | 24px |
| Button | 14–16px | 600 | 20–24px |
| Caption/chip | 12px | 600 | 16px |

Use `header_size: "span"` or `"div"` for decorative text (badges, labels).
Always add `"view": "traditional"` on heading, button, and image widgets.

---

## Step 7 — Widget Rules

**Icons:** Use dedicated `icon` widget — never `<i>` in HTML widget.
```json
{ "settings": { "selected_icon": { "value": "far fa-users", "library": "fa-regular" }, "primary_color": "#D3DEE9", "size": { "unit": "px", "size": 20, "sizes": [] } }, "widgetType": "icon", "elType": "widget" }
```

**Buttons:** Always include `button_css_id` for tracking: `"cta-[page]-[section]-[action]-000001"`.

**Images:** Use `"source": "library"` and descriptive `alt` text.

**HTML widget:** Only for stars, gradient text, status chips, pricing tables, custom badges.

**Stats:** Never use HTML widget. Use container + `icon` + two `heading` widgets.

**CSS:**
- No inline `style=""` attributes — ever
- `custom_css` in `settings` for widget/container scope
- `css_classes` on containers, `_css_classes` on widgets
- Always scope CSS: `.stat-card .far.fa-users {}` not bare `i {}`

---

## Step 8 — UWorld Color Reference

| Token | Hex |
|---|---|
| Brand blue | `#0066CC` |
| Blue hover | `#0052a3` |
| Text dark | `#0d1a26` |
| Text body | `#264D73` |
| Border | `#dde6ee` |
| BG gray | `#F1F5F8` |
| Light blue btn | `#d5e6ff` |
| Yellow CTA | `#FFD600` |
| Star yellow | `#FFDD55` |

---

## Step 9 — Build Order

1. Verify Figma MCP is connected (`get_design_context` returns data)
2. Parse Figma URL → extract `fileKey` and `nodeId`
3. Call `get_design_context` and extract all design tokens
4. Build JSON bottom-up: leaf widgets first → parent containers → root
5. Run pre-flight checklist
6. Save to output directory

---

## Step 10 — Pre-flight Checklist

- [ ] File starts with `{"content": [...]}` — no version/title/type
- [ ] `isInner` and `elType` at END of every object
- [ ] `flex_gap` has `column`/`row` string keys alongside `size`
- [ ] `flex_gap_tablet` and `flex_gap_mobile` on all containers
- [ ] `_offset_x/y` and `_offset_x_end/y_end` on all containers and widgets
- [ ] Standalone icons use `widgetType: "icon"` with `selected_icon`
- [ ] No inline `style=""` anywhere
- [ ] `custom_css` (not `_custom_css`) for widget CSS
- [ ] `css_classes` on containers, `_css_classes` on widgets
- [ ] Stars use UWorld `uw-star uw-star-filled` pattern
- [ ] `view: "traditional"` on heading/button/image widgets
- [ ] Buttons have `button_css_id` tracking ID
- [ ] Responsive variants included (`_tablet`, `_mobile`)
- [ ] All IDs are unique short alphanumeric strings
- [ ] File saved to correct output directory

---

## Output

Save the completed JSON file to:
`C:\Users\sbiswal\Downloads\Productivity Tool\Elementor JSON Exports\<section-name>.json`

Report: file path, section count, widget count, any values that required MCP fallback.
