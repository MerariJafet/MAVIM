"""
MAVIM DevRel — Stack Overflow Monitor
Uses the official Stack Exchange API (via stackapi) to find unanswered questions.
Prioritizes questions with 0 accepted answers — highest opportunity.
Read-only.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Optional
from stackapi import StackAPI
from intelligence.relevance import Thread
from config import STACKOVERFLOW_KEY, STACKOVERFLOW_TAGS, MAX_RESULTS_PER_SOURCE, SEEN_DIR

SEEN_FILE = SEEN_DIR / "stackoverflow_seen.json"


def _load_seen() -> set[str]:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def _save_seen(seen: set[str]) -> None:
    SEEN_FILE.write_text(json.dumps(list(seen)[-5000:]))


def fetch_threads(limit_per_tag: int = 25) -> list[Thread]:
    """
    Fetch recent unanswered questions for monitored tags.
    Focuses on questions with no accepted answer — highest value to answer.
    """
    try:
        kwargs = {"key": STACKOVERFLOW_KEY} if STACKOVERFLOW_KEY else {}
        site = StackAPI("stackoverflow", **kwargs)
        site.max_pages = 1
    except Exception as e:
        print(f"[StackOverflow] Init error: {e}")
        return []

    seen = _load_seen()
    threads: list[Thread] = []
    new_seen: set[str] = set()

    for tag in STACKOVERFLOW_TAGS:
        try:
            # Fetch recent questions — unanswered first
            result = site.fetch(
                "questions",
                tagged=tag,
                sort="creation",
                order="desc",
                pagesize=min(limit_per_tag, 50),
                filter="withbody",  # Include question body
            )
            questions = result.get("items", [])

            for q in questions:
                qid = str(q["question_id"])
                if qid in seen:
                    continue
                new_seen.add(qid)

                # Boost score for unanswered questions (prime opportunity)
                base_score = q.get("score", 0)
                if q.get("answer_count", 1) == 0:
                    base_score += 5  # Unanswered = highest opportunity
                elif not q.get("is_answered", True):
                    base_score += 2  # Has answers but none accepted

                body = q.get("body", "") or q.get("body_markdown", "")
                # Strip HTML tags for cleaner text
                import re
                body = re.sub(r"<[^>]+>", " ", body)[:2000]

                threads.append(Thread(
                    id=f"so_{qid}",
                    source="stackoverflow",
                    title=q["title"],
                    body=body,
                    url=q["link"],
                    author=q.get("owner", {}).get("display_name", "anonymous"),
                    score=base_score,
                    created_utc=float(q["creation_date"]),
                    tags=q.get("tags", []),
                ))

            time.sleep(0.3)  # SE API rate limit

        except Exception as e:
            print(f"[StackOverflow] Error fetching tag '{tag}': {e}")
            continue

    seen.update(new_seen)
    _save_seen(seen)
    print(f"[StackOverflow] Fetched {len(threads)} new questions across {len(STACKOVERFLOW_TAGS)} tags")
    return threads
