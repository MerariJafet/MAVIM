"""
MAVIM DevRel — Reddit Monitor
Uses PRAW (official Reddit API wrapper) to scan subreddits for relevant threads.
Read-only — never posts automatically.
"""
from __future__ import annotations
import time
import json
from pathlib import Path
from typing import Optional
import praw
from intelligence.relevance import Thread
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    REDDIT_SUBREDDITS, MAX_RESULTS_PER_SOURCE, SEEN_DIR
)

SEEN_FILE = SEEN_DIR / "reddit_seen.json"


def _load_seen() -> set[str]:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def _save_seen(seen: set[str]) -> None:
    # Keep only last 5000 IDs to prevent unbounded growth
    limited = list(seen)[-5000:]
    SEEN_FILE.write_text(json.dumps(limited))


def _make_client() -> Optional[praw.Reddit]:
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        return None
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        # Read-only mode — no username/password needed
    )


def fetch_threads(limit_per_sub: int = MAX_RESULTS_PER_SOURCE) -> list[Thread]:
    """
    Fetch recent and hot threads from monitored subreddits.
    Skips already-seen thread IDs. Returns normalized Thread objects.
    """
    client = _make_client()
    if client is None:
        print("[Reddit] Skipping — REDDIT_CLIENT_ID/SECRET not configured.")
        return []

    seen = _load_seen()
    threads: list[Thread] = []
    new_seen: set[str] = set()

    for subreddit_name in REDDIT_SUBREDDITS:
        try:
            subreddit = client.subreddit(subreddit_name)
            # Scan both 'new' (unanswered) and 'hot' (high visibility)
            posts = list(subreddit.new(limit=limit_per_sub // 2)) + \
                    list(subreddit.hot(limit=limit_per_sub // 2))

            for post in posts:
                if post.id in seen:
                    continue
                new_seen.add(post.id)

                # Skip extremely short posts (likely link-only)
                body = post.selftext or ""
                if len(body) < 20 and not post.title:
                    continue

                threads.append(Thread(
                    id=f"reddit_{post.id}",
                    source="reddit",
                    title=post.title,
                    body=body[:2000],  # truncate for scoring
                    url=f"https://reddit.com{post.permalink}",
                    author=str(post.author) if post.author else "[deleted]",
                    score=post.score,
                    created_utc=post.created_utc,
                    tags=[subreddit_name, f"flair:{post.link_flair_text or ''}"],
                ))

            time.sleep(0.5)  # Respect Reddit rate limits

        except Exception as e:
            print(f"[Reddit] Error scanning r/{subreddit_name}: {e}")
            continue

    seen.update(new_seen)
    _save_seen(seen)
    print(f"[Reddit] Fetched {len(threads)} new threads across {len(REDDIT_SUBREDDITS)} subreddits")
    return threads
