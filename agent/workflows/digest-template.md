# LinkedIn Digest — {{DATE}}

**Total drafts:** {{N}} (target: {{TARGET}})
**Sources:** {{HOMEFEED_COUNT}} home feed · {{HASHTAG_COUNT}} hashtags · {{ENGAGER_COUNT}} recent engagers · {{TOPICSEARCH_COUNT}} topic search · {{HIGHCOMMENT_COUNT}} high-comment threads
**Mode mix:** {{OPERATOR_COUNT}} operator · {{QUESTION_COUNT}} question · {{POV_COUNT}} sharp POV

To post: edit the `Action:` line under each draft. Replace `[ ]` with `[x]` next to
APPROVE, EDIT, or SKIP. If you choose EDIT, rewrite the comment text in the code block.
Then in the LinkedIn Digest widget, click Submit — or in chat, say "post my approved
LinkedIn comments" and the second pass will publish them (and like each commented post).

Every entry must have a working LinkedIn post URL. If a URL could not be captured,
the post should not appear in this digest.

---

## 1. {{AUTHOR_NAME}} — {{AUTHOR_HEADLINE}}

**Open post:**

{{POST_URL}}

**Author profile:** {{AUTHOR_PROFILE_URL}}
**Excerpt:** {{POST_EXCERPT_2_3_LINES}}
**Engagement:** {{LIKES}} likes · {{COMMENTS}} comments
**Source:** {{home_feed | hashtag:#tag | engager | topic_search:phrase | high_comment_1d}}
**Mode:** {{OPERATOR_INSIGHT | SHARP_POV | CURIOUS_QUESTION}}
**Why this:** {{ONE_LINE_RATIONALE}}
**Score:** {{SCORE}}/10

```comment
{{DRAFT_COMMENT}}
```

**Action:** `[ ] APPROVE   [ ] EDIT   [ ] SKIP`

---

## 2. {{AUTHOR_NAME}} — {{AUTHOR_HEADLINE}}

**Open post:**

{{POST_URL}}

**Author profile:** {{AUTHOR_PROFILE_URL}}
**Excerpt:** {{POST_EXCERPT_2_3_LINES}}
**Engagement:** {{LIKES}} likes · {{COMMENTS}} comments
**Source:** {{home_feed | hashtag:#tag | engager | topic_search:phrase | high_comment_1d}}
**Mode:** {{OPERATOR_INSIGHT | SHARP_POV | CURIOUS_QUESTION}}
**Why this:** {{ONE_LINE_RATIONALE}}
**Score:** {{SCORE}}/10

```comment
{{DRAFT_COMMENT}}
```

**Action:** `[ ] APPROVE   [ ] EDIT   [ ] SKIP`

---

<!-- Repeat the block above for items 3..N.

Link format rule: put the URL as plain text on its own line, with a blank line before
and after it. Do NOT wrap it in [text](url) markdown link syntax, do NOT wrap it in
backticks, do NOT prefix with anything. Cowork's file viewer auto-links plain URLs
but does not always activate inline-styled markdown links. Plain raw URLs are the
most reliably clickable across all viewers. -->

## Notes from this run

{{ANY_FAILURES_OR_WARNINGS}}

If any candidate posts had to be dropped because their URL could not be captured, list
them here with author name and one-line reason, so you can see what was missed.

If the post-type filter dropped a high count of candidates, log the count and the
most-matched signal — useful for tuning the filter over time.
