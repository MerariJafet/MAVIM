# MAVIM SOP 03: Parallel Synthesis Phase

**Objetivo:** Definir cómo múltiples agentes (o instancias) trabajan de forma concurrente sin crear conflictos en el código base, simulando un equipo de desarrollo de alto rendimiento.

## Flujo de Trabajo Multi-Agente

### 1. Branching Model (Gestión de Ramas)
- Ningún agente desarrolla directamente en la rama principal (`main`/`master`).
- Cada agente o tarea específica trabaja en una rama de Git completamente aislada y separada (ej. `feature/modulo-xyz`, `fix/login-bug`).

### 2. Roles y Revisión (Pull Requests)
- Se asignará un agente con el rol de **Lead Developer Agent** o Reviewer.
- Este agente será responsable de revisar los Pull Requests generados por los **Feature Agents**. Solo se fusiona un PR si pasa las validaciones del Gatekeeper.

### 3. Contexto y Meta-Prompting
- Se debe utilizar **Meta-prompting** en cada sesión del agente para asegurar que el agente siempre recuerde el contexto global y, especialmente, las **fronteras del módulo** (Boundaries) en el que se encuentra trabajando actualmente. No debe alterar código fuera de su dominio asignado.
