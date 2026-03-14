# MAVIM SOP 01: Intention Phase (Vibe to Spec)

**Objetivo:** Transformar el lenguaje natural y el "vibe" (idea vaga) en un documento de requisitos técnicos, funcionales y no funcionales sin perder la esencia inicial.

## Reglas de Ejecución

Antes de generar cualquier línea de código, el agente MAVIM **DEBE** producir un archivo `INTENT_MANIFEST.md`. 
Este manifiesto debe incluir obligatoriamente:
1. **El Problema:** Descripción clara del problema a resolver.
2. **Los Actores:** Quiénes interactúan con el sistema.
3. **Casos de Éxito (Definition of Done):** Qué debe cumplirse para considerar la tarea como finalizada exitosamente.

> [!IMPORTANT]
> **Ambigüedad Cero:** Si la intención del usuario es ambigua o falta información clave para definir los requisitos, el agente DEBE detenerse y preguntar al usuario para aclarar todas las dudas antes de avanzar.
