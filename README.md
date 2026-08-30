# Token Ledger

A Claude Code plugin that shows you where your AI usage costs are actually
going — broken down by skill, plugin, and tool — live, right in your
terminal, while you work.

## What it does

Token Ledger reads your own Claude Code session data as you use it, and
shows a running line in your status bar like:

```
💰 $11.17 this session · general 95% · Bash 5%
```

So you can see, in real time, what's actually costing you tokens — not
just a total number, but which skill, plugin, or tool is behind it.

## Privacy

Nothing here ever leaves your machine. Token Ledger only reads files
already sitting on your own computer, and never sends anything anywhere —
no servers, no accounts, no network calls. That's not a footnote, it's the
whole design.

## Install

1. Clone or add this plugin to your Claude Code plugins.
2. Add this to your `~/.claude/settings.json` (or your project's
   `.claude/settings.json`):

```json
{
  "statusLine": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/statusline.py"
}
```

3. That's it — the status line starts showing your live cost breakdown
   automatically.

## How it works

Under the hood: a small pipeline reads your session's log file, filters
out noise and duplicate entries (a real bug found and fixed during
development), figures out which skill/plugin/tool was active for each
entry, and estimates a dollar cost using known Claude pricing.

See [`docs/superpowers/specs/design.md`](docs/superpowers/specs/design.md)
for the full design reasoning, including a scope change partway through.

## Limitations (and why)

- **Pricing can go stale.** Dollar amounts come from a small hardcoded
  pricing table. Anthropic doesn't offer a public API for checking current
  prices — the only cost-related endpoint (an Admin API) needs special
  admin credentials most people won't have, and even then it reports your
  own account spend, not general pricing rates. So this needs a manual
  update in `lib/pricing.py` whenever prices change.
- **Attribution relies on naming patterns.** To figure out which plugin was
  used, the code looks at the *name* of the action taken — plugin-provided
  actions are named like `mcp__plugin_claude-mem_...`, with the plugin's
  name built right into the name itself. If Claude Code ever changes this
  naming convention, the detection logic here would need updating to match.
- **Standalone MCP servers aren't cleanly labeled.** This only recognizes
  MCP tools that come bundled with an installed plugin. If someone adds an
  MCP server directly (not through a plugin), its usage falls into the
  generic `tool` bucket under its raw technical name, instead of being
  cleanly attributed.
- **One manual setup step required.** Claude Code doesn't currently let a
  plugin automatically turn on the status line for you — you have to add
  one line to your own settings file yourself (see Install above). This is
  a limitation of Claude Code's plugin system itself, not something this
  project can work around.
- **Shows only the current session, not history — on purpose.** Other tools
  already cover "historical spending report" well — like
  [`ccusage`](https://github.com/ryoppippi/ccusage), a popular open-source
  tool with great day/month/session reports, or Claude Code's own built-in
  `/usage` and `/insights` commands. None of them show a **live, in-session
  breakdown by skill/plugin/tool** while you're actively working, though —
  that's the specific, real gap Token Ledger fills. It's not trying to
  replace tools that already do historical reporting well.
- **Re-reads the whole session file on every refresh.** Fine for now;
  could get slower on very long sessions.

## Possible future improvements

- Cache parsed results instead of reprocessing the whole file each refresh
- Revisit attribution logic if Claude Code's internal naming ever changes
- Optionally add a historical report command back in, if there's real demand

## Development

```bash
python3 -m pytest
```
