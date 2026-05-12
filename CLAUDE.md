# CLAUDE.md — Instructions for Claude Code Users

This file is read by Claude when this plugin is loaded. If you're using Claude Code
to work with the LinkedIn Brand Agent, here's what you need to know.

## What this plugin does

A two-pass LinkedIn engagement agent. Drafts comments every morning, lets the user
approve them in a widget, then posts the approved ones and likes the post.

Full overview: [README.md](README.md). Full setup walkthrough: [GUIDE.md](GUIDE.md).

## How the pieces fit together

The user runs `/linkedin-setup` (or says "set up the LinkedIn agent") on first install.
That triggers the `linkedin-brand-agent-setup` skill, which walks them through 8
configuration questions and writes filled-in versions of `config.md` and `voice.md`
into their workspace folder (path of their choosing — typically
`Desktop/LinkedIn-Agent/`).

The setup wizard also:

- Copies workflow files (`workflow-digest.md`, `workflow-post.md`,
  `digest-template.md`) into the user's workspace, substituting `[AGENT_HOME]` with
  the real path
- Copies the Python scripts (`commit-widget-state.py`, `verify-digest-urls.py`) into
  the user's workspace
- Sets the `LINKEDIN_AGENT_HOME` environment variable to the workspace path
- Registers two scheduled tasks (`linkedin-daily-digest`, `linkedin-post`) using
  prompts from `agent/scheduled-tasks/`
- Creates a Cowork artifact (`linkedin-digest`) using the template at
  `artifacts/linkedin-digest.html`

After setup, the daily flow is:

1. Cowork's scheduled task fires at the user's chosen time, runs
   `workflow-digest.md`, which produces a `digest-YYYY-MM-DD.md` file and refreshes
   the LinkedIn Digest widget.
2. The user reviews the widget, marks Approve/Edit/Skip on each draft, clicks Submit.
3. The widget writes the decisions to Google Drive and triggers the `linkedin-post`
   ad-hoc task.
4. The post task runs `workflow-post.md`, which verifies URLs, posts each approved
   comment, and likes each post.

## When working on this plugin

If a user asks for help modifying the agent's behaviour, the right edits are usually
in their workspace folder (`$LINKEDIN_AGENT_HOME`), not in this plugin folder. The
plugin holds the templates; the user's workspace holds the live config.

Common edits:

- **"Drafts feel generic"** → edit `$LINKEDIN_AGENT_HOME/voice.md`. Tighten the
  positioning, add banned phrases, add a "good example" the agent will reference.
- **"Wrong posts surfacing"** → edit `$LINKEDIN_AGENT_HOME/config.md`. Tune
  hashtags, target accounts, blocklist, post-type filter.
- **"Voice is off"** → edit `$LINKEDIN_AGENT_HOME/voice.md > brand_positioning`.
- **"Wrong volume"** → edit `$LINKEDIN_AGENT_HOME/config.md > runs_per_day` and
  `drafts_per_run`. Re-register the scheduled task with new cron if changing runs.
- **"URL capture is drifting"** → LinkedIn's DOM has changed.
  `$LINKEDIN_AGENT_HOME/workflow-digest.md` Step 2 has the URN-extraction JS — that
  selector may need updating.

If a user asks for a *new feature* (e.g., reply-to-comments-on-our-own-posts,
multi-account support, non-English voice), that's a plugin-level change and goes in
this folder, not in the user's workspace.

## Safety rails to enforce

- **Never post anything that wasn't explicitly marked APPROVE or EDIT-with-`[x]`.**
- **Never modify a comment between reading it from the digest and posting it.**
- **Never raise `hard_daily_cap_comments` above 30 in `config.md`.** LinkedIn's
  rate-limit threshold sits around 15–20 comments/day. The cap exists to prevent
  the user's account from being flagged.
- **Stop immediately on CAPTCHA / login wall / security challenge.** Never try to
  solve them.
- **Apply `config.md > domain_guardrails` to every draft.** These exist for
  regulatory reasons (healthcare, legal, finance, education).
- **Never name competitors** from `config.md > competitors`.

## Files in this plugin

```
linkedin-brand-agent/
├── .claude/
│   ├── skills/linkedin-brand-agent-setup/SKILL.md   ← The setup wizard skill
│   └── commands/linkedin-setup.md                   ← Slash command
├── claude-plugin/plugin.json
├── agent/                                           ← Templates the wizard copies into user's workspace
│   ├── templates/
│   │   ├── config-template.md
│   │   └── voice-template.md
│   ├── workflows/
│   │   ├── workflow-digest.md
│   │   ├── workflow-post.md
│   │   └── digest-template.md
│   └── scheduled-tasks/
│       ├── linkedin-daily-digest.md
│       └── linkedin-post.md
├── scripts/
│   ├── commit-widget-state.py
│   └── verify-digest-urls.py
├── artifacts/
│   └── linkedin-digest.html                         ← Widget template
├── docs/                                            ← Screenshots (later)
├── examples/
│   └── digest-example.md                            ← Anonymised real output
├── README.md
├── GUIDE.md
├── CLAUDE.md                                        ← (this file)
├── CONTRIBUTING.md
└── LICENSE
```

## When in doubt

- Default to user agency. Show drafts, ask before posting, log everything.
- The markdown files are the source of truth. The widget is the polished surface.
- The system is designed to be improved by the user, not magically perfect on day 1.
  Push back gently if a user expects zero-curation output.
