# MAVIM SOP 06: Continuity & State Persistence

**Objetivo:** Eliminar la amnesia de los agentes. Proveer una "Caja Negra" inmutable que permita a cualquier agente MAVIM o proceso recursivo saber exactamente el estado actual del proyecto al iniciar y finalizar su turno, garantizando un **Ciclo Cerrado de Ejecución**.

## Regla de Oro de Continuidad
**ANTES de finalizar cualquier turno o devolver el control al usuario/orquestador, el agente DEBE actualizar el archivo `PROGRESS_LOG.json` en la raíz del proyecto.**

Si un agente (ej. Claude Code o Codex) es reiniciado, su **primera acción obligatoria** es leer el `PROGRESS_LOG.json` antes de tomar cualquier decisión.

## Estructura de `PROGRESS_LOG.json`

El archivo debe mantener estrictamente este esquema:

```json
{
  "project_status": "IN_PROGRESS | FINISHED | BLOCKED",
  "current_phase": "ARCHITECTURE | SYNTHESIS | EVALUATION",
  "last_step_completed": "Breve descripción de la última mutación de código o diseño.",
  "current_agent_role": "MAVIM-Developer",
  "pending_subtasks": [
    "Crear componente Y",
    "Integrar evento Z"
  ],
  "blockers": "Falta API Key de Stripe",
  "last_updated_timestamp": "ISO_DATE",
  "active_branch": "feature/payments-module"
}
```

## Protocolo de Desbloqueo y Recursión
1. Si el `project_status` es `BLOCKED`, el agente debe leer la propiedad `blockers` y notificar inmediatamente al Orquestador o al Usuario para pedir intervención.
2. Si el estado es `IN_PROGRESS`, el agente lee `pending_subtasks` y escoge la primera tarea disponible para ejecutar.
3. Si el estado es `FINISHED`, el agente finaliza su proceso o notifica al usuario que el proyecto está listo para `Release`.

## Poda de Contexto (Context Pruning / Amnesia Control)
Los agentes de IA sufren de degradación cognitiva cuando la ventana de contexto se alarga demasiado y se saturan de tokens irrelevantes debatiendo soluciones.

- **Regla de Poda:** Cuando el contexto de la conversación o sesión exceda o comience a volverse repetitivo, el agente en curso **DEBE** detener su accionar técnico.
- **Ejecución:** El agente tomará todos los descubrimientos valiosos recientes y actualizará el `PROGRESS_LOG.json` (o un `KNOWLEDGE_LOG.md` temporal). Luego, instruirá explícitamente el cierre de su propia sesión de terminal o chat, para que un ciclo recursivo (ej. el Orquestador o el loop) levante un **nuevo agente fresco** con el contexto podado, leyendo únicamente el registro condensado.
