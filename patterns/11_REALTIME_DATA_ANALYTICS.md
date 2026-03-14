# MAVIM Pattern 11: Real-Time Data Analytics (Kappa Architecture)

Este patrón define la integración de analítica en tiempo real masiva dentro del ecosistema MAVIM, resolviendo la ingestión, procesamiento y visualización sin comprometer el rendimiento de los módulos transaccionales.

## 1. Arquitectura Kappa (The Single Truth)
En lugar de mantener pipelines Batch y Streaming separados (Lambda), MAVIM exige **Arquitectura Kappa** usando un único log inmutable (ej. Apache Kafka o Redpanda) como la única fuente de la verdad para todos los datos analíticos.

- **Ingestión de Eventos:** Los Módulos Transaccionales (ej. `Sales`, `Auth`) actúan como *Producers*. Emiten JSONs al broker.
- **PROHIBICIÓN ESTRICTA:** Queda prohibido consultar directamente las bases de datos transaccionales (`OLTP`) para generar dashboards en tiempo real. Esto bloquea las tablas. Siempre leer desde el flujo de eventos (`OLAP`).

## 2. Invariantes de Módulo (Modular Monolith)
- El módulo `Analytics` debe ser un Bounded Context independiente. 
- **Consumo:** Solo se alimenta suscribiéndose pasivamente a eventos de dominio públicos emitidos por otros módulos (ej. `OrderCompletedEvent_v1`).
- **Almacenamiento:** Mantiene su propia base de datos optimizada para lectura rápida (ej. ClickHouse, Apache Druid o PostgreSQL con índices particionados).

## 3. Watermarking & Late Data Handling
Para sistemas que reciben eventos desordenados o retrasados (ej. dispositivos móviles sin conexión), evitar cálculos erróneos promediando ventanas de tiempo ciegamente.
- Implementar **Watermarking** basado en el `event_time` real generado en el cliente, no en el `processing_time` del servidor.
- Configurar ventanas (Tumbling/Sliding) con un límite de tolerancia (Allowed Lateness) antes de cerrar y congelar la métrica.

## 4. Identificadores y Trazabilidad
- **Correlation_ID (UUIDv4):** TODO evento analítico debe portar un `correlation_id` único para seguir la traza completa de la petición (Observabilidad distribuida).
- **Tenant_ID (UUIDv4):** Para entornos B2B, incluir obligatoriamente el `tenant_id` en cada evento para el aislamiento lógico de métricas con filtrado RLS (Row-Level Security). Nunca usar IDs incrementales.

## 5. El Contrato de Entorno (Ports & Env)
Antes de programar el pipeline analítico, incluir esta configuración en el `ARCHITECTURE_CONTRACT.md`:

```env
# Broker
KAFKA_BROKER_URL=broker:29092
KAFKA_TOPIC_PREFIX=mavim.events.

# Analytics Database
CLICKHOUSE_URL=http://clickhouse:8123
CLICKHOUSE_USER=mavim_analytics

# API Ports
ANALYTICS_API_PORT=8005
```
**Regla:** El módulo de Analytics debe arrancar buscando `ANALYTICS_API_PORT` y `KAFKA_BROKER_URL`. Valores hardcodeados como `localhost:9092` resultarán en un fallo del *Smoke Test* y rechazo del Gatekeeper.
