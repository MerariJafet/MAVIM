# SOP_10 — COGNITIVE BRIDGE (Transición de Contexto entre IAs)

**Versión:** 1.0.0
**Fecha:** 2026-03-14
**Autor:** MAVIM-ORCHESTRATOR
**Estado:** ACTIVO — Obligatorio al finalizar sesión y al iniciar sesión nueva

---

## 1. Propósito

La mayor pérdida de productividad en proyectos asistidos por IA ocurre en los **bordes de sesión**: cuando el contexto de conversación se corta (límite de tokens, cambio de proveedor, reinicio de sesión) y el agente entrante debe reconstruir desde cero todo el estado que el agente saliente conocía.

Este SOP define el protocolo **COGNITIVE BRIDGE**: un formato estándar de transferencia de contexto que permite a cualquier IA (Claude, GPT-4, Gemini, agente local) continuar el trabajo exactamente donde el agente anterior lo dejó, con el mismo nivel de comprensión del sistema.

---

## 2. Principio Rector

> **"El conocimiento de un agente no debe morir con su sesión. El Cognitive Bridge es la memoria persistente entre instancias de IA."**

Sin este protocolo, cada nueva sesión repite los mismos errores, redescubre los mismos patrones, y pierde el momentum acumulado. Con él, la mejora del sistema es continua e independiente del modelo que la ejecuta.

---

## 3. Anatomía del Cognitive Bridge

El Bridge es un archivo JSON estructurado en 5 capas:

```
COGNITIVE_BRIDGE.json
├── 1. identity       — Quién soy, qué proyecto, qué versión
├── 2. state          — Qué está terminado, qué está en progreso
├── 3. decisions      — Por qué se tomaron las decisiones clave
├── 4. dangers        — Qué NO hacer (errores conocidos, trampas)
├── 5. handoff        — Próximos pasos exactos para el agente entrante
```

---

## 4. Formato Completo: `COGNITIVE_BRIDGE.json`

```json
{
  "bridge_version": "1.0.0",
  "bridge_id": "uuid-v4",
  "created_at": "ISO-8601",
  "project": {
    "name": "itsme",
    "repo": "https://github.com/MerariJafet/itsme",
    "branch": "master",
    "last_commit": "5916631",
    "tech_stack": ["React 18", "FastAPI", "PostgreSQL", "Shadcn/UI", "Playwright"]
  },
  "outgoing_agent": {
    "model": "claude-sonnet-4-6",
    "session_started": "ISO-8601",
    "session_ended": "ISO-8601",
    "tasks_completed": [
      "Migración visual completa a Shadcn (18 páginas)",
      "Playwright 18 gates — 18/18 passing",
      "SOP_08 + SOP_09 + SOP_10 creados",
      "Sistema de autodiagnóstico implementado"
    ]
  },
  "state": {
    "phase": "MAVIM 2.0 — Post-cirugía visual",
    "health": "GREEN",
    "last_test_run": {
      "tool": "playwright",
      "result": "18/18 passed",
      "run_id": "uuid-del-run",
      "timestamp": "ISO-8601"
    },
    "pending_tasks": [
      {
        "id": "T001",
        "priority": "HIGH",
        "description": "Migrar páginas pendientes: Calendar, Agent, Integrations",
        "context": "Identificadas en scan anterior — tienen bg-white hardcodeado"
      }
    ],
    "in_progress": []
  },
  "architecture_decisions": [
    {
      "id": "ADR-001",
      "decision": "CSS Variables sobre Tailwind hardcoded",
      "reason": "Dark mode funcional sin clases dark:* duplicadas",
      "alternatives_rejected": ["tailwind dark: prefix", "styled-components"],
      "date": "2026-03-14"
    },
    {
      "id": "ADR-002",
      "decision": "Playwright sobre jest-dom para E2E",
      "reason": "Chromium real detecta errores de CSS que jsdom no ve (caso Badge bg-slate-100)",
      "date": "2026-03-14"
    },
    {
      "id": "ADR-003",
      "decision": "No inyectar X-MAVIM-Test header globalmente en Playwright",
      "reason": "Rompe CORS preflight en Google Fonts CDN, causando fallos en gates 01/04/06",
      "alternatives_rejected": ["extraHTTPHeaders global"],
      "date": "2026-03-14"
    }
  ],
  "known_dangers": [
    {
      "id": "D001",
      "category": "CSS",
      "description": "bg-white y bg-slate-* en componentes de formulario rompen dark mode",
      "detection": "Gate 10 Playwright",
      "files_to_check": ["badge.tsx", "AppointmentFormDialog.tsx", "PatientFormDialog.tsx"]
    },
    {
      "id": "D002",
      "category": "Auth",
      "description": "El credential helper de git apuntaba a una ruta inválida (/VMarx Dione DB/gh)",
      "fix": "gh auth setup-git reconfigura el helper al gh correcto",
      "date_fixed": "2026-03-14"
    },
    {
      "id": "D003",
      "category": "CI",
      "description": "gh repo create requiere scope 'workflow' para subir .github/workflows/",
      "fix": "gh auth refresh -h github.com -s workflow"
    }
  ],
  "environment_snapshot": {
    "ref": "Ver ENVIRONMENT_SNAPSHOT.json (SOP_09)",
    "node": "20.x",
    "python": "3.12.x",
    "key_ports": {
      "5173": "Vite dev server",
      "8000": "FastAPI backend",
      "5432": "PostgreSQL"
    }
  },
  "handoff_instructions": {
    "activation_prompt": "Activa SOP_09 (scan), lee este Bridge, luego ejecuta npm run test:smoke para verificar estado base.",
    "first_actions": [
      "1. bash scripts/mavim_scan.sh — verificar entorno",
      "2. npm run test:smoke — confirmar 18/18 gates verdes",
      "3. Leer pending_tasks y continuar desde T001"
    ],
    "files_to_read_first": [
      "COGNITIVE_BRIDGE.json",
      "frontend/src/index.css (design tokens)",
      "frontend/e2e/smoke.spec.ts (gates actuales)"
    ],
    "do_not_touch": [
      "frontend/src/components/ui/ — migrado y testeado",
      ".github/workflows/ci.yml — gate final de CI"
    ]
  }
}
```

---

## 5. Protocolo de Escritura (Agente Saliente)

Al detectar cualquiera de estos eventos, el agente DEBE escribir el Bridge:

| Evento | Trigger |
|--------|---------|
| Límite de tokens próximo (> 80% contexto) | Escribir Bridge inmediatamente |
| Usuario dice "continuamos mañana" | Escribir Bridge antes de responder OK |
| Cambio de modelo/proveedor solicitado | Escribir Bridge + confirmar al usuario |
| Tarea completada (milestone) | Actualizar `state.tasks_completed` |
| Error crítico encontrado | Agregar a `known_dangers` |

### Script de escritura automática

```python
# scripts/write_bridge.py
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

def write_cognitive_bridge(project_root: str, **kwargs):
    bridge = {
        "bridge_version": "1.0.0",
        "bridge_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project": kwargs.get("project", {}),
        "state": kwargs.get("state", {}),
        "architecture_decisions": kwargs.get("decisions", []),
        "known_dangers": kwargs.get("dangers", []),
        "handoff_instructions": kwargs.get("handoff", {})
    }

    output_path = Path(project_root) / "COGNITIVE_BRIDGE.json"
    output_path.write_text(json.dumps(bridge, indent=2, ensure_ascii=False))
    print(f"✅ Cognitive Bridge written: {output_path}")
    return bridge

if __name__ == "__main__":
    write_cognitive_bridge(".")
```

---

## 6. Protocolo de Lectura (Agente Entrante)

Al iniciar sesión con un proyecto MAVIM, el agente DEBE:

```
PASO 1: ¿Existe COGNITIVE_BRIDGE.json?
  └─ SÍ: Leer completamente antes de cualquier acción
  └─ NO: Ejecutar SOP_09 para construir contexto desde cero

PASO 2: Verificar bridge_version
  └─ Compatible: Continuar desde handoff_instructions
  └─ Obsoleto: Ejecutar SOP_09 + actualizar Bridge

PASO 3: Ejecutar first_actions en orden
  └─ mavim_scan.sh (SOP_09)
  └─ test:smoke (SOP_08)
  └─ Confirmar estado antes de operar

PASO 4: Anunciar al usuario el estado del sistema
  "He leído el Cognitive Bridge. Sistema en estado [GREEN/YELLOW/RED].
   Últimas tareas: [X]. Próximo paso: [Y]."
```

---

## 7. Niveles de Salud del Sistema

| Estado | Condición | Acción del agente entrante |
|--------|-----------|---------------------------|
| 🟢 GREEN | Playwright 18/18, sin cambios sin commit | Continuar desde pending_tasks |
| 🟡 YELLOW | Playwright < 18/18 O cambios sin commit | Resolver antes de nueva tarea |
| 🔴 RED | Backend caído O errores de build | Diagnóstico prioritario (SOP_09) |

---

## 8. Diferencia con PROGRESS_LOG.json

| Archivo | Propósito | Audiencia | Frecuencia |
|---------|-----------|-----------|-----------|
| `PROGRESS_LOG.json` | Tracking de sprints y features | Humano + IA | Por sprint |
| `COGNITIVE_BRIDGE.json` | Transferencia de contexto entre sesiones IA | Solo IA | Por sesión |
| `ENVIRONMENT_SNAPSHOT.json` | Estado del sistema en un momento | IA | Al inicio |

---

## 9. Compatibilidad Multi-Modelo

El formato está diseñado para ser legible por cualquier LLM moderno:

```
Claude Sonnet/Opus → Lee JSON nativo, entiende toda la estructura
GPT-4o / o3       → Compatible, misma estructura JSON
Gemini Pro        → Compatible
Agente local      → Puede parsear con cualquier JSON parser
```

El campo `outgoing_agent.model` identifica qué IA generó el Bridge, permitiendo detectar si hubo cambio de modelo y ajustar expectativas de continuidad.

---

## 10. Checklist de Cumplimiento

- [ ] `COGNITIVE_BRIDGE.json` existe en la raíz del proyecto
- [ ] `bridge_id` es un UUID único (no copiado de sesión anterior)
- [ ] `state.pending_tasks` refleja el estado real actual
- [ ] `known_dangers` incluye todos los errores encontrados en la sesión
- [ ] `handoff_instructions.first_actions` son ejecutables sin contexto adicional
- [ ] Agente entrante confirma lectura del Bridge antes de operar
- [ ] Bridge actualizado después de cada milestone completado

---

## Referencias

- SOP_09_ENVIRONMENT_AWARENESS.md — Genera `ENVIRONMENT_SNAPSHOT.json`
- SOP_08_AUTOMATED_TESTING.md — Genera `mavim-trace.json` (incluir en Bridge)
- SOP_07_REFACTORING.md — Cirugías deben registrarse en `architecture_decisions`
- `scripts/write_bridge.py` — Generador automático del Bridge
