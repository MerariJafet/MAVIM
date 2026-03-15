"""
MAVIM DevRel — Relevance Scoring Engine
Scores discussion threads against MAVIM's value proposition
and maps them to specific SOPs.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional
from config import MAVIM_KEYWORDS, MAVIM_SOP_MAP, MIN_RELEVANCE_SCORE


@dataclass
class Thread:
    """Normalized representation of a discussion thread from any source."""
    id: str
    source: str          # "reddit" | "stackoverflow" | "github"
    title: str
    body: str
    url: str
    author: str
    score: int           # upvotes / views / reactions
    created_utc: float
    tags: list[str] = field(default_factory=list)
    # Computed by scorer
    relevance_score: float = 0.0
    matched_keywords: list[str] = field(default_factory=list)
    mapped_sops: list[dict] = field(default_factory=list)
    priority: str = "LOW"  # LOW | MEDIUM | HIGH | CRITICAL


def score_thread(thread: Thread) -> Thread:
    """
    Compute relevance score and map to MAVIM SOPs.
    Returns the thread with relevance_score, matched_keywords, mapped_sops filled.
    """
    text = f"{thread.title} {thread.body} {' '.join(thread.tags)}".lower()
    total_score = 0.0
    matched: list[str] = []

    # Keyword scoring
    for kw in MAVIM_KEYWORDS["critical"]:
        if kw.lower() in text:
            total_score += 3.0
            matched.append(kw)

    for kw in MAVIM_KEYWORDS["high"]:
        if kw.lower() in text:
            total_score += 1.5
            matched.append(kw)

    for kw in MAVIM_KEYWORDS["medium"]:
        if kw.lower() in text:
            total_score += 0.5
            matched.append(kw)

    # Boost for question indicators (unanswered or low-answer threads are opportunities)
    question_signals = ["how do i", "how to", "why does", "is there a way",
                        "does anyone", "best way to", "struggling with", "help with",
                        "not working", "broken", "failing", "issue with"]
    for qs in question_signals:
        if qs in text:
            total_score += 1.0
            break

    # Boost for specific MAVIM pain points
    pain_patterns = [
        (r"agent.{0,30}(forget|lose|lost).{0,30}context", 3.0),
        (r"context.{0,30}(limit|window|full|overflow)", 2.5),
        (r"(dark.?mode|css).{0,30}(broken|wrong|hardcode)", 2.0),
        (r"refactor.{0,30}(broke|broken|regression)", 2.0),
        (r"(no|zero|without).{0,20}test", 1.5),
        (r"ai.{0,20}(autonomous|autonomously|itself)", 2.0),
        (r"(multi.?agent|agent.?orchestrat)", 3.0),
        (r"(vibe.?cod|vibecod)", 4.0),
    ]
    for pattern, boost in pain_patterns:
        if re.search(pattern, text):
            total_score += boost

    # Community score boost (popular threads = more visibility)
    if thread.score > 100:
        total_score += 1.5
    elif thread.score > 20:
        total_score += 0.5

    # Map to relevant SOPs
    mapped_sops = []
    for problem_id, sop_info in MAVIM_SOP_MAP.items():
        for kw in sop_info["keywords"]:
            if kw.lower() in text:
                if sop_info not in mapped_sops:
                    mapped_sops.append({
                        "problem": problem_id,
                        "sop": sop_info["sop"],
                        "url": sop_info["url"],
                        "summary": sop_info["summary"],
                    })
                break

    # Priority classification
    if total_score >= 12:
        priority = "CRITICAL"
    elif total_score >= 8:
        priority = "HIGH"
    elif total_score >= MIN_RELEVANCE_SCORE:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    thread.relevance_score = round(total_score, 2)
    thread.matched_keywords = list(set(matched))[:10]
    thread.mapped_sops = mapped_sops
    thread.priority = priority
    return thread


def filter_relevant(threads: list[Thread], min_score: float = MIN_RELEVANCE_SCORE) -> list[Thread]:
    """Score all threads and return only those meeting the minimum relevance threshold."""
    scored = [score_thread(t) for t in threads]
    relevant = [t for t in scored if t.relevance_score >= min_score]
    return sorted(relevant, key=lambda t: t.relevance_score, reverse=True)
