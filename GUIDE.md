# LinkedIn Brand Agent — Setup and Operating Guide

Everything you need to install, configure, and refine the agent. If you've read the
README and want depth on a specific section, find it below.

---

## Contents

1. [What you get when you install](#what-you-get-when-you-install)
2. [Preflight requirements](#preflight-requirements)
3. [Setup wizard — the 8 questions explained](#setup-wizard--the-8-questions-explained)
4. [Day 1 — what to expect](#day-1--what-to-expect)
5. [The first two weeks — how to refine](#the-first-two-weeks--how-to-refine)
6. [Customising config.md](#customising-configmd)
7. [Customising voice.md](#customising-voicemd)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## What you get when you install

A folder on your machine (location is your choice — the setup wizard asks) that
contains:

- `config.md` — your engagement settings, hashtags, target accounts, blocklist
- `voice.md` — your brand voice, allowed-facts list, three comment modes
- `workflow-digest.md` — the morning gather + draft workflow
- `workflow-post.md` — the posting + auto-like workflow
- `digest-template.md` — the output format
- `scheduled-tasks/` — the prompts that fire the morning task
- `scripts/` — Python helpers for the widget integration
- `digests/` — where each day's digest .md file lives

Plus two things registered with Cowork:

- A scheduled task `linkedin-daily-digest` that runs every morning (or 2–3 times
  per day, your choice) at the time you set
- A widget called the LinkedIn Digest that renders the day's drafts for review

## Preflight requirements

Before running the setup wizard:

**Claude in Chrome MCP** must be installed and connected. The agent uses it to read
LinkedIn (your home feed, hashtags, search) and to post comments. Without it,
nothing works. Install from `https://claude.ai/chrome` and confirm it shows up
in Cowork's MCP list.

**A logged-in LinkedIn session in Chrome.** The agent uses your existing browser
session — it does not log in, it does not store credentials. If you're logged out,
the agent will halt at the login wall and tell you.

**Google Drive MCP** is *recommended but not required*. The widget submits decisions
through a Drive write because it's the most reliable cross-platform channel. If you
don't have Drive connected, the widget falls back to clipboard mode — clicking
Submit copies a base64-encoded payload to your clipboard that you paste into Cowork
chat to trigger posting. Works fine, just one extra step.

**Scheduled tasks** must be enabled in Cowork. Check Settings → Capabilities.

## Setup wizard — the 8 questions explained

Type `/linkedin-setup` in any Cowork chat. The wizard walks through:

**1. Brand positioning (1–3 sentences)** — Who is this brand, who does it serve,
what's the operator lens? This sets the voice for every comment. Be specific.
"We're a friendly SaaS for SMBs" is bad — every brand says that. "We're a payroll
product for restaurants; we've shipped 800+ small operators through tipping
seasons; our brand should sound like someone who's worked a Friday night shift,
not a HR consultant" is good. The wizard pushes back once if you give a generic
answer.

**2. Allowed facts (3–5 specific facts)** — Real numbers, real moments, real
results from the brand's work. These are the only specifics the agent will cite in
OPERATOR_INSIGHT mode. Each fact should be verifiable if anyone asked. Examples:
"Reduced churn from 14% to 6% by adding a weekly retro flow", "Cut deploy time
from 40 minutes to 8 by parallelising the test suite". The agent never invents
new facts — if a comment needs a number you didn't supply, it picks a different
angle or drops the post.

**3. Target accounts (5–10 LinkedIn accounts)** — People whose posts you most want
the brand to show up under. Prospects, influencers, partners, decision-makers.
Posts from these accounts get a +2 boost to their relevance score. The wizard
accepts names; you can optionally add profile URLs for your own reference.

**4. Hashtags (5–12)** — Active hashtags in your space. Not too broad
(`#marketing` alone surfaces too much), not too narrow (brand-specific tags
won't have volume). The agent scans these every morning and also runs a Monday
hashtag-discovery pass that suggests new ones based on what's appearing in your
feed.

**5. Topic-phrase searches (4–8)** — Short phrases the agent searches LinkedIn
content for. Catches posts that hashtags miss. Examples: `attribution dashboard`,
`D2C brand`, `in-housing creative`. Pick phrases your brand has a real angle on,
not just topics you find interesting.

**6. Domain guardrails (optional)** — If your brand operates in a regulated or
sensitive domain — healthcare, legal, finance, education — list rules the agent
applies to every draft. Examples: "No medical advice", "No investment guarantees",
"No outcome promises". If your brand isn't regulated, skip this question.

**7. Competitor blocklist** — Names the agent never mentions in any comment, even
neutrally. Include both direct competitors and any brands you don't want to be
associated with publicly.

**8. Engagement schedule** — How often the agent runs and how many drafts per run.
The wizard offers four sensible combinations and refuses anything above the safety
cap (30 comments/day). Recommended starting point: 1 run/day at 10am local with
8 drafts. You can scale up after two weeks if the rhythm is comfortable.

After question 8, the wizard asks for your Google Drive MCP tool ID (if you have
Drive connected) and then writes everything to your workspace, registers both
scheduled tasks, and creates the artifact.

## Day 1 — what to expect

The first morning after setup:

1. At the time you set, the scheduled task fires. The agent opens LinkedIn, scans
   your feed and your configured sources, and drafts comments for the top posts.
2. A Cowork notification appears: "Today's digest is ready — 8 drafts."
3. Open the LinkedIn Digest widget (or open the digest .md file in your workspace).
4. For each draft, you have three buttons: Approve, Edit, Skip.
   - **Approve** — post the draft verbatim.
   - **Edit** — rewrite the comment in place (click in the comment box, type your
     version, click Edit again to confirm the action).
   - **Skip** — don't post this one.
5. When you've gone through them, click Submit at the bottom.
6. The posting agent fires automatically. It opens LinkedIn, verifies each post URL,
   posts each approved comment, likes the post, waits 30–90 seconds, moves to the
   next.
7. When done, a Cowork notification confirms results: "Posted 5 of 7. Liked 5 of 7.
   2 skipped."

The whole review takes 5 minutes the first day, less once you've calibrated.

**Expect the first few digests to feel mid.** The agent doesn't know your brand
yet. The drafts will be in the right shape but the voice will need tuning. That's
what the next two weeks are for.

## The first two weeks — how to refine

The agent gets sharper the more you tell it what to drop. After each digest, take
60 seconds to notice patterns:

- **A draft that should have been killed.** Add a line to `voice.md` under
  "Hard rules" about why it doesn't work, or add a banned phrase if a specific
  word keeps showing up.
- **A draft that was almost there.** Edit it once, then look at what you changed.
  If you keep making the same edits, write them up as a rule in `voice.md`.
- **A post you skipped because the agent shouldn't have surfaced it.** Add the
  matching keyword to `config.md > blocked_keywords`, or add the post-type to the
  filter if it's a recurring shape.
- **A target account that got picked over and over with weak drafts.** Reconsider
  whether they should be a target — sometimes someone's content just doesn't fit
  the brand's angle.

This is the part most agent tools skip. The system is designed to be improved by
the user, not magically perfect on day 1. Five minutes of curation per day for
two weeks turns it into something sharp.

## Customising config.md

The wizard writes most of this, but here's what each section does — useful when
you want to edit by hand.

**`runs_per_day` and `drafts_per_run`** — change these to scale engagement up or
down. Total daily output is `runs_per_day × drafts_per_run`, capped at
`hard_daily_cap_comments` (default 30, do not raise above 25 unless you're
willing to risk LinkedIn flagging).

**`hashtags:`** — add or remove anytime. The agent reads on every run. If a
hashtag stops surfacing good posts, move it to a comment block to disable.

**`target_accounts:`** — add anyone whose attention helps your brand. The
priority boost is +2 to score. There's a soft cap of `target_account_author_cap`
(default 3) so the same target doesn't dominate every digest.

**`blocked_authors:` and `blocked_keywords:`** — your mute list. The agent skips
matches before scoring.

**`strict_post_type_filter`** — four toggles. All default `true` and you almost
never want to flip any of them off. These drop job posts, product launches, role
announcements, and milestone posts — the four categories that never sustain a
real comment discussion.

**`domain_guardrails:`** — list rules the agent must apply. The agent runs every
draft through this check before adding it to the digest.

**`competitors:`** — names never mentioned in any comment.

**`trending_signals`** — boosts scores for posts gaining traction. Adjust
thresholds if your feed is much busier or quieter than typical.

**`extra_gather_sources`** — the topic-phrase search list and the
high-comment-density toggle. Edit the search phrases to catch the shape of
conversations your brand has an angle on.

**`voice_mix`** — the rough split between question, sharp POV, and operator
insight modes. Adjust if you want more or less of any mode.

**`max_drafts_with_citation`** — hard cap on how many drafts per digest may cite
a specific allowed-fact. Default 2. Keep it low — too many citations and the
brand sounds like it's flexing.

## Customising voice.md

The wizard writes the positioning and allowed-facts. The rest is the operating
manual for the brand's voice — edit it whenever the agent gets a draft wrong.

**Brand positioning** — the 1–3 sentence summary. Rewrite when the brand's
positioning shifts.

**Voice texture rules** — bullets about plain words over technical terms, short
declarative sentences, the angle test (solution / most-important-aspect /
what-should-be-tracked). These travel across brands without much editing.

**The three modes** — SHARP_POV, OPERATOR_INSIGHT, CURIOUS_QUESTION. Each has a
format spec, good and bad examples, and rules for when to use it. Add your own
"good example" once you've seen a draft that nailed it — the agent will reference
your example on future runs.

**Allowed facts** — the engine of OPERATOR_INSIGHT. Add a fact whenever the brand
ships something quotable. Remove a fact if it stops being current.

**Hard rules** — the things never to do. Banned phrases (em dashes, AI filler,
generic agreement), no tagging, no hashtags in comments. Add a banned phrase
when you keep editing the same word out of drafts.

**Length calibration** — per-mode length targets. Tighten if comments feel long;
loosen if they feel clipped.

**Self-check** — what the agent verifies before adding a draft to the digest.

## Troubleshooting

**No digest appeared this morning.** Check the Cowork sidebar → Scheduled tasks
→ `linkedin-daily-digest`. If the task ran but failed, the failure shows there
or in the digest file. Most common cause: not signed in to LinkedIn in Chrome.

**Digest appeared but all drafts feel generic.** Tighten `voice.md` — add
banned phrases, sharpen the positioning, add more specific allowed-facts. Then
re-run the digest manually by saying "run my LinkedIn agent" in Cowork.

**Same author keeps showing up every day.** Increase `max_author_appearances_in_7d`
in `config.md > cross_day_dedup`. Or add the author to `blocked_authors` if you
genuinely want them muted.

**Widget submit failed with "Drive write returned error".** The widget falls
back to clipboard mode automatically — your decisions are copied as a `post
eyJ...` payload. Paste that into Cowork chat to trigger posting. To fix Drive,
check the Google Drive MCP connection status in Cowork settings.

**LinkedIn challenge appeared mid-post.** The agent stops immediately and logs
results so far. Solve the challenge manually in your browser, then say "post
my approved LinkedIn comments" in chat to resume the batch.

**Comment posted but the like didn't register.** Logged as `like_failed` in the
post results. Usually due to LinkedIn UI variation — the agent looks for the
Like button on the post but sometimes the selector misses. The comment is still
live; the like just didn't fire. You can manually like the post in your browser.

**Too many URLs failed verification.** If 3+ URLs need recovery in one run, the
agent flags it in chat. LinkedIn occasionally changes the DOM selectors used to
capture URLs — open an issue on the repo or update `workflow-digest.md` Step 2
with the new selectors.

## FAQ

**Can I use this for my personal LinkedIn instead of a brand?**
Yes. The setup wizard's "positioning" question absorbs either framing. You'd
phrase it as "I'm a marketing leader who's run X kind of work, comments should
sound like an operator thinking out loud." Everything else works the same.

**Does this work outside India / outside English?**
Probably, but it hasn't been tested. The voice rules and length calibration are
English-specific. Hashtag, target-account, and content-search mechanics work
regardless of region. If you try a non-English run, open an issue with what
worked and what didn't.

**How is this different from posting AI-generated comments at scale?**
Two ways. First, you approve every comment — the agent never posts without your
explicit approval. Second, the system is designed to *teach* you what good
engagement looks like, not to flood LinkedIn with mediocre output. The
recommended volume is 8 comments/day, not 80.

**Can the agent reply to comments on the brand's own posts?**
Not in v1. The current scope is top-level comments only. Reply handling would
need separate workflows (different voice rules, different volume caps).

**What's the data flow? Does the agent see my personal LinkedIn?**
It uses your existing logged-in browser session via Claude in Chrome MCP. It
never stores credentials. The only data persisted is in your workspace folder
(digests, configs) — nothing leaves your machine except the LinkedIn read/post
traffic to LinkedIn itself.

**Can I disable the auto-like?**
No, it's coupled to commenting by design. Commenting without liking reads as
drive-by criticism. If you want a no-like flow, fork the repo and remove Step 4.7
from `workflow-post.md`.

**How do I uninstall?**
Three things: delete the scheduled tasks (Cowork sidebar → Scheduled → delete
`linkedin-daily-digest` and `linkedin-post`), delete the artifact (Cowork
artifacts → delete `linkedin-digest`), and delete your `LINKEDIN_AGENT_HOME`
folder. That's it.
