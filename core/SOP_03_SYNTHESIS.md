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

---

## Parte C: Sistema Oficial de Subagentes Claude Code (.claude/agents/)

Esta sección documenta el mecanismo oficial de Claude Code para definir y activar subagentes persistentes. Los archivos en `.claude/agents/` son la implementación formal del protocolo de la Parte B.

### 1. Estructura de un Subagente MAVIM

Los subagentes se definen como archivos Markdown con frontmatter YAML en `.claude/agents/[nombre].md`:

```yaml
---
name: mavim-developer          # identificador único (sin espacios)
description: |                  # CRÍTICO: Claude Code lee esto para decidir cuándo activar
  Cuándo usar este agente. Sé específico — esta descripción es el selector.
model: claude-sonnet-4-6        # modelo asignado por SOP_16
tools:                          # subset de herramientas permitidas
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
permissionMode: acceptEdits     # default | acceptEdits | dontAsk | bypassPermissions
maxTurns: 60                    # límite de turnos (evita loops infinitos)
memory:                         # scopes de memoria persistente
  - project                     # ~/.claude/agent-memory/[project]/
  - user                        # ~/.claude/agent-memory/user/
isolation: worktree             # git worktree aislado (opcional, para cirugías)
---

# Prompt del sistema del agente aquí
```

### 2. Agentes MAVIM Disponibles

| Archivo | Modelo | permissionMode | Uso |
|---------|--------|----------------|-----|
| `mavim-orchestrator.md` | Opus 4.6 | default | Director de equipo |
| `mavim-planner.md` | Opus 4.6 | default | Planificación estratégica |
| `mavim-architect.md` | Opus 4.6 | default | Diseño de módulos |
| `mavim-developer.md` | Sonnet 4.6 | acceptEdits | Implementación |
| `mavim-critic.md` | Sonnet 4.6 | default | Auditoría y review |
| `mavim-scraper.md` | Haiku 4.5 | default | Web intelligence |

### 3. Modos de Activación

**a) @-mención en el prompt:**
```
@mavim-orchestrator Inicia el sprint para el módulo de autenticación.
```

**b) Delegación desde el Orchestrator (Agent tool):**
```python
# El Orchestrator lanza subagentes con el Agent tool de Claude Code
# Cada subagente tiene su propio contexto aislado
Agent(
  subagent_type="mavim-developer",  # nombre del archivo en .claude/agents/
  prompt="Implementa /src/modules/auth según TASK_AUTH.md",
  run_in_background=False  # True para tareas paralelas no bloqueantes
)
```

**c) CLI con --agents flag (agentes de sesión):**
```bash
claude --agents '[{"name":"dev-a","model":"claude-sonnet-4-6","systemPrompt":"Implementa auth..."},{"name":"dev-b","model":"claude-sonnet-4-6","systemPrompt":"Implementa billing..."}]'
```

### 4. Aislamiento con Git Worktrees

Cuando `isolation: worktree` está activo, Claude Code crea automáticamente una copia del repo en un directorio temporal. Esto garantiza:
- **Zero conflictos de merge** durante el desarrollo paralelo.
- Si el agente no hace cambios → worktree se elimina automáticamente.
- Si hace cambios → worktree path + branch son retornados al Orchestrator.

**Cuándo activar `isolation: worktree`:**
- Developers en paralelo sobre el mismo repo.
- Cualquier cirugía de refactoring (SOP_07).
- **No activar** para agentes read-only (Critic, Scraper).

### 5. Memoria Persistente de Subagentes

Los agentes con `memory: [project]` pueden leer/escribir en:
- `~/.claude/agent-memory/[project-hash]/` — compartida entre agentes del mismo proyecto
- `~/.claude/agent-memory/user/` — compartida entre todos los proyectos del usuario

**Uso en MAVIM:** El `PROGRESS_LOG.json` en el repo es el mecanismo primario de coordinación. La memoria de Claude Code (`memory:`) es secundaria para contexto de usuario/proyecto persistente entre sesiones.

### 6. Hooks de Coordinación

Para automatizar eventos del ciclo de vida del agente, configura en `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStart": [{
      "command": "echo 'Agent started' >> .claude/agent_activity.log"
    }],
    "SubagentStop": [{
      "command": "python3 scripts/update_progress_log.py --event=stop"
    }],
    "PreToolUse": [{
      "matcher": "Write",
      "command": "python3 scripts/check_boundary.py --file=${TOOL_INPUT_PATH}"
    }]
  }
}
```

**Hook PreToolUse para boundary enforcement:** El script `check_boundary.py` verifica que el Developer no está editando archivos fuera de su módulo asignado antes de permitir el Write.

### 7. Checklist de Cumplimiento (Parte C)

- [ ] Cada agente MAVIM tiene su archivo en `.claude/agents/[nombre].md`
- [ ] La `description` es específica y accionable (Claude la usa como selector)
- [ ] Modelo asignado según SOP_16 (Opus/Sonnet/Haiku por rol)
- [ ] `permissionMode` mínimo necesario (principio de mínimo privilegio)
- [ ] `maxTurns` definido (nunca omitir — evita loops infinitos)
- [ ] `isolation: worktree` activo para Developers en paralelo
- [ ] Hooks configurados para boundary enforcement en Developers
- [ ] `PROGRESS_LOG.json` como fuente primaria de coordinación entre agentes
