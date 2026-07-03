---
name: elementor-content-sync
description: "Update an existing Elementor JSON export with a new content brief while keeping design, layout, structure, CSS, classes, IDs, and functionality 100% identical. Use when the user provides an exported Elementor page JSON plus updated content (headings, paragraphs, CTAs, FAQs, testimonials, feature blocks) and wants it merged in without any redesign. Trigger phrases: 'update this page with new content', 'implement this content into the JSON', 'content-only update, no design changes', 'map this content brief into the existing Elementor JSON'."
version: 1.1.0
user-invokable: true
argument-hint: "<path-to-elementor-json> <updated-content-brief-or-paste>"
---

# Elementor Content Sync

Merge a new content brief into an existing Elementor JSON export, changing **only** text/content-bearing fields. Every design, layout, CSS, class, ID, and behavior stays byte-for-byte identical unless it is directly carrying content (e.g. an icon class or image URL the brief explicitly names).

**Usage:** `/elementor-content-sync <path-to-json> <content-brief-path-or-paste>`

---

## NON-NEGOTIABLE RULES

1. **Content only.** Never touch `typography_*`, `*_color`, `padding*`, `margin*`, `background_*`, `border_*`, `box_shadow*`, `flex_*`, `width`/`height`, `css_classes`/`_css_classes`, `custom_css`, `_offset_*`, responsive (`_tablet`/`_mobile`) variants, `elType`, `widgetType`, `isInner`, or any `id` (except when cloning — see Phase 4).
2. **Never delete an existing element** just because the brief has fewer items for it (e.g. brief has 9 FAQs, JSON has 13). Replace what you have content for; leave the rest completely unchanged.
3. **Never invent a new section** to hold brief content that has no structural home in the JSON. Flag it in the Gaps Report and ask the user — do not silently drop it, and do not silently add a section.
4. **Never fabricate a URL.** If the brief relabels a CTA but gives no destination, keep the existing `link.url` unless the user explicitly supplies a new one.
5. **Never guess when two sections could equally fit one brief block, or vice versa.** Batch every such ambiguity into one round of clarifying questions before writing anything.
6. **Stop and flag before editing** if the JSON's actual content theme doesn't match the brief's theme (e.g. file is titled "X Study Planner" but its sections are all about "X Study Guide" books). Do not force-fit.

---

## CONTEXT BUDGET — Keep This Cheap and Fast

Elementor exports are typically 50–200K characters on a single minified line. Handled wrong, one of these files can burn six figures of tokens before any real editing happens. Follow all of these:

1. **The user provides the existing JSON as a file path or attachment — never as pasted text.** Pasted JSON becomes permanent conversation history that's re-sent every subsequent turn. A file path lets Node.js read/write it on disk without its raw content ever entering the model's context.
2. **Never call a line-based file reader (e.g. `Read`) on the raw export — not even once, "just to peek."** It will truncate mid-object on large files anyway, and every character you do get back is billed to context. Go straight to the Phase 2 inventory script; it's the only view of the file you need.
3. **Do the whole pipeline (Phases 1–8) inside one subagent call**, not the main conversation thread. Spawn a general-purpose agent with the source JSON path, the content brief, and this skill's instructions; let it run every Node script, validation, and file write internally. Have it return only a short final report (output path, change log, gaps) to the parent conversation. This keeps the parent thread's context flat regardless of file size, and each subsequent request in the same session starts from that same small footprint instead of accumulating raw JSON across turns.
4. **Keep every intermediate script's console output short.** Print counts, spot-checked field values, and short previews — never dump full file contents, full HTML blobs, or the entire inventory-of-everything to stdout if a filtered/truncated view would do.
5. **One page = one session.** Don't chain multiple unrelated page content-syncs in a single long-running conversation — each additional page's JSON and brief compounds the same session's context. Start a fresh session per page; the skill is fully self-contained on disk, so nothing is lost by starting clean.
6. **If the content brief itself is long** (multi-page brief, dozens of FAQs), save it to a file and pass the path rather than re-pasting it — the same permanent-history problem applies to oversized pasted content as it does to pasted JSON.

---

## Phase 0 — Mismatch Detection

Before anything else, skim the JSON's headings/testimonials/FAQ topics (via the inventory in Phase 2) against the brief's subject. If the page's *actual* content is about a meaningfully different product/topic than the brief (not just outdated copy — a different subject entirely), STOP and present a short comparison to the user:

```
The JSON's sections are about: [X]
Your content brief is about: [Y]
```

Offer options via AskUserQuestion: (a) get the correct JSON export, (b) best-effort remap content into the closest-matching existing sections, (c) let the user clarify. Do not proceed past this phase without a decision if a real mismatch exists. If the brief and JSON are clearly about the same page (the common case), skip this phase silently.

---

## Phase 1 — Intake

- Load the content brief (pasted text, doc, or file).
- Locate the Elementor JSON file. **Do not read it with the Read tool if it's a large single-line minified export** — it will truncate mid-object and can't be paginated by line. Instead go straight to Phase 2.
- Confirm the output path: default to `<original-name>-UPDATED.json` in the same directory as the source. Never overwrite the original input file.

---

## Phase 2 — Structural Inventory (mandatory, do this in Node.js, not by reading raw JSON)

Write and run a Node script that parses the JSON and prints a compact, human-readable map of every content-bearing widget: its `id`, `widgetType`, the section/container it belongs to (via `css_classes`/`_element_id`/`_title` on an ancestor, if present), and a short preview of its current content. This is your working map for every later phase — build your mapping decisions from this output, not from re-reading the raw file.

```js
const fs = require('fs');
const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const roots = Array.isArray(data.content) ? data.content : (Array.isArray(data) ? data : [data]);

function preview(s) {
  if (s == null) return '';
  const t = String(s).replace(/\s+/g, ' ').replace(/<[^>]+>/g, '').trim();
  return t.length > 90 ? t.slice(0, 90) + '…' : t;
}

function walk(node, ctx, path) {
  if (!node || typeof node !== 'object') return;
  const s = node.settings || {};
  if (s.css_classes || s._element_id || s._title) {
    ctx = [s._title, s.css_classes, s._element_id].filter(Boolean).join(' | ');
  }
  if (node.widgetType) {
    let info = '';
    switch (node.widgetType) {
      case 'heading': info = preview(s.title); break;
      case 'html': info = preview(s.html) + (( s.html && (s.html.match(/<li/g)||[]).length > 1) ? `  [${(s.html.match(/<li/g)||[]).length} <li> items]` : ''); break;
      case 'button': info = `"${s.text}" -> ${s.link && s.link.url}`; break;
      case 'image': info = `${s.image && s.image.url}  alt="${s.image && s.image.alt}"`; break;
      case 'toggle': info = `${(s.tabs||[]).length} accordion items: ` + (s.tabs||[]).slice(0,3).map(t=>preview(t.tab_title)).join(' | '); break;
      case 'nested-carousel': info = `${(node.elements||[]).length} carousel slides`; break;
      default: info = preview(JSON.stringify(s).slice(0, 80));
    }
    console.log(`[${path}] ${node.widgetType.padEnd(14)} id=${node.id}  (${ctx})  ${info}`);
  }
  (node.elements || []).forEach((c, i) => walk(c, ctx, path + '.' + i));
}
roots.forEach((r, i) => walk(r, '', String(i)));
```

Run: `node inventory.js "<path-to-json>"`. Read the printed map (not the raw JSON) to understand what each section currently says and which repeating groups exist (accordions, carousels, card grids, zigzag image+text blocks).

---

## Phase 3 — Parse the Content Brief

Break the brief into typed blocks, same discipline as a content-match audit:

| Type | Examples |
|---|---|
| H1 / H2 / H3 | Section headings |
| Paragraph | Body copy |
| CTA | Button label (+ URL if given) |
| Image | URL/description + alt text |
| Icon+Title+Description (repeating) | Step lists, feature grids, checkpoint grids |
| Testimonial | Quote + attribution |
| FAQ | Question + answer |
| List | Bullet items under a heading |

Note the **count** of every repeating group (how many steps, how many FAQs, how many testimonials, how many feature blocks) — you'll need it in Phase 4.

---

## Phase 4 — Map Content to Structure

For each brief block, find its best-fit widget(s) in the Phase 2 inventory using **content-type + theme fit**, not just position. A repeating group in the brief (e.g. "4 feature blocks with image + bullets") should map to a repeating group in the JSON with the same shape (e.g. 4 zigzag image/text containers), even if the JSON's existing copy is about something else entirely — shape match matters more than the old label.

Apply exactly one of these outcomes per brief block / JSON group pairing:

- **Same count** → replace each existing item's content fields in place (reuse existing `id`s).
- **Brief has MORE items than the JSON group** → clone the template item's full structure the required number of extra times (see Phase 5 for the cloning mechanics), then fill content into originals + clones.
- **Brief has FEWER items than the JSON group** → fill only as many existing slots as you have content for, **leave the remaining items completely untouched** (do not delete, do not blank).
- **JSON has an element/section with no matching brief content at all** → leave it exactly as-is.
- **Brief has content with no matching structural section anywhere in the JSON** → do not invent a section. Add it to the Gaps Report (Phase 7) and ask the user in Phase 5.

For fields the brief doesn't specify but that the mapped widget still needs a value for (eyebrow labels, CTA link destinations, icon choices not named in the brief) — default to **leaving the existing value unchanged**. Only change an icon, label, or link if the brief explicitly specifies it for that slot.

---

## Phase 5 — Batch Clarifying Questions

Before writing anything, collect every genuine ambiguity from Phase 4 into a single round of `AskUserQuestion` calls (max 4 questions per call, multiple calls if needed). Genuine ambiguities include:
- A brief content block could fit two or more equally-plausible existing sections.
- A relabeled CTA needs a URL the brief doesn't provide.
- Content exists in the brief with no structural home (per rule 3).
- The brief provides fewer/more repeating items than exist and the user might want different handling than the default rule.

Do **not** ask about anything with an obvious default (e.g. "keep unchanged" for a field the brief simply never mentions) — only ask when the answer would materially change what gets written. Do not resume implementation until these are resolved.

---

## Phase 6 — Implementation (Node.js, not hand-edited strings)

Write a mutation script that parses the JSON with `JSON.parse`, indexes every widget by `id`, applies content changes via small helper functions, then serializes with `JSON.stringify`. This avoids manual escaping mistakes on large minified files and keeps every untouched byte of the original structure intact.

```js
const fs = require('fs');
const SRC = process.argv[2];
const OUT = process.argv[3];
const data = JSON.parse(fs.readFileSync(SRC, 'utf8'));

const byId = {};
function index(node) {
  if (node && typeof node === 'object') {
    if (node.id && node.settings) byId[node.id] = node;
    (node.elements || []).forEach(index);
  }
}
(Array.isArray(data.content) ? data.content : data).forEach(index);

function genId() { return Math.random().toString(16).slice(2, 10); }
function deepClone(n) { return JSON.parse(JSON.stringify(n)); }
function findById(root, id) {
  if (!root || typeof root !== 'object') return null;
  if (root.id === id) return root;
  for (const c of (root.elements || [])) { const f = findById(c, id); if (f) return f; }
  return null;
}
function regenerateIds(node) {
  if (node && typeof node === 'object') {
    if (typeof node.id === 'string') node.id = genId();
    (node.elements || []).forEach(regenerateIds);
  }
}

// ---- content-only setters ----
const setTitle  = (id, v) => { byId[id].settings.title = v; };
const setHtml   = (id, v) => { byId[id].settings.html = v; };
const setButton = (id, text, url) => { byId[id].settings.text = text; if (url) byId[id].settings.link.url = url; };
const setImage  = (id, url, alt) => { if (url) byId[id].settings.image.url = url; if (alt != null) byId[id].settings.image.alt = alt; };

// ---- repeating-array (e.g. FAQ `tabs`) upsert: replace in place, clone to grow, never shrink ----
function upsertTabs(widgetId, items /* [{title, content}] */) {
  const tabs = byId[widgetId].settings.tabs;
  items.forEach((item, i) => {
    if (tabs[i]) {
      tabs[i].tab_title = item.title;
      tabs[i].tab_content = item.content;
    } else {
      const clone = deepClone(tabs[tabs.length - 1]);
      clone._id = genId();
      clone.tab_title = item.title;
      clone.tab_content = item.content;
      tabs.push(clone);
    }
  });
  // any tabs[i] beyond items.length are left untouched
}

// ---- repeating full-subtree clone (e.g. a testimonial slide or a feature-block container) ----
// 1. capture references to the nodes you'll need to edit INSIDE the clone using their
//    still-original (pre-regeneration) nested ids, 2. regenerate every id in the clone,
//    3. push the clone into the parent's elements array, 4. edit via the captured references.
function cloneSubtree(parentContainerId, templateChildId) {
  const parent = byId[parentContainerId];
  const template = findById(parent, templateChildId);
  const clone = deepClone(template);
  return clone; // caller: findById(clone, '<nested-id-from-template>') BEFORE regenerateIds(clone),
                //         keep the reference, THEN regenerateIds(clone), THEN parent.elements.push(clone)
}

// ... apply your Phase 4 mapping decisions here using the helpers above ...

fs.writeFileSync(OUT, JSON.stringify(data));
console.log('Wrote', OUT);
```

Run it: `node apply.js "<source.json>" "<output.json>"`.

---

## Phase 7 — Validation

Re-parse the output file and confirm:
- [ ] It's valid JSON (`JSON.parse` succeeds).
- [ ] Every original widget `id` referenced in Phase 4 still exists (nothing accidentally dropped).
- [ ] Repeating-group counts match: originals-kept + brief-provided-new = final array length (for grow cases); untouched tail count is correct (for shortfall cases).
- [ ] Every brief content block was placed somewhere, OR is explicitly listed in the Gaps Report.
- [ ] Spot-check a handful of mutated fields (button text+link, a couple of headings, image alt) by printing them from the parsed output.

---

## Phase 8 — Report

Give the user:
1. **Output file path.**
2. **Change log** — one line per section: what was updated and which widget IDs.
3. **Left unchanged (intentionally)** — eyebrow labels, CTA links, or unmatched repeating items that had no brief content, so the user knows it wasn't an oversight.
4. **Gaps Report** — any brief content with no structural home, and the options offered to the user (skip / add new section anyway / find alternate placement).

---

## Field Safety Reference

| Widget type | Safe to edit (content) | Never touch (design) |
|---|---|---|
| `heading` | `title` (text/HTML value only) | `header_size`, `title_color`, `typography_*`, `view`, alignment |
| `html` | the text nodes and `alt`/`href` values **the brief explicitly specifies** inside the markup | every tag, class, id, attribute not named by the brief; do not restructure the markup skeleton |
| `button` | `text`; `link.url` **only if the brief gives a destination** | `background_color`, `border_*`, `typography_*`, `_css_classes`, `button_css_id` |
| `image` | `image.url`, `image.alt` (only fields the brief provides) | `width`, `link_to`, `open_lightbox`, sizing settings |
| `toggle` / accordion | `tabs[].tab_title`, `tabs[].tab_content` | `title_typography_*`, `icon_color`, `border_color`, `content_padding*` |
| carousel slides | nested `heading`/`html` widget content | slide container styling, carousel navigation/arrow settings |
| icon class embedded in HTML (`class="fal fa-x"`) | only if the brief explicitly names an icon for that exact slot | otherwise leave as-is even if it seems thematically off |

---

## NEVER DO

- Never touch a design/layout/CSS/typography/spacing/responsive field.
- Never delete an existing element because the brief has fewer matching items.
- Never invent a brand-new section for orphaned brief content without asking first.
- Never fabricate a link URL, image URL, or icon that the brief didn't specify.
- Never read a large minified single-line Elementor export directly with a line-based file reader — parse it with Node.js instead.
- Never hand-edit large JSON via string search/replace when a programmatic parse+mutate script is available — escaping mistakes silently corrupt the file.
- Never skip the Phase 0 mismatch check — a page whose real content theme conflicts with the brief's theme must be flagged, not force-fit.
- Never overwrite the original source JSON file; always write to a new `-UPDATED` path.
- Never silently guess on a genuine ambiguity — batch it into Phase 5 questions instead.

---

## Version History

- **v1.1.0**: Added CONTEXT BUDGET section — file-path-not-paste rule for the source JSON, ban on ever reading the raw export with a line-based reader, run-the-whole-pipeline-in-a-subagent guidance, short-stdout discipline, one-page-per-session recommendation. Distilled from a follow-up session where reading the raw JSON directly (before this skill existed) cost roughly 80K+ tokens before any editing began.
- **v1.0.0**: Initial version, distilled from a live CFA Study Planner content-sync session — codifies the structural-inventory-via-Node approach (to avoid truncated reads of large minified JSON), the content-vs-design field safety table, repeating-group grow/shrink rules (clone to grow, never delete to shrink), the Phase 0 theme-mismatch guard, and the batched-clarifying-questions pattern.
