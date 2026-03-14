# MAVIM Handover Protocol (Paso de Estafeta)

**Objetivo:** Garantizar que cuando el control del repositorio pase de un agente a otro (ej. de Architect a Developer, o de Developer a Critic), no haya duplicidad de trabajo, pérdida de contexto o colisiones en el código.

## Mecanismo de Traspaso (The Git Tickets)

El paso de estafeta entre agentes en MAVIM NO se hace mediante memoria efímera de chat. Se hace estrictamente a través de artefactos asíncronos alojados en control de versiones.

### 1. Del Architect al Developer (Handoff)
- El **Architect** diseña los modelos y actualiza `MAPA_LEGO.md` y `DATA_SCHEMA.md`.
- El Architect crea un "Ticket" físico mediante un archivo en una carpeta de tareas (ej. `/tasks/TASK_AUTH_MODULE.md`) que contiene:
  - Referencia al módulo en el esquema.
  - Los endpoints a crear.
  - Comandos para instanciar el servidor.
- El Architect actualiza el estado en `PROGRESS_LOG.json` indicando que el rol activo ahora es `MAVIM-Developer`.
- El Architect termina su tarea.

### 2. Del Developer al Critic (The Audit Request)
- El **Developer** implementa el código en una rama nueva (ej. `feat/auth-module`).
- Cuando termina la sub-tarea definida en su ticket, el Developer **DEBE** generar un "Pull Request Local/Remoto" o generar un archivo `.diff`.
- El Developer actualiza `PROGRESS_LOG.json` marcando el rol activo a `MAVIM-Critic` y definiendo el estado como `REVIEW_PENDING`.
- El Developer termina su tarea.

### 3. Del Critic de regreso al Developer o Fin (The Verdict)
- El **Critic** se despierta, lee el `PROGRESS_LOG.json` que lo invoca.
- Ejecuta los checklist contra el código en el PR/diff.
- Devuelve el control:
  - Si hay errores: Cambia el rol de vuelta a `MAVIM-Developer`, inyecta en `blockers` la lista de correcciones, y termina su turno.
  - Si es perfecto: Autoriza la fusión (merge), marca la subtarea como completada en `PROGRESS_LOG.json` y devuelve el rol al `Orchestrator` o toma el siguiente ticket.
