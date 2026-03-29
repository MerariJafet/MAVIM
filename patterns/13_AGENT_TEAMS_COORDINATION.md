# MAVIM Pattern 13: Agent Teams Coordination

> **Estado:** Experimental — requiere `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
> **Distinto de:** Subagentes (`.claude/agents/`) — ver diferencias abajo.
> **Mínimo:** Claude Code v2.1.32

---

## Qué es Agent Teams vs Subagentes

Son **dos sistemas diferentes** en Claude Code. No confundirlos:

| Dimensión | Subagentes (`.claude/agents/`) | Agent Teams (experimental) |
|-----------|-------------------------------|---------------------------|
| **Independencia** | Contexto propio; reportan al caller | Instancias completamente independientes |
| **Comunicación** | Solo reportan al agente padre | Mensajes directos entre teammates |
| **Coordinación** | El agente padre gestiona todo | Task list compartida, auto-coordinación |
| **Costo** | Menor (contexto delegado) | Mayor (~15x tokens vs chat) |
| **Estado** | GA (estable) | Experimental (feature flag) |
| **Nesting** | Sí, el padre puede lanzar múltiples | No — un teammate no puede crear sub-teams |
| **Persistencia** | Session resumable | No — no hay `/resume` para teammates in-process |

**Regla MAVIM:** Usar **Subagentes** (`.claude/agents/`) como default. Reservar **Agent Teams** para tareas que requieren comunicación real entre agentes independientes.

---

## Activación del Feature Flag

```bash
# Opción 1: Variable de entorno
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Opción 2: settings.json del proyecto
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

# Opción 3: ~/.claude.json (global)
{ "teammateMode": "in-process" }
```

---

## Arquitectura de un Team

```
Team Lead (sesión principal — Opus)
├── Task List compartida (~/.claude/tasks/{team-name}/)
│   ├── task-01: pending → in-progress → completed
│   ├── task-02: blocked_by=[task-01]
│   └── task-03: pending (independiente)
│
├── Teammate A (Sonnet) — implementa módulo auth
│   └── Mailbox: ~/.claude/teams/{team}/inboxes/teammate-a.json
│
├── Teammate B (Sonnet) — implementa módulo billing
│   └── Mailbox: ~/.claude/teams/{team}/inboxes/teammate-b.json
│
└── Teammate C (Sonnet) — ejecuta tests de integración
    └── Mailbox: ~/.claude/teams/{team}/inboxes/teammate-c.json
```

**Storage local:**
- Config del team: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`
- Mailboxes: `~/.claude/teams/{team-name}/inboxes/{agent}.json`

---

## Modos de Display

```bash
# In-process (default) — todos en el mismo terminal
# Shift+Down: cicla entre teammates
# Ctrl+T: toggle task list
# Enter: ver sesión de un teammate
# Escape: interrumpir
claude

# Split-pane — cada teammate en su propio panel (requiere tmux o iTerm2)
claude --teammate-mode tmux
```

**NO funciona split-pane en:** VS Code terminal integrado, Windows Terminal, Ghostty.

---

## Cómo Iniciar un Team (Instrucción Natural)

```
Crea un agent team para implementar el sprint de autenticación.
Lanza tres teammates:
- Teammate A (Sonnet): implementa /src/modules/auth — boundary: solo ese directorio
- Teammate B (Sonnet): implementa /src/modules/session — boundary: solo ese directorio
- Teammate C (Sonnet): escribe tests de integración para auth+session

Dependencias: Teammate C bloqueado hasta que A y B completen.
Requiero plan approval antes de que algún teammate haga writes.
```

Claude propone y crea el team — el usuario confirma antes de ejecutar.

---

## Hooks Específicos de Agent Teams

```json
// .claude/settings.json
{
  "hooks": {
    "TeammateIdle": [{
      "command": "python3 scripts/assign_next_task.py --teammate=${TEAMMATE_NAME}"
    }],
    "TaskCreated": [{
      "command": "python3 scripts/validate_task_scope.py --task=${TASK_ID}",
      "comment": "exit code 2 previene la creación de la tarea"
    }],
    "TaskCompleted": [{
      "command": "npm run test:smoke -- --module=${TASK_MODULE}",
      "comment": "exit code 2 bloquea el marcado como completado"
    }]
  }
}
```

**`TeammateIdle`:** Cuando un teammate termina su tarea y no hay más. Exit code 2 = enviarle feedback y mantenerlo activo.

**`TaskCreated`:** Gate de validación al crear tareas. Exit code 2 = rechaza la tarea.

**`TaskCompleted`:** Quality gate obligatorio. El test de smoke debe pasar antes de marcar completado.

---

## Plan Approval Gate (Para Cirugías)

Para cambios de alto riesgo, exigir aprobación explícita:

```
Spawn an architect teammate to refactor the auth module.
Require plan approval before they make any writes.
```

1. El teammate trabaja read-only hasta que el Lead aprueba.
2. Lead puede rechazar con feedback; teammate revisa y reenvía.
3. Solo cuando el Lead aprueba → el teammate hace writes.

**Embedded en el prompt del Lead:**
> "Only approve plans that include test coverage for every modified function and an IMPACT_MAP section."

---

## Sizing Óptimo del Team (Datos de Producción)

| Parámetro | Valor recomendado |
|-----------|-------------------|
| Tamaño del team | 3–5 teammates |
| Tareas por teammate | 5–6 |
| Overhead de tokens vs chat | ~15x |
| Cuándo justifica el costo | Tareas complejas con múltiple paralelismo real |

---

## Limitaciones Actuales (Experimental)

- **Sin session resumption:** `/resume` y `/rewind` no restauran teammates in-process.
- **Un team por sesión:** El Lead no puede gestionar múltiples teams simultáneamente.
- **Sin nesting:** Un teammate no puede crear su propio team.
- **El rol de Lead es fijo:** No cambia durante la sesión.
- **Task status puede lagear:** Teammates pueden fallar en marcar tareas completadas — monitorear.

---

## Cuándo Usar Qué (Árbol de Decisión MAVIM)

```
¿Los subagentes necesitan comunicarse entre sí directamente?
├── NO → Usar Subagentes (.claude/agents/) [DEFAULT MAVIM]
│         Más eficiente, estable, GA.
│
└── SÍ → ¿La tarea justifica ~15x tokens vs chat?
          ├── NO → Usar Subagentes + PROGRESS_LOG.json como bus de mensajes
          └── SÍ → Activar Agent Teams (experimental)
                    Requiere CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## Los 10 Patrones de Producción (Incorporar en MAVIM)

### P1: Model Tiering Jerárquico
```
Opus (Lead, orquestación) → Sonnet (workers) → Haiku (búsquedas, verificación)
```
Resultado documentado: +90.2% performance vs. flat single-model approach.

### P2: Task Graph con Dependencias
Declarar dependencias explícitas antes de lanzar teammates. Bloquea tareas que no pueden ejecutar hasta que otras completen. Previene trabajo duplicado.

### P3: Plan Approval Gate
Para cambios de alto riesgo: plan → aprobación del Lead → implementación. Embed criterios de aprobación en el prompt del Lead.

### P4: Context Isolation + Handoff Resumido
Los subagentes manejan operaciones verbosas (test suites, análisis de logs). Solo el resumen final vuelve al padre. Los subagentes **no heredan el historial de conversación del padre** — reciben solo lo que se pasa explícitamente.

### P5: Memoria Persistente por Dominio
`memory: project` en el frontmatter → agentes acumulan conocimiento del codebase entre sesiones. Primeros 200 líneas / 25KB de MEMORY.md se auto-inyectan al inicio.

### P6: Tool Restriction + Hook Validation
`tools:` allowlist + hooks `PreToolUse` para control fino. Defense-in-depth más allá de las restricciones de herramientas.

### P7: Worktree Isolation para Paralelo
`isolation: worktree` → cada agente trabaja en copia temporal del repo. Zero conflictos de archivo. Auto-limpiado si no hay cambios.

### P8: Hook-Enforced Quality Gates
`TaskCompleted` hook = gate de calidad (linter, test coverage). Exit code 2 bloquea la finalización y envía feedback al agente.

### P9: Evaluator-Optimizer Loop
Agente A genera → Agente B evalúa contra rúbrica explícita → feedback a A → itera. Efectivo cuando los criterios de evaluación son medibles y la condición de termino está bien definida.

### P10: Swarm Self-Organization
Pool de tareas grande, N workers idénticos, auto-reclaman la siguiente tarea disponible. El Lead monitorea stalls. Ideal para: review de 50+ archivos, migrar 30+ endpoints.

---

## Checklist de Cumplimiento

- [ ] Feature flag activo si se usa Agent Teams: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- [ ] Distingo correcto: Subagentes para delegation; Agent Teams para colaboración independiente
- [ ] Team size: 3–5 teammates máximo
- [ ] Dependencias declaradas en task list antes de lanzar teammates
- [ ] Hooks `TaskCompleted` con quality gate
- [ ] Plan approval gate para cirugías (SOP_07)
- [ ] `isolation: worktree` en developers paralelos
- [ ] `effort: high` en todos los agentes Opus 4.6
- [ ] MEMORY.md activo en agentes con `memory: project`

---

## Referencias

- `core/SOP_03_SYNTHESIS.md` — Protocolo multi-agente MAVIM
- `core/SOP_16_CLAUDE_MODEL_ROUTING.md` — Routing de modelos por rol
- `.claude/agents/` — Definiciones de subagentes MAVIM
- `prompts/AGENT_TEAMS_MASTER_PROMPT.md` — Prompts listos para usar
