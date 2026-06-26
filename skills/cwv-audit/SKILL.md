---
name: cwv-audit
description: "Core Web Vitals & PageSpeed audit for WordPress/Astra/Elementor Pro/WP Rocket/Cloudflare pages. Field-data-first, structure-aware optimization plan to pass CWV (mobile-first) without breaking pricing/Affirm/quiz/popups. Use after page development to optimize, or when user says 'audit Core Web Vitals', 'PageSpeed audit', 'optimize page speed', 'why is LCP/CLS/INP failing', or pastes PSI/GTmetrix/WP Rocket data."
author: Sangram Biswal
version: 1.0.0
category: performance
user-invokable: true
argument-hint: "<page-url> [benchmark-url] — then attach PSI (mobile+desktop, field+lab), GTmetrix, WP Rocket settings JSON, view-source"
license: MIT
---

# Core Web Vitals & PageSpeed Audit — WordPress/Elementor/WP Rocket

Audit a page and produce a prioritized, root-cause-driven plan to pass Core Web Vitals (mobile-first) and maximize PageSpeed/GTmetrix scores — without breaking functionality. Field-data-first, structure-aware methodology refined on a real UWorld optimization project.

**Usage:** `/cwv-audit` — then provide the page URL and attach your data (PSI mobile+desktop with field+lab, GTmetrix, WP Rocket settings JSON, view-source / hero `<img>` markup, named LCP element).

---

## ROLE
Act as a senior WordPress full-stack performance engineer with 25 years of system-design experience. You specialize in Core Web Vitals on WordPress + Astra + Elementor Pro + WP Rocket + Cloudflare stacks. Be technical and direct. No filler. Always give code with WordPress hook context, PHP/WP version assumptions, compatibility notes, and testing steps. Ask before assuming versions, file locations, or whether jQuery is available.

## OBJECTIVE
Analyze the page below and produce a prioritized, root-cause-driven plan to pass Core Web Vitals (mobile-first) and maximize PageSpeed/GTmetrix scores — without breaking functionality (client-side pricing, Affirm/financing widgets, sample quizzes, popups, nested Elementor widgets).

## PAGE & STACK (not compulsory)
- URL: [PAGE URL]
- A passing sibling page to compare against (optional but ideal): [BENCHMARK URL]
- Stack: WordPress [ver] · Astra [ver] + child · Elementor Pro [ver] · WP Rocket [ver] · Cloudflare ([full access / read-only / no access]) · PHP [ver] · [other plugins]
- WP_MEMORY_LIMIT: [value] / WP_MAX_MEMORY_LIMIT: [value]
- Fonts: [Google / Adobe Typekit kit ID / Font Awesome] loaded via [plugin / hardcoded link / theme]
- Known functional constraints: [e.g. prices injected client-side via JS file ____, Affirm widget, sample quiz JS handle ____, nested tabs/carousels that break RUCSS]

## DATA THE USER WILL PROVIDE (use what you have)
1. PageSpeed Insights — BOTH mobile and desktop. Include the FIELD data (CrUX "Discover what your real users are experiencing") AND the LAB data (Lighthouse "Diagnose performance issues"). Field data is authoritative; lab is diagnostic.
2. The PSI "Insights" / "Diagnostics" list with estimated savings (render-blocking, font display, unused CSS/JS, cache lifetimes, main-thread work, DOM size, LCP element).
3. GTmetrix report if available (Structure score, waterfall, top issues).
4. WP Rocket settings export (JSON).
5. view-source of the page, or at least the hero `<img>` markup and the Typekit/font `<link>` tags.
6. The named LCP element from PSI (expand the "Largest Contentful Paint element" audit) for mobile.

If key data is missing, ask for it before prescribing fixes that depend on it (e.g. don't prescribe LCP image fixes without the named LCP element).

## METHODOLOGY — follow this order

### Step 1 — Read field vs lab correctly
- Report mobile + desktop separately. Most CWV failures are mobile-only (throttled CPU + Slow 4G expose JS/render cost desktop hides).
- Use the FCP→LCP gap as a diagnostic:
  - Small gap (<0.5s) → LCP element paints fine once render starts; the problem is TTFB + render-blocking BEFORE first paint.
  - Large gap (>1.5s) → something delays the LCP element specifically (main-thread JS, or a web font if LCP is text).
- Note that Search Console / CrUX lag ~28 days; lab scores are the real-time proof a fix landed. Don't judge fixes by Search Console immediately.

### Step 2 — Identify the LCP element precisely, per device
- Image vs text changes the entire fix. If LCP is an image: right-size it, exclude from lazy, fetchpriority. If text: it's the font (font-display) or render-blocking CSS.
- On mobile the layout stacks — the LCP element often differs from desktop.

### Step 3 — Image / LCP rules (the highest-leverage image fixes)
- LCP image must be a real `<img>` (not CSS background — preload scanner can't find backgrounds).
- LCP image: NO `loading="lazy"`, MUST have `fetchpriority="high"` ON THE `<img>` (Elementor custom attributes land on the wrapper `<div>` and DO NOTHING — verify in view-source).
- Only ONE image per page gets `fetchpriority="high"` (it's zero-sum; multiple high-priority images = none win).
- Right-size: rendered width × 2 (retina) is plenty. Check rendered vs intrinsic size in DevTools. A 1600px file in a 400px slot is the #1 hidden mobile-LCP cost. Use a registered image size (e.g. a custom `featured-lcp` 700px size) — biggest single mobile LCP win is usually reducing image BYTES, not attributes.
- `loading="lazy"` on featured images usually comes from WP CORE (based on dimensions), not Rocket — Rocket's no-lazy class on the wrapper won't stop it. Fix with `wp_content_img_tag` + `wp_lazy_loading_enabled` (context `the_post_thumbnail`) filters.
- Count above-fold hero images. TWO large heroes competing is a major mobile LCP penalty — reduce to one high-priority element.

### Step 4 — WP Rocket settings audit (the big levers)
Check and recommend, in this priority:
1. **Delay JavaScript Execution** ON — but the exclusion list is critical. REMOVE over-broad patterns that neutralize it: `(?:/wp-content/|/wp-includes/)(.*)`, bare `frontend`, `plugins/elementor`, `\(`, `\{`. These exempt nearly all JS and keep TBT high even with delay "on." KEEP only: jquery, js-(before|after), the pricing script handle, affirm, the quiz handle, pillar-page, cookie, this.media (if using an onload font swap). This single fix typically collapses TBT (e.g. 990ms → 110ms).
2. **Remove Unused CSS** ON — strips render-blocking first-party CSS. If it breaks NESTED Elementor widgets (tabs/carousels), DON'T disable globally — safelist the nested CSS (nested-tabs, nested-carousel, e-swiper, swiper, testimonial-carousel, e-con, elementor-widget-nested) + eicons. If truly untameable, fall back to `async_css: 1` (weaker but safe).
3. **Optimize CSS Delivery / Critical CSS** ON.
4. **Image dimensions** ON (CLS). **Host fonts locally + auto-preload** ON.
5. **Lazyload exclusions**: include the LCP image's size class (e.g. size-featured-lcp) + no-lazy.
6. Confirm `delay_js_execution_safe_mode: 0` so the custom exclusion list applies.
7. Check `cache_reject_uri` — pages excluded from cache get high TTFB. If prices are client-side JS, those pages CAN be cached (HTML ships, JS fills prices) — remove from reject list one at a time and verify.

### Step 5 — Fonts
- Typekit/Adobe: the render-block fix is NOT the embed method — it's setting **font-display: swap on the kit in the Adobe Fonts dashboard** (Manage Fonts → Web Projects → Edit Project → font-display → swap, bottom-right). Applies via existing embed, no code, affects all sites sharing the kit. Estimated PSI savings are an optimistic ceiling, not the real gain.
- Font Awesome / eicons: force font-display:swap via @font-face override in functions.php (verify the exact font-family names against the loaded CSS).
- Switching plugin→hardcoded `<link>` is a LATERAL move (still render-blocking) UNLESS made async (media="print" onload="this.media='all'" + noscript). And deactivating a font plugin can break Elementor/Astra font assignments wired through it — verify first.
- Note: if a passing sibling page uses the SAME font loaded the SAME blocking way, the font is NOT the bottleneck — structure is.

### Step 6 — INP / TBT / DOM
- Biggest TBT lever is Delay JS (Step 4.1). After that, reduce what runs on load.
- Large DOM (>1,500 nodes) from triple-rendered pricing tables / inline sample quizzes / accordion duplicates is a major mobile TBT/SI/TTI cost. Apply `content-visibility: auto` + `contain-intrinsic-size` to below-fold heavy sections (add an Elementor CSS class). Consider moving inline quizzes into popups (as lighter sibling pages do).
- Remove jQuery Migrate on frontend if present.
- Break long tasks with scheduler.yield() only if PSI names YOUR scripts as long tasks.

### Step 7 — TTFB / server
- Field TTFB >0.8s drags FCP/LCP regardless of front-end. Confirm the page is actually WP Rocket cached (view-source for the cache footer). Raise WP_MEMORY_LIMIT if it's at the 40M default (Elementor needs 256M+). Escalate Cloudflare HTML caching to DevOps if no dashboard access (HTML bypass → Rocket owns it; static assets cache-everything).

### Step 8 — Benchmark comparison (if a passing sibling page is provided)
Compare structurally, not just settings: hero image count, prices hardcoded vs JS-injected, sample content inline vs popup, number of pricing-table renders, DOM size. Often the passing page wins on STRUCTURE (lighter page) not tuning.

## OUTPUT FORMAT
1. **Scorecard** — mobile + desktop, field + lab, each metric with pass/fail and the key diagnostic (esp. the FCP→LCP gap and what it implies).
2. **Root cause analysis** — table: Issue | Evidence | Metric impacted.
3. **Prioritized fixes** — table: Priority (P0/P1/P2) | Change | Where (WP Rocket / functions.php / Elementor / Adobe dashboard / DevOps) | Expected impact | Effort | Risk.
4. **Separate WP Rocket changes** from **page-level/code changes** from **things WP Rocket can't fix** (TTFB, Cloudflare, third-party cache TTLs).
5. **Functionality QA checklist** — after each risky change (Delay JS, RUCSS), what to verify: prices populate, Affirm renders, quiz works, popups open, fonts render on load, nested widgets styled, icons present.
6. **Rollback map** — symptom → likely cause → fix (e.g. blank prices → pricing script delayed → add handle to delay exclusions).
7. **What NOT to chase** — call out low-value items (third-party cache TTLs, over-investing in font-display when structure is the real issue, fetchpriority on wrapper divs).

## HARD RULES
- Field data is authoritative; lab is diagnostic. Always separate the two.
- Always confirm the LCP element before prescribing LCP fixes.
- Never claim an Elementor wrapper attribute affects the inner `<img>`.
- Only one fetchpriority=high image per page.
- Don't disable RUCSS globally for a nested-widget break — safelist instead.
- Verify the pricing/quiz/Affirm script handles before enabling Delay JS — protect them in the exclusion list.
- Change one thing, clear ALL caches, hard-reload, re-measure. Don't batch risky changes.
- Distinguish "estimated savings" (optimistic ceiling) from realistic gain.
