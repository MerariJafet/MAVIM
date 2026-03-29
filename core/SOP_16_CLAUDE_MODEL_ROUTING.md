# MAVIM SOP 08: Claude Model Routing (Selección de Modelo por Rol)

**Objetivo:** Garantizar que cada agente MAVIM opere con el modelo Claude óptimo para su tarea específica. El modelo correcto maximiza calidad, velocidad y eficiencia de costos en un sistema multi-agente local.

---

## La Regla de Oro del Routing

> **Principio:** Usa el modelo más potente solo cuando el razonamiento profundo lo requiera. Para tareas mecánicas o de alta velocidad, usa modelos más rápidos y eficientes.

---

## Tabla de Routing por Rol MAVIM

| Rol MAVIM | Modelo Recomendado | Model ID | Justificación |
| :--- | :--- | :--- | :--- |
| **MAVIM-Orchestrator** | Claude Opus 4.6 | `claude-opus-4-6` | Decisiones estratégicas, resolución de conflictos arquitectónicos y gestión de agentes requieren máximo razonamiento |
| **MAVIM-Planner** | Claude Opus 4.6 | `claude-opus-4-6` | Diseño de sistemas complejos, análisis de trade-offs y planificación de largo alcance |
| **MAVIM-Architect** | Claude Opus 4.6 | `claude-opus-4-6` | Definición de Bounded Contexts y esquemas de datos — errores aquí son costosos de revertir |
| **MAVIM-Developer** | Claude Sonnet 4.6 | `claude-sonnet-4-6` | Implementación de código: velocidad y capacidad balanceadas, excelente para ciclos cortos de PR |
| **MAVIM-Critic** | Claude Sonnet 4.6 | `claude-sonnet-4-6` | Revisión de código y auditoría de checklists: no requiere razonamiento estratégico profundo |
| **MAVIM-Scraper** (sub-rol) | Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Extracción y clasificación de datos de páginas web: máxima velocidad, mínimo costo |

---

## Protocolo de Invocación por Modelo

### Para Claude Code (CLI local)

```bash
# Orchestrator / Architect / Planner — máxima capacidad
claude --model claude-opus-4-6 [opciones]

# Developer / Critic — balanceado
claude --model claude-sonnet-4-6 [opciones]

# Scraper / Extractor — velocidad y volumen
claude --model claude-haiku-4-5-20251001 [opciones]
```

### Para subagentes Claude (dentro de Claude Code)

Cuando el Orchestrator lanza un subagente, debe especificar el modelo:

```
# Patrón de instrucción al lanzar subagente:
"Actúa como MAVIM-Developer usando claude-sonnet-4-6. Tu tarea es: [TAREA]"
```

---

## Reglas de Escalamiento de Modelo (Model Escalation)

### Cuándo escalar a Opus:
1. El agente Sonnet/Haiku lleva **más de 3 iteraciones** sin resolver un problema.
2. La tarea requiere razonamiento multi-paso con **más de 5 variables interdependientes**.
3. Se está definiendo una **decisión arquitectónica irreversible** (schema de base de datos, API contract).
4. El Critic detecta un problema de diseño (no de implementación) que requiere repensar la arquitectura.

### Cuándo degradar a Haiku:
1. La tarea es **extracción pura de datos** sin razonamiento complejo.
2. Se está procesando **volumen alto** de páginas o documentos en paralelo.
3. La tarea es **clasificación, parsing o transformación de formato**.

---

## Optimización de Context Window por Modelo

| Modelo | Context Window | Estrategia MAVIM |
| :--- | :--- | :--- |
| Claude Opus 4.6 | 200K tokens | Cargar PROGRESS_LOG.json + INTENT_MANIFEST + módulo relevante |
| Claude Sonnet 4.6 | 200K tokens | Cargar PROGRESS_LOG.json + ticket de tarea específico + módulo |
| Claude Haiku 4.5 | 200K tokens | Cargar solo el prompt de extracción + URL/contenido objetivo |

> [!IMPORTANT]
> **Regla de Poda (SOP_06):** Independientemente del modelo, cuando el contexto se vuelve repetitivo o supera las 80K tokens de contenido relevante, ejecutar Context Pruning y actualizar `PROGRESS_LOG.json` antes de iniciar una sesión nueva.

---

## Routing para Pipelines Multi-Agente

Cuando múltiples agentes trabajan en paralelo, el Orchestrator asigna modelos según el grafo de dependencias:

```
MAVIM-Orchestrator (Opus)
    ├── MAVIM-Planner (Opus)       ← Diseño del sprint
    │       └── MAVIM-Architect (Opus)   ← LEGO Map
    │
    ├── MAVIM-Developer A (Sonnet) ← Módulo Auth     ] paralelo
    ├── MAVIM-Developer B (Sonnet) ← Módulo Billing  ]
    │
    ├── MAVIM-Scraper (Haiku)      ← Investigación web concurrente
    │
    └── MAVIM-Critic (Sonnet)      ← Auditoría final
```

> [!CAUTION]
> **Nunca** lances múltiples instancias de Opus simultáneamente sin una necesidad clara — el costo se multiplica. Reserva Opus para el cuello de botella de razonamiento; paraleliza con Sonnet/Haiku.
