# MAVIM: The Bootloader (Agent Quick-Start)

> **META-INSTRUCTION:** Si eres un agente de IA (Claude Code, Codex, Windsurf), **LEE ESTO PRIMERO**. Este es el resumen ultra-comprimido de la Metodología Multi-Agentic VibeCoding (MAVIM) para que puedas comenzar a trabajar instantáneamente sin alucinar.

## 1. Reglas Inmutables (Senior Architecture)
- **Monolito Modular:** Todo proyecto se divide en módulos (`Bounded Contexts`) limpios.
- **Sin JOINs cruzados:** Prohibido mezclar datos de módulos mediante SQL JOINs. Usa APIs internas o Eventos (`Domain Events`).
- **TODO es UUIDv4:** Prohibido usar IDs autoincrementales escalares que revelen volumen de datos.
- **No uses Floats para Dinero:** Usa `Int` (centavos) y respeta el esquema de [Doble Entrada (Ledger)](patterns/02_MARKETPLACE_ADVANCED.md).
- **Cero UI Genérica:** Utiliza **Shadcn UI + Tailwind CSS** (Dark Mode from day 1) para un *Premium Vibe*.

## 2. El Flujo de Trabajo Recursivo (Closed-Loop)
1. **Paso 0 - Secretos:** Dile al usuario humano que ejecute `./setup_mavim.sh`. Los agentes tienen *estrictamente prohibido* leer ese `.env`.
2. **Paso 1 - Estado:** LEE `/PROGRESS_LOG.json` antes de escribir cualquier línea de código para conocer tu rol actual y las tareas pendientes.
3. **Paso 2 - Meta-Prompt:** Carga la instrucción específica de tu rol (`/roles/ARCHITECT.md`, `/roles/DEVELOPER.md`, o `/roles/CRITIC.md`).
4. **Paso 3 - Ejecución:** Revisa los `/patterns` para inspirarte en arquitecturas previas (SaaS, E-commerce, Logística). Construye el código.
5. **Paso 4 - Evaluación:** Antes del commit de tu rama, valida tu código usando `/evals/CHECKLISTS.md` y revisa que no rompas los Anti-Patrones (`/patterns/COMMON_TRAPS.md`).
6. **Paso 5 - Fin de Ciclo:** Escribe formalmente tu conclusión actualizando `/PROGRESS_LOG.json` (dejando subtareas en `pending_subtasks` para el siguiente).

---
*Fin del Bootloader. Estás listo para codificar como un Senior. Revisa `PROGRESS_LOG.json`.*
