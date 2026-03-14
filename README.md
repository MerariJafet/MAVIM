# MAVIM-Methodology
**Multi Agentic VibeCoding Methodology**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Built for Agents](https://img.shields.io/badge/Built%20for-AI%20Agents-blueviolet.svg)](#)

> **From high-level intent to production-ready SaaS in minutes.**
> A methodology designed to transform the process of software creation from syntax-writing to intention-orchestrating, using specialized Autonomous AI Agents.

---

## ⚡ Agent Quick Start (The Bootloader)
If you are an AI Agent (Claude Code, Cursor, Windsurf), start your execution loop here:
👉 **READ: [`MAVIM.md`](MAVIM.md)** (Ultra-compressed 30-second primer)

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
3. **[Fase de Síntesis Paralela](core/SOP_03_SYNTHESIS.md):** Dicta cómo iterar constructivamente sin colisionar con otros agentes usando Git Branches.
4. **[Fase de Evaluación (The Gatekeeper)](core/SOP_04_EVALUATION.md):** Controles obligatorios de calidad, UX, Seguridad y consistencia lógica pre-despliegue.
5. **[Fase de Resiliencia (Circuit Breakers)](core/SOP_05_RESILIENCE.md):** Políticas obligatorias de reintentos (Exponential Backoff) y Cortacircuitos ante APIs LLM caídas.
6. **[Fase de Continuidad (Memoria Persistente)](core/SOP_06_CONTINUITY.md):** Reglas para mantener una "Caja Negra" mediante un `PROGRESS_LOG.json` inmutable y protocolos de **Poda de Contexto**.

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
7. **[Anti-Patrones (Lista Negra)](patterns/COMMON_TRAPS.md):** Prácticas estrictamente prohibidas en MAVIM (Fat controllers, IDs secuenciales, Floats en moneda, Transacciones rotas).

## Fase 4: Agent Roles (System Prompts)

El "Cerebro" de la metodología. Instrucciones y metaprompts que cada agente MAVIM debe cargar antes de operar en el repositorio para alinear su comportamiento con los SOPs.

0. **[MAVIM-Orchestrator (The Supreme Director)](roles/MAVIM_ORCHESTRATOR.md):** Rompe bucles infinitos, dicta la política suprema al resto de agentes, y asegura iteraciones positivas constantes.
1. **[MAVIM-Architect (The Visionary)](roles/ARCHITECT.md):** Diseña los bloques LEGO y la estructura de datos basados en Monolitos Modulares.
2. **[MAVIM-Developer (The Builder)](roles/DEVELOPER.md):** Construye la lógica funcional estrictamente dentro de las fronteras de los módulos asignados.
3. **[MAVIM-Critic (The Gatekeeper)](roles/CRITIC.md):** Evalúa heurísticas UX, prevención de inyección AI, revisión de integridad de fronteras ("cross-imports") y cumplimiento de requerimientos lógicos.

## Fase 5: Deep Knowledge Injection (El 100% Real)

Para garantizar arquitecturas y código fuente de "Nivel Senior", los agentes utilizan plantillas avanzadas de validación y conocimiento profundo. Los 4 patrones arquitectónicos de la Fase 3 incluyen secciones completas con *Detalles Críticos de Implementación* (Ledgers, H3, Tenant Isolation, Fan-out, Cursor Pagination).

Además, se cuenta con material de auto-evaluación:

1. **[MAVIM Meta-Prompts](prompts/META_PROMPTS.md):** Contiene plantillas "Chain-of-Thought" (`VIBE_TO_ARCH`, `CODE_REVIEW`) para inicializar el contexto del agente MAVIM-Architect y MAVIM-Critic respectivamente.
2. **[Technical Evaluation Checklists](evals/CHECKLISTS.md):** La lista de validación estricta de The Gatekeeper. Cubriendo "Security Check (Zero Trust)", "Senior Architecture Check", y "UX Heuristics". Un PR no se aprueba si no pasa el 100% de los puntos de control.

## Fase 8: Closed-Loop Execution (Motores Auto-Sostenibles)
Para que MAVIM pase de ser un solo "Manual" a una plataforma de despliegue ininterrumpido a lo largo del tiempo, incorpora herramientas de continuidad para agentes de IA que les impiden entrar en amnesia:
1. **[MAVIM Handover Protocol](core/MAVIM_HANDOVER_PROTOCOL.md):** Mecanismo estandarizado para pasarse la estafeta entre Architect -> Developer -> Critic usando un sistema de tickets físicos y `PROGRESS_LOG.json`.
2. **[Secret Injector Tool (`setup_mavim.sh`)](setup_mavim.sh):** Script interactivo para el humano (o entorno CI/CD) destinado a la generación super segura de `.env`, prohibiendo por completo la lectura o listado a los agentes de programación.
