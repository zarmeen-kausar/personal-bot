# Personal Claude Bot — Module 6 Assessment

A personal Claude Code bot built in the live session, upgraded with three Module 6 moves:
a skill file, a scheduled loop, and an event-driven hook.

---

## Module 6 Features

### 1. Skill — `/daily-wrapup`

**File:** `.claude/skills/daily-wrapup/SKILL.md`

A proper Claude Code skill that reads today's notes and writes a concise dated
summary (Done / Doing / Next) to `log/<date>.md`.

**Proof it fired:** `log/2026-07-16.md` — written by running `/daily-wrapup` manually on 2026-07-16.

---

### 2. Loop — Weekday 6 PM cron

**Routine ID:** `trig_0173eVve9cZ2tfo6sPi4T7tk`
**Schedule:** Every Monday–Friday at 6 PM Karachi time (cron `0 13 * * 1-5` UTC)
**Manage:** https://claude.ai/code/routines/trig_0173eVve9cZ2tfo6sPi4T7tk

A cloud Claude Code agent that runs every weekday evening, clones this repo,
reads today's notes, writes the wrap-up log, and commits it back.

**Proof it fired:** Routine triggered manually on 2026-07-16 — cloud session `cse_017ipcja72MwRPbJBsgbyhET` ran.

---

### 3. Hook — notes/ file-save event

**Config:** `.claude/settings.json` → `FileChanged` matcher on `notes/`

Every time a file is saved in the `notes/` folder, Claude Code re-wakes and
automatically runs `/daily-wrapup` to keep the log current.

**Proof it fired:** `notes/2026-07-16.md` was saved on 2026-07-16, triggering the hook
and re-invoking `/daily-wrapup` via `asyncRewake`.

---

## Structure

```
.claude/
  settings.json              ← hook: FileChanged on notes/ triggers /daily-wrapup
  skills/
    daily-wrapup/
      SKILL.md               ← skill: name, when, steps, example
log/
  2026-07-16.md              ← proof: skill fired (written by /daily-wrapup)
notes/
  2026-07-16.md              ← proof: hook fired (saving this file triggered re-wake)
```

## How to use

1. Clone this repo and open in Claude Code
2. Save any file in `notes/` → hook auto-runs `/daily-wrapup`
3. Type `/daily-wrapup` → skill runs manually
4. The cron routine fires automatically every weekday at 6 PM (Karachi time)
