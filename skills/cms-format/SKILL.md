---
name: cms-format
description: "Convert raw CMS HTML into UWorld golden standard question format — passage, choices, hint, explanation structure. Use when formatting CMS content, cleaning question HTML, or converting question markup."
user-invokable: true
---

# CMS Question Formatter

Format raw CMS question content into UWorld production-ready HTML.

**Usage:** `/cms-format` — then paste your raw CMS content

You are a Senior UWorld Web Developer. Output raw HTML only — no markdown fences, no explanation, no preamble.

---

## Complete Output Structure

```html
<p class="passage-text"><strong>Question</strong></p>
<p>Question stem text here.</p>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<div class="explanation-container">
  <table class="answer-table custom-image-table">
    <tr>
      <td><input type="radio" name="answer" value="A"></td>
      <td class="formula-td"><span>A.</span> <span>Answer A text here.</span></td>
    </tr>
    <tr>
      <td class="correct-answer"><i class="fas fa-check-circle"></i><input type="radio" name="answer" value="B"></td>
      <td class="formula-td"><span>B.</span> <span>Correct answer text here.</span></td>
    </tr>
    <tr>
      <td><input type="radio" name="answer" value="C"></td>
      <td class="formula-td"><span>C.</span> <span>Answer C text here.</span></td>
    </tr>
    <tr>
      <td><input type="radio" name="answer" value="D"></td>
      <td class="formula-td"><span>D.</span> <span>Answer D text here.</span></td>
    </tr>
  </table>

  <button class="submit-btn">Submit</button>
  <button class="next-btn">Next Question</button>

  <div class="hint-block">
    <strong>Hint:</strong><br/>
    <p>First hint sentence.</p>
    <p class="no-margin-bottom">Last hint sentence.</p>
  </div>

  <div class="explanation-text">
    <p class="passage-exp-text"><strong>Explanation</strong></p>
    <p>First explanation paragraph.</p>
    <p class="align-center"><img title="Image ID: LXXXXX; Click here to see more information" draggable="false" src="URL" alt="" /></p>
    <p>More explanation paragraphs.</p>
    <div>
      <table class="no-border-table compact-table left-table">
        <tbody>
          <tr>
            <td>table cell</td>
            <td>table cell</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p><strong>(Choice A)</strong> Explanation of wrong choice A.</p>
    <p><strong>(Choice C)</strong> Explanation of wrong choice C.</p>
    <p><strong>(Choice D)</strong> Explanation of wrong choice D.</p>
    <p><strong>Things to remember:</strong></p>
    <ul class="no-margin-bottom">
      <li>Bullet point one.</li>
      <li>Bullet point two.</li>
    </ul>
  </div>

  <div class="bottom-navigation">
    <button class="next-btn">Next Question</button>
  </div>
</div>
```

---

## If a Passage exists

Insert the passage BEFORE the question header block:

```html
<div class="passage-container">
  <p class="passage-header"><strong>Passage</strong></p>
  <div class="passage-body">
    <p>Passage paragraph.</p>
    <p class="no-margin-bottom">Last passage paragraph.</p>
  </div>
</div>

<p class="passage-text"><strong>Question</strong></p>
<p>Question stem.</p>
...
```

---

## Transformation Rules

### Question Header & Stem
- Question label: `<p class="passage-text"><strong>Question</strong></p>`
- Question stem: plain `<p>` with no class

### MathJax
- Always include the MathJax script tag immediately after the question stem `<p>`, before `<div class="explanation-container">`
- Preserve all LaTeX inline math: `\(formula\)` and display math: `\[formula\]`
- Preserve all MathML blocks verbatim

### Answer Choices Table
- Wrapper: `<table class="answer-table custom-image-table">`
- Each choice: `<tr><td><input type="radio" name="answer" value="A"></td><td class="formula-td"><span>A.</span> <span>text</span></td></tr>`
- **Correct answer row only**: add `class="correct-answer"` to the `<td>` and prepend `<i class="fas fa-check-circle"></i>` before the `<input>`
- Strip: percentage stats `[26%]`, `(13%)`, `[correct]`, `SELF STUDY [ ]`, `LP ( )` — these are CMS UI artifacts

### Hint Block
- If CMS input contains hint content, include `<div class="hint-block">`
- Last `<p>` inside hint-block: `class="no-margin-bottom"`
- If no hint content exists, omit the hint-block div entirely

### Explanation
- Wrapper: `<div class="explanation-text">`
- Header: `<p class="passage-exp-text"><strong>Explanation</strong></p>`
- Each paragraph: plain `<p>`

### Images in Explanation
```html
<p class="align-center"><img title="Image ID: LXXXXX; Click here to see more information" draggable="false" src="URL" alt="" /></p>
```
- No `<a>` wrapper around images
- Use `class="align-center"` on the `<p>` (not `aligncenter`)
- Preserve the `title` attribute with the Image ID text
- `alt=""` (empty) unless descriptive alt text is provided
- Self-closing `<img />` tag

### Tables in Explanation
```html
<div>
  <table class="no-border-table compact-table left-table">
    <tbody>
      ...
    </tbody>
  </table>
</div>
```
Wrap every explanation table in a `<div>`.

### "Things to Remember" Section
- Convert to: `<p><strong>Things to remember:</strong></p>` followed by `<ul class="no-margin-bottom"><li>...</li></ul>`
- Each bullet point becomes a `<li>`
- If "Things to remember" is a single paragraph (not bullets), keep as `<p>` with `class="no-margin-bottom"`

### Wrong Choice Explanations
- Format as: `<p><strong>(Choice A)</strong> explanation text.</p>`
- One `<p>` per wrong choice

### Last Paragraph Rule
- Last `<p>` in `.passage-body` → `class="no-margin-bottom"`
- Last `<p>` in `.hint-block` → `class="no-margin-bottom"`
- Last element in `.explanation-text` before closing tag — if it is a `<p>`, add `class="no-margin-bottom"`; if it is a `<ul>`, add `class="no-margin-bottom"` to the `<ul>`

### Bottom Navigation
Always close with:
```html
<div class="bottom-navigation">
  <button class="next-btn">Next Question</button>
</div>
```

### Preserve
- All `<strong>`, `<em>`, `<u>`, `<sub>`, `<sup>`
- All `<span>` with semantic classes (eg, `class="blue-text"`)
- All MathML (`<math>`, `<mrow>`, `<mi>`, `<mfrac>`, etc.)
- All LaTeX: `\( \)` and `\[ \]`
- All HTML entities: `&hellip;` `&nbsp;` `&mdash;` `&ndash;` `&le;` `&ge;` `&minus;`
- Hyperlinks inside explanation text: `<a href="URL">linked text</a>`

### Strip
- CMS UI classes and wrappers: `d-flex`, `ml-10`, `my-15`, `chocies`, `spliterSection`, `ff-default`, `questionContainer`, `answerContainer`, `spliter`, etc.
- Percentage/stat indicators: `[26%]`, `(13%)`, `[60%]`, `[correct]`
- `SELF STUDY [ ]`, `LP ( )`, `Correct Answer: X` lines
- Empty `<div>` wrappers with no semantic purpose
- Duplicate `<br>` tags (max 1 in sequence)

---

## Output

Raw HTML only. No markdown code fences. No explanation before or after.
