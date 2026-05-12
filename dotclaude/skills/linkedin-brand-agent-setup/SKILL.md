---
name: linkedin-brand-agent-setup
description: Set up the LinkedIn Brand Agent for a user. Walk them through configuring their brand positioning, allowed facts, target accounts, hashtags, blocklist, domain guardrails, engagement schedule, and Google Drive integration. Copy the agent templates into their workspace, register the two scheduled tasks (linkedin-daily-digest and linkedin-post), and create the LinkedIn Digest artifact. Trigger when the user runs /linkedin-setup, says "set up the LinkedIn agent", "install the LinkedIn brand agent", "configure my LinkedIn agent", or any first-run intent for this plugin.
---

# LinkedIn Brand Agent — Setup Wizard

You are setting up the LinkedIn Brand Agent for a new user. The plugin is installed
and you have access to its `agent/` folder of templates and workflows. Your job is to
walk the user through the configuration questions, write their answers into their
workspace, register two scheduled tasks, and create the LinkedIn Digest artifact.

This is a 5-minute conversation if the user has their answers ready. Take it slowly
if they need to think.

## Before you start — preflight checks

Confirm these three things are in place. If any is missing, tell the user and stop.

1. **Claude in Chrome MCP** is installed. Test by calling
   `mcp__Claude_in_Chrome__list_connected_browsers`. If it fails or returns nothing,
   the user needs to install Claude in Chrome before this agent will work.
2. **Google Drive MCP** is connected. The widget submits decisions through a Drive
   write. Without it, the widget falls back to clipboard mode, which works but is
   clunky. Ask the user whether Drive is connected — if not, offer to proceed in
   clipboard-only mode and warn them about the trade-off.
3. **Scheduled tasks** are enabled in Cowork (Settings → Capabilities). If not, the
   user must enable them before the daily digest will fire.

## Step 1 — Pick the agent home folder

Ask: "Where should I put your LinkedIn agent files? This is the folder the agent
will read its config from and write digests to. I recommend a dedicated folder like
`Desktop/LinkedIn-Agent/` so it's easy to find."

Wait for an absolute path. Confirm it. If the folder doesn't exist, create it with
bash (`mkdir -p`). Remember this path as `AGENT_HOME` for the rest of setup.

## Step 2 — Brand positioning

Ask: "In 1–3 sentences, who is this brand and what's its operator lens? This sets
the voice for every comment. Bad answer: 'We're a friendly SaaS company helping
businesses grow.' Good answer: 'We're a payroll product for restaurants. We've
helped 800+ small operators run weekly payroll through tipping season. The brand
voice should sound like someone who has actually run a restaurant Friday-night
shift, not like a HR consultant.'"

Wait for their answer. If it's generic, push back once: "Can you make that more
specific? What's the one thing the brand has actually done that gives it the right
to opinion?" Then accept whatever they give.

Save as `POSITIONING_TEXT`.

## Step 3 — Allowed facts

Ask: "List 3–5 specific facts from your brand's work that you'd be willing to cite
in comments. Each fact should be: specific (a real number, a real moment), verifiable
if anyone asked, and the kind of thing only an operator would know. Format them as
one fact per line."

Examples to share if they're stuck:

- "Helped 800+ restaurants run payroll through tipping season"
- "Reduced churn from 14% to 6% by adding a weekly retro flow"
- "Cut deploy time from 40 minutes to 8 by parallelising the test suite"

Wait for 3–5 facts. If they give fewer, accept it — they can add more later by
editing `voice.md`.

Save as `ALLOWED_FACTS` (a list).

## Step 4 — Target accounts

Ask: "Name 5–10 LinkedIn accounts whose posts you most want the brand to engage
with. These can be prospects, influencers, partners, or anyone whose attention
matters to the brand's goals. Posts from these accounts get a priority lift in the
scoring. Format: one per line, name as it appears on their profile. Optionally add
their profile URL on the next line."

Wait for 5–10 names. Accept fewer if that's what they have.

Save as `TARGET_ACCOUNTS` (a list of `(name, profile_url_optional)` tuples).

## Step 5 — Hashtags

Ask: "Name 5–12 hashtags that are active in your brand's space. The agent will scan
these for posts to engage with. Pick hashtags that are not too broad (e.g. just
`#marketing`) and not too narrow (e.g. brand-specific). Comma-separated or one per
line, both work."

Save as `HASHTAGS` (a list).

## Step 6 — Topic-phrase search terms

Ask: "List 4–8 short phrases the agent should search LinkedIn content for. These
catch posts that hashtags miss — operator-grade language people use in posts even
when they don't tag them. Examples: 'attribution dashboard', 'D2C brand', 'in-housing
creative'. Pick phrases your brand has a real angle on."

Save as `TOPIC_SEARCH_PHRASES` (a list).

## Step 7 — Domain guardrails

Ask: "Does the brand operate in a regulated or sensitive domain — healthcare, legal,
finance, education, anything with strict content rules? If yes, list rules the agent
must apply to every comment. If no, just say 'no' and we'll skip this. Examples:
'No medical advice', 'No investment guarantees', 'No outcome promises'."

If they say no, set `DOMAIN_GUARDRAILS` to an empty list. Otherwise capture the
rules as a list.

## Step 8 — Competitor blocklist

Ask: "Are there competitor brand names the agent should never mention in comments?
List them comma-separated, or say 'none' to skip."

Save as `COMPETITORS` (a list).

## Step 9 — Engagement schedule

Ask: "How often should the agent run, and how many drafts per run? More runs = more
reach, but LinkedIn rate-limits comments above ~15–20/day. The safety cap is 30
comments/day across all runs."

Offer four sensible combinations:

| Choice | Runs/day | Drafts/run | Total comments/day | Best for |
|--------|----------|-----------|--------------------|----------|
| A | 1 | 5 | 5 | Just starting out, low risk |
| B | 1 | 8 | 8 | Default, balanced (recommended) |
| C | 2 | 8 | 16 | Active brand, more reach |
| D | 3 | 8 | 24 | Aggressive engagement, near the rate-limit edge |

Let them choose A/B/C/D or specify custom values. Refuse combinations that exceed
30/day total.

Save as `RUNS_PER_DAY` and `DRAFTS_PER_RUN`.

Then ask: "What time(s) of day should the daily digest fire? Default is 10:00 AM
local. If you picked multiple runs per day, also specify the second/third time —
morning + late afternoon works well, or split them into morning/midday/evening."

Build the cron expression(s). For runs_per_day=1: `0 <hour> * * *`. For 2 or 3 runs,
register the SAME task multiple times with different cron expressions, or use a
single task with a list of cron triggers if Cowork supports it.

## Step 10 — Google Drive MCP tool ID

If the user confirmed Drive in preflight, ask: "What's your Google Drive MCP tool
ID? It looks like `mcp__<hash>__create_file`. You can find it by looking at your
installed MCP servers list in Cowork Settings."

Save as `GDRIVE_CREATE_FILE_TOOL_ID`.

If they don't have Drive connected, set this to the placeholder and tell them: "OK,
the widget will fall back to clipboard mode — when you click Submit, it will copy a
payload to your clipboard that you paste into chat to trigger posting. Less polished
but works fine. You can connect Drive later and re-run this step."

## Step 11 — Write the config files into the user's workspace

Now you have everything. Copy the templates from the plugin's `agent/` folder into
`AGENT_HOME` and substitute placeholders. Use bash:

```bash
# Copy the workflow files (no substitutions needed except [AGENT_HOME])
cp -r [PLUGIN_PATH]/agent/workflows/* "$AGENT_HOME/"
cp -r [PLUGIN_PATH]/agent/scheduled-tasks "$AGENT_HOME/scheduled-tasks"
cp -r [PLUGIN_PATH]/scripts "$AGENT_HOME/scripts"
mkdir -p "$AGENT_HOME/digests"
```

Then for each workflow file in `$AGENT_HOME/`, substitute `[AGENT_HOME]` with the
real path. Use sed in-place:

```bash
find "$AGENT_HOME" -type f -name "*.md" -exec sed -i.bak "s|\[AGENT_HOME\]|$AGENT_HOME|g" {} \;
find "$AGENT_HOME" -name "*.bak" -delete
```

For the `linkedin-post.md` scheduled-task prompt, also substitute the Drive tool ID:

```bash
sed -i.bak "s|<gdrive-tool-id>|${GDRIVE_CREATE_FILE_TOOL_ID//mcp__/mcp__}|g" \
  "$AGENT_HOME/scheduled-tasks/linkedin-post.md"
```

Now build the filled `config.md` and `voice.md`. Read each template and substitute
the captured values. Write the results to `$AGENT_HOME/config.md` and
`$AGENT_HOME/voice.md`. Use the Edit or Write tool for this (it's text manipulation
of a longer file — easier to do via Read+Write than sed for complex substitutions).

Substitutions for `config.md`:

- `runs_per_day: 1` → `runs_per_day: $RUNS_PER_DAY`
- `drafts_per_run: 8` → `drafts_per_run: $DRAFTS_PER_RUN`
- The `hashtags:` block — replace the example list with `$HASHTAGS`
- The `target_accounts:` block — replace with `$TARGET_ACCOUNTS`
- The `domain_guardrails:` block — replace with `$DOMAIN_GUARDRAILS` (or an empty
  list with a comment if user said no)
- The `competitors:` block — replace with `$COMPETITORS`
- The `topic_search_phrases:` block — replace with `$TOPIC_SEARCH_PHRASES`

Substitutions for `voice.md`:

- `[YOUR_POSITIONING]` → `$POSITIONING_TEXT`
- The `allowed_facts:` block — replace with `$ALLOWED_FACTS`

## Step 12 — Set the LINKEDIN_AGENT_HOME env var

The Python scripts find the digest file via the `LINKEDIN_AGENT_HOME` env var or a
glob fallback. Set the env var so scripts run reliably:

```bash
# Linux/Mac:
echo "export LINKEDIN_AGENT_HOME=\"$AGENT_HOME\"" >> ~/.bashrc

# Windows (PowerShell):
[System.Environment]::SetEnvironmentVariable('LINKEDIN_AGENT_HOME', '$AGENT_HOME', 'User')
```

Tell the user: "I've set `LINKEDIN_AGENT_HOME` so the scripts can find your digest
folder. The agent will still work without it via path globbing, but the env var is
the cleanest setup."

## Step 13 — Register the scheduled tasks

Use `mcp__scheduled-tasks__create_scheduled_task` twice.

**Task 1 — `linkedin-daily-digest`:**

- Task ID: `linkedin-daily-digest`
- Cron(s): the cron(s) from Step 9 (one or multiple)
- Description: "Daily LinkedIn comment digest — gathers posts, scores them, drafts
  comments for review."
- Prompt: the content of `$AGENT_HOME/scheduled-tasks/linkedin-daily-digest.md`
  (from below the horizontal rule)

**Task 2 — `linkedin-post`:**

- Task ID: `linkedin-post`
- Cron: none (ad-hoc, triggered from widget)
- Description: "Posts the user's approved LinkedIn comments and likes each commented
  post. Triggered by the LinkedIn Digest widget's Submit button."
- Prompt: the content of `$AGENT_HOME/scheduled-tasks/linkedin-post.md`
  (from below the horizontal rule)

Confirm both are registered.

## Step 14 — Create the LinkedIn Digest artifact

Read the template from `[PLUGIN_PATH]/artifacts/linkedin-digest.html`. Substitute:

- `[TODAY_DATE]` → today's date in YYYY-MM-DD format (use bash `date +%Y-%m-%d`)
- `[GDRIVE_CREATE_FILE_TOOL_ID]` (in both the `mcpTools` JSON and the
  `GDRIVE_TOOL` JS constant) → `$GDRIVE_CREATE_FILE_TOOL_ID`

Use `mcp__cowork__create_artifact` with:

- `title`: `linkedin-digest`
- `widget_code`: the substituted HTML
- A short loading message

Confirm the artifact is created.

## Step 15 — Confirm and offer a dry run

Tell the user: "Setup done. Here's what you'll have:

- `LINKEDIN_AGENT_HOME` → `$AGENT_HOME`
- Scheduled task `linkedin-daily-digest` runs at `<cron-time>`
- Scheduled task `linkedin-post` triggered by the LinkedIn Digest widget
- Artifact `linkedin-digest` ready to receive drafts

Tomorrow morning at `<cron-time>`, you'll get your first digest in the widget. Want
me to do a dry run now to test the gather and draft flow? I'll write the digest but
won't post anything."

If yes: trigger `linkedin-daily-digest` manually via `mcp__cowork__runScheduledTask`
or just execute `workflow-digest.md` directly. Show the user the resulting digest
and the populated widget. Walk them through approving one comment and submitting,
so they see the full loop.

If no: leave them with one piece of advice — "After the first real digest tomorrow,
edit `voice.md` and `config.md` to refine. The agent gets sharper the more you tell
it what to drop."

## Edge cases

- **User wants to re-run setup later.** Re-running is safe — confirm with them
  first, then re-execute the steps. Their existing digests are preserved.
- **User runs setup before installing Claude in Chrome.** Refuse with a clear
  message: "I need Claude in Chrome installed first. Once that's in place, type
  `/linkedin-setup` again and I'll continue."
- **User has no Google Drive MCP.** Proceed in clipboard-only mode (skip Step 10).
  The widget's `clipboardFallback` handles this.
- **User wants a per-brand version, not personal.** The wizard already accommodates
  this — the positioning question absorbs either personal or brand framing. No
  special handling needed.
