# MAVIM SOP 03: Parallel Synthesis Phase

**Objetivo:** Definir cómo múltiples agentes Claude trabajan de forma concurrente sin crear conflictos en el código base. Este SOP cubre tanto el modelo de ramas Git como el protocolo real de colaboración entre subagentes Claude.

---

## Parte A: Modelo de Ramas Git (Branching Model)

### 1. Aislamiento por Rama
- Ningún agente desarrolla directamente en la rama principal (`main`/`master`).
- Cada agente o tarea específica trabaja en una rama completamente aislada (ej. `feature/modulo-xyz`, `fix/login-bug`, `refactor/auth-upgrade`).

### 2. Roles y Revisión (Pull Requests)
- Se asignará un agente con el rol de **Lead Developer Agent** o Reviewer.
- Este agente revisará los Pull Requests generados por los **Feature Agents**. Solo se fusiona un PR si pasa las validaciones del Gatekeeper (MAVIM-Critic).

### 3. Contexto y Meta-Prompting
- Usar **Meta-prompting** en cada sesión del agente para asegurar que recuerde el contexto global y las **fronteras del módulo** (Boundaries) en el que trabaja. No debe alterar código fuera de su dominio asignado.

---

## Parte B: Protocolo Claude Multi-Agente (Teams Agent Pattern)

Este es el protocolo operativo para cuando Claude Code (Orchestrator) lanza subagentes Claude en paralelo.

### 1. Cuándo Usar Subagentes Paralelos

Lanzar agentes en paralelo cuando:
- Hay **2 o más módulos independientes** que no comparten código ni datos en esa iteración.
- Una tarea requiere **investigación externa** (Web Intelligence via SOP_09) mientras otra tarea requiere **código**.
- El MAVIM-Architect ha completado el `MAPA_LEGO.md` y los módulos están bien delimitados.

**No** lanzar agentes en paralelo cuando:
- Los módulos tienen dependencias directas entre sí en el sprint actual.
- Hay un `BLOCKED` en `PROGRESS_LOG.json` sin resolver.

### 2. Protocolo de Lanzamiento de Subagentes (Claude Code)

El Orchestrator sigue este patrón para lanzar agentes paralelos:

```
# Patrón de instrucción para subagente Developer A:
"Eres MAVIM-Developer usando claude-sonnet-4-6.
Lee PROGRESS_LOG.json y SPRINT_PLAN.md.
Tu tarea exclusiva: implementar /src/modules/auth según TASK_AUTH_MODULE.md.
NO toques archivos fuera de /src/modules/auth/.
Al terminar: actualiza PROGRESS_LOG.json marcando tu subtarea como completada."

# Patrón de instrucción para subagente Developer B (simultáneo):
"Eres MAVIM-Developer usando claude-sonnet-4-6.
Lee PROGRESS_LOG.json y SPRINT_PLAN.md.
Tu tarea exclusiva: implementar /src/modules/billing según TASK_BILLING_MODULE.md.
NO toques archivos fuera de /src/modules/billing/.
Al terminar: actualiza PROGRESS_LOG.json marcando tu subtarea como completada."
```

### 3. Protocolo de Comunicación Inter-Agente

Los agentes **no se comunican directamente**. La comunicación es asíncrona mediante artefactos de Git:

```
Orchestrator (Opus)
    ├── Escribe: PROGRESS_LOG.json (estado global)
    ├── Escribe: /tasks/TASK_*.md (tickets por agente)
    │
    ├── Developer A (Sonnet) — lee su TASK, escribe en su rama
    │       └── Al terminar: actualiza PROGRESS_LOG.json
    │
    ├── Developer B (Sonnet) — lee su TASK, escribe en su rama
    │       └── Al terminar: actualiza PROGRESS_LOG.json
    │
    └── Critic (Sonnet) — lee PRs de A y B, emite veredicto
            └── Al terminar: actualiza PROGRESS_LOG.json → rol: Orchestrator
```

### 4. Prevención de Conflictos (Anti-Collision Rules)

1. **Boundaries estrictos:** Cada agente opera exclusivamente en su módulo. Si necesita datos de otro módulo, los lee vía la Interface Pública (API interna), nunca edita el código del otro módulo.
2. **Un archivo a la vez:** Si dos agentes necesitan editar el mismo archivo de configuración compartida (ej. `docker-compose.yml`), uno espera — el Orchestrator serializa esa tarea.
3. **PROGRESS_LOG como mutex:** Antes de escribir al log, el agente verifica que no haya otro agente activo en su misma zona (`current_agent_role` + `active_branch`).

### 5. Modelo de Paralelismo Óptimo por Sprint

```
Sprint tipo "Feature completa" (3 módulos):

Fase 1 (Secuencial):
  Orchestrator → Planner → Architect (MAPA_LEGO + tickets)

Fase 2 (Paralelo):
  Developer A (módulo Auth)     ] simultáneos
  Developer B (módulo Billing)  ]

Fase 3 (Secuencial):
  Critic (audita PRs de A y B juntos)

Fase 4 (Paralelo si hay correcciones):
  Developer A corrige auth     ] simultáneos si los
  Developer B corrige billing  ] errores son independientes
```

### 6. Protocolo de Escalamiento al Orchestrator

Si un subagente detecta cualquiera de estas condiciones, **debe detenerse** y escalar al Orchestrator (no intentar resolver por su cuenta):
- Un error de diseño que requiere cambiar el `MAPA_LEGO.md`.
- Un conflicto con el `ARCHITECTURE_CONTRACT.md`.
- Un bloqueo externo (API key faltante, servicio caído).
- Más de 3 iteraciones fallidas en la misma tarea.
