#!/usr/bin/env python3
"""
Commit widget approvals to today's LinkedIn digest .md file.

Called by the LinkedIn Digest artifact on Submit. Reads a base64-encoded JSON state
object on stdin; updates the matching digest file in-place; prints a single OK line
on success or ERROR line on failure.

Stdin format (after base64 decode):
{
  "date": "YYYY-MM-DD",
  "decisions": {
    "1": {"action": "approve"},
    "2": {"action": "edit", "text": "new comment body"},
    "3": {"action": "skip"}
  }
}

Drafts not present in `decisions` are left untouched in the file.

How it finds the digest file:
- First, check the LINKEDIN_AGENT_HOME environment variable. If set, look at
  $LINKEDIN_AGENT_HOME/digests/digest-<date>.md.
- Second, glob common workspace locations (Cowork session mounts, common Desktop
  paths) for `digests/digest-<date>.md` underneath any directory named
  `LinkedIn-Agent`, `linkedin-brand-agent`, or `linkedin-agent`.
- If multiple candidates are found, the most recently modified one wins.

The setup wizard sets LINKEDIN_AGENT_HOME for you. If the env var is missing, the
script's glob fallback will still find the file in most setups.
"""
import sys
import os
import json
import base64
import re
import glob


def find_digest(date):
    """Locate the digest .md file for the given date."""
    candidates = []

    # 1) Env var (set by the setup wizard)
    home = os.environ.get("LINKEDIN_AGENT_HOME")
    if home:
        path = os.path.join(home, "digests", f"digest-{date}.md")
        if os.path.isfile(path):
            return path

    # 2) Glob common locations
    patterns = [
        # Cowork sandboxed sessions
        f"/sessions/*/mnt/**/LinkedIn-Agent/digests/digest-{date}.md",
        f"/sessions/*/mnt/**/linkedin-brand-agent/digests/digest-{date}.md",
        f"/sessions/*/mnt/**/linkedin-agent/digests/digest-{date}.md",
        # Direct mounts on macOS/Linux/WSL
        f"/mnt/**/LinkedIn-Agent/digests/digest-{date}.md",
        f"/mnt/**/linkedin-brand-agent/digests/digest-{date}.md",
        f"/mnt/**/linkedin-agent/digests/digest-{date}.md",
        # Home directory
        os.path.expanduser(f"~/**/LinkedIn-Agent/digests/digest-{date}.md"),
        os.path.expanduser(f"~/**/linkedin-brand-agent/digests/digest-{date}.md"),
        os.path.expanduser(f"~/**/linkedin-agent/digests/digest-{date}.md"),
    ]
    for p in patterns:
        candidates.extend(glob.glob(p, recursive=True))

    if not candidates:
        return None

    # Most recently modified wins
    return max(candidates, key=lambda p: os.path.getmtime(p))


def main():
    try:
        raw = sys.stdin.read().strip()
        data = json.loads(base64.b64decode(raw).decode("utf-8"))
        date = data["date"]
        decisions = data.get("decisions", {})
    except Exception as e:
        print(f"ERROR parsing input: {e}", file=sys.stderr)
        sys.exit(2)

    path = find_digest(date)
    if not path:
        print(
            f"ERROR digest file not found for date {date}. "
            f"Set LINKEDIN_AGENT_HOME to your agent folder, or check that "
            f"digests/digest-{date}.md exists.",
            file=sys.stderr,
        )
        sys.exit(3)

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    header_re = re.compile(r"^## (\d+)\.")
    current_rank = None
    edit_state = None  # None, 'awaiting_open', 'inside_old'
    out = []

    for ln in lines:
        m = header_re.match(ln)
        if m:
            current_rank = int(m.group(1))
            out.append(ln)
            decision = decisions.get(str(current_rank))
            if (
                decision
                and decision.get("action") == "edit"
                and isinstance(decision.get("text"), str)
                and decision["text"].strip()
            ):
                edit_state = "awaiting_open"
            else:
                edit_state = None
            continue

        if edit_state == "awaiting_open":
            if ln.strip() == "```comment":
                out.append("```comment")
                out.append(decisions[str(current_rank)]["text"])
                out.append("```")
                edit_state = "inside_old"
                continue
            out.append(ln)
            continue

        if edit_state == "inside_old":
            if ln.strip() == "```":
                edit_state = None
            continue

        decision = decisions.get(str(current_rank)) if current_rank else None
        if decision and decision.get("action") and ln.startswith("**Action:**"):
            # When the user APPROVE'd an edited draft, mark EDIT so the post pass picks
            # up the new comment text rather than the original.
            action_word = decision["action"].upper()
            new_action = "**Action:** `[ ] APPROVE   [ ] EDIT   [ ] SKIP`"
            new_action = new_action.replace(
                f"[ ] {action_word}", f"[x] {action_word}"
            )
            out.append(new_action)
            continue

        out.append(ln)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    counts = {"approve": 0, "edit": 0, "skip": 0}
    for d in decisions.values():
        a = d.get("action")
        if a in counts:
            counts[a] += 1
    print(
        f"OK saved digest-{date}.md approved={counts['approve']} "
        f"edited={counts['edit']} skipped={counts['skip']}"
    )


if __name__ == "__main__":
    main()
