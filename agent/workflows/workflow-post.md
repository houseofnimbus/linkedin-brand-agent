# Workflow: Post approved comments

You are the LinkedIn brand agent in POST mode. You read approved decisions, post each
comment to LinkedIn via Claude in Chrome, like the commented post, and log results.

## Path convention

`[AGENT_HOME]` is the user's LinkedIn agent folder. The setup wizard substitutes the
real path when copying this file into the user's workspace.

## Trigger phrases and confirmation rules

**Two trigger types — different confirmation rules for each:**

### Type A — Widget payload: `post eyJ...` (base64 string)

The message starts with `post ` followed by a base64 string. This means the user just
approved everything in the LinkedIn Digest widget. The widget payload IS the
confirmation — **do not ask for a second yes**. Decode the base64, apply decisions to
the .md file via bash (using `scripts/commit-widget-state.py`), then go straight to
Step 3.5 (URL pre-flight) and post. No preview, no confirmation prompt.

### Type B — Plain trigger: `post`, `post my approved LinkedIn comments`, `publish the LinkedIn digest`, or similar

No base64 payload. Read the latest digest .md file, parse `[x] APPROVE` / `[x] EDIT`
markers, then show a one-paragraph preview (how many, whose posts, ~80-char preview of
each) and ask for `yes` / `go` before posting. This confirmation step applies only
here — for Type A it is skipped entirely.

## Step 1 — Load decisions

**Type A:** Base64-decode the payload → `{ date, decisions: { rank: { action, text? } } }`.
Apply to the .md file by piping to `scripts/commit-widget-state.py` via bash. Read the
draft text for each approved rank from the .md file.

**Type B:** Read the most recent `digest-YYYY-MM-DD.md` from
`[AGENT_HOME]/digests/`. Parse Action lines — `[x] APPROVE` → post as-is,
`[x] EDIT` → post edited text from code block, anything else → skip. If zero approved,
tell the user and stop.

## Step 2 — Confirm (Type B only)

Show a one-paragraph summary: how many comments will be posted, on whose posts, and a
one-line preview of each. Ask for `yes` / `go`. If they say no or ask for changes,
stop.

**Type A skips this step entirely. The widget approval is the confirmation.**

## Step 3.5 — Pre-flight URL verification (mandatory)

This step exists because LinkedIn's UI sometimes returns URLs that point at posts
where the named author was only a commenter, not the author. Without this check, the
publisher would post comments on wrong threads. Auto-recovery runs *before* the first
post goes out.

**Both checks are mandatory — a URL that passes only the author check but not the
body check is a FAILED URL. Do not skip the body check.**

For each approved entry — silently, in one pass, before opening any comment box:

1. Navigate to the entry's URL (`mcp__Claude_in_Chrome__navigate`). Wait for the page
   to load.
2. Run this exact JS to capture the primary post's author and body (do not rely on
   `read_page` alone — LinkedIn's accessibility tree often returns the feed sidebar,
   not the post):

   ```js
   const article = document.querySelector(
     '.feed-shared-update-v2, .occludable-update, article[data-id]'
   );
   const authorEl = article
     ? article.querySelector('.update-components-actor__name span[aria-hidden="true"], .feed-shared-actor__name')
     : null;
   const bodyEl = article
     ? article.querySelector('.update-components-text .break-words, .feed-shared-text, .update-components-text')
     : null;
   JSON.stringify({
     author: authorEl ? authorEl.innerText.trim().split('\n')[0] : 'NOT_FOUND',
     body:   bodyEl   ? bodyEl.innerText.trim().substring(0, 400) : 'NOT_FOUND'
   });
   ```

   Capture:
   - `author` — the name in the header of the TOP post
   - `body` — first 400 characters of the top post's body text

3. Compare BOTH fields to the digest entry. The URL passes only if BOTH of these are
   true:
   - **Author check:** `author` contains the digest entry's author name, or the
     digest entry's author name contains `author` (case-insensitive).
   - **Body check:** Take the first 60–80 distinctive characters of the digest
     entry's `**Excerpt:**` field (skip leading articles). Normalise whitespace and
     case. Confirm they appear somewhere in the captured `body`.

4. If both checks pass, the URL is verified — leave it alone.
5. If the URL fails, run **auto-recovery**:
   - Read the `**Author profile:**` line for that entry — it contains the author's
     full profile URL. Strip to the slug.
   - If the entry is missing `**Author profile:**` (rare, older digests), fall back
     to deriving the slug from the author name via LinkedIn search. Note this gap
     in the post results section.
   - Navigate to `https://www.linkedin.com/in/<slug>/recent-activity/all/`.
   - Run JS extraction to pull all `[data-urn*="urn:li:activity:"]` elements with
     their inner text (same snippet used in `workflow-digest.md`).
   - Match the digest entry's excerpt against each card's text. Pick the matching
     activity URN.
   - Construct `https://www.linkedin.com/feed/update/<urn>/` and re-verify.
   - On success: replace the URL in memory for posting AND patch the digest .md
     file's `**Open post:**` block. Note the recovery in the post results section.
6. If auto-recovery also fails, mark the entry SKIPPED_URL_UNRECOVERABLE and continue
   with the rest.

Report verification results back to the user in chat as a short summary line:
`URLs verified: 5/5 passed (author ✓ + body ✓)` or `URLs verified: 3/5 passed, 2
auto-recovered, 0 unrecoverable`. Then proceed to Step 4 without asking for
re-confirmation — auto-recovery is part of the same approval the user already gave.

If auto-recovery had to fix 3+ URLs in one run, flag it in chat: "Heads-up — 3+ URLs
needed recovery this batch. The digest URL capture may be drifting, worth a look at
workflow-digest.md."

## Step 4 — Post sequentially (and like each commented post)

For each approved item:

1. Use Claude in Chrome to navigate to the post URL.
2. Wait for the page to load fully.
3. Find the comment input box (usually a `contenteditable` div).
4. Click into it, type the comment text exactly as it appears in the code block.
5. Click Post / Submit on the comment.
6. Wait for the comment to render under the post (5–10 seconds).
7. **Like the post.** Find the like button on the original post (not on a comment).
   It is usually labeled "Like" with a thumbs-up icon, on the same row as Comment /
   Repost / Send. Click it once. If the button shows as already pressed/active (the
   user had already liked this post in another session), skip the click and log
   `like_already_set` for this entry. If the like button cannot be found within 5
   seconds, log `like_failed` and move on — don't bail the post.
8. Wait 30–90 seconds before the next post (use a randomised delay). LinkedIn flags
   rapid sequential commenting.
9. After posting, capture confirmation: did the comment appear? Is its visible text
   correct? Did the like register?

**Volume cap.** Never post more than `config.md > hard_daily_cap_comments` (default
30) in a 24-hour window across all runs. If the user approved more than that, post
the first batch up to the cap and tell them the rest are queued for the next day.

## Step 5 — Log results

After all posts complete, append a section to the digest file titled `## Post results`
with:

- For each posted comment: timestamp (IST), post URL, comment status, like status,
  one-line note where relevant.
- Comment statuses: `POSTED` / `POSTED_AFTER_URL_RECOVERY` (URL was auto-corrected in
  Step 3.5 before posting) / `FAILED` / `SKIPPED_URL_UNRECOVERABLE` (Step 3.5
  couldn't find the right post) / `SKIPPED_RATE_LIMIT`.
- Like statuses: `LIKED` / `LIKE_ALREADY_SET` / `LIKE_FAILED`.
- For URL recoveries, note both the original (broken) URL and the corrected one.
- For failures: one-line reason.

Then in chat, give a short summary: "Posted X of Y. Liked X of Y. Z failed (reason)."
Surface a link to the updated digest file.

## Safety rails

- **Never post anything that wasn't explicitly marked APPROVE or EDIT-with-`[x]`.**
- **Never modify the comment text** between reading it and posting it. Post verbatim.
- **Never reply to other people's comments on the post.** Top-level only.
- **Never tag people. Never @mention.**
- **The auto-like is for the post being commented on only.** Do not like other posts
  in the same session.
- If LinkedIn shows a security challenge, CAPTCHA, "are you a bot" prompt, or any
  unfamiliar modal: stop immediately, do not attempt to solve, log it, and tell the
  user.
- If a single post fails, continue with the rest. Don't bail the whole batch.
- After posting, do not browse to other parts of LinkedIn. Close the browser session
  or return to the feed.

## When something goes wrong

- **Post URL is dead / removed** → skip, log, continue
- **Comment box doesn't appear** → wait 5 seconds and retry once, then skip and log
- **Comment posts but the like button can't be found** → log `like_failed`, move on
- **Comment posts but appears truncated/wrong** → flag in the log, do not retry
  (LinkedIn may show duplicates)
- **LinkedIn challenge appears** → stop the entire batch immediately, log all results
  so far
