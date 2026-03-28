# 🚀 MAVIM: Multi-Agentic VibeCoding Methodology

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vibe Coding](https://img.shields.io/badge/Vibe--Coding-Enabled-blueviolet)](https://x.com/karpathy)
[![Built for Agents](https://img.shields.io/badge/Built--for-Claude--Code%20%7C%20Codex-blue)](https://github.com/MerariJafet/MAVIM)

### ⚡ Quick Start (The One-Click Prompt)
Copy and paste this into your favorite Agent (Claude Code, Cursor, Codex, Windsurf):
```text
Use MAVIM from github.com/MerariJafet/MAVIM to build [YOUR_APP_IDEA]. Run the setup script, assume the roles, and don't stop until the progress log is 100%.
```

**MAVIM** es el primer framework diseñado específicamente para que **Agentes de IA** (Claude Code, Cursor, Codex) construyan software de grado industrial de forma autónoma, sin perder el contexto y siguiendo estándares de ingeniería Senior.

### 🧠 ¿Por qué MAVIM?
Los agentes suelen fallar en proyectos largos debido a la amnesia de contexto y la falta de estructura. MAVIM soluciona esto mediante:
- **Estado Persistente:** Un log de progreso que sobrevive a reinicios.
- **Arquitectura LEGO:** Monolitos modulares que evitan el código spaghetti.
- **Protocolos de Seguridad:** Manejo de secretos y auditoría de inyecciones.

### 🛠️ Quick Start for AI Agents
Si eres un agente, simplemente lee `MAVIM.md` para entender tus instrucciones de orquestación y empieza a construir.

### 🌟 GitHub Topics
`#vibe-coding` `#agentic-ai` `#saas-framework` `#multi-agent-systems` `#autonomous-agents`

---

## 🗺️ The 4 Critical Phases of MAVIM

```text
+-----------------------+       +-------------------------+       +------------------------+       +-------------------------+
|      PHASE 1          |       |        PHASE 2          |       |       PHASE 3          |       |        PHASE 4          |
|    INTENTION          | ----> |      ARCHITECTURE       | ----> |      SYNTHESIS         | ----> |      EVALUATION         |
|                       |       |                         |       |                        |       |                         |
| User Vibe -> Spec     |       | The LEGO Map (Modular)  |       | Parallel Dev & PRs     |       | The Gatekeeper Review   |
| (INTENT_MANIFEST)     |       | (DATA_SCHEMA, UUIDs)    |       | (Branch isolation)     |       | (Sec, Arch, UX checks)  |
+-----------------------+       +-------------------------+       +------------------------+       +-------------------------+
            |                               |                                |                                |
            v                               v                                v                                v
+-------------------------------------------------------------------------------------------------------------------------+
|                                    PHASE 8: CONTINUITY & CLOSED-LOOP EXECUTION                                          |
|                         PROGRESS_LOG.json • setup_mavim.sh • MAVIM_HANDOVER_PROTOCOL.md                                 |
+-------------------------------------------------------------------------------------------------------------------------+
```

## Estructura del Repositorio (Docs)

## Fase 2: MAVIM Core SOPs (Standard Operating Procedures)

El núcleo de MAVIM está cimentado en 4 fases críticas de ejecución de la tarea. Todos los agentes deben comprender y adherirse estrictamente a estas políticas:

1. **[Fase de Intención (Vibe to Spec)](core/SOP_01_INTENTION.md):** Cómo transformar lenguaje natural y ambiguo en requisitos técnicos exactos (`INTENT_MANIFEST`).
2. **[Fase de Arquitectura (The LEGO Map)](core/SOP_02_ARCHITECTURE.md):** Exige implementar siempre un patrón de Monolito Modular con fronteras estrictas.
3. **[Fase de Síntesis Paralela + Multi-Agente](core/SOP_03_SYNTHESIS.md):** Protocolo de colaboración entre subagentes Claude: paralelismo, comunicación asíncrona por artefactos Git y prevención de conflictos.
4. **[Fase de Evaluación (The Gatekeeper)](core/SOP_04_EVALUATION.md):** Controles obligatorios de calidad, UX, Seguridad y consistencia lógica pre-despliegue.
5. **[Fase de Resiliencia (Circuit Breakers)](core/SOP_05_RESILIENCE.md):** Políticas obligatorias de reintentos (Exponential Backoff) y Cortacircuitos ante APIs LLM caídas.
6. **[Fase de Continuidad (Memoria Persistente)](core/SOP_06_CONTINUITY.md):** Reglas para mantener una "Caja Negra" mediante un `PROGRESS_LOG.json` inmutable y protocolos de **Poda de Contexto**.
7. **[Refactorización Quirúrgica](core/SOP_07_REFACTORING.md):** Protocolo para trabajar sobre código existente (Brownfield) sin introducir regresiones.
8. **[Claude Model Routing](core/SOP_08_CLAUDE_MODEL_ROUTING.md):** ⭐ **NUEVO** — Selección del modelo Claude óptimo por rol: Opus para estrategia, Sonnet para código, Haiku para scraping. Incluye tabla de routing y reglas de escalamiento.
9. **[Web Intelligence & Scraping](core/SOP_09_WEB_INTELLIGENCE.md):** ⭐ **NUEVO** — Protocolo de investigación web, extracción de contenido, análisis de diseño y CSS. Herramientas: Crawl4AI, Firecrawl, Playwright, ScrapeGraphAI. MCP servers para Claude Code.

## Fase 3: The Intelligence Patterns (Blueprints)

Modelos de referencia técnicos base ('Bloques LEGO') listos para implementar arquitectura de alta disponibilidad.

0. **[Design System (Shadcn/UI)](patterns/00_DESIGN_SYSTEM_SHADCN.md):** Reglas obligatorias de Tailwind CSS, paleta de colores, Dark Mode y Skeletons para UIs Premium out-of-the-box.
0. **[Deployment & Infra (Docker/Vercel)](patterns/00_DEPLOYMENT_DOCKER_VERCEL.md):** Exigencias de empaquetado Docker (backends), Edge (frontends) y CI/CD continuo `deploy.yml`.
1. **[Plataforma E-Commerce](patterns/01_ECOMMERCE.md):** Flujo transaccional, separando Catálogo, Carrito, Pagos e Inventario.
2. **[Marketplace Avanzado](patterns/02_MARKETPLACE_ADVANCED.md):** Ledger de doble entrada inmutable, Catálogo Polimórfico (JSONB) y Escrow.
3. **[SaaS Multi-Tenant B2B](patterns/04_SAAS_MULTITENANT.md):** Aislamiento de capas (Tenants), Feature Gating y Suscripciones.
4. **[ERP & CRM (Internal Ops)](patterns/07_ERP_CRM.md):** Desacoplamiento de flujos de venta y backoffice operativo.
5. **[Logística On-Demand](patterns/08_ONDEMAND_LOGISTICS.md):** Indexación Espacial H3, Algoritmo de Surge Pricing y Batched Matching.
6. **[AI App Modular (LLM Integration)](patterns/10_AI_APP_MODULAR.md):** Prevención de Prompt Injection, RAG pipeline aislado y Orchestration Core.
7. **[Real-Time Data Analytics (Kappa)](patterns/11_REALTIME_DATA_ANALYTICS.md):** Arquitectura de streaming con Kafka y procesamiento en tiempo real.
8. **[Web Intelligence & Scraping Pipeline](patterns/12_WEB_INTELLIGENCE_SCRAPING.md):** ⭐ **NUEVO** — Blueprint completo para pipelines de extracción web: Crawl4AI, Playwright, Firecrawl, ScrapeGraphAI. Módulos: Intelligence Collector, Content Pipeline, Design Extractor, Knowledge Store.
9. **[Anti-Patrones (Lista Negra)](patterns/COMMON_TRAPS.md):** Prácticas estrictamente prohibidas en MAVIM (Fat controllers, IDs secuenciales, Floats en moneda, Transacciones rotas).

## Fase 4: Agent Roles (System Prompts)

El "Cerebro" de la metodología. Instrucciones y metaprompts que cada agente MAVIM debe cargar antes de operar en el repositorio para alinear su comportamiento con los SOPs.

0. **[MAVIM-Orchestrator (The Supreme Director)](roles/MAVIM_ORCHESTRATOR.md):** `claude-opus-4-6` — Rompe bucles, dicta la política suprema, lanza subagentes paralelos y da el GO/NO-GO final.
1. **[MAVIM-Planner (The Strategic Designer)](roles/PLANNER.md):** ⭐ **NUEVO** `claude-opus-4-6` — Investiga con Web Intelligence, evalúa viabilidad y produce `SPRINT_PLAN.md` antes de la arquitectura.
2. **[MAVIM-Architect (The Visionary)](roles/ARCHITECT.md):** `claude-opus-4-6` — Diseña los bloques LEGO y la estructura de datos basados en Monolitos Modulares.
3. **[MAVIM-Developer (The Builder)](roles/DEVELOPER.md):** `claude-sonnet-4-6` — Construye la lógica funcional estrictamente dentro de las fronteras de los módulos asignados.
4. **[MAVIM-Critic (The Gatekeeper)](roles/CRITIC.md):** `claude-sonnet-4-6` — Evalúa heurísticas UX, prevención de inyección AI, revisión de integridad de fronteras y cumplimiento de requerimientos.

## Fase 5: Deep Knowledge Injection (El 100% Real)

Para garantizar arquitecturas y código fuente de "Nivel Senior", los agentes utilizan plantillas avanzadas de validación y conocimiento profundo. Los 4 patrones arquitectónicos de la Fase 3 incluyen secciones completas con *Detalles Críticos de Implementación* (Ledgers, H3, Tenant Isolation, Fan-out, Cursor Pagination).

Además, se cuenta con material de auto-evaluación:

1. **[MAVIM Meta-Prompts](prompts/META_PROMPTS.md):** Contiene plantillas "Chain-of-Thought" (`VIBE_TO_ARCH`, `CODE_REVIEW`) para inicializar el contexto del agente MAVIM-Architect y MAVIM-Critic respectivamente.
2. **[Technical Evaluation Checklists](evals/CHECKLISTS.md):** La lista de validación estricta de The Gatekeeper. Cubriendo "Security Check (Zero Trust)", "Senior Architecture Check", y "UX Heuristics". Un PR no se aprueba si no pasa el 100% de los puntos de control.

## Fase 8: Closed-Loop Execution (Motores Auto-Sostenibles)
Para que MAVIM pase de ser un solo "Manual" a una plataforma de despliegue ininterrumpido a lo largo del tiempo, incorpora herramientas de continuidad para agentes de IA que les impiden entrar en amnesia:
1. **[MAVIM Handover Protocol](core/MAVIM_HANDOVER_PROTOCOL.md):** Mecanismo estandarizado para pasarse la estafeta entre Architect -> Developer -> Critic usando un sistema de tickets físicos y `PROGRESS_LOG.json`.
2. **[Secret Injector Tool (`setup_mavim.sh`)](setup_mavim.sh):** Script interactivo para el humano (o entorno CI/CD) destinado a la generación super segura de `.env`, prohibiendo por completo la lectura o listado a los agentes de programación.
