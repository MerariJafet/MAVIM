# MAVIM Cheat Sheet v2.0 (Agent Instruction Layer)
Lee esto para activarte instantáneamente:

1. **Roles y Modelos:**
   - Orchestrator/Planner/Architect → `claude-opus-4-6` (estrategia y diseño)
   - Developer/Critic → `claude-sonnet-4-6` (código y revisión)
   - Scraper (web intelligence) → `claude-haiku-4-5-20251001` (extracción masiva)
   - Ver `core/SOP_08_CLAUDE_MODEL_ROUTING.md` y `roles/ROLES.md`

2. **Flujo Principal (v2.0):**
   Orchestrator → Planner (SPRINT_PLAN.md) → Architect (MAPA_LEGO.md) → Developers paralelos (PRs) → Critic → GO/NO-GO

3. **Memoria:** Lee y actualiza `PROGRESS_LOG.json` en cada turno. Sin esto, el agente tiene amnesia.

4. **Secreto:** Ejecuta `setup_mavim.sh` al inicio. Prohibido filtrar el `.env`.

5. **Arquitectura:** Monolito Modular, UUIDs, Ledger para dinero, H3 para mapas. Ver `core/SOP_02_ARCHITECTURE.md`.

6. **Web Intelligence:** Si necesitas investigar tecnologías, competidores o extraer datos de páginas web, activa `core/SOP_09_WEB_INTELLIGENCE.md`. Herramientas: Crawl4AI (open source), Firecrawl (gestionado), Playwright (diseño CSS). Siempre respetar `robots.txt` y rate limiting.

7. **Multi-Agente:** Los agentes se comunican por artefactos Git — no por chat. Ver `core/SOP_03_SYNTHESIS.md` (Parte B) para el protocolo de subagentes paralelos.

8. **Refactoring Mode:** Si el usuario pide mejorar código existente → `core/SOP_07_REFACTORING.md`. El `IMPACT_MAP.json` es el **primer entregable obligatorio**. No borres código sin mapear dependencias.
