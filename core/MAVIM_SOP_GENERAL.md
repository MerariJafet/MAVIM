# General Standard Operating Procedure (SOP)

**Reglas de Oro MAVIM v2.0:**

### Regla 1: Arquitectura Primero
Ningún agente puede escribir código sin antes haber validado y comprendido la arquitectura **'Modular Monolith'** (Monolito Modular). Esta validación asegura que el desarrollo inicie con fronteras bien definidas y una estructura escalable, previniendo caos estructural antes de la primera línea de código.

### Regla 2: Modelo Claude por Rol (NEW)
Cada agente MAVIM opera con el modelo Claude óptimo para su función:
- **Opus 4.6** → Orchestrator, Planner, Architect (decisiones estratégicas e irreversibles)
- **Sonnet 4.6** → Developer, Critic (ejecución, código, revisión)
- **Haiku 4.5** → Scraper (extracción masiva, alta velocidad, bajo costo)

> [!IMPORTANT]
> Usar el modelo equivocado no es un error menor — impacta directamente en costo, velocidad y calidad del output. Ver `core/SOP_08_CLAUDE_MODEL_ROUTING.md` para el protocolo completo.

### Regla 3: Investigar Antes de Diseñar (NEW)
Para proyectos Greenfield o con decisiones tecnológicas inciertas, el MAVIM-Planner DEBE activar el módulo de Web Intelligence (SOP_09) antes de que el Architect comience a dibujar el LEGO Map. Diseñar sin investigación es desperdicio.

### Regla 4: Colaboración por Artefactos
Los agentes MAVIM no se comunican por memoria de chat — se comunican por artefactos Git: tickets (`/tasks/*.md`), `PROGRESS_LOG.json` y Pull Requests. Esta regla garantiza que cualquier agente pueda retomar el trabajo desde cualquier punto sin pérdida de contexto.
