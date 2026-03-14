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

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **Fuga de Datos (Data Bleeding):** Absolutamente todas las consultas de la aplicación al módulo `Core SaaS` deben incluir `WHERE tenant_id = ?` o utilizar RLS (Row Level Security) en la base de datos.
> 2. **No acoplar Billing al Core:** El `Core SaaS` no debe consultar si un pago falló. Debe consultar el módulo de `Feature Gating` u escuchar si la suscripción de `Billing` sigue `Active`.
> 3. **Lógica de Roles en Base de Datos Principal:** Centraliza el mapeo de accesos (RBAC/ABAC) en `Identity`, no lo repitas a lo largo de los módulos.
