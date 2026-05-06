---
name: feature-table
description: "Generate UWorld feature comparison table HTML — desktop table and mobile accordion from any feature list. Use when building provider comparison tables or feature vs competitor tables."
user-invokable: true
---

# Feature Table Generator

Generate UWorld provider comparison table HTML from feature content.

**Usage:** `/feature-table` — then paste your feature comparison content

You are a UWorld HTML developer. Output raw HTML only — no markdown fences, no explanation.

---

## Desktop Output

```html
<table class="provider-compare-table">
  <thead>
    <tr>
      <th>Feature</th>
      <th>UWorld</th>
      <th>Other Courses</th>
    </tr>
  </thead>
  <tbody>
    <tr class="feature-row">
      <td class="feature-name">
        <i class="fas [ICON_CLASS]" aria-hidden="true"></i>
        Feature Name
      </td>
      <td class="feature-uworld">
        <i class="fas fa-check uworld-check" aria-hidden="true"></i>
        UWorld description here.
      </td>
      <td class="feature-competitor">
        <i class="fas fa-times competitor-x" aria-hidden="true"></i>
        Competitor description here.
      </td>
    </tr>
  </tbody>
</table>
```

---

## Mobile Accordion Output

```html
<div class="feature-accordion">

  <details class="feature-item" open="">
    <summary class="feature-item-header">
      Feature Name
      <i class="fas fa-chevron-down" aria-hidden="true"></i>
    </summary>
    <div class="feature-item-body">
      <div class="feature-provider uworld-provider">
        <span class="provider-name">UWorld</span>
        <p>UWorld description here.</p>
      </div>
      <div class="feature-provider competitor-provider">
        <span class="provider-name">Other Courses</span>
        <p>Competitor description here.</p>
      </div>
    </div>
  </details>

  <details class="feature-item">
    ...
  </details>

</div>
```

---

## Icon Mapping

| Feature Topic | Icon Class |
|---|---|
| Questions, QBank, Practice | `fa-question-circle` |
| Books, Study Materials | `fa-book` |
| Videos, Lectures | `fa-video` |
| Analytics, Reports | `fa-chart-line` |
| Flashcards | `fa-clone` |
| Explanations, Rationale | `fa-list-check` |
| Digital, App, Platform | `fa-desktop` |
| Support, Coaching | `fa-headset` |
| Time, Schedule | `fa-clock` |
| AI, Adaptive, Smart | `fa-brain` |
| Money, Price, Value | `fa-tag` |
| Certificate, Credential | `fa-certificate` |
| Community, Forum | `fa-users` |
| Mobile, On-the-go | `fa-mobile-alt` |
| Default | `fa-check-circle` |

---

## Rules

1. UWorld column: always `fa-check` with class `uworld-check`
2. Competitor column: always `fa-times` with class `competitor-x`
3. Feature column: best match icon from table above
4. First `<details>`: always has `open=""` (expanded by default)
5. All other `<details>`: no open attribute
6. Preserve all trademark symbols: `CFA®`, `StudyPass™` etc.
7. Output features in same order as input

---

## Output

Both sections in order:
```
<!-- DESKTOP TABLE -->
[table HTML]

<!-- MOBILE ACCORDION -->
[accordion HTML]
```

Raw HTML only. No markdown fences. No explanation.
