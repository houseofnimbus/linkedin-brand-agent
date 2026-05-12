#!/usr/bin/env python3
"""
Structural pre-flight for a LinkedIn digest .md file.

Browser-free verification: catches malformed URLs, missing URLs, duplicates, and
entries that look ill-formed BEFORE the publisher opens a browser. The real content
verification (does this URL actually point at the right post?) happens in
workflow-post.md Step 3.5 with Claude in Chrome — this script is the cheap first
pass.

Usage:
    python3 verify-digest-urls.py <date>        # checks digests/digest-<date>.md
    python3 verify-digest-urls.py path/to.md    # explicit file path

How it finds the digest file: same logic as commit-widget-state.py
(LINKEDIN_AGENT_HOME env var, then glob fallback).

Exit codes:
    0  all entries OK
    1  one or more entries failed structural checks
    2  digest file not found / parse error
"""
import sys
import os
import re
import glob
from pathlib import Path


URL_VALID_RE = re.compile(
    r"^https://www\.linkedin\.com/"
    r"(feed/update/urn:li:activity:\d+/?"
    r"|posts/[^?\s]+"
    r"|company/[^/?\s]+/posts/[^?\s]+)"
    r"$"
)

ENTRY_HEADER_RE = re.compile(r"^## (\d+)\.\s+(.+?)\s+—\s+(.+)$")
URL_LINE_RE = re.compile(r"^https?://\S+$")


def find_digest(arg):
    """Resolve arg to a digest file path. Accepts a date or a path."""
    p = Path(arg)
    if p.exists() and p.is_file():
        return p

    home = os.environ.get("LINKEDIN_AGENT_HOME")
    if home:
        path = Path(home) / "digests" / f"digest-{arg}.md"
        if path.exists():
            return path

    patterns = [
        f"/sessions/*/mnt/**/LinkedIn-Agent/digests/digest-{arg}.md",
        f"/sessions/*/mnt/**/linkedin-brand-agent/digests/digest-{arg}.md",
        f"/sessions/*/mnt/**/linkedin-agent/digests/digest-{arg}.md",
        f"/mnt/**/LinkedIn-Agent/digests/digest-{arg}.md",
        f"/mnt/**/linkedin-brand-agent/digests/digest-{arg}.md",
        f"/mnt/**/linkedin-agent/digests/digest-{arg}.md",
        os.path.expanduser(f"~/**/LinkedIn-Agent/digests/digest-{arg}.md"),
        os.path.expanduser(f"~/**/linkedin-brand-agent/digests/digest-{arg}.md"),
        os.path.expanduser(f"~/**/linkedin-agent/digests/digest-{arg}.md"),
    ]
    found = []
    for pat in patterns:
        found.extend(glob.glob(pat, recursive=True))
    if found:
        return Path(max(found, key=os.path.getmtime))

    return None


def parse_entries(text):
    """Extract (rank, author, headline, url, excerpt) tuples from a digest."""
    lines = text.split("\n")
    entries = []
    current = None

    for i, ln in enumerate(lines):
        m = ENTRY_HEADER_RE.match(ln)
        if m:
            if current is not None:
                entries.append(current)
            current = {
                "rank": int(m.group(1)),
                "author": m.group(2).strip(),
                "headline": m.group(3).strip(),
                "url": None,
                "excerpt": None,
                "line_no": i + 1,
            }
            continue

        if current is None:
            continue

        if current["url"] is None and URL_LINE_RE.match(ln.strip()):
            current["url"] = ln.strip()
            continue

        if current["excerpt"] is None and ln.startswith("**Excerpt:**"):
            current["excerpt"] = ln.replace("**Excerpt:**", "").strip()

    if current is not None:
        entries.append(current)
    return entries


def check_entry(e):
    """Return list of issue strings for one entry. Empty list = clean."""
    issues = []
    if not e["url"]:
        issues.append("NO_URL")
        return issues

    url = e["url"]
    if not URL_VALID_RE.match(url):
        issues.append(f"MALFORMED_URL ({url})")
    if "?" in url:
        issues.append("TRACKING_PARAMS_NOT_STRIPPED")
    if "/recent-activity/" in url:
        issues.append("FALLBACK_URL_USED_AS_PRIMARY")
    if not e["excerpt"]:
        issues.append("NO_EXCERPT")
    return issues


def find_url_duplicates(entries):
    """Return ranks where the same URL appears twice."""
    seen = {}
    dups = []
    for e in entries:
        if not e["url"]:
            continue
        if e["url"] in seen:
            dups.append((seen[e["url"]], e["rank"], e["url"]))
        else:
            seen[e["url"]] = e["rank"]
    return dups


def main():
    if len(sys.argv) != 2:
        print("Usage: verify-digest-urls.py <date|path>", file=sys.stderr)
        sys.exit(2)

    path = find_digest(sys.argv[1])
    if not path:
        print(
            f"ERROR digest not found for: {sys.argv[1]}. "
            f"Set LINKEDIN_AGENT_HOME or pass a full path.",
            file=sys.stderr,
        )
        sys.exit(2)

    text = path.read_text(encoding="utf-8")
    entries = parse_entries(text)

    if not entries:
        print(f"ERROR no entries parsed from {path}", file=sys.stderr)
        sys.exit(2)

    failed = 0
    print(f"Digest: {path}")
    print(f"Entries: {len(entries)}")
    print("")

    for e in entries:
        issues = check_entry(e)
        status = "OK" if not issues else "FAIL"
        if issues:
            failed += 1
        author = e["author"][:40]
        print(f'  [{status}] #{e["rank"]:>2}  {author:<40}  {e["url"] or "(no url)"}')
        for i in issues:
            print(f"         └─ {i}")

    dups = find_url_duplicates(entries)
    if dups:
        print("")
        print("  URL DUPLICATES:")
        for a, b, u in dups:
            print(f"    #{a} and #{b} share URL: {u}")
            failed += 1

    print("")
    if failed:
        print(
            f"FAIL  {failed} issue(s) found. Run workflow-digest.md URL recapture or "
            f"hand-fix before publish."
        )
        sys.exit(1)

    print(
        "OK  all entries pass structural checks. Browser verification still happens "
        "in workflow-post.md Step 3.5."
    )


if __name__ == "__main__":
    main()
