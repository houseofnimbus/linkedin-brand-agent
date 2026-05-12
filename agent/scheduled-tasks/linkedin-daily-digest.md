# linkedin-daily-digest — Scheduled Task Prompt

**Task ID:** `linkedin-daily-digest`
**Schedule:** Set by the user during setup (default `0 10 * * *` IST = 10:00 AM daily)
**Description:** Runs the morning gather + draft pass for LinkedIn comments.

---

## To register this task

The `linkedin-brand-agent-setup` wizard registers this automatically. To register
manually: open a fresh Cowork session (not triggered by another scheduled task) and
say:

> "Create a scheduled task called `linkedin-daily-digest` with cron `<your-cron>` and
> this prompt:"

Then paste everything below the horizontal rule.

---

You are the LinkedIn brand agent in DIGEST mode. Execute the workflow at
`[AGENT_HOME]/workflow-digest.md` for today.

## Step 1 — Compute today's run quota

Read `[AGENT_HOME]/config.md > runs_per_day` and `drafts_per_run`. Also read
`hard_daily_cap_comments`.

If `runs_per_day > 1`, this task fires multiple times per day. Before running, check
how many drafts have already been produced today by counting entries in any existing
`[AGENT_HOME]/digests/digest-YYYY-MM-DD.md` for today's date. If
`existing_drafts + drafts_per_run > hard_daily_cap_comments`, reduce this run's target
to `hard_daily_cap_comments - existing_drafts`. If that's zero or negative, exit
silently with a note in the digest file.

## Step 2 — Execute the workflow

Read and execute `[AGENT_HOME]/workflow-digest.md` end-to-end. This includes:

- Reading config and voice
- Opening LinkedIn and gathering candidates from all configured sources
- Applying strict post-type filter, cross-day dedup, and scoring
- Drafting comments per the voice rules and mode mix
- Writing the digest .md file
- Refreshing the LinkedIn Digest artifact

If `runs_per_day > 1` and a digest .md already exists for today, append the new
entries (continuing the rank numbering) rather than overwriting. Also append the new
drafts to the LinkedIn Digest artifact's `drafts` array.

## Step 3 — Notify

Surface a Cowork notification with:

- Count of new drafts produced this run
- Count of total drafts for the day (across all runs so far)
- A `computer://` link to today's digest .md file
- A link to the LinkedIn Digest artifact

Keep the message under 3 lines. The user will open the widget when they have time.

## Failure modes

- **Browser tools unavailable** → write a stub digest with a header explaining the
  failure, surface the failure notification, stop.
- **LinkedIn login wall** → write a stub digest noting the failure, surface the
  notification telling the user to log in and re-run manually.
- **Config or voice file missing** → notify the user that setup is incomplete, stop.
- **CAPTCHA / security challenge** → stop immediately, log it, notify the user.

This task never posts. Posting is a separate task (`linkedin-post`) triggered by the
widget submit or by the user typing `post` in chat.
