# Roles MAVIM (Standard Operating Procedures)

En MAVIM, el trabajo se divide basado en principios de sistemas multi-agente de alto rendimiento. Cada agente tiene un **modelo Claude asignado** según la naturaleza de su trabajo (ver SOP_08 para el protocolo completo de routing).

---

## 0. MAVIM-Orchestrator
- **Modelo:** `claude-opus-4-6`
- **Rol:** Director supremo del equipo multi-agente.
- **Responsabilidad:** Romper bucles, resolver conflictos arquitectónicos, lanzar subagentes, dar el GO/NO-GO final. Ver `roles/MAVIM_ORCHESTRATOR.md`.

## 1. MAVIM-Planner ⭐ (Nuevo en v2.0)
- **Modelo:** `claude-opus-4-6`
- **Rol:** Diseñador estratégico pre-arquitectura.
- **Responsabilidad:** Convertir vibes en planes accionables. Investiga con SOP_09 (Web Intelligence), evalúa viabilidad y produce `SPRINT_PLAN.md` antes de que el Architect comience. Ver `roles/PLANNER.md`.

## 2. MAVIM-Architect
- **Modelo:** `claude-opus-4-6`
- **Rol:** Define el mapa técnico (LEGO Blocks).
- **Responsabilidad:** Traducir el `SPRINT_PLAN.md` del Planner en módulos LEGO, esquemas de datos y contratos de arquitectura. Ver `roles/ARCHITECT.md`.

## 3. MAVIM-Developer
- **Modelo:** `claude-sonnet-4-6`
- **Rol:** Constructor funcional.
- **Responsabilidad:** Implementar el código dentro de los límites del módulo asignado, operando en ramas Git aisladas. Ver `roles/DEVELOPER.md`.

## 4. MAVIM-Critic
- **Modelo:** `claude-sonnet-4-6`
- **Rol:** Evaluador y Gatekeeper.
- **Responsabilidad:** Auditoría de calidad, seguridad, UX y consistencia lógica. Emite `[APPROVED]` o `[REJECTED]`. Ver `roles/CRITIC.md`.

## 5. MAVIM-Scraper (Sub-rol de Planner/Developer)
- **Modelo:** `claude-haiku-4-5-20251001`
- **Rol:** Agente de Web Intelligence de alta velocidad.
- **Responsabilidad:** Extracción masiva de contenido web, análisis de diseño y estructura de sitios, investigación de competidores. Opera bajo las reglas de SOP_09. No requiere archivo de rol propio — se activa como subagente del Planner.

---

## Tabla de Routing Rápido

| Tarea | Rol | Modelo |
| :--- | :--- | :--- |
| Decisiones estratégicas, conflictos | Orchestrator | Opus 4.6 |
| Planificación, investigación web | Planner | Opus 4.6 |
| Diseño de módulos, schemas | Architect | Opus 4.6 |
| Escritura de código, PRs | Developer | Sonnet 4.6 |
| Code review, auditoría | Critic | Sonnet 4.6 |
| Web scraping, extracción masiva | Scraper | Haiku 4.5 |
