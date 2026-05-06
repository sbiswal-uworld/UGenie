# Installation Guide

Step-by-step instructions for installing UWorld WebGenie skills on any machine.

---

## Windows Installation (Git Bash)

### Step 1 — Install Claude Code

If Claude Code is not already installed:

1. Go to [https://claude.ai/code](https://claude.ai/code)
2. Download the installer for Windows
3. Run the installer
4. Open **Git Bash** and verify:

```bash
claude --version
```

Expected:
```
2.1.114 (Claude Code)
```

### Step 2 — Install Git

If Git is not installed:

1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer
3. Open **Git Bash** from Start Menu

### Step 3 — Clone the Repository

In Git Bash:

```bash
git clone https://github.com/YOUR-ORG/uworld-webgenie-commands.git
cd uworld-webgenie-commands
```

### Step 4 — Run the Installer

```bash
bash install.sh
```

### Step 5 — Verify

```bash
ls ~/.claude/skills/
```

Expected:
```
cms-format/     content-match/  feature-table/  figma-to-code/
page-audit/     table-compare/  visual-diff/
```

### Step 6 — Test in Claude Code

Open a new terminal and run:
```bash
claude
```
Type `/` and look for the 7 WebGenie skills in the autocomplete list.

---

## Mac Installation

### Step 1 — Open Terminal

Press `Cmd + Space`, type "Terminal", press Enter.

### Step 2 — Verify Claude Code

```bash
claude --version
```

### Step 3 — Clone and Install

```bash
git clone https://github.com/YOUR-ORG/uworld-webgenie-commands.git
cd uworld-webgenie-commands
bash install.sh
```

---

## What the Installer Does

The `install.sh` script:

1. Checks that `claude` command exists
2. Creates `~/.claude/skills/` directory if it doesn't exist
3. For each of the 7 skills:
   - Creates `~/.claude/skills/<skill-name>/` directory
   - Copies `SKILL.md` from the repo into it
   - Backs up any existing version as `SKILL.md.bak`
4. Prints confirmation of each installed skill

---

## File Locations After Install

On **Windows** (Git Bash paths):
```
/c/Users/YourName/.claude/skills/page-audit/SKILL.md
/c/Users/YourName/.claude/skills/cms-format/SKILL.md
...
```

On **Windows** (Windows Explorer paths):
```
C:\Users\YourName\.claude\skills\page-audit\SKILL.md
C:\Users\YourName\.claude\skills\cms-format\SKILL.md
...
```

On **Mac/Linux**:
```
~/.claude/skills/page-audit/SKILL.md
~/.claude/skills/cms-format/SKILL.md
...
```

---

## Re-installing / Repairing

If skills stop working or get corrupted, run `install.sh` again:

```bash
bash install.sh
```

It's safe to run multiple times. Existing files are backed up before overwriting.
