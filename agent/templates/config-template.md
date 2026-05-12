# LinkedIn agent config

This file controls how the agent finds posts, scores them, and limits engagement volume.
The agent reads this on every run, so changes take effect immediately — no redeploy.

The `linkedin-brand-agent-setup` wizard writes most of this for you the first time you
run it. You can edit any value by hand later.

---

## Engagement schedule

How often the agent runs and how many drafts it produces per run. The wizard asks for
these during setup and writes them here.

```
runs_per_day: 1                    # 1 | 2 | 3
drafts_per_run: 8                  # 5 | 8 | 12 | 15
```

**Safety cap.** The agent will never produce more than 30 comment drafts in a single
day, even if `runs_per_day × drafts_per_run` exceeds that. LinkedIn flags accounts that
comment 15–20+ times a day as bot-like — keep total daily comments well under 30 to
avoid a soft account flag.

```
hard_daily_cap_comments: 30        # absolute ceiling, do not exceed
```

## Auto-like coupling

When the posting agent successfully posts a comment, it also clicks the like button on
that same post. This is automatic and not configurable — commenting without liking
reads as a drive-by, and likes are the cheapest engagement signal LinkedIn rewards.

```
auto_like_commented_posts: true    # always true, kept here for visibility
```

## Source quotas

How many candidate posts to pull from each source before scoring. Higher numbers =
broader sweep, more tool calls, slower runs.

```
home_feed_scan: 30                 # top posts in your home feed
posts_per_hashtag: 10              # per hashtag in the list below
recent_engagers_to_check: 10       # people who liked/commented on your posts recently
```

## Hashtags to monitor

Hashtags the agent scans for relevant posts. The wizard asks you to seed this list
during setup. Pick 5–12 hashtags that are active in your space — not too broad
(e.g. `#marketing` alone surfaces too much), not too narrow (e.g. brand-specific tags
won't have enough volume).

Edit freely — add, remove, reorder. Hashtags discovered each Monday via the agent's
discovery pass land in `hashtag-suggestions.md` for you to review and copy across.

```
hashtags:
  # Replace these with your own. Comment out with # to disable temporarily.
  - example-replace-me
  - another-example
```

## Target accounts (priority lift)

Posts from these people get a +2 boost to their relevance score. Use this for accounts
whose attention matters to you — prospects, influencers, partners, decision-makers in
your space.

The wizard asks for 5–10 of these during setup. Add more by hand later.

Format: free-text lines under `target_accounts:`. The agent does a fuzzy match against
post author names, so write the name as it appears on their LinkedIn profile.
Optionally add the profile URL as a comment for your own reference.

```
target_accounts:
  # Replace these with your own targets.

  - Example Person Name
  # https://www.linkedin.com/in/example-slug/
  # Why this person matters to you (optional comment for your own reference)

  - Another Example
  # https://www.linkedin.com/in/another-example/
```

## Blocklist

The agent skips any post matching these patterns. Useful for muting noisy accounts,
recurring spammy patterns, or keywords that always misfire.

```
blocked_authors:
  # Full names or profile URLs of people you don't want to engage with.
  # Leave empty if you don't have any to start with.

blocked_keywords:
  # Words/phrases that disqualify a post from the digest regardless of author.
  # The defaults below are a generally-useful starting set.

  - hiring spam
  - MLM
  - crypto airdrop
  - astrology
  - sponsored
```

## Strict post-type filter

Drops four kinds of post that almost never sustain a real comment discussion: job
posts, product launch announcements, role-change announcements, milestone posts.
These signals are detected via post body keywords and visual cues.

Keep all four `true` unless you have a strong reason — these are the most common
sources of low-quality digest entries.

```
strict_post_type_filter:

  drop_job_posts: true
    # signals: "We're hiring", "Looking for", "open role", "join our team",
    #          "apply now", job-card preview attached, #hiring as primary tag

  drop_product_launches: true
    # signals: "Excited to announce", "launching", "new product", "introducing",
    #          press-release shape (logo + product hero image + feature bullets)
    # exception: operator teardowns of OTHER companies' launches are kept
    #            (those are POV posts, not announcements)

  drop_role_announcements: true
    # signals: "thrilled to share", "joining as", "new chapter", "stepping into",
    #          "honoured to take on", "promoted to", LinkedIn auto-job-update card

  drop_milestone_posts: true
    # signals: "completed N years at X", anniversary posts, certification badges,
    #          award acceptances, "X years ago today", first-job nostalgia
```

When a candidate matches any of these signals, the agent logs the drop in the digest's
"Posts dropped during gather" notes so you can audit false positives.

## Domain guardrails

If your brand operates in a regulated or sensitive domain (healthcare, legal, finance,
education, etc.), list rules the agent must apply to every draft. The wizard asks
about this during setup.

Common examples — replace or extend with your own:

```
domain_guardrails:
  # Healthcare brand:
  #   - "No medical advice or clinical claims"
  #   - "No cure or treatment guarantees"
  #   - "No fearmongering around symptoms"
  #
  # Legal brand:
  #   - "No specific legal advice"
  #   - "Frame everything as general information, not counsel"
  #
  # Financial services brand:
  #   - "No investment advice or return promises"
  #   - "No predictions about specific securities"
  #
  # Education brand:
  #   - "No outcome guarantees"
  #   - "No claims about specific student results without sourcing"

  # Replace with your own (or remove this block if unregulated):
  - example-guardrail-replace-me
```

## Competitor blocklist

Names the agent will never mention in any comment, even neutrally. The wizard asks for
these during setup. Edit freely.

```
competitors:
  # Replace with your competitors. Leave empty if you don't have a list.
  - Example Competitor 1
  - Example Competitor 2
```

## Trending signals

Boosts scores for posts gaining traction in your feed. Defaults are calibrated for
active LinkedIn users — adjust thresholds if your feed is much busier or quieter than
typical.

```
trending_signals:

  enable_velocity_boost: true
  velocity_threshold_per_hour: 40      # posts above this rate get +2 to score
  velocity_high_threshold: 100         # also flagged with a TRENDING badge in the digest

  enable_connection_engagement_boost: true
  connection_count_threshold: 3        # 3+ visible 1st-degree connections engaged → +1

  enable_weekly_hashtag_discovery: true
  hashtag_discovery_day: monday        # only runs on this day
  min_appearances_to_suggest: 3        # hashtag must appear in N+ feed posts to be suggested
```

## Gather sources

Beyond the home feed, the agent searches for relevant posts in two additional ways:
content search by topic phrase, and high-comment-density 1st-degree threads.

```
extra_gather_sources:

  enable_topic_search: true
  topic_search_phrases:
    # 4–8 short phrases the agent uses to search LinkedIn content. Pick phrases that
    # surface posts in your industry where the brand would have something to say.
    # Replace these examples:
    - example phrase one
    - example phrase two
  topic_search_picks_per_phrase: 3

  enable_high_comment_first_degree: true
  min_comments_for_first_degree_pick: 20
  # Posts on the home feed with comment_count >= this AND OP is 1st-degree
  # (or a 1st-degree has commented) get a +2 score boost.
```

Source priority (the order the agent walks):

1. High-comment 1st-degree threads (highest signal)
2. Home feed (with strict post-type filter applied)
3. Topic-phrase content search (broadest)
4. Recent engagers / target accounts' recent activity
5. Hashtag scans (fallback when others are dry)

## Voice mix preference

Across a digest of N drafts, the agent aims for roughly this mode split:

```
voice_mix:
  curious_question_share: 0.4     # ~40% — default safe mode, builds reach, high reply rate
  sharp_pov_share: 0.4            # ~40% — when the brand has a real counter-position
  operator_insight_share: 0.2     # ~20% — only when a specific brand fact is the natural unlock
```

The agent decides per-post. If a post doesn't fit any mode cleanly, it's dropped from
the digest rather than padded. Better a 5-draft digest of strong picks than 8 with three
forced ones.

**Hard cap on citations.** Across a daily digest, the agent will cite a specific
fact/number from `voice.md > allowed_facts` in at most 2 drafts. Often the right number
is zero. The brand perspective should mostly come through in *how* posts are reacted to,
not as name-drops of metrics.

```
max_drafts_with_citation: 2     # per digest, never more
```

## Cross-day de-duplication

The agent reads the last 7 days of digest files and applies two filters before scoring:

```
cross_day_dedup:
  drop_already_seen_urls: true        # never show the same post twice in 7 days
  max_author_appearances_in_7d: 2     # cap any one author at 2 of last 7 digests
  target_account_author_cap: 3        # target accounts get a higher cap (3 of 7)
```

If these filters reduce the candidate pool below `drafts_per_run`, the agent ships what
it has rather than padding with weaker picks.
