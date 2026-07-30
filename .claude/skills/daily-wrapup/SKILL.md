---
name: daily-wrapup
description: Daily wrap-up — reads today's notes and open beads issues, then writes a short dated Done/Doing/Next summary to log/<date>.md. Run at the end of a work day to capture momentum and set up tomorrow.
when: End of each work day, or whenever the user says "wrap up", "end of day", "daily summary", or "write today's summary".
---

# daily-wrapup

Write a concise, dated wrap-up entry to `log/<YYYY-MM-DD>.md` that captures what happened today, what's in flight, and what comes next — formatted so tomorrow's session can orient in under 30 seconds.

## When to invoke

- User says "wrap up", "end of day", "daily summary", or "/daily-wrapup"
- At the end of any session where meaningful work happened
- When the user wants a checkpoint before switching context

## Steps

### 1. Collect today's context

Gather from the current conversation and project state:

**From the conversation:**
- What was asked and completed this session
- Decisions made, approaches chosen, things the user confirmed or redirected

**From beads:**
```bash
bd list --status=in_progress   # What's actively being worked
bd list --status=open          # What's open and ready
bd stats                       # Health snapshot
```

**From git:**
```bash
git log --oneline --since="6am" --author="$(git config user.name)"
```

Use today's date from the `currentDate` context variable. Never guess the date.

### 2. Check for existing notes

Look for any notes file the user may have kept today:
- `notes/<YYYY-MM-DD>.md`
- `notes/today.md`
- `scratch.md` or `notes.md` in the project root

If found, read it and incorporate its content. Do not modify it.

### 3. Ensure the log directory exists

```bash
mkdir -p log
```

On Windows PowerShell: `New-Item -ItemType Directory -Force -Path log`

### 4. Write the wrap-up file

Write to `log/<YYYY-MM-DD>.md` (overwrite if it already exists for today).

Format:

```markdown
# Daily Wrap-Up — <YYYY-MM-DD>

## Done
- <specific thing completed — include file paths or issue IDs where relevant>
- <another completed item>

## Doing (in progress)
- <beads issue title> (`<id>`) — <last known state or blocker>
- <another in-progress item>

## Next
- <highest-priority next action — be concrete, not vague>
- <second priority>
- <third if relevant>

## Notes
<Optional: anything worth remembering that doesn't fit above — a decision rationale,
a gotcha, a question to resolve tomorrow. Omit this section if empty.>
```

Rules for content:
- **Done** entries must be specific — "added SchoolCard component to dashboard" not "did frontend work"
- **Doing** entries must name the beads issue ID if one exists
- **Next** entries must be actionable — start with a verb ("implement", "fix", "review", "ask about")
- Keep the whole file under 40 lines — this is a checkpoint, not a report
- Never include secrets, tokens, or credentials

### 5. Confirm to the user

Report back in this exact format:

```
**Wrap-up saved → log/<YYYY-MM-DD>.md**

Done today: <2-3 bullet summary>
In flight: <count> issue(s)
Up next: <top next action>
```

## Example output

```
**Wrap-up saved → log/2026-07-04.md**

Done today:
- Added /daily-wrapup skill with full step-by-step format
- Closed beads-042 (audit-fix for planning.md §6)

In flight: 2 issues
Up next: Implement FastAPI skeleton for /schools endpoint (beads-039)
```

## Rules

- Always use the date from `currentDate` context — never infer or guess
- Create `log/` at this project's own root (wherever this repo is checked out) if it doesn't exist
- Overwrite today's log file if it already exists — this is idempotent
- If there is nothing to report in a section, write `- (nothing today)` rather than omitting the heading
- Do not run `git add` or `git commit` — the user controls when the log gets committed
- Do not call `/handover` from this skill — they serve different purposes (handover writes to memory; wrapup writes to log/)
