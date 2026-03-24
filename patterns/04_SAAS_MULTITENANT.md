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

---

## Lecciones de Producción Real (It's Me SaaS — 2026)

> Estos patrones se extrajeron después de llevar el SaaS a producción con tenants reales.
> Ver case study completo: `showcase/itsme-production-v3/CASE_STUDY_PRODUCTION.md`

### 4. Variables de Entorno en Vite/Next.js — La Trampa del Bundle

**Problema:** Las env vars se embeben en tiempo de compilación. `VITE_API_URL=http://localhost:8000` en `.env` queda hardcodeado en el bundle de producción.

```
# Regla: Crear .env.production con VITE_API_URL='' (vacío)
# En producción las rutas son relativas → Nginx hace el proxy
# NUNCA usar || para valores que pueden ser string vacío:
apiUrl: import.meta.env.VITE_API_URL ?? ''   # ✓ ?? maneja '' correctamente
apiUrl: import.meta.env.VITE_API_URL || ''   # ✗ || ignora '' y usa fallback
```

### 5. OAuth 2.0 es Autenticación, No Registro

**Regla crítica:** Nunca crear entidades de negocio (Owner, Tenant, Subscription) desde un callback de OAuth.

```
Flujo correcto:
  OAuth callback → buscar usuario existente → login si existe
  OAuth callback → usuario no existe → 404 "no_account" → redirect a /register
  Flujo de registro → Stripe → crear Owner + User → luego pueden linkear OAuth

Flujo incorrecto (crea agujero de seguridad):
  OAuth callback → usuario no existe → crear Owner+User gratis → login sin pago
```

### 6. Multi-Email en OAuth: El Patrón de Doble Lookup

Un usuario puede tener su email de cuenta (`user@clinica.com`) distinto de su email de Google (`user@gmail.com`). El login por OAuth debe buscar en ambos:

```python
# Siempre buscar en email primario PRIMERO, luego en google_email:
result = db.execute(text("SELECT ... FROM auth_get_user_by_email(:email)"), {"email": google_email}).first()
if not result:
    result = db.execute(text("SELECT ... FROM auth_get_user_by_google_email(:email)"), {"email": google_email}).first()
```

Requiere columna `google_email TEXT` en la tabla `users` con índice único `LOWER(google_email)`.

### 7. RLS y SECURITY DEFINER: El Patrón de Autenticación

Con RLS activo, las queries de login fallan porque no hay contexto de tenant todavía. Solución:

```sql
-- Toda función de auth debe ser SECURITY DEFINER para bypasear RLS:
CREATE OR REPLACE FUNCTION auth_get_user_by_email(p_email text)
RETURNS TABLE(id uuid, owner_id uuid, email text, hashed_password text, ...)
LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  RETURN QUERY SELECT id, owner_id, email, hashed_password, ...
  FROM users WHERE LOWER(email) = LOWER(p_email);
END; $$;
-- También crear: auth_get_user_by_google_email, auth_get_user_by_google_email
-- También: funciones para audit logs que se ejecutan sin contexto de tenant
```

### 8. JWT Multi-Tenant: El Contenido Mínimo del Token

```python
# Todo lo que el frontend necesita para operar sin queries extra:
token_data = {
    "sub": user.email,           # RFC estándar
    "tenant_id": str(owner_id),  # Para RLS y filtros multi-tenant
    "user_id": str(user.id),     # Para operaciones sobre el usuario
    "role": user.role,           # Para RBAC en frontend (qué ver) y backend (qué hacer)
    "full_name": user.full_name, # Evita GET /me en cada carga
    # Condicionales:
    "doctor_id": str(doctor.id), # Si el user es médico — para filtrar sus citas/pacientes
    "is_superuser": True,        # Solo si aplica
}
# Access token: 30min | Refresh token: 7 días con rotación
```

### 9. React Query en Apps Multi-Role: enabled Guards

```typescript
// SIEMPRE usar enabled cuando la query depende de datos del usuario:
const { data } = useQuery({
    queryKey: ['mis-datos', user?.doctorId],
    queryFn: () => api.get(`/api/datos?doctor_id=${user.doctorId}`),
    enabled: !!user?.doctorId,  // Sin esto: query dispara con undefined, key cambia, doble fetch
    staleTime: 30_000,          // Sin esto: cada mount hace background refetch
});

// Regla: si la queryKey contiene datos del usuario → enabled es obligatorio
```

### 10. Deploy a VM: Checklist Anti-Errores

```bash
# 1. Build con Vite (NUNCA tsc && vite build):
npx vite build

# 2. Limpiar assets viejos ANTES de subir (scp no borra):
ssh admin@servidor "rm -rf /var/www/app/dist/assets/"

# 3. Subir build:
scp -r dist/* admin@servidor:/var/www/app/dist/

# 4. Verificar que Nginx apunta a dist/ correcto

# 5. Si cambió el backend: pull + pip install + pm2 restart
```

### 11. SMTP Deliverability

```python
# Headers mínimos para no ir a spam:
from email.utils import formataddr
msg['From'] = formataddr(("Tu App", 'noreply@tudominio.com'))  # Display name obligatorio
msg['Reply-To'] = 'support@tudominio.com'
msg['Message-ID'] = f'<{uuid.uuid4()}@tudominio.com>'

# DNS requerido:
# SPF: v=spf1 include:_spf.tuproveedor.com ~all
# DKIM: configurar en tu proveedor de DNS + servidor de correo
# DMARC: v=DMARC1; p=none; rua=mailto:dmarc@tudominio.com
```

### 12. Nginx para SPA + API (El Config Que Funciona)

```nginx
server {
    listen 443 ssl;
    server_name tuapp.com;

    # Servir el SPA:
    root /var/www/app/dist;
    index index.html;

    # Todas las rutas del SPA → index.html (para React Router):
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy al backend FastAPI:
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;           # Crítico para CORS
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;  # Crítico para HTTPS callbacks
    }

    # Upload limit:
    client_max_body_size 10M;
}
```
