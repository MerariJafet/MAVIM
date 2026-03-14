# MAVIM-Methodology

**MAVIM (Multi Agentic VibeCoding Methodology)**

MAVIM es una metodología diseñada para el desarrollo de software de inicio a fin utilizando VibeCoding y agentes de Inteligencia Artificial. La metodología captura la transición de escribir sintaxis manual a orquestar intenciones ("vibes") mediante agentes especializados.

Este repositorio no es solo código, sino un **Manual de Operaciones Ejecutable**, estructurado para que cualquier agente pueda descargar y comprender cómo ejecutar un proyecto estructurado y bien orquestado.

## Fase 2: MAVIM Core SOPs (Standard Operating Procedures)

El núcleo de MAVIM está cimentado en 4 fases críticas de ejecución de la tarea. Todos los agentes deben comprender y adherirse estrictamente a estas políticas:

1. **[Fase de Intención (Vibe to Spec)](core/SOP_01_INTENTION.md):** Cómo transformar lenguaje natural y ambiguo en requisitos técnicos exactos (`INTENT_MANIFEST`).
2. **[Fase de Arquitectura (The LEGO Map)](core/SOP_02_ARCHITECTURE.md):** Exige implementar siempre un patrón de Monolito Modular con fronteras estrictas.
3. **[Fase de Síntesis Paralela](core/SOP_03_SYNTHESIS.md):** Dicta cómo iterar constructivamente sin colisionar con otros agentes usando Git Branches.
4. **[Fase de Evaluación (The Gatekeeper)](core/SOP_04_EVALUATION.md):** Controles obligatorios de calidad, UX, Seguridad y consistencia lógica pre-despliegue.

## Fase 3: The Intelligence Patterns (Blueprints)

Modelos de referencia técnicos base ('Bloques LEGO') listos para implementar arquitectura de alta disponibilidad.

1. **[Plataforma E-Commerce](patterns/01_ECOMMERCE.md):** Flujo transaccional, separando Catálogo, Carrito, Pagos e Inventario.
2. **[Marketplace Avanzado](patterns/02_MARKETPLACE_ADVANCED.md):** Ledger de doble entrada inmutable, Catálogo Polimórfico (JSONB) y Escrow.
3. **[SaaS Multi-Tenant B2B](patterns/04_SAAS_MULTITENANT.md):** Aislamiento de capas (Tenants), Feature Gating y Suscripciones.
4. **[ERP & CRM (Internal Ops)](patterns/07_ERP_CRM.md):** Desacoplamiento de flujos de venta y backoffice operativo.
5. **[Logística On-Demand](patterns/08_ONDEMAND_LOGISTICS.md):** Indexación Espacial H3, Algoritmo de Surge Pricing y Batched Matching.
6. **[AI App Modular (LLM Integration)](patterns/10_AI_APP_MODULAR.md):** Prevención de Prompt Injection, RAG pipeline aislado y Orchestration Core.

## Fase 4: Agent Roles (System Prompts)

El "Cerebro" de la metodología. Instrucciones y metaprompts que cada agente MAVIM debe cargar antes de operar en el repositorio para alinear su comportamiento con los SOPs.

1. **[MAVIM-Architect (The Visionary)](roles/ARCHITECT.md):** Diseña los bloques LEGO y la estructura de datos basados en Monolitos Modulares.
2. **[MAVIM-Developer (The Builder)](roles/DEVELOPER.md):** Construye la lógica funcional estrictamente dentro de las fronteras de los módulos asignados.
3. **[MAVIM-Critic (The Gatekeeper)](roles/CRITIC.md):** Evalúa heurísticas UX, prevención de inyección AI, revisión de integridad de fronteras ("cross-imports") y cumplimiento de requerimientos lógicos.

## Fase 5: Deep Knowledge Injection (El 100% Real)

Para garantizar arquitecturas y código fuente de "Nivel Senior", los agentes utilizan plantillas avanzadas de validación y conocimiento profundo. Los 4 patrones arquitectónicos de la Fase 3 incluyen secciones completas con *Detalles Críticos de Implementación* (Ledgers, H3, Tenant Isolation, Fan-out, Cursor Pagination).

Además, se cuenta con material de auto-evaluación:

1. **[MAVIM Meta-Prompts](prompts/META_PROMPTS.md):** Contiene plantillas "Chain-of-Thought" (`VIBE_TO_ARCH`, `CODE_REVIEW`) para inicializar el contexto del agente MAVIM-Architect y MAVIM-Critic respectivamente.
2. **[Technical Evaluation Checklists](evals/CHECKLISTS.md):** La lista de validación estricta de The Gatekeeper. Cubriendo "Security Check (Zero Trust)", "Senior Architecture Check", y "UX Heuristics". Un PR no se aprueba si no pasa el 100% de los puntos de control.
