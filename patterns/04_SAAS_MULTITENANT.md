# Blueprint 04: SaaS Multitenant

**Objetivo:** Arquitectura diseñada para Software as a Service B2B/B2C que atiende a múltiples organizaciones (tenants) desde la misma infraestructura, garantizando el aislamiento de datos y esquemas de facturación por niveles.

## Mapa de Módulos

| Módulo | Responsabilidad | Interface (API Síncrona) | Eventos (Asíncronos) |
| :--- | :--- | :--- | :--- |
| **Identity/Tenant** | Aislamiento de datos organizacionales y autenticación. | `GET /tenant/auth` | `TenantOnboarded`, `UserAddedToTenant` |
| **Billing** | Gestión de suscripciones, métodos de pago y facturación. | `GET /billing/status` | `SubscriptionActive`, `SubscriptionExpired`, `PaymentFailed` |
| **Feature Gating** | Control de acceso a funciones basado en el plan del Tenant. | `GET /features/{tenant_id}` | `PlanUpgraded`, `PlanDowngraded` |
| **Core SaaS** | El valor de negocio central de la aplicación. | `(Módulo dependiente del App)`| `CoreEntityCreated`, `CoreEntityUpdated` |

## Esquema de Datos (Entidades Clave)

Todas las entidades **DEBEN** utilizar `UUID v4` como identificador primario.

- **Identity:** `Tenant (id: UUID, domain: String)`, `User (id: UUID, tenant_id: UUID, role: String)`
- **Billing:** `Subscription (id: UUID, tenant_id: UUID, plan_tier: String, status: String)`
- **Feature Gating:** `FeatureEntitlement (id: UUID, plan_tier: String, features: JSON)`
- **Core SaaS:** `Resource (id: UUID, tenant_id: UUID, data: JSON)`

## Detalles Críticos de Implementación (Senior Level)

### 1. Aislamiento Físico vs Lógico (Tenant Isolation)
- **Nivel 1 (Lógico - Shared DB):** Todas las tablas tienen `tenant_id`. Se exige usar "Row-Level Security" (RLS) en Postgres para forzar que el ORM nunca extraiga datos de otro tenant por error.
- **Nivel 2 (Físico - DB per Tenant):** Para tenants Enterprise con requerimientos de compliance estrictos, el mapeo de conexión debe resolverse dinámicamente según el subdominio.

### 2. Distribución de Eventos Masivos (Pattern Fan-out)
Si el SaaS tiene características de red social (ej: Notificaciones a todos los empleados o Feed de actividad):
- **Estrategia (Fan-out on write):** Cuando el 'Jefe' publica, el evento se inserta iterativamente asíncronamente en los inboxes de memoria (Redis) de los 10,000 empleados, en lugar de que cada empleado consulte a la base de datos central en lectura (Fan-out on read).

### 3. Paginación Infinita (Cursor Pagination)
- **Regla Estricta:** NUNCA uses `OFFSET / LIMIT` para tablas con alto volumen (>1M filas) porque el rendimiento decae O(N). **Siempre** usar Paginación por Cursor (buscando el registro posterior al último `id` o `timestamp` conocido: `WHERE created_at < ? ORDER BY created_at DESC LIMIT X`).

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **Fuga de Datos (Data Bleeding):** Absolutamente todas las consultas de la aplicación al módulo `Core SaaS` deben incluir `WHERE tenant_id = ?` o utilizar RLS (Row Level Security) en la base de datos.
> 2. **No acoplar Billing al Core:** El `Core SaaS` no debe consultar si un pago falló. Debe consultar el módulo de `Feature Gating` u escuchar si la suscripción de `Billing` sigue `Active`.
> 3. **Lógica de Roles en Base de Datos Principal:** Centraliza el mapeo de accesos (RBAC/ABAC) en `Identity`, no lo repitas a lo largo de los módulos.
