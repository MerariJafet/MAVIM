# MAVIM Agent Teams — Master Prompt

> **Uso:** Copia el bloque correspondiente a tu escenario y úsalo como prompt inicial en Claude Code.
> Los agentes en `.claude/agents/` se activan automáticamente vía `@mavim-[rol]` o el Orchestrator los delega.

---

## Prompt 1: Proyecto Nuevo (Greenfield) — Equipo Completo

```
Activa el agente @mavim-orchestrator.

Nuevo proyecto: [DESCRIPCIÓN EN 2-3 ORACIONES]

Contexto:
- Usuario objetivo: [quién lo usa]
- Problema central: [qué resuelve]
- Stack preferido (si aplica): [o "decide tú"]
- Fecha límite: [o "sin restricción"]

Sigue la secuencia MAVIM completa:
1. Escanea el entorno (SOP_09)
2. Activa @mavim-planner para producir SPRINT_PLAN.md
3. Activa @mavim-architect para ARCHITECTURE_CONTRACT.md + MAPA_LEGO.md
4. Lanza @mavim-developer (uno por módulo) en paralelo
5. Activa @mavim-critic al terminar cada módulo
6. Aplica SOP_14 (Art Direction) ANTES de cualquier código UI
7. Corre Playwright 18 gates antes de cualquier merge a main
8. Escribe COGNITIVE_BRIDGE.json al finalizar la sesión

No pares hasta que el Critic diga APPROVED en todos los módulos.
```

---

## Prompt 2: Feature Nueva sobre Código Existente — Modo Quirúrgico

```
Activa el agente @mavim-orchestrator en modo quirúrgico (SOP_07).

Feature a implementar: [DESCRIPCIÓN EXACTA]
Archivos afectados (si los conoces): [o "identifica tú"]

Protocolo obligatorio:
1. Genera IMPACT_MAP.json PRIMERO — sin excepciones
2. Crea rama refactor/[nombre-feature]
3. Corre smoke test base antes de tocar código
4. Activa @mavim-architect si la feature requiere nuevo diseño de módulo
5. Activa @mavim-developer para la implementación
6. Activa @mavim-critic para auditoría
7. Zero cambios fuera del scope definido en el IMPACT_MAP

Avísame antes de mergear a main.
```

---

## Prompt 3: Investigación Tecnológica — Solo Scraper

```
Activa el agente @mavim-scraper.

Investiga: [TECNOLOGÍA / LIBRERÍA / STACK]

Quiero saber:
- Top 5 opciones disponibles en 2025-2026
- Estrellas GitHub, licencia, última release
- Si tienen servidor MCP para Claude Code
- Cuándo usar cada una vs las otras
- Recomendación final con justificación

Output esperado: TECH_RESEARCH_[tema].md con tabla comparativa y fuentes verificadas.
No incluyas herramientas sin URL verificada.
```

---

## Prompt 4: Sprint Paralelo — Múltiples Módulos

```
Activa el agente @mavim-orchestrator.

Tenemos SPRINT_PLAN.md y ARCHITECTURE_CONTRACT.md listos.
Módulos a implementar en paralelo:

- Módulo A: [nombre] — archivos: [lista]
- Módulo B: [nombre] — archivos: [lista]
- Módulo C: [nombre] — archivos: [lista]

Lanza un @mavim-developer por módulo simultáneamente.
Cada Developer trabaja en su rama feature/[modulo] sin tocar las otras.
Cuando los tres terminen, lanza @mavim-critic para revisar los tres PRs.

Estado del sistema:
- PROGRESS_LOG.json: [adjuntar o indicar path]
- Tests base: [passing / failing / no disponibles]
```

---

## Prompt 5: Auditoría de Código Existente

```
Activa el agente @mavim-critic.

Audita el módulo: [path al módulo]
Contexto: [qué hace este módulo]

Checklist prioritario:
1. Seguridad OWASP Top 10
2. MAVIM Compliance (boundaries, UUIDs, Ledger, resilience)
3. UI/UX: anti-AI-slop, spring physics, paleta
4. Performance: N+1 queries, bundle size, memory leaks

Output: reviews/REVIEW_[modulo].md con veredicto APPROVED / CONDITIONAL / REJECTED.
Sé específico: archivo:línea para cada hallazgo.
```

---

## Prompt 6: Handoff entre Sesiones — Cognitive Bridge

```
Activa el agente @mavim-orchestrator.

Estamos retomando trabajo de una sesión anterior.

1. Lee COGNITIVE_BRIDGE.json para ver el estado exacto
2. Verifica PROGRESS_LOG.json para los módulos pendientes
3. Corre mavim_scan.sh para verificar el entorno actual
4. Reanuda desde el último checkpoint sin duplicar trabajo
5. Si hay inconsistencias entre el Bridge y el estado real del repo → díme antes de continuar

Contexto adicional: [cualquier cosa que cambió desde la última sesión]
```

---

## Prompt 7: UI/UX Surgery — Art Direction + Implementation

```
Activa el agente @mavim-orchestrator con foco en SOP_14 + SOP_15.

Trabajo visual a realizar: [descripción]
Componentes afectados: [lista o "identifica tú"]

Protocolo obligatorio:
1. Lee SOP_14_HIGH_FIDELITY_UI_UX_MOTION.md completo
2. Verifica o crea ART_DIRECTION.md para el proyecto
3. Confirma tokens: --spring-bounce, --font-display, --primary-rgb en index.css
4. Activa skill: ui-ux-pro-max
5. Activa skill: animation-libraries-expert (si hay motion)
6. Activa skill: threejs-skills (si hay 3D)
7. Implementa con @mavim-developer
8. Corre Playwright gates A01-A07 (UI) + S01-S08 (Sensory) al terminar

Anti-AI-Slop check:
- Prohibido: system-ui, bg-white, text-gray-900, transition all 0.2s ease
- Obligatorio: spring physics, paleta personalizada, micro-interacciones
```

---

## Referencia Rápida de Agentes

| Agente | Modelo | Cuándo | Produce |
|--------|--------|--------|---------|
| `@mavim-orchestrator` | Opus 4.6 | Siempre primero | Coordinación |
| `@mavim-planner` | Opus 4.6 | Greenfield / ambigüedad | SPRINT_PLAN.md |
| `@mavim-architect` | Opus 4.6 | Antes de BUILD | ARCHITECTURE_CONTRACT.md |
| `@mavim-developer` | Sonnet 4.6 | Implementar módulo | Código + tests |
| `@mavim-critic` | Sonnet 4.6 | Post-implementación | REVIEW_[modulo].md |
| `@mavim-scraper` | Haiku 4.5 | Investigación web | TECH_RESEARCH_[tema].md |

---

## Tips de Eficiencia

1. **Paralelismo máximo:** Lanza N Developers en simultáneo si los módulos son independientes. Un Critic puede revisar todos al terminar.
2. **Scraper en background:** Si el Planner necesita investigación, lanza el Scraper mientras el Architect trabaja en otro módulo independiente.
3. **Critic rápido:** Dale el checklist exacto. Sin contexto vago = review específico y accionable.
4. **Orchestrator como árbitro:** Si dos Developers tienen conflicto en un archivo compartido, el Orchestrator serializa. Nunca dejan que ambos editen el mismo archivo.
5. **PROGRESS_LOG como heartbeat:** Cualquier agente que no actualiza el log en 10 minutos = stalled. Orchrestrator interviene.
