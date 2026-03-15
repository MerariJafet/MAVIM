# SOP_11 — HEALTH CHECK (Reporte Visual de Salud del Sistema)

**Versión:** 1.0.0
**Fecha:** 2026-03-14
**Autor:** MAVIM-ORCHESTRATOR
**Estado:** ACTIVO — Ejecutar antes de merge, después de deploy, y bajo demanda

---

## 1. Propósito

El agente necesita una **vista unificada y legible** del estado del sistema completo antes de tomar decisiones. Un reporte de salud fragmentado (logs aquí, métricas allá, tests en otro lado) produce decisiones erróneas. Este SOP define el protocolo para generar un **Health Dashboard** que el agente puede consumir en segundos y que cualquier humano puede entender de un vistazo.

---

## 2. Principio Rector

> **"Lo que no se mide no se puede reparar. Lo que no se visualiza no se entiende."**

El Health Check no es un simple `ping`. Es el cuadro de mando completo del sistema: infraestructura, código, tests, y experiencia de usuario — todo en un solo reporte con semáforo visual.

---

## 3. Los 5 Dominios de Salud

```
┌─────────────────────────────────────────────────────────────┐
│              MAVIM HEALTH DASHBOARD                          │
├─────────┬──────────────┬───────────────────────────────────┤
│ Dominio │   Estado     │   Descripción                      │
├─────────┼──────────────┼───────────────────────────────────┤
│  CODE   │  🟢 GREEN    │  Build OK, 0 TS errors, lint pass  │
│  TESTS  │  🟢 GREEN    │  18/18 Playwright gates passing    │
│  API    │  🟡 YELLOW   │  Backend up, 2 endpoints lentos    │
│  DATA   │  🟢 GREEN    │  DB conectada, migraciones al día  │
│  UX     │  🟢 GREEN    │  0 errores frontend en 24h         │
└─────────┴──────────────┴───────────────────────────────────┘
Overall: 🟡 YELLOW — Investigar latencia en /api/appointments
```

---

## 4. Protocolo de Ejecución

### Gate 1 — Code Health

```bash
# TypeScript — 0 errores es el único resultado aceptable
cd frontend && npx tsc --noEmit 2>&1 | tail -5
echo "TS_ERRORS: $(npx tsc --noEmit 2>&1 | grep -c 'error TS' || echo 0)"

# Build — debe completar sin warnings críticos
npm run build 2>&1 | grep -E '(error|warning|Error)' | grep -v '//' | head -10
```

**Criterio:** `TS_ERRORS = 0` → 🟢 | `> 0` → 🔴

### Gate 2 — Test Health

```bash
# Playwright — todos los gates deben pasar
cd frontend && npm run test:smoke 2>&1 | tail -5
cat playwright-report/mavim-trace.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'PASSED: {data[\"passed\"]}/{data[\"total\"]}')
print(f'STATUS: {\"GREEN\" if data[\"failed\"] == 0 else \"RED\"}')
"
```

**Criterio:** `failed = 0` → 🟢 | `failed > 0` → 🔴

### Gate 3 — API Health

```bash
# Backend health check
curl -sf http://localhost:8000/health | python3 -m json.tool

# Diagnóstico completo MAVIM
curl -sf http://localhost:8000/api/diagnostics/snapshot | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'API STATUS: {data[\"status\"]}')
print(f'DB: {data[\"health\"].get(\"database\", \"unknown\")}')
for w in data.get('warnings', []):
    print(f'  ⚠ {w}')
"

# Frontend errors acumulados
curl -sf http://localhost:8000/api/diagnostics/errors | python3 -c "
import json, sys
data = json.load(sys.stdin)
count = data.get('total_stored', 0)
print(f'FRONTEND_ERRORS: {count} ({\"GREEN\" if count == 0 else \"RED\"})')
"
```

**Criterio:** `status: ok` + `DB: ok` → 🟢 | warnings → 🟡 | error → 🔴

### Gate 4 — Data Health

```bash
# Migraciones aplicadas
python3 -c "
import os, psycopg2
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \'public\'')
    tables = cur.fetchone()[0]
    print(f'TABLES: {tables}')
    print('DB_STATUS: GREEN')
except Exception as e:
    print(f'DB_STATUS: RED — {e}')
"
```

**Criterio:** tables > 0 + sin errores → 🟢 | error de conexión → 🔴

### Gate 5 — UX Health

```bash
# Errores de frontend en las últimas 24h
curl -sf http://localhost:8000/api/diagnostics/errors | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta
data = json.load(sys.stdin)
cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
recent = [e for e in data.get('errors', [])
          if datetime.fromisoformat(e['received_at']) > cutoff]
print(f'UX_ERRORS_24H: {len(recent)}')
for e in recent[:3]:
    print(f'  [{e[\"error_type\"]}] {e[\"message\"][:80]}')
"
```

**Criterio:** `0 errores en 24h` → 🟢 | `1-5` → 🟡 | `>5` → 🔴

---

## 5. Script Unificado: `scripts/health_check.sh`

```bash
#!/usr/bin/env bash
# MAVIM SOP_11 — Full Health Check
# Uso: bash scripts/health_check.sh [--json]

set -uo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JSON_MODE="${1:-}"

declare -A STATUS
declare -A DETAILS

# ── Gate 1: Code ──────────────────────────────────────────────
TS_ERRORS=$(cd "$PROJECT_ROOT/frontend" && npx tsc --noEmit 2>&1 | grep -c 'error TS' || echo 0)
if [[ "$TS_ERRORS" -eq 0 ]]; then
    STATUS[CODE]="GREEN"; DETAILS[CODE]="0 TypeScript errors"
else
    STATUS[CODE]="RED"; DETAILS[CODE]="$TS_ERRORS TypeScript errors"
fi

# ── Gate 2: Tests ─────────────────────────────────────────────
TRACE="$PROJECT_ROOT/frontend/playwright-report/mavim-trace.json"
if [[ -f "$TRACE" ]]; then
    FAILED=$(python3 -c "import json; d=json.load(open('$TRACE')); print(d.get('failed',1))")
    PASSED=$(python3 -c "import json; d=json.load(open('$TRACE')); print(d.get('passed',0))")
    TOTAL=$(python3 -c "import json; d=json.load(open('$TRACE')); print(d.get('total',18))")
    if [[ "$FAILED" -eq 0 ]]; then
        STATUS[TESTS]="GREEN"; DETAILS[TESTS]="$PASSED/$TOTAL gates passing"
    else
        STATUS[TESTS]="RED"; DETAILS[TESTS]="$FAILED failures ($PASSED/$TOTAL passing)"
    fi
else
    STATUS[TESTS]="YELLOW"; DETAILS[TESTS]="No test results found — run npm run test:smoke"
fi

# ── Gate 3: API ───────────────────────────────────────────────
API_HEALTH=$(curl -sf --max-time 3 http://localhost:8000/health 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','error'))" 2>/dev/null || echo "unreachable")
if [[ "$API_HEALTH" == "ok" ]]; then
    DIAG=$(curl -sf --max-time 5 http://localhost:8000/api/diagnostics/snapshot 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','UNKNOWN'))" 2>/dev/null || echo "UNKNOWN")
    STATUS[API]="$DIAG"; DETAILS[API]="Backend up — diagnostics: $DIAG"
else
    STATUS[API]="RED"; DETAILS[API]="Backend unreachable at :8000"
fi

# ── Gate 4: Frontend Errors (UX) ─────────────────────────────
FE_ERRORS=$(curl -sf --max-time 3 http://localhost:8000/api/diagnostics/errors 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('total_stored',0))" 2>/dev/null || echo "?")
if [[ "$FE_ERRORS" == "?" ]]; then
    STATUS[UX]="YELLOW"; DETAILS[UX]="Cannot reach diagnostics endpoint"
elif [[ "$FE_ERRORS" -eq 0 ]]; then
    STATUS[UX]="GREEN"; DETAILS[UX]="0 frontend errors"
elif [[ "$FE_ERRORS" -lt 5 ]]; then
    STATUS[UX]="YELLOW"; DETAILS[UX]="$FE_ERRORS frontend errors — review /api/diagnostics/errors"
else
    STATUS[UX]="RED"; DETAILS[UX]="$FE_ERRORS frontend errors — immediate attention required"
fi

# ── Overall ───────────────────────────────────────────────────
OVERALL="GREEN"
for domain in CODE TESTS API UX; do
    [[ "${STATUS[$domain]}" == "RED" ]] && OVERALL="RED" && break
    [[ "${STATUS[$domain]}" == "YELLOW" ]] && OVERALL="YELLOW"
done

# ── Render ────────────────────────────────────────────────────
icon() { case $1 in GREEN) echo "🟢";; YELLOW) echo "🟡";; RED) echo "🔴";; *) echo "⚪";; esac; }

if [[ "$JSON_MODE" == "--json" ]]; then
    python3 - <<PYEOF
import json
print(json.dumps({
    "overall": "$OVERALL",
    "domains": {
        "code": {"status": "${STATUS[CODE]}", "detail": "${DETAILS[CODE]}"},
        "tests": {"status": "${STATUS[TESTS]}", "detail": "${DETAILS[TESTS]}"},
        "api": {"status": "${STATUS[API]}", "detail": "${DETAILS[API]}"},
        "ux": {"status": "${STATUS[UX]}", "detail": "${DETAILS[UX]}"}
    }
}, indent=2))
PYEOF
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  MAVIM SOP_11 — System Health Dashboard"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "  %-8s  %s  %s\n" "Domain" "St" "Detail"
    echo "  ──────────────────────────────────────────────"
    for domain in CODE TESTS API UX; do
        printf "  %-8s  %s  %s\n" "$domain" "$(icon ${STATUS[$domain]})" "${DETAILS[$domain]}"
    done
    echo "  ──────────────────────────────────────────────"
    echo "  Overall   $(icon $OVERALL)  $OVERALL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi
```

---

## 6. Integración con CI/CD

Agregar al workflow:

```yaml
- name: MAVIM Health Check
  run: bash scripts/health_check.sh --json > health-report.json
  working-directory: .

- name: Gate — Fail if RED
  run: |
    OVERALL=$(cat health-report.json | python3 -c "import json,sys; print(json.load(sys.stdin)['overall'])")
    if [ "$OVERALL" = "RED" ]; then
      echo "❌ Health check RED — blocking merge"
      cat health-report.json
      exit 1
    fi
    echo "✅ Health check: $OVERALL"
```

---

## 7. Interpretación para el Agente

| Overall | Acción del agente |
|---------|------------------|
| 🟢 GREEN | Proceder con la siguiente tarea del `COGNITIVE_BRIDGE.json` |
| 🟡 YELLOW | Investigar warnings antes de nueva cirugía. No bloquea operación. |
| 🔴 RED | **STOP.** Diagnosticar y reparar antes de cualquier otra acción. Leer domain con RED para causa raíz. |

---

## 8. Checklist de Cumplimiento

- [ ] `scripts/health_check.sh` ejecuta sin errores en el entorno del proyecto
- [ ] Dashboard visual legible en < 10 segundos
- [ ] Output `--json` consumible por otros scripts y CI
- [ ] Todos los dominios cubiertos: CODE, TESTS, API, UX
- [ ] Overall status integrado en `COGNITIVE_BRIDGE.json` como `state.health`
- [ ] CI bloquea merge si Overall = RED

---

## Referencias

- SOP_08_AUTOMATED_TESTING.md — Test domain (Gate 2)
- SOP_09_ENVIRONMENT_AWARENESS.md — Pre-requisito del environment
- SOP_10_COGNITIVE_BRIDGE.md — Consume el overall status
- `backend/app/routers/diagnostics.py` — Fuente de datos para Gates 3 y 5
