# Contributing to LinkedIn Brand Agent

Pull requests welcome. This document covers what's in scope, the editorial bar,
and the workflow for getting changes merged.

## What's in scope

The agent is built around a specific architecture: morning gather + human approval
+ assisted post + auto-like. Improvements in any of these layers are welcome:

- **Better gather** — new source types, smarter scoring, better URL capture, faster
  filtering.
- **Better drafts** — sharper voice rules, additional modes, better length
  calibration, language additions.
- **Better widget** — keyboard shortcuts, better mobile layout, accessibility fixes,
  preview-while-editing.
- **Better safety** — earlier detection of rate-limit risk, better challenge
  handling, smarter recovery from failed runs.
- **Better setup** — clearer wizard questions, smarter defaults, language additions.

What's *not* in scope (forks welcome, but won't be merged):

- Direct-message automation. The agent is for public engagement only.
- Connection-request automation. Same reason.
- Removing the human approval step. The two-pass design is the point.
- Removing the auto-like coupling. Commenting without liking is drive-by.
- Multi-account support inside a single agent install. (Run multiple installs
  instead.)

## Editorial bar

Three rules:

1. **No silent magic.** Every behaviour should be inspectable in plain markdown or
   plain Python. If a user can't read the source and understand what'll happen,
   the change is too clever.
2. **Default to user agency.** Anything the agent does should be either approved
   by the user explicitly or clearly logged so they can audit after.
3. **Tone is direct, confident, a little playful.** No AI filler in documentation
   either ("dive into", "let's unpack", "in today's fast-paced", em dashes
   everywhere). The voice rules in `agent/templates/voice-template.md` apply to
   the docs too.

## Workflow for getting changes merged

1. **Open an issue first** for anything beyond a typo fix or a small bug. It saves
   you from building something that won't land.
2. **Fork and branch.** Branch name should describe the change: `add-language-rules`,
   `fix-url-capture-may-2026`, `widget-keyboard-shortcuts`.
3. **Test it on a real LinkedIn account.** If your change touches the gather or
   post workflow, run an actual digest and an actual post pass. Note what you
   tested in the PR.
4. **PR with a 100-word summary.** What problem this solves, what you changed,
   how you tested.
5. **Be open to edits.** The maintainers may rewrite sections of your prose to
   match the existing tone — that's not a critique of you, it's the editorial bar.

## Specific change types — what to know

**Adding a new voice mode** — Touch `agent/templates/voice-template.md` (define
the mode, give a good example, give a bad example, add a length target). Touch
`agent/workflows/workflow-digest.md` Step 4 (let the agent pick this mode when
appropriate). Touch the README's "How does it work" section if the mode is
user-visible. Update the wizard skill if the mode needs a configuration question.

**Adding a new gather source** — Touch `agent/workflows/workflow-digest.md`
(add the source with letter ID, document the URL pattern and capture method).
Touch `agent/templates/config-template.md > extra_gather_sources` (add the toggle
and any tuning parameters). Touch the source priority list.

**Adding a new domain guardrail pattern** — Document the pattern in
`agent/templates/config-template.md > domain_guardrails` as an example block. The
agent reads this on every run, so the pattern just needs to be expressible in
plain English.

**Updating URL capture** — LinkedIn changes its DOM occasionally. When that
happens, the URN-extraction JS in `agent/workflows/workflow-digest.md` Step 2
needs to be updated. Test on at least 10 real posts (mix of feed, hashtag,
search-result, company-page, reshare). Verify both the author check and body
check pass.

**Updating the widget** — `artifacts/linkedin-digest.html` is self-contained.
The agent re-uses the same template every install, so changes here ship
immediately. Test the widget against the existing data flow (decisions written
to Drive, then `runScheduledTask` fires `linkedin-post`).

## Code style

- **Markdown** — short paragraphs, no em dashes, no AI filler (see the
  `voice-template.md` banned-phrases list). Two-space indentation in YAML-style
  config examples.
- **Python** — Black-formatted, type hints where they help, no exotic dependencies
  (the standard library is enough for what's in `scripts/`). Comments explain
  *why*, not *what*.
- **HTML/CSS/JS in the widget** — vanilla, no build step, no external libraries.
  The widget loads in seconds and survives Cowork's sandboxed iframe — keep it
  simple.

## Community

Bugs → open an issue. Ideas → open a discussion. Wins → tag the project on
LinkedIn; the maintainers like seeing it in the wild.

Thanks for considering a contribution.
