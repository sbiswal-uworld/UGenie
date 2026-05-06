# How to Create a Claude Code Skill

A complete authoring guide for adding new slash commands to the UWorld WebGenie toolkit.

---

## What is a Skill File?

A skill is a single Markdown file (`SKILL.md`) inside a named folder. The folder name becomes the slash command. Claude Code reads the file contents as the system prompt when you invoke the command.

```
~/.claude/skills/
└── my-skill/          ← folder name = /my-skill
    └── SKILL.md       ← the instructions Claude follows
```

---

## Anatomy of a SKILL.md File

Every SKILL.md has two parts: **frontmatter** and **instructions**.

```markdown
---
name: skill-name
description: "What this skill does and when to use it."
user-invokable: true
argument-hint: "<required> [optional]"
---

# Skill Title

Instructions for Claude go here in plain Markdown.
```

---

## Frontmatter Reference

The YAML block between the `---` markers controls how Claude Code registers and displays the skill.

```yaml
---
name: page-audit
description: "Full UWorld page QA audit — SEO, images, links, schema, trademark compliance."
user-invokable: true
argument-hint: "<url> [product|pillar|blog]"
---
```

### Field Descriptions

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | ✅ | Must match the folder name. No spaces — use hyphens. |
| `description` | string | ✅ | Shown in `/` autocomplete. Keep under 120 chars. Claude also reads this to decide when to auto-invoke. |
| `user-invokable` | boolean | ✅ | Set to `true`. Without this, the skill won't appear in `/` autocomplete. |
| `argument-hint` | string | Optional | Shown as grey hint text after the command name in autocomplete. Use `<angle-brackets>` for required args, `[square-brackets]` for optional. |

### Description Writing Tips

The description is shown in two places:
1. **Autocomplete menu** — user sees it when typing `/`
2. **Auto-trigger** — Claude reads it to decide whether to invoke the skill automatically

Write it as: **"Does X for Y. Use when [trigger phrase]."**

```yaml
# Good
description: "Compare a brief or doc against a live UWorld page — flags every content, price, CTA, and trademark mismatch. Use when checking if a live page matches a brief."

# Too vague
description: "Content comparison tool"
```

---

## Step-by-Step: Creating a New Skill

### 1. Choose a name

Pick a short, hyphenated name that describes the action:

| ✅ Good Names | ❌ Bad Names |
|---|---|
| `page-audit` | `pageaudit` |
| `cms-format` | `format cms` |
| `content-match` | `check` |
| `price-checker` | `tool1` |

### 2. Create the folder and file

```bash
# From inside the repo root:
mkdir -p skills/my-skill-name
touch skills/my-skill-name/SKILL.md
```

### 3. Open the file and add frontmatter first

```yaml
---
name: my-skill-name
description: "One clear sentence. Use when [trigger]."
user-invokable: true
argument-hint: "<url>"
---
```

**Critical:** The frontmatter MUST be at the very top of the file. No blank lines before the first `---`.

### 4. Add a role declaration

Tell Claude who it is for this skill:

```markdown
# My Skill Title

You are a [specific role] for UWorld. Your job is to [specific task].

**Usage:** `/my-skill-name <arg>` — then [what user should do next]
```

### 5. Add numbered steps

Structure the instructions as explicit numbered steps with clear inputs and outputs:

```markdown
## Step 1 — Receive Input

The user provides [X]. This is the source of truth.

## Step 2 — Fetch/Process

Use [tool] to [action].

## Step 3 — Analyse

Check each of the following:
- Rule 1
- Rule 2
- Rule 3

## Step 4 — Output

Return results in this exact format:

[Output template]
```

### 6. Define a strict output format

Always end with an exact output template. This is the most important part — without it, Claude improvises formatting each time.

```markdown
## Output Format

Return results in this exact structure:

\`\`\`
=== MY SKILL REPORT ===
URL: [url]
Date: [date]

SUMMARY
[structured data]

ISSUES
P1: [list]
P2: [list]
\`\`\`
```

### 7. Add output rules

```markdown
## Output Rules

- Raw HTML only. No markdown fences. No explanation.
- OR: Plain text only. No code blocks.
- Be exhaustive. Never truncate.
- Quote exact text strings — never paraphrase.
```

---

## Complete Minimal Example

Here is the smallest valid skill file:

```markdown
---
name: price-checker
description: "Extract and validate all prices on a UWorld page. Use when checking pricing accuracy."
user-invokable: true
argument-hint: "<url>"
---

# Price Checker

You are a QA engineer for UWorld. Extract every price from the page and validate its format.

**Usage:** `/price-checker <url>`

## Step 1 — Fetch Page

Use WebFetch to retrieve the page at the provided URL.
Extract all text that matches price patterns: $X, $X,XXX, $X/month, etc.

## Step 2 — Validate Format

For each price found, check:
- Dollar sign present: `$`
- Comma formatting: `$1,299` not `$1299`
- Correct suffix: `/month`, `/year`, or none

## Output Format

\`\`\`
=== PRICE CHECK REPORT ===
URL: [url]

Prices Found: [count]

| Location     | Price Found | Format Valid | Issue          |
|--------------|-------------|--------------|----------------|
| Hero section | $1299       | ❌           | Missing comma  |
| Pricing card | $1,299/mo   | ✅           |                |

Issues: [count]
\`\`\`
```

---

## Installing Your New Skill

After creating `skills/my-skill-name/SKILL.md`, run:

```bash
bash install.sh
```

Or install just the new one:

```bash
mkdir -p ~/.claude/skills/my-skill-name
cp skills/my-skill-name/SKILL.md ~/.claude/skills/my-skill-name/SKILL.md
```

Open Claude Code and type `/my-skill-name` — it appears immediately, no restart needed.

---

## Common Mistakes

### ❌ Missing `user-invokable: true`

```yaml
# Wrong — skill won't appear in autocomplete
---
name: my-skill
description: "Does something."
---

# Correct
---
name: my-skill
description: "Does something."
user-invokable: true
---
```

### ❌ Blank line before first `---`

```markdown
                    ← this blank line breaks frontmatter parsing
---
name: my-skill
---
```

### ❌ Folder name doesn't match `name:` field

```
skills/page-audit/SKILL.md   but name: pageaudit   ← mismatch
```

The folder name is what creates the slash command. The `name:` field should match.

### ❌ No output format defined

Without a strict output format, Claude improvises a different structure every run. Always define the exact template.

---

## Testing Checklist

Before submitting a PR with a new skill:

- [ ] Folder name is hyphenated, no spaces
- [ ] `SKILL.md` exists inside the folder
- [ ] Frontmatter is at top of file, no blank line before first `---`
- [ ] `name:` matches folder name
- [ ] `description:` is under 120 chars and explains when to use it
- [ ] `user-invokable: true` is present
- [ ] Skill has a role declaration ("You are a...")
- [ ] Skill has numbered steps
- [ ] Skill has a strict output format template
- [ ] Installed and tested with `bash install.sh`
- [ ] Skill appears in `/` autocomplete
- [ ] Skill produces correct output when invoked
