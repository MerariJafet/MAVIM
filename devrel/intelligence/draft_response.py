"""
MAVIM DevRel — Response Draft Generator
Generates high-value technical response drafts grounded in MAVIM documentation.
The human DevRel engineer reviews, personalizes, and decides whether to post.
"""
from __future__ import annotations
from intelligence.relevance import Thread
from config import MAVIM_REPO_URL, MAVIM_DOCS_BASE


# Response templates per problem type — grounded in real MAVIM docs
_TEMPLATES: dict[str, str] = {

    "context_loss": """\
This is one of the core problems MAVIM (a methodology for AI agent engineering) \
addresses with its **Cognitive Bridge** pattern.

The idea: at the end of each session, the agent writes a `COGNITIVE_BRIDGE.json` \
that captures:
- Completed tasks and pending work
- Architecture decisions made (with reasoning)
- Known dangers / gotchas encountered
- Exact `first_actions` for the next agent instance

On session start, the incoming agent reads this before taking any action. \
It's model-agnostic — works with Claude, GPT-4o, Gemini, or local agents.

The full protocol is documented here:
{sop_url}

The key insight: if the information is already in a file in the repo, \
it doesn't need to live in the context window. The agent can re-read \
in milliseconds what it spent tokens to understand originally.""",

    "blind_refactoring": """\
The pattern you're describing — AI modifying code and breaking unrelated things — \
is what MAVIM calls "blind surgery."

The fix is the **Surgical Refactoring** protocol (SOP_07):

1. **Generate an IMPACT_MAP first** — before touching any code, map every file \
that depends on what you're changing. This is the mandatory first deliverable, no exceptions.
2. **Isolate in a branch** — never operate on main until you have a smoke test baseline
3. **Zero changes outside the defined scope** — if it's not in the impact map, don't touch it
4. **Validate with E2E tests before merge** — not "it compiles", but "it works in a real browser"

Real example from the It's Me project: a Badge component had a hardcoded \
`bg-slate-100` that was invisible in light mode reviews but broke dark mode completely. \
Manual review missed it. Playwright running with `data-theme=dark` caught it in 23 seconds.

Full SOP: {sop_url}""",

    "no_tests": """\
For AI-assisted development specifically, unit tests / jsdom tests are insufficient. \
You need **real browser validation** because the AI can produce code that is syntactically \
correct, passes TypeScript, and still has broken CSS or runtime behavior.

MAVIM's approach is 18 mandatory Playwright gates in Chromium:

- React mounts without console errors
- CSS variables are defined (design system exists)
- Dark mode activates correctly
- Protected routes redirect without auth token
- Forms have correct Shadcn components
- Loading states use Skeleton (not plain "Loading..." text)

The gate that catches what code review misses: activating `data-theme=dark` \
and scanning all visible elements for hardcoded color classes. Found a critical \
bug that 3 manual reviews had approved.

The loop: run → read `mavim-trace.json` failure_summary → surgical fix → re-run. \
When `"failed": 0` → merge.

Details: {sop_url}""",

    "agent_environment": """\
This class of failures — agent executing commands that fail because it assumed \
the wrong Node version, wrong port, missing env var — has a name in MAVIM: \
**infrastructure hallucination**.

SOP_09 (Environment Awareness) mandates a scan in the first 60 seconds of \
any session:

```bash
bash scripts/mavim_scan.sh
# → ENVIRONMENT_SNAPSHOT.json with status GREEN/YELLOW/RED
```

It checks: runtime versions, ports in use, env var presence (not values — \
never leak secrets), disk space, git state, installed dependencies.

If status is RED → communicate to user before doing anything else.
If YELLOW → resolve warnings before surgery.

The principle: *"An agent that doesn't know its environment operates with \
infrastructure hallucinations."*

Full script pattern: {sop_url}""",

    "long_sessions": """\
Long AI sessions degrade in three specific ways that MAVIM's SOP_12 addresses:

1. **Context bloat** — old error traces, resolved debugging, file explorations \
that are now irrelevant consuming the context window
2. **Tool repetition** — re-reading the same files multiple times
3. **Decision drift** — architecture decisions made at minute 5 forgotten by minute 60

The fixes:

**Context Pruning:** If information is in a file in the repo, it doesn't need \
to be in context. Write a Cognitive Bridge (SOP_10), then continue from that state.

**Parallel tool execution:** Independent file reads, independent writes → \
execute in a single message. 40-60% session time reduction.

**Decision Anchoring:** At the start of each new task in a long session, \
re-read `COGNITIVE_BRIDGE.json` (takes 5 seconds). Prevents architectural drift.

**The 3-attempt rule:** Same approach failing 3 times → STOP. Diagnose root cause \
or escalate to user. Never attempt 4+ times with the same strategy.

Full protocol: {sop_url}""",

    "agent_architecture": """\
For multi-tenant SaaS with AI agents, MAVIM's architecture pattern is the \
**Modular Monolith** — not microservices, not a big ball of mud.

Key constraints it enforces:
- UUIDs everywhere (never sequential IDs — they leak tenant info and block distribution)
- Ledger pattern for money (append-only, never UPDATE balance rows)
- H3 spatial indexing for geo features
- Strict module boundaries — cross-module imports are a red flag in code review
- Row Level Security at DB level for tenant isolation, not just in application code

The reason for monolith over microservices at early SaaS stage: \
the agent can navigate and refactor a monolith with full context. \
Microservices require network contracts the agent can break silently.

Architecture SOP: {sop_url}
Multi-tenant pattern: {mavim_repo}/blob/main/patterns/04_SAAS_MULTITENANT.md""",
}


def generate_draft(thread: Thread) -> dict[str, str]:
    """
    Generate a response draft for a thread based on its mapped SOPs.
    Returns dict with 'draft', 'tone_notes', 'cta', 'sops_referenced'.
    """
    if not thread.mapped_sops:
        return _generic_draft(thread)

    # Use the highest-priority mapped SOP
    primary_sop = thread.mapped_sops[0]
    problem_id = primary_sop["problem"]
    sop_url = primary_sop["url"]

    template = _TEMPLATES.get(problem_id)
    if not template:
        return _generic_draft(thread)

    draft_body = template.format(
        sop_url=sop_url,
        mavim_repo=MAVIM_REPO_URL,
    )

    # Add secondary SOP references if relevant
    if len(thread.mapped_sops) > 1:
        secondary = thread.mapped_sops[1]
        draft_body += f"\n\nRelated pattern that might also help: [{secondary['sop']}]({secondary['url']})"

    return {
        "draft": draft_body,
        "tone_notes": _tone_notes(thread.source),
        "cta": _cta(thread.source),
        "sops_referenced": [s["sop"] for s in thread.mapped_sops],
        "word_count": len(draft_body.split()),
        "edit_reminder": (
            "REVIEW BEFORE POSTING: personalize the opening line to reference "
            "the specific problem in the thread. Remove any section that doesn't "
            "directly apply. Add a genuine question at the end to invite dialogue."
        ),
    }


def _generic_draft(thread: Thread) -> dict[str, str]:
    keywords_str = ", ".join(thread.matched_keywords[:4]) if thread.matched_keywords else "agent orchestration"
    return {
        "draft": (
            f"The challenges around {keywords_str} in AI-assisted development "
            f"are exactly what MAVIM (a methodology for agentic engineering) was "
            f"designed for. The core insight: agents need structured protocols, "
            f"not just prompts.\n\n"
            f"The full framework is open source: {MAVIM_REPO_URL}\n\n"
            f"Specifically relevant to your situation: the SOP index in MAVIM.md "
            f"maps common problems to protocols. Which aspect is blocking you most?"
        ),
        "tone_notes": _tone_notes(thread.source),
        "cta": _cta(thread.source),
        "sops_referenced": [],
        "word_count": 80,
        "edit_reminder": "Generic draft — personalize heavily before posting.",
    }


def _tone_notes(source: str) -> str:
    notes = {
        "reddit": (
            "Reddit tone: conversational, no marketing language. "
            "Lead with the technical solution, MAVIM reference comes second. "
            "Redditors flag self-promotion — be a developer helping a developer."
        ),
        "stackoverflow": (
            "SO tone: precise, structured, code-first. "
            "Use code blocks for any commands. Reference documentation with direct links. "
            "Avoid opinion language — SO prefers factual, reproducible answers."
        ),
        "github": (
            "GitHub tone: technical peer, constructive. "
            "Acknowledge their specific use case before offering the solution. "
            "Link to specific SOP sections, not just the repo root."
        ),
    }
    return notes.get(source, "Be technical, helpful, and concise. Lead with value.")


def _cta(source: str) -> str:
    ctas = {
        "reddit": "End with a genuine question to continue the conversation.",
        "stackoverflow": "No CTA needed — SO rewards direct answers. Just answer.",
        "github": "Offer to elaborate or open a discussion in the MAVIM repo.",
    }
    return ctas.get(source, "Invite follow-up questions.")
