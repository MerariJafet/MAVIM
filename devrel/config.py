"""
MAVIM DevRel Intelligence System — Configuration
Central configuration and MAVIM knowledge base for relevance scoring.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
SEEN_DIR = DATA_DIR / "seen"

for d in [DATA_DIR, REPORTS_DIR, SEEN_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API Credentials ───────────────────────────────────────────────────────
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "mavim-devrel/1.0")

STACKOVERFLOW_KEY = os.getenv("STACKOVERFLOW_KEY", "")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
NOTIFY_SMTP_HOST = os.getenv("NOTIFY_SMTP_HOST", "smtp.gmail.com")
NOTIFY_SMTP_PORT = int(os.getenv("NOTIFY_SMTP_PORT", "587"))
NOTIFY_SMTP_USER = os.getenv("NOTIFY_SMTP_USER", "")
NOTIFY_SMTP_PASS = os.getenv("NOTIFY_SMTP_PASS", "")
NOTIFY_IMAP_HOST = os.getenv("NOTIFY_IMAP_HOST", "imap.gmail.com")

MAVIM_REPO_URL = os.getenv("MAVIM_REPO_URL", "https://github.com/MerariJafet/MAVIM")
MAVIM_DOCS_BASE = os.getenv("MAVIM_DOCS_BASE", "https://github.com/MerariJafet/MAVIM/blob/main")
SCAN_INTERVAL_MINUTES = int(os.getenv("SCAN_INTERVAL_MINUTES", "60"))

# ── MAVIM Knowledge Base for Relevance Scoring ───────────────────────────
# Keywords that indicate a thread is relevant to MAVIM's value proposition

MAVIM_KEYWORDS = {
    # Core problem space (highest weight)
    "critical": [
        "agent context", "ai agent", "agentic", "multi-agent", "llm agent",
        "context window", "context limit", "token limit", "agent memory",
        "agent loses context", "agent forgets", "agent loop", "agent autonomous",
        "vibe coding", "vibecoding", "ai coding", "autonomous coding",
        "claude code", "cursor ai", "codex", "windsurf",
        "agent orchestration", "agent framework",
    ],
    # Secondary signals (medium weight)
    "high": [
        "refactoring", "technical debt", "dark mode", "design system",
        "css variables", "tailwind", "shadcn", "playwright", "e2e testing",
        "react", "fastapi", "multi-tenant", "saas architecture",
        "prompt injection", "llm security", "ai workflow",
        "continuous improvement", "self-improving", "auto-fix",
        "code review ai", "ai architecture", "agent memory",
        "context management", "session handoff",
    ],
    # Tertiary signals (low weight)
    "medium": [
        "typescript", "python backend", "docker compose",
        "ci/cd", "github actions", "code quality",
        "software methodology", "engineering best practices",
        "ai tools", "developer productivity",
    ],
}

# MAVIM SOPs mapped to problem patterns — used for response drafting
MAVIM_SOP_MAP = {
    "context_loss": {
        "sop": "SOP_10_COGNITIVE_BRIDGE",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_10_COGNITIVE_BRIDGE.md",
        "summary": "COGNITIVE_BRIDGE.json transfiere el estado completo entre sesiones IA: tareas, decisiones arquitectónicas, peligros conocidos, y primeras acciones para el agente entrante.",
        "keywords": ["context", "session", "forget", "restart", "memory", "handoff"],
    },
    "blind_refactoring": {
        "sop": "SOP_07_REFACTORING",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_07_REFACTORING.md",
        "summary": "Modo Quirúrgico: IMPACT_MAP.json primero, luego cero cambios fuera del alcance. Nunca tocar código sin mapear dependencias.",
        "keywords": ["refactor", "breaking changes", "dependencies", "impact", "regression"],
    },
    "no_tests": {
        "sop": "SOP_08_AUTOMATED_TESTING",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_08_AUTOMATED_TESTING.md",
        "summary": "18 gates Playwright en Chromium real. Si Playwright falla, la cirugía no está terminada. El bucle de auto-mejora detectó un bug crítico de dark mode invisible en revisión manual.",
        "keywords": ["testing", "playwright", "e2e", "automated test", "no tests", "validation"],
    },
    "agent_environment": {
        "sop": "SOP_09_ENVIRONMENT_AWARENESS",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_09_ENVIRONMENT_AWARENESS.md",
        "summary": "Escaneo inicial obligatorio: stack, puertos, env vars, git state. Un agente que no conoce su entorno opera con alucinaciones de infraestructura.",
        "keywords": ["environment", "setup", "configuration", "env vars", "ports", "dependencies"],
    },
    "agent_architecture": {
        "sop": "SOP_02_ARCHITECTURE",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_02_ARCHITECTURE.md",
        "summary": "Monolito Modular con fronteras estrictas. UUIDs, Ledger para dinero, H3 para mapas. Bloques LEGO en vez de código spaghetti.",
        "keywords": ["architecture", "monolith", "microservices", "modular", "saas", "multi-tenant"],
    },
    "long_sessions": {
        "sop": "SOP_12_RESOURCE_OPTIMIZATION",
        "url": f"{MAVIM_DOCS_BASE}/core/SOP_12_RESOURCE_OPTIMIZATION.md",
        "summary": "4 estrategias: Context Pruning, Lazy Loading, Parallel Tool Execution, Decision Anchoring. Regla de los 3 intentos.",
        "keywords": ["long session", "token", "context bloat", "efficiency", "optimize", "slow"],
    },
}

# ── Reddit Subreddits to Monitor ──────────────────────────────────────────
REDDIT_SUBREDDITS = [
    "ClaudeAI",
    "ChatGPTCoding",
    "AIAssistants",
    "MachineLearning",
    "LocalLLaMA",
    "artificial",
    "programming",
    "Python",
    "reactjs",
    "webdev",
    "softwarearchitecture",
    "devops",
    "ExperiencedDevs",
]

# ── Stack Overflow Tags to Monitor ───────────────────────────────────────
STACKOVERFLOW_TAGS = [
    "ai-agent",
    "llm",
    "claude",
    "chatgpt",
    "react",
    "tailwindcss",
    "playwright",
    "fastapi",
    "multi-tenant",
    "software-architecture",
]

# ── GitHub Repos/Orgs to Monitor Discussions ─────────────────────────────
GITHUB_REPOS_TO_WATCH = [
    "anthropics/claude-code",
    "getcursor/cursor",
    "continuedev/continue",
    "microsoft/autogen",
    "langchain-ai/langchain",
]

# ── Scoring Thresholds ────────────────────────────────────────────────────
MIN_RELEVANCE_SCORE = 3      # Minimum score to include in report
HIGH_PRIORITY_SCORE = 8      # Score above which → immediate email notification
MAX_RESULTS_PER_SOURCE = 50  # Max items to fetch per scan per source
