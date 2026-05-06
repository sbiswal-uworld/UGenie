# Troubleshooting Guide

Solutions for common issues with UWorld WebGenie skills.

---

## ❌ "Unknown command: /page-audit"

**What it means:** Claude Code can't find the skill file.

**Most likely cause:** The skill was installed as a flat `.md` file in `~/.claude/commands/` instead of as a directory in `~/.claude/skills/`.

**Fix:**
```bash
bash install.sh
```

This copies skills to the correct location: `~/.claude/skills/<name>/SKILL.md`.

Then restart Claude Code.

---

## ❌ Skill not appearing in `/` autocomplete

**Check 1 — Verify the file exists:**
```bash
ls ~/.claude/skills/page-audit/
```
Should show: `SKILL.md`

**Check 2 — Verify frontmatter is correct:**
```bash
head -6 ~/.claude/skills/page-audit/SKILL.md
```
Should show:
```yaml
---
name: page-audit
description: "..."
user-invokable: true
---
```

**Check 3 — No blank line before first `---`:**

Open the file and make sure the very first character is `-`, not a blank line.

**Check 4 — Restart Claude Code:**

If the `~/.claude/skills/` directory was created for the first time during this session, Claude Code needs a restart to begin watching it.

```bash
# Close Claude Code, then reopen:
claude
```

---

## ❌ Skill appears but does nothing / wrong output

**Cause:** The SKILL.md content may have been overwritten or corrupted.

**Fix:**
```bash
bash update.sh
```

This re-syncs all skill files from the repo source.

---

## ❌ `bash install.sh` — "Permission denied"

```bash
chmod +x install.sh update.sh
bash install.sh
```

---

## ❌ `bash install.sh` — "claude: command not found"

Claude Code is not in your PATH.

**Fix:**
1. Close and reopen Git Bash
2. Try: `which claude`
3. If still not found, reinstall Claude Code from [claude.ai/code](https://claude.ai/code)

---

## ❌ Git Bash not available on Windows

Install Git for Windows from [git-scm.com](https://git-scm.com).
During installation, select **"Git Bash Here"** option.

---

## 🔍 Diagnostic Commands

Run these to quickly diagnose any issue:

```bash
# 1. Check Claude Code version
claude --version

# 2. List installed skills
ls ~/.claude/skills/

# 3. Check a specific skill file
cat ~/.claude/skills/page-audit/SKILL.md | head -10

# 4. Count skills installed
ls ~/.claude/skills/ | wc -l

# 5. Re-run installer
bash install.sh
```

---

## Getting Help

If none of the above fixes your issue:

1. Run the diagnostic commands above and copy the output
2. Open an issue on this repository with the diagnostic output
3. Include your OS, Claude Code version, and the exact error message
