#!/usr/bin/env bash
# =============================================================================
# MAVIM setup.sh — Universal Project Initializer
# Multi-Agent VIbe coding Methodology
# Uso: bash <(curl -s https://raw.githubusercontent.com/MerariJafet/MAVIM/main/setup.sh)
# O:   bash setup.sh [--target /path/to/project] [--stack react|python|fullstack]
# =============================================================================
set -euo pipefail

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; RESET='\033[0m'

ok()   { echo -e "${GREEN}✅  $*${RESET}"; }
warn() { echo -e "${YELLOW}⚠️   $*${RESET}"; }
err()  { echo -e "${RED}❌  $*${RESET}"; exit 1; }
info() { echo -e "${BLUE}ℹ️   $*${RESET}"; }
hdr()  { echo -e "\n${BOLD}$*${RESET}"; }

# ── Banner ────────────────────────────────────────────────────────────────────
echo -e "${BOLD}"
cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║       MAVIM — Multi-Agent VIbe coding Methodology        ║
║                  Universal Project Setup                  ║
║            github.com/MerariJafet/MAVIM                  ║
╚═══════════════════════════════════════════════════════════╝
BANNER
echo -e "${RESET}"

# ── Args ──────────────────────────────────────────────────────────────────────
TARGET_DIR="${PWD}"
STACK="generic"
MAVIM_REPO="https://github.com/MerariJafet/MAVIM"
MAVIM_LOCAL=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --target) TARGET_DIR="$2"; shift 2 ;;
    --stack)  STACK="$2"; shift 2 ;;
    --local)  MAVIM_LOCAL="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: bash setup.sh [--target DIR] [--stack react|python|fullstack|generic] [--local /path/to/MAVIM]"
      exit 0 ;;
    *) warn "Unknown arg: $1"; shift ;;
  esac
done

# ── Step 1: Autodiscovery ─────────────────────────────────────────────────────
hdr "▶ Step 1/5 — Autodiscovery"

if [[ -n "$MAVIM_LOCAL" && -d "$MAVIM_LOCAL" ]]; then
  MAVIM_DIR="$MAVIM_LOCAL"
  ok "Using local MAVIM at $MAVIM_DIR"
elif [[ -d "${HOME}/MAVIM" ]]; then
  MAVIM_DIR="${HOME}/MAVIM"
  ok "Found MAVIM at $MAVIM_DIR"
elif [[ -d "./MAVIM" ]]; then
  MAVIM_DIR="./MAVIM"
  ok "Found MAVIM at $MAVIM_DIR"
else
  info "MAVIM not found locally. Cloning from GitHub..."
  git clone "$MAVIM_REPO" "${HOME}/MAVIM" || err "Failed to clone MAVIM. Check network connection."
  MAVIM_DIR="${HOME}/MAVIM"
  ok "Cloned MAVIM to $MAVIM_DIR"
fi

# ── Step 2: Target validation ─────────────────────────────────────────────────
hdr "▶ Step 2/5 — Target Project"

[[ ! -d "$TARGET_DIR" ]] && mkdir -p "$TARGET_DIR"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
ok "Target: $TARGET_DIR"

# Detect stack if not provided
if [[ "$STACK" == "generic" ]]; then
  [[ -f "$TARGET_DIR/package.json" ]]           && STACK="react"
  [[ -f "$TARGET_DIR/requirements.txt" || -f "$TARGET_DIR/pyproject.toml" ]] && STACK="python"
  [[ -f "$TARGET_DIR/package.json" && -f "$TARGET_DIR/requirements.txt" ]]   && STACK="fullstack"
fi
ok "Stack detected: $STACK"

# ── Step 3: Copy MAVIM core files ─────────────────────────────────────────────
hdr "▶ Step 3/5 — Installing MAVIM Core Files"

# MAVIM.md (single source of truth)
cp "$MAVIM_DIR/MAVIM.md" "$TARGET_DIR/MAVIM.md"
ok "MAVIM.md → source of truth installed"

# CLAUDE.md (stub for Claude Code compatibility)
cp "$MAVIM_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
ok "CLAUDE.md → agent stub installed"

# scripts/
mkdir -p "$TARGET_DIR/scripts"
for script in mavim_scan.sh health_check.sh write_bridge.py; do
  if [[ -f "$MAVIM_DIR/scripts/$script" ]]; then
    cp "$MAVIM_DIR/scripts/$script" "$TARGET_DIR/scripts/$script"
    ok "scripts/$script installed"
  else
    warn "scripts/$script not found in MAVIM — skipping"
  fi
done

# ── Step 4: Bootstrap project artifacts ───────────────────────────────────────
hdr "▶ Step 4/5 — Bootstrapping Project Artifacts"

PROJECT_NAME="$(basename "$TARGET_DIR")"
TODAY="$(date +%Y-%m-%d)"

# COGNITIVE_BRIDGE.json skeleton
if [[ ! -f "$TARGET_DIR/COGNITIVE_BRIDGE.json" ]]; then
  cat > "$TARGET_DIR/COGNITIVE_BRIDGE.json" << EOF
{
  "project": "$PROJECT_NAME",
  "methodology": "MAVIM",
  "created": "$TODAY",
  "state": {
    "health": "GREEN",
    "phase": "setup",
    "sprint": 0
  },
  "completed_tasks": [],
  "pending_tasks": [
    "Run SOP_09 environment scan",
    "Define INTENT_MANIFEST (SOP_01)",
    "Create ARCHITECTURE_CONTRACT (SOP_02)"
  ],
  "known_hazards": [],
  "adr": [],
  "handoff_instructions": {
    "first_actions": [
      "Read MAVIM.md",
      "Run bash scripts/mavim_scan.sh",
      "Review pending_tasks in this file"
    ]
  }
}
EOF
  ok "COGNITIVE_BRIDGE.json skeleton created"
else
  warn "COGNITIVE_BRIDGE.json already exists — not overwritten"
fi

# .gitignore additions
if [[ -f "$TARGET_DIR/.gitignore" ]]; then
  if ! grep -q "COGNITIVE_BRIDGE.json" "$TARGET_DIR/.gitignore" 2>/dev/null; then
    echo -e "\n# MAVIM\nENVIRONMENT_SNAPSHOT.json\n.mavim_cache/" >> "$TARGET_DIR/.gitignore"
    ok ".gitignore updated with MAVIM entries"
  else
    info ".gitignore already has MAVIM entries"
  fi
fi

# Stack-specific additions
case "$STACK" in
  react|fullstack)
    if [[ -f "$TARGET_DIR/package.json" ]] && ! grep -q "test:smoke" "$TARGET_DIR/package.json" 2>/dev/null; then
      info "Add 'test:smoke' script to package.json manually:"
      info '  "test:smoke": "playwright test e2e/smoke.spec.ts --project=chromium"'
    fi
    ;;
esac

# ── Step 5: Environment scan ──────────────────────────────────────────────────
hdr "▶ Step 5/5 — Environment Scan (SOP_09)"

if [[ -f "$TARGET_DIR/scripts/mavim_scan.sh" ]]; then
  info "Running environment scan..."
  bash "$TARGET_DIR/scripts/mavim_scan.sh" 2>/dev/null && ok "Scan complete" || warn "Scan script needs configuration for this project"
else
  warn "mavim_scan.sh not available — run SOP_09 manually"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}════════════════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}  MAVIM initialized in: $TARGET_DIR${RESET}"
echo -e "${BOLD}════════════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  Next steps:"
echo -e "  ${YELLOW}1.${RESET} Read MAVIM.md — your source of truth"
echo -e "  ${YELLOW}2.${RESET} Run: ${BOLD}cat COGNITIVE_BRIDGE.json${RESET}"
echo -e "  ${YELLOW}3.${RESET} Start with SOP_09 → SOP_01 → SOP_02"
echo ""
echo -e "  Activate any agent with:"
echo -e "  ${BOLD}Actúa como MAVIM-ORCHESTRATOR, lee MAVIM.md y ejecuta los protocolos para [TU_TAREA]${RESET}"
echo ""
