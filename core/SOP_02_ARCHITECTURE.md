# MAVIM SOP 02: Architecture Phase (The Map)

**Objetivo:** Establecer una base técnica robusta, escalable y mantenible.

Este es el SOP más importante de MAVIM. Establece que toda aplicación construida bajo esta metodología **DEBE** seguir el patrón de arquitectura de **Monolito Modular** (Modular Monolith).

## Reglas de Oro Arquitectónicas

### 1. Aislamiento Estricto (Boundaries)
- Cada módulo (ej. `Auth`, `Billing`, `Inventory`, `Core`) debe ser autónomo, con sus propios datos y su propia lógica de negocio.
- **PROHIBIDO:** Realizar `JOINs` directos en base de datos entre tablas que pertenecen a módulos diferentes.

### 2. Identificadores Universales
- **SIEMPRE** se deben utilizar `UUID v4` (o superior) como identificadores principales (Primary Keys) para las entidades del dominio expuestas.
- **NUNCA** usar IDs autoincrementales numéricos (`1`, `2`, `3`...) ya que revelan el volumen de datos de la aplicación y el orden de creación.

### 3. Comunicación Inter-módulo
- Los módulos deben comunicarse entre sí exclusivamente mediante:
  - **Síncrona:** Llamadas a métodos o interfaces públicas bien definidas (Contratos).
  - **Asíncrona:** Mediante la emisión y suscripción a Eventos de Dominio (Domain Events).
