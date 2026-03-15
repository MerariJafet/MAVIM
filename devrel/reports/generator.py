"""
MAVIM DevRel — Report Generator
Produces structured Markdown opportunity reports with response drafts,
engagement metrics, and documentation improvement suggestions.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from intelligence.relevance import Thread
from intelligence.draft_response import generate_draft
from config import REPORTS_DIR, MAVIM_REPO_URL


def generate_report(
    threads: list[Thread],
    inbox_replies: list[dict] | None = None,
    previous_report: dict | None = None,
) -> tuple[str, str]:
    """
    Generate a Markdown opportunity report.
    Returns (report_markdown, report_file_path).
    """
    now = datetime.now(timezone.utc)
    report_id = now.strftime("%Y%m%d_%H%M")
    report_file = REPORTS_DIR / f"devrel_report_{report_id}.md"

    critical = [t for t in threads if t.priority == "CRITICAL"]
    high = [t for t in threads if t.priority == "HIGH"]
    medium = [t for t in threads if t.priority == "MEDIUM"]

    # Source breakdown
    sources = {"reddit": 0, "stackoverflow": 0, "github": 0}
    for t in threads:
        sources[t.source] = sources.get(t.source, 0) + 1

    # SOP demand analysis — which SOPs are most needed?
    sop_demand: dict[str, int] = {}
    for t in threads:
        for sop in t.mapped_sops:
            sop_name = sop["sop"]
            sop_demand[sop_name] = sop_demand.get(sop_name, 0) + 1

    # Docs improvement suggestions based on demand
    doc_suggestions = _generate_doc_suggestions(sop_demand, threads)

    md = f"""# MAVIM DevRel — Opportunity Report
**Generated:** {now.strftime("%Y-%m-%d %H:%M UTC")}
**Scan ID:** `{report_id}`

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total relevant threads | {len(threads)} |
| CRITICAL priority | {len(critical)} |
| HIGH priority | {len(high)} |
| MEDIUM priority | {len(medium)} |
| Reddit threads | {sources.get('reddit', 0)} |
| Stack Overflow | {sources.get('stackoverflow', 0)} |
| GitHub | {sources.get('github', 0)} |
| Community replies (inbox) | {len(inbox_replies or [])} |

---

## SOP Demand Analysis

Which MAVIM protocols are most needed in the community right now:

| SOP | Demand Count | Action |
|-----|-------------|--------|
"""
    for sop, count in sorted(sop_demand.items(), key=lambda x: -x[1])[:8]:
        action = "High demand — review docs clarity" if count >= 3 else "Normal"
        md += f"| {sop} | {count} | {action} |\n"

    md += "\n---\n\n"

    # CRITICAL threads with full drafts
    if critical:
        md += f"## CRITICAL Opportunities ({len(critical)})\n\n"
        md += "> These threads have the highest relevance score. Respond within 24h.\n\n"
        for t in critical[:5]:
            md += _format_thread_section(t)

    # HIGH threads with drafts
    if high:
        md += f"## HIGH Priority ({len(high)})\n\n"
        for t in high[:8]:
            md += _format_thread_section(t)

    # MEDIUM — summary only
    if medium:
        md += f"## MEDIUM Priority ({len(medium)}) — Summary\n\n"
        md += "| Thread | Source | Score | SOPs | URL |\n"
        md += "|--------|--------|-------|------|-----|\n"
        for t in medium[:15]:
            sops = ", ".join(s["sop"][:20] for s in t.mapped_sops[:2]) or "—"
            md += f"| {t.title[:50]}... | {t.source} | {t.relevance_score} | {sops} | [link]({t.url}) |\n"
        md += "\n"

    # Inbox replies
    if inbox_replies:
        md += "## Community Inbox Replies\n\n"
        for r in inbox_replies:
            md += f"- `[{r['source'].upper()}]` {r['subject']} — *from {r['from']}*\n"
        md += "\n"

    # Documentation suggestions
    if doc_suggestions:
        md += "## Documentation Improvement Suggestions\n\n"
        md += "> Based on recurring confusion patterns in this scan.\n\n"
        for sug in doc_suggestions:
            md += f"- **{sug['sop']}**: {sug['suggestion']}\n"
        md += "\n"

    md += f"""---

## How to Use This Report

1. **Review CRITICAL threads** — read the original post for full context
2. **Personalize the draft** — the opening line MUST reference their specific problem
3. **Remove inapplicable sections** — only include what directly helps
4. **Add a genuine question** — invite dialogue, don't just drop a link
5. **Post manually** — copy the draft to the platform and post as yourself
6. **Track the response** — note the thread URL for engagement follow-up

> **IMPORTANT:** Never post the draft verbatim. It's a starting point.
> Authentic responses get upvoted. Generic ones get downvoted or flagged.

---

*MAVIM DevRel Intelligence System — {MAVIM_REPO_URL}*
"""

    report_file.write_text(md)
    print(f"[Report] Generated: {report_file}")
    return md, str(report_file)


def _format_thread_section(thread: Thread) -> str:
    draft_data = generate_draft(thread)
    keywords_str = ", ".join(f"`{k}`" for k in thread.matched_keywords[:6])
    sops_str = " | ".join(
        f"[{s['sop']}]({s['url']})" for s in thread.mapped_sops[:2]
    ) or "No direct SOP match"

    return f"""### [{thread.title[:80]}]({thread.url})

**Source:** {thread.source.upper()} | **Priority:** {thread.priority} | **Relevance:** {thread.relevance_score}
**Author:** {thread.author} | **Community Score:** {thread.score}
**Matched signals:** {keywords_str}
**Relevant SOPs:** {sops_str}

<details>
<summary>📝 Response Draft ({draft_data['word_count']} words)</summary>

```
{draft_data['draft']}
```

**Tone notes:** {draft_data['tone_notes']}
**CTA:** {draft_data['cta']}
**⚠️ {draft_data['edit_reminder']}**

</details>

---

"""


def _generate_doc_suggestions(
    sop_demand: dict[str, int],
    threads: list[Thread],
) -> list[dict]:
    """
    Analyze patterns to suggest documentation improvements.
    High demand for a SOP = the documentation may not be findable or clear enough.
    """
    suggestions = []
    for sop, count in sop_demand.items():
        if count >= 4:
            suggestions.append({
                "sop": sop,
                "demand": count,
                "suggestion": (
                    f"High demand ({count} threads) — consider adding more concrete examples "
                    f"or a FAQ section. Community is finding the problem but may not find MAVIM's solution."
                ),
            })
        elif count >= 2:
            # Check if threads are from different sources (broader signal)
            sources_for_sop = set()
            for t in threads:
                for s in t.mapped_sops:
                    if s["sop"] == sop:
                        sources_for_sop.add(t.source)
            if len(sources_for_sop) >= 2:
                suggestions.append({
                    "sop": sop,
                    "demand": count,
                    "suggestion": (
                        f"Appearing across {len(sources_for_sop)} platforms — "
                        f"cross-link this SOP from the README quick-start section."
                    ),
                })

    return suggestions[:6]


def load_previous_report() -> dict | None:
    """Load the most recent report for comparison/trend analysis."""
    reports = sorted(REPORTS_DIR.glob("devrel_report_*.json"), reverse=True)
    if not reports:
        return None
    try:
        return json.loads(reports[0].read_text())
    except Exception:
        return None
