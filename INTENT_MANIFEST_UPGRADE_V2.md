# INTENT MANIFEST — MAVIM Upgrade v2.0

> Generado siguiendo SOP_01 (Intention Phase). Requerido antes de cualquier modificación.

## El Problema

MAVIM v1.x es una metodología sólida para agentes de IA, pero carece de:
1. **Guía de modelo Claude por rol** — No especifica qué modelo (Opus, Sonnet, Haiku) usar para cada tarea, causando uso ineficiente de recursos y calidad subóptima.
2. **Protocolo real de colaboración multi-agente** — SOP_03 describe branching de Git, pero no cómo los agentes Claude se comunican, se delegan trabajo y operan en paralelo usando la herramienta `Agent`.
3. **Módulo de Web Intelligence** — No existe soporte para que los agentes scrapen páginas web, extraigan información, estructura y diseño de sitios como parte del flujo de trabajo.

## Los Actores

| Actor | Descripción |
| :--- | :--- |
| **Claude Code (local)** | Agente principal que ejecuta la metodología en el entorno del usuario |
| **Sub-agentes Claude** | Instancias especializadas lanzadas por el Orchestrator para tareas paralelas |
| **Usuario/Desarrollador** | Persona que define la intención y valida los entregables finales |
| **GitHub/Git** | Sistema de control de versiones que actúa como medio de comunicación asíncrona entre agentes |

## Casos de Éxito (Definition of Done)

1. **[Modelo por Rol]** Cada archivo de rol (`ARCHITECT.md`, `DEVELOPER.md`, etc.) especifica explícitamente el modelo Claude recomendado (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`) y la justificación.
2. **[SOP_08 creado]** Existe un `SOP_08_CLAUDE_MODEL_ROUTING.md` con reglas de selección de modelo, patrones de cost-optimization y tabla de routing completa.
3. **[SOP_09 creado]** Existe un `SOP_09_WEB_INTELLIGENCE.md` con: herramientas recomendadas (open source y MCP), protocolo de extracción de contenido y diseño, y integración con el flujo MAVIM.
4. **[Multi-agente mejorado]** `SOP_03_SYNTHESIS.md` actualizado con patrones reales de `claude --agent`, subagents, paralelismo y comunicación inter-agente.
5. **[Nuevo rol PLANNER]** `roles/PLANNER.md` creado usando Claude Opus como agente de diseño estratégico pre-arquitectura.
6. **[README actualizado]** El índice refleja todos los cambios.
7. **[Commit + Push]** Todos los cambios en el repositorio remoto.
