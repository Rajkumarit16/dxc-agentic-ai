# AskIT Program — Participant Guide

> **Orbit Corp's IT Helpdesk is drowning in tickets. You are building AskIT — an AI helpdesk agent that answers, acts and escalates.**

First time? Do **[setup/SETUP_GUIDE.md](setup/SETUP_GUIDE.md)** once (Session 1, Lab A). Git help: **[GIT_INSTRUCTIONS.md](GIT_INSTRUCTIONS.md)**. What is on which day: **[COURSE_MAP.md](COURSE_MAP.md)**.

---

## Your daily routine (3 steps)

| When | Do this | What happens |
|---|---|---|
| **Morning** | Double-click `C:\AskIT\dxc-agentic-ai\START_DAY.bat` | Pulls today's content from the trainer and opens today's session page in your browser. **Keep the black window open all day.** |
| **During class** | Follow the session page. At each 🧪 lab card, open the file it names in VS Code and complete the TODOs. | Your XP, quiz answers and lab progress build up. |
| **End of class** | Last page of the session → click **🏁 Day End · Save & Push** | Saves your XP + exit ticket, checks your labs, commits and pushes to your GitHub fork. |

See your own progress any time at **http://localhost:8765/me** (**My Status**).\n\nDay End button didn't work? Double-click `DAY_END.bat` (backup). Still stuck → call the trainer.

---

## Folder map (same on every VM)

```
C:\AskIT\dxc-agentic-ai\
  START_DAY.bat        <- every morning
  DAY_END.bat          <- backup for the Day End button
  SETUP.bat            <- once, in Session 1
  me.json              <- your name, GitHub user, team (created by SETUP)
  .env                 <- your keys (NEVER shared, never pushed)
  Day01\Content\      <- Day 1 session page (opened for you by START_DAY)
  Day01\Labs\lab01-hello-llm\
      README.md        <- lab steps and challenges
      *.py             <- code with TODO-1, TODO-2 ... for you to complete
      *.md             <- AWS console steps (when a lab uses AWS)
      tests\           <- auto-checks (one per challenge)
      submission\      <- your evidence (outputs, trace links)
  askit_data\          <- helpdesk data: kb\, tickets.csv, users.csv
  askit_core\          <- shared code used by all labs
  teams\team-a ... d\  <- your team's ADRs and review-board files
  governance\          <- templates (ADR, ARB, SRB, PRR ...)
  progress\            <- written by Day End (XP + lab results). Don't edit.
  Day02\ Day03\ ...  <- each new day appears here (Content\ = session page, Labs\ = lab code)
  solutions\           <- released after each session
```

## Rules that keep everything working

1. The repo lives **only** at `C:\AskIT\dxc-agentic-ai`. Don't move or rename it.
2. Edit **only** files inside the `DayNN\Labs\` folders and your own `teams\team-x\` folder.
3. Don't edit `progress\` by hand — Day End writes it.
4. Never paste keys into code. Keys go in `.env` only.
5. Use **one browser** (Edge) for the session page — your XP is stored in that browser.
6. Keep the **START_DAY black window open** all class — it saves your progress to GitHub every 15 minutes.
7. Check a lab yourself any time — in the VS Code terminal:
   `pytest Day01\Labs\lab01-hello-llm`
