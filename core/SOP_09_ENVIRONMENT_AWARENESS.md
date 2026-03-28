# SOP_09 — ENVIRONMENT AWARENESS (Escaneo Inicial del Sistema)

**Versión:** 1.0.0
**Fecha:** 2026-03-14
**Autor:** MAVIM-ORCHESTRATOR
**Estado:** ACTIVO — Obligatorio en cada sesión nueva

---

## 1. Propósito

Antes de escribir una sola línea de código, el agente DEBE conocer el entorno exacto en el que opera. Un diagnóstico erróneo del entorno provoca:
- Comandos que fallan silenciosamente
- Conflictos de versión no detectados
- Dependencias asumidas que no existen
- Decisiones arquitectónicas basadas en suposiciones falsas

Este SOP define el **protocolo de activación** que convierte al agente de estado "ciego" a estado "consciente del entorno" en los primeros 60 segundos de sesión.

---

## 2. Principio Rector

> **"Un agente que no conoce su entorno opera con alucinaciones de infraestructura."**

El escaneo no es opcional. Es el primer entregable obligatorio de cualquier sesión, antes que cualquier tarea técnica.

---

## 3. Protocolo de Activación (orden estricto)

### Fase 1 — Identidad del Sistema (< 5 segundos)

```bash
# Ejecutar en secuencia al inicio de sesión
uname -a                          # OS + kernel
whoami && id                      # Usuario y permisos
pwd                               # Directorio de trabajo
echo $SHELL && $SHELL --version   # Shell activo
```

**Output esperado:** `ENVIRONMENT_SNAPSHOT.json` sección `system`.

### Fase 2 — Stack Tecnológico (< 15 segundos)

```bash
# Lenguajes y runtimes
node --version 2>/dev/null || echo "node: NOT FOUND"
python3 --version 2>/dev/null || echo "python3: NOT FOUND"
go version 2>/dev/null || echo "go: NOT FOUND"
rustc --version 2>/dev/null || echo "rust: NOT FOUND"
java -version 2>/dev/null || echo "java: NOT FOUND"

# Package managers
npm --version 2>/dev/null || echo "npm: NOT FOUND"
pip3 --version 2>/dev/null || echo "pip3: NOT FOUND"
docker --version 2>/dev/null || echo "docker: NOT FOUND"
docker compose version 2>/dev/null || echo "compose: NOT FOUND"

# Git
git --version && git config user.name && git config user.email
```

### Fase 3 — Estado del Proyecto (< 20 segundos)

```bash
# Git status del repositorio activo
git status --short
git log --oneline -5
git branch -a

# Dependencias instaladas vs requeridas
[ -f package.json ] && node -e "
  const p = require('./package.json');
  const deps = Object.keys({...p.dependencies, ...p.devDependencies});
  console.log('JS deps:', deps.length);
"
[ -f requirements.txt ] && pip3 list --format=freeze | wc -l
```

### Fase 4 — Recursos del Sistema (< 10 segundos)

```bash
# Puertos en uso (detecta conflictos)
ss -tlnp 2>/dev/null | grep -E ':(3000|5173|8000|8080|5432|6379)' || \
  netstat -tlnp 2>/dev/null | grep -E ':(3000|5173|8000|8080|5432|6379)'

# Disco y memoria
df -h . | tail -1
free -h 2>/dev/null || vm_stat 2>/dev/null | head -5

# Procesos relevantes corriendo
pgrep -la "node|python|uvicorn|vite|postgres|redis" 2>/dev/null || true
```

### Fase 5 — Variables de Entorno Críticas (< 5 segundos)

```bash
# Verificar presencia (NO el valor — nunca filtrar secrets)
for var in DATABASE_URL SECRET_KEY OPENAI_API_KEY STRIPE_SECRET_KEY \
           VITE_API_URL REDIS_URL SUPABASE_URL; do
  [ -n "${!var}" ] && echo "$var: SET" || echo "$var: MISSING"
done
```

---

## 4. Formato de Salida: `ENVIRONMENT_SNAPSHOT.json`

```json
{
  "snapshot_id": "uuid-v4",
  "captured_at": "ISO-8601",
  "session_context": "descripción breve de qué se va a hacer",
  "system": {
    "os": "Linux 6.17.0-14-generic x86_64",
    "shell": "bash 5.2.21",
    "user": "merari-acero",
    "working_dir": "/home/merari-acero/itsme"
  },
  "stack": {
    "node": "20.11.0",
    "python": "3.12.3",
    "npm": "10.2.4",
    "docker": "27.0.3",
    "git": "2.43.0"
  },
  "project": {
    "branch": "master",
    "last_commit": "5916631",
    "uncommitted_files": 0,
    "js_deps_installed": true,
    "python_deps_installed": true
  },
  "ports": {
    "5173": "free",
    "8000": "in_use_by: uvicorn",
    "5432": "in_use_by: postgres"
  },
  "env_vars": {
    "DATABASE_URL": "SET",
    "SECRET_KEY": "SET",
    "VITE_API_URL": "SET",
    "OPENAI_API_KEY": "MISSING"
  },
  "warnings": [
    "OPENAI_API_KEY not set — AI features will be disabled",
    "Port 8000 already in use — backend may already be running"
  ],
  "ready": true
}
```

---

## 5. Matriz de Decisión Post-Escaneo

| Condición detectada | Acción del agente |
|--------------------|--------------------|
| `node: NOT FOUND` | Instalar Node antes de cualquier tarea frontend |
| Puerto 5173 en uso | Verificar si es el servidor propio o conflicto |
| `git status` con 50+ archivos modificados | Crear commit de seguridad antes de cualquier cirugía |
| `DATABASE_URL: MISSING` | Alertar al usuario — operaciones de DB fallarán |
| Disco < 1GB libre | Warning — builds de Docker pueden fallar |
| Deps JS no instaladas | Ejecutar `npm install` antes de `npm run dev` |
| Python venv no activo | Activar venv o instalar deps en entorno global |

---

## 6. Script de Activación Automatizado

Guardar en el proyecto como `scripts/mavim_scan.sh`:

```bash
#!/usr/bin/env bash
# MAVIM SOP_09 — Environment Awareness Scanner
# Uso: bash scripts/mavim_scan.sh > environment_snapshot.json

set -euo pipefail

SNAP_ID=$(python3 -c "import uuid; print(uuid.uuid4())" 2>/dev/null || uuidgen)
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{"
echo "  \"snapshot_id\": \"$SNAP_ID\","
echo "  \"captured_at\": \"$NOW\","

# System
OS=$(uname -a)
SHELL_VER=$($SHELL --version 2>&1 | head -1)
echo "  \"system\": {"
echo "    \"os\": \"$OS\","
echo "    \"shell\": \"$SHELL_VER\","
echo "    \"user\": \"$(whoami)\","
echo "    \"working_dir\": \"$(pwd)\""
echo "  },"

# Stack
NODE=$(node --version 2>/dev/null || echo "NOT FOUND")
PYTHON=$(python3 --version 2>/dev/null || echo "NOT FOUND")
DOCKER=$(docker --version 2>/dev/null | cut -d' ' -f3 | tr -d ',' || echo "NOT FOUND")
echo "  \"stack\": {"
echo "    \"node\": \"$NODE\","
echo "    \"python\": \"$PYTHON\","
echo "    \"docker\": \"$DOCKER\""
echo "  },"

# Ports
echo "  \"ports_in_use\": ["
ss -tlnp 2>/dev/null | grep -oP ':\K[0-9]+(?=\s)' | sort -u | \
  grep -E '^(3000|5173|8000|8080|5432|6379)$' | \
  sed 's/.*/"&"/' | paste -sd ',' || echo ""
echo "  ],"

# Warnings
echo "  \"ready\": true"
echo "}"
```

---

## 7. Integración con otros SOPs

```
SOP_09 (Environment Scan)
    ↓ snapshot listo
SOP_07 (Refactoring) — lee puertos, git status
SOP_08 (E2E Testing) — verifica que Node y Playwright existen
SOP_10 (Cognitive Bridge) — incluye snapshot en el handoff
```

---

## 8. Checklist de Cumplimiento

- [ ] `ENVIRONMENT_SNAPSHOT.json` generado en los primeros 60s de sesión
- [ ] Stack tecnológico verificado (versiones documentadas)
- [ ] Git status limpio o con commit de seguridad antes de operar
- [ ] Puertos críticos mapeados (sin conflictos ocultos)
- [ ] Variables de entorno verificadas (presencia, no valor)
- [ ] Warnings activos comunicados al usuario antes de proceder
- [ ] `ready: true` confirmado antes de iniciar cualquier cirugía

---

## Referencias

- SOP_07_REFACTORING.md — Prerequisito para cirugías
- SOP_10_COGNITIVE_BRIDGE.md — Usa el snapshot en el handoff entre IAs
- `scripts/mavim_scan.sh` — Implementación ejecutable de este SOP
