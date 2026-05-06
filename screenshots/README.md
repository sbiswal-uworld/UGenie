# Screenshots Needed

Capture these screenshots and save them with the exact filenames listed.
All screenshots should be PNG format, 1280px wide minimum.

---

## 01-verify-claude-version.png
**What to capture:** Git Bash terminal showing `claude --version` command and output
```
$ claude --version
2.1.114 (Claude Code)
```

---

## 02-git-clone.png
**What to capture:** Git Bash showing the `git clone` command running
```
$ git clone https://github.com/YOUR-ORG/uworld-webgenie-commands.git
Cloning into 'uworld-webgenie-commands'...
remote: Enumerating objects: 25, done.
...
```

---

## 03-install-success.png
**What to capture:** Git Bash showing `bash install.sh` running with the success output:
```
╔══════════════════════════════════════════════════╗
║     UWorld WebGenie — Claude Code Installer      ║
╚══════════════════════════════════════════════════╝
✓  Claude Code found: 2.1.114 (Claude Code)
✓  Skills directory ready: /c/Users/.../.claude/skills
Installing skills...
  ✓     /page-audit
  ✓     /cms-format
  ...
Installation complete! 7 skills installed.
```

---

## 04-slash-autocomplete.png
**What to capture:** Claude Code terminal with `/` typed and the autocomplete dropdown showing all 7 WebGenie skills

---

## 05-page-audit-output.png
**What to capture:** Claude Code showing the full output of `/page-audit https://gradschool.uworld.com/mcat/prep-books/` — scroll to show the overall score and section scores at the top

---

## 06-cms-format-output.png
**What to capture:** Claude Code showing the HTML output from `/cms-format` with a sample question

---

## 07-new-skill-autocomplete.png
**What to capture:** Claude Code autocomplete showing a newly created custom skill appearing in the `/` menu

---

## How to Take Good Screenshots

### Windows
- Press `Win + Shift + S` → drag to select area → paste into Paint or Snagit
- Or use Snipping Tool (search in Start Menu)

### Recommended tool
Use **Snagit** or **ShareX** for consistent, annotated screenshots.

### Tips
- Use a dark terminal theme (easier to read in docs)
- Make the terminal window wide enough to show full output
- Zoom in slightly (Ctrl+scroll) so text is readable in the screenshot
