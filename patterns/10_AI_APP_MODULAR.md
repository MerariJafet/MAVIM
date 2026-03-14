# Blueprint 10: AI App Modular

**Objetivo:** Establecer la arquitectura base para aplicaciones que integran modelos de IA o Large Language Models (LLMs), enfocada fuertemente en la seguridad (Prompt Injection prevention) y el flujo predictivo.

## Mapa de Módulos

| Módulo | Responsabilidad | Interface (API Síncrona) | Eventos (Asíncronos) |
| :--- | :--- | :--- | :--- |
| **Orchestration Core** | Controlador principal de negocio y flujos de usuario. | `POST /core/workflow` | `WorkflowStarted`, `WorkflowCompleted` |
| **AI Gateway** | Capa de abstracción, throttling y ruteo a diversos LLMs (OpenAI, Anthropic). | `POST /llm/generate` | `ModelInvoked`, `ThresholdReached` |
| **RAG Engine** | Recuperación de información, vectorización (embeddings) y búsqueda semántica. | `POST /rag/query` | `DocumentEmbedded`, `ContextRetrieved` |
| **Guardrails & Evals** | Evaluación de Entradas y Salidas en tiempo real (Detección PII, Prompt Injection, Toxicidad).| `POST /eval/check` | `InjectionDetected`, `ResponseFiltered` |

## Esquema de Datos (Entidades Clave)

Todas las entidades **DEBEN** utilizar `UUID v4` como identificador primario.

- **Orchestration Core:** `Session (id: UUID, user_id: UUID, context: JSON)`
- **AI Gateway:** `PromptRequest (id: UUID, model: String, tokens_used: Int, cost: Decimal)`
- **RAG Engine:** `DocumentChunk (id: UUID, source_id: UUID, embedding_vector: Array)`
- **Guardrails:** `AuditLog (id: UUID, session_id: UUID, flag_type: String, blocked: Boolean)`

## Detalles Críticos de Implementación (Senior Level)

### 1. Permisos Basados en Relaciones (Google Zanzibar)
Cuando integres RAG sobre millones de documentos empresariales, el LLM no puede acceder a información prohibida para ese usuario/empleado.
- La recuperación vectorial DEBE cruzar un sistema de autorización estilo **Google Zanzibar** (Relationship-Based Access Control, ReBAC) para filtrar el contexto recuperado *antes* de enviarlo al modelo base.

### 2. Gestión Estratégica de Context Windows
- Las Ventanas de Contexto (Context Windows) son costosas. NUNCA cargues el historial entero del chat sin pensar.
- Implementa **Summarization Rings**: Conserva los últimos 5 mensajes intactos y pasa el historial antiguo por una rutina secundaria más barata que extraiga y compacte los hechos (Entity/Fact Extraction) en un solo párrafo inyectable en el System Prompt.

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **Prompt Injection:** NUNCA pasar la entrada directa del usuario del `Orchestration Core` al `AI Gateway`. **Debe** pasar primero obligatoriamente por el módulo `Guardrails & Evals`.
> 2. **Fuga de PII en RAG:** Antes de incrustar documentos en la base de datos vectorial (RAG Engine), se debe ejecutar un pase del módulo de `Guardrails` para eliminar y enmascarar información personal (SSNs, tarjetas, emails confidenciales).
> 3. **Acoplamiento Directo al Provider (Vendor Lock-in):** Construye la inferencia siempre contra el `AI Gateway`, no programes librerías dependientes de OpenAI directamente en el `Core`. Esto permite "VibeCoding" flexible si un modelo mejor sale al mercado.
