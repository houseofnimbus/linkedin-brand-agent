# LinkedIn Brand Agent

A two-pass LinkedIn engagement agent for marketing teams. Every morning it drafts
the day's comments for your brand. You click Approve, Edit, or Skip on each one.
It posts the approved ones and likes each post.

You set the brand voice. The agent shows up smartly. You stay in control.

Built for [Cowork](https://claude.ai/cowork). Requires Claude in Chrome and Google
Drive MCP.

---

## What problem does this solve?

Brand engagement on LinkedIn is the highest-leverage social channel for B2B and
operator-led brands, but most teams do it badly:

- They post their own content and ignore everyone else's.
- They drop generic "Great post!" comments that read worse than silence.
- They have no system, so engagement happens in bursts when someone remembers, then
  goes dark for weeks.

What works is the opposite: showing up with sharp, specific comments on posts in
your space, every day, in your brand's voice. The problem is *that takes 30–60
minutes a day*, and nobody on a marketing team has 60 minutes a day to spend
scrolling LinkedIn.

This agent compresses it to 5 minutes. The morning gather + draft pass is
automated. You spend the 5 minutes choosing which drafts to ship.

## How does it work?

Two passes, with you in the middle.

**Pass 1 — Morning gather and draft (automatic, at the time you set).**
The agent opens LinkedIn in your browser, scans your home feed plus the hashtags,
topic phrases, and target accounts you configured during setup. It scores every
candidate post on three axes (relevance to your brand, engagement potential, can
your brand add real value). It drops job posts, product announcements, role
changes, and milestone posts — the four categories that never sustain real
conversation. It picks the top N posts and drafts a comment for each one in your
brand's voice, choosing between three modes (sharp pushback, operator insight with
a brand fact, curious specific question). Drafts land in a widget called the
LinkedIn Digest, ready for review.

**Pass 2 — Review (whenever you have 5 minutes).**
Open the widget. For each draft, click Approve, Edit, or Skip. If you click Edit,
rewrite the comment in place. When you've gone through them, click Submit.

**Pass 3 — Post (automatic, triggered by your Submit).**
The agent goes back into LinkedIn and posts each approved comment, then likes the
post it commented on. It logs every result. 30–90 second delays between posts so
LinkedIn doesn't flag the account.

You stay in control of every word that leaves your account. The agent never posts
anything you didn't approve.

## Show me an example output

A morning digest looks like this (one entry — a real one would have 5 to 12):

```
## 3. Sarah Williams — General Manager at The Burnside Group

**Open post:**

https://www.linkedin.com/feed/update/urn:li:activity:0123456789/

**Author profile:** https://www.linkedin.com/in/example-slug/
**Excerpt:** Staff retention in QSR hit a new low this quarter. We've tried every
playbook. The pattern I keep seeing is that people don't leave for money, they leave
for predictability.
**Engagement:** ~89 reactions · ~16 comments · 8h old
**Source:** topic_search:staff retention restaurant
**Mode:** OPERATOR_INSIGHT
**Why this:** The "predictability over money" angle directly maps to the brand's
allowed-facts. Worth citing once.
**Score:** 9/10
```

The agent then drafts the comment in a fenced block:

> The predictability point lands. We see the same pattern across the 800+ restaurants
> we work with: payroll consistency moves retention more than the absolute number
> does. Once weekly pay stops being a question, half the resignation conversations
> stop happening.

And finishes with the Action line:

```
**Action:** `[ ] APPROVE   [ ] EDIT   [ ] SKIP`
```

In the widget, the same entry renders as a card with one-click Approve / Edit / Skip
buttons. See `examples/digest-example.md` for a full anonymised day.

## How do I install and use it?

Five things to do. The setup wizard does most of them for you.

1. **Install Claude in Chrome.** The agent uses it to read LinkedIn and post
   comments. Get it [here](https://claude.ai/chrome).
2. **Connect Google Drive MCP** to Cowork. The widget needs it to submit decisions.
   (You can skip this and use clipboard-fallback mode, but the widget experience
   is sharper with Drive.)
3. **Install this plugin** in Cowork. Either clone this repo into your plugins
   folder or use the Cowork plugin installer pointed at this repo.
4. **Run the setup wizard.** Type `/linkedin-setup` in any Cowork chat (or just
   say "set up the LinkedIn agent"). It walks you through 8 questions in about
   5 minutes — brand positioning, allowed facts, target accounts, hashtags,
   topic-phrase searches, domain guardrails, competitors, engagement schedule.
5. **Wait for tomorrow morning.** At the time you set, the first digest fires.
   Open the LinkedIn Digest widget, approve a few, click Submit.

For the full setup walkthrough including how to refine the agent over the first
two weeks, see [GUIDE.md](GUIDE.md).

---

## What this is *not*

- **Not a replacement for your own thinking.** The agent drafts. You approve. Every
  word that goes out is one you signed off on.
- **Not a tool for posting your own content.** The agent doesn't write your posts.
  It only comments on other people's posts.
- **Not safe at high volume.** LinkedIn flags accounts that comment 15–20+ times a
  day. The agent has a hard cap at 30/day and the recommended setting is 8.
- **Not a black box.** Every workflow, every voice rule, every guardrail lives in
  plain markdown files in your workspace. Edit them whenever the agent gets
  something wrong — each edit improves all future runs.

## Credits

The architecture (two-pass approval, scheduled digest, file-as-source-of-truth,
markdown-card-and-widget review surface) is loosely modelled on
[autodecision](https://github.com/harshilmathur/autodecision) by Harshil Mathur.

The voice framework (three modes, length calibration, the angle test, the hard-cap
on citations) was developed iteratively over months of running comments for a real
brand. Most of the rules in `voice-template.md` were learned by getting them wrong
first.

## License

MIT. See [LICENSE](LICENSE).
