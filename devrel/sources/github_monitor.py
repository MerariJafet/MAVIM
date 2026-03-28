"""
MAVIM DevRel — GitHub Discussions & Issues Monitor
Uses PyGithub to scan discussions and issues in relevant repos.
Also monitors MAVIM repo itself for incoming questions.
Read-only.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from github import Github, GithubException
from intelligence.relevance import Thread
from config import GITHUB_TOKEN, GITHUB_REPOS_TO_WATCH, MAVIM_REPO_URL, SEEN_DIR

SEEN_FILE = SEEN_DIR / "github_seen.json"
MAVIM_REPO = "MerariJafet/MAVIM"


def _load_seen() -> set[str]:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def _save_seen(seen: set[str]) -> None:
    SEEN_FILE.write_text(json.dumps(list(seen)[-5000:]))


def _make_client() -> Github | None:
    if not GITHUB_TOKEN:
        print("[GitHub] Skipping — GITHUB_TOKEN not configured.")
        return None
    return Github(GITHUB_TOKEN)


def fetch_threads(limit_per_repo: int = 20) -> list[Thread]:
    """
    Fetch recent issues and discussions from monitored repos.
    Also monitors incoming issues/discussions on the MAVIM repo itself.
    """
    client = _make_client()
    if client is None:
        return []

    seen = _load_seen()
    threads: list[Thread] = []
    new_seen: set[str] = set()

    all_repos = list(set(GITHUB_REPOS_TO_WATCH + [MAVIM_REPO]))

    for repo_name in all_repos:
        try:
            repo = client.get_repo(repo_name)
            is_own_repo = repo_name == MAVIM_REPO

            # ── Issues ────────────────────────────────────────────────────
            issues = repo.get_issues(state="open", sort="created", direction="desc")
            count = 0
            for issue in issues:
                if count >= limit_per_repo:
                    break
                if issue.pull_request:  # Skip PRs
                    continue

                item_id = f"gh_issue_{repo_name}_{issue.number}"
                if item_id in seen:
                    count += 1
                    continue
                new_seen.add(item_id)
                count += 1

                body = issue.body or ""
                # Own repo issues are always high priority
                score = (issue.reactions.get("total_count", 0) + 1) * (10 if is_own_repo else 1)

                threads.append(Thread(
                    id=item_id,
                    source="github",
                    title=f"[{repo_name}] {issue.title}",
                    body=body[:2000],
                    url=issue.html_url,
                    author=issue.user.login if issue.user else "unknown",
                    score=score,
                    created_utc=issue.created_at.timestamp(),
                    tags=[label.name for label in issue.labels] + [repo_name],
                ))

            time.sleep(0.2)

        except GithubException as e:
            print(f"[GitHub] Error accessing {repo_name}: {e.status} {e.data}")
            continue
        except Exception as e:
            print(f"[GitHub] Unexpected error for {repo_name}: {e}")
            continue

    seen.update(new_seen)
    _save_seen(seen)
    print(f"[GitHub] Fetched {len(threads)} new items across {len(all_repos)} repos")
    return threads


def fetch_mavim_feedback() -> list[Thread]:
    """
    Specifically monitors the MAVIM repo for incoming questions and feedback.
    These get highest priority — someone is actively engaging with MAVIM.
    """
    client = _make_client()
    if client is None:
        return []

    threads = []
    try:
        repo = client.get_repo(MAVIM_REPO)
        for issue in repo.get_issues(state="open"):
            if issue.pull_request:
                continue
            threads.append(Thread(
                id=f"mavim_feedback_{issue.number}",
                source="github",
                title=f"[MAVIM Feedback] {issue.title}",
                body=issue.body or "",
                url=issue.html_url,
                author=issue.user.login if issue.user else "unknown",
                score=999,  # Always highest priority
                created_utc=issue.created_at.timestamp(),
                tags=["mavim-feedback"],
            ))
    except Exception as e:
        print(f"[GitHub] Error fetching MAVIM feedback: {e}")

    return threads
