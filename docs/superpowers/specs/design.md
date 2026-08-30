# Token Ledger — v1.0.0 Design
(Written Aug 26, 2026)

**Note: scope was revised on Aug 27 — see the update at the end of this doc for what is actually being built.**

## What this is
A Claude Code plugin that reads your own Claude Code session log files and
shows a report of where your tokens and money went — split by skill, plugin,
and tool. It's a spending report, not a live counter. Everything happens on
your own computer; nothing gets sent anywhere.

## Goals (v1.0.0)
- Read real session log files without crashing, even on weird or unexpected data
- Count tokens correctly, even when one AI turn shows up as multiple lines
  (a real bug we found — see below)
- Sort usage into 4 groups: skill, plugin, tool, or general (catch-all)
- Show both the raw token count and an estimated dollar cost for each group
- A `/cost-report` command that prints a text summary
- An HTML dashboard — the same info, shown visually
- Filters: only show the last N days, or group by skill/plugin/tool

## Not doing in v1.0.0
- A live, real-time usage counter — decided against this for now. It can
  reuse this same counting logic later, just pointed at today's session
  file instead of a finished one — so this isn't a dead end, just not v1.
- OpenTelemetry-based advanced mode — a stretch goal, only after v1 ships
- Changing or deleting your log files — this tool only reads, never writes
  to your Claude Code data

## Where the data comes from, and a real bug we found
Claude Code saves one log file per session here:
```
~/.claude/projects/<project-name>/<session-id>.jsonl
```
Each line is one event, saved as JSON. Some lines are just internal notes
(like `"type":"queue-operation"`) — we skip those. The lines we care about
say `"type":"assistant"` and have a `usage` section with token counts inside.

**Real bug found by checking an actual file:** when the AI does two things in
one turn, the file writes that as two separate lines — but both lines show
the exact same cost. In one real file: 403 lines looked like AI replies, but
only 218 were actually unique. If we don't catch this, some costs get
counted twice. The fix: remove duplicates by message ID before adding
anything up.

## Folder structure
```
token-ledger/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── cost-report.md
├── lib/
│   ├── parser.py
│   ├── attribution.py
│   ├── pricing.py
│   ├── aggregate.py
│   └── dashboard.py
├── tests/
├── .gitignore
├── LICENSE
└── README.md
```

## How we handle errors
If a line doesn't make sense, skip it — don't crash. Keep a simple count of
"X lines skipped" so nothing's hidden, but one weird line should never break
the whole report. Claude Code's log format could change over time, so the
tool needs to bend, not break.

## How we test it
- Using pytest, one test file per piece of code
- Test data is small and made-up — never real private logs
- One test specifically checks the "counted twice" bug never comes back
- Before calling v1 done, manually check the numbers against 2-3 real files

## Privacy
This tool never sends your data anywhere. It only reads files already on
your computer, and only writes a report file also on your computer. That's
a main selling point of this project, not a small detail.

## Update (Aug 27, 2026) — scope change
Originally planned: `/cost-report` command + HTML dashboard.
After researching existing tools - specifically `ccusage` (a popular CLI tool
that already covers historical cost reporting well, by day/month/session) and
Claude Code's own built-in `/usage` and `/insights` commands - the real gap
isn't historical reporting, it's a **live, in-session view** of cost broken
down by skill/plugin/tool, which none of these provide. Dropping the HTML
dashboard and `/cost-report` command from v1. New v1 goal: a status-line
script showing cost + skill/plugin/tool breakdown, updating automatically
after each message.
