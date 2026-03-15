# MAVIM — Master Interaction Contract for AI Agents

> Read this file completely before taking any action in this repository.
> This is the binding contract between any AI agent and the MAVIM ecosystem.

## What This Repository Is

MAVIM is a 12-SOP engineering methodology for AI agents building production software.
It is **not** an application — it is a framework of protocols, patterns, and case studies.

```
Type:     Documentation + tooling framework
Language: Markdown, Python, Bash
Audience: AI agents (Claude Code, Cursor, Codex) + human engineers
Repo:     github.com/MerariJafet/MAVIM
```

## Activation Sequence (Every Session)

Run in this exact order before any task:

```bash
# 1. Read this file (you are doing this now ✓)
# 2. Check Cognitive Bridge
cat COGNITIVE_BRIDGE.json 2>/dev/null || echo "No bridge — fresh session"
# 3. Environment scan
bash devrel/../showcase/../ 2>/dev/null || true
# 4. Confirm your understanding
echo "MAVIM agent ready. Phase: [state current phase from Bridge]"
```

## Repository Structure

```
MAVIM/
├── CLAUDE.md              ← You are here — read first, always
├── MAVIM.md               ← Agent instruction cheat sheet (read second)
├── COGNITIVE_BRIDGE.json  ← Session state transfer (read third)
├── core/                  ← SOPs 01–12 (the methodology)
├── patterns/              ← Architecture blueprints (LEGO blocks)
├── roles/                 ← Agent role definitions (Architect/Developer/Critic)
├── showcase/              ← Documented case studies with metrics
├── devrel/                ← Community intelligence tooling (Python)
├── prompts/               ← Meta-prompts and chain-of-thought templates
└── evals/                 ← Technical evaluation checklists
```

## Commands

```bash
# DevRel monitor (community intelligence)
cd devrel && source .venv/bin/activate
python monitor.py              # single scan
python monitor.py --watch      # continuous (every 60 min)
python monitor.py --dry-run    # no files saved, no email

# Health check (if running alongside itsme project)
bash ../itsme/scripts/health_check.sh 2>/dev/null || echo "itsme not available"
```

## Core Constraints — Non-Negotiable

### Documentation Quality
- Every new SOP must follow the exact format of existing SOPs (header, principles, protocol, checklist, references)
- SOP numbers are sequential — never reuse or skip
- The `## Checklist de Cumplimiento` section is mandatory in every SOP
- Cross-references between SOPs must use relative paths: `../core/SOP_XX_NAME.md`

### Content Integrity
- Never delete content from existing SOPs — append or create new sections
- `MAVIM.md` is the agent activation layer — changes must not break the activation sequence
- `README.md` is the public manifesto — tone is technical but accessible
- Case studies in `showcase/` must include real metrics, not estimates

### Commit Discipline
- One logical change per commit
- Commit message format: `feat(scope): description` or `fix(scope): description`
- Never commit `.env` files, `.venv/`, `__pycache__/`, or `data/` directories

## GSD Planning Gate (Required Before New SOPs or Patterns)

Before creating any new SOP or major pattern, answer these 5 questions:

```
1. PROBLEM: What specific failure mode does this address? (one sentence)
2. EVIDENCE: Where has this failure been observed? (cite source/project)
3. SCOPE: What is explicitly OUT of scope for this SOP?
4. VALIDATION: How will the agent know it applied this SOP correctly?
5. CONFLICT: Does this conflict with any existing SOP? (check SOPs 01–12)
```

Only proceed when all 5 are answered. Document the answers in the SOP's frontmatter.

## UI/UX Standards (for documentation and tooling interfaces)

When creating CLI output, reports, or any human-facing interface within MAVIM tooling:

**Information hierarchy:**
- Lead with status (GREEN/YELLOW/RED) before detail
- Use `rich` tables for structured data, never raw print loops
- Error messages: `[source] action failed: reason — suggested fix`
- Progress: spinner for unknown duration, bar for known steps

**Report structure:**
- Executive summary first (numbers only, no prose)
- CRITICAL items before HIGH before MEDIUM
- Collapsible detail sections (`<details>` in Markdown)
- Every actionable item must have an explicit next step

**Terminal color semantics (rich):**
- `green` = success, ready, passing
- `yellow` = warning, needs attention, degraded
- `red` = failure, blocked, requires immediate action
- `blue` = informational, in-progress
- `dim` = metadata, timestamps, secondary info

## Agent Role Assignment

When operating in this repository:

| Task | Role to assume |
|------|---------------|
| Creating a new SOP | MAVIM-Architect |
| Reviewing/auditing a SOP | MAVIM-Critic |
| Writing Python tooling | MAVIM-Developer |
| Integrating external standards | MAVIM-Orchestrator |
| Responding to community questions | DevRel (use `devrel/intelligence/draft_response.py`) |

## What This Repository Does NOT Need

- Unit tests for documentation
- A web server or API
- A database
- Authentication
- Docker containers (devrel tool runs locally with venv)
- More than 12 SOPs without clear evidence of a new failure mode

## Escalation Protocol

If you encounter ambiguity about what to build:

1. Read `COGNITIVE_BRIDGE.json` — the answer is likely in `pending_tasks`
2. Read the relevant SOP — the answer is likely in its checklist
3. If still unclear — ask the user ONE specific question, not multiple

Never start building something to fill ambiguity. Stop and ask.
