# Caso de Éxito: It's Me — De Prototipo a SaaS en Producción
## MAVIM-ORCHESTRATOR Case Study | Sprints S9 → V3.1 | 2026-03-24

> **Este es el case study de la fase más difícil: llevar un SaaS de "funciona en local" a "funciona en producción con clientes reales".**
> Cada sección documenta un problema real, su causa raíz, y el protocolo derivado.

---

## El Contexto

**Stack:** FastAPI + PostgreSQL (RLS) + React 18 + TypeScript + Vite + Nginx + PM2
**Infraestructura:** Google Cloud VM (35.225.44.140), dominio itsme.com.mx, HTTPS via Let's Encrypt
**Modelo:** SaaS B2B multi-tenant para clínicas médicas. Un Owner = una clínica = un tenant.
**Autenticación:** JWT (access 30min + refresh 7d) + Google OAuth 2.0
**Pagos:** Stripe Checkout + webhooks
**Email:** SMTP relay con headers RFC-compliant para deliverability
**IA:** Ollama local para agente de lenguaje natural

---

## PROBLEMA #1 — El Bundle de Producción Apuntaba a localhost

### Síntoma
Usuarios en producción no podían iniciar sesión. La app cargaba visualmente pero todas las llamadas API fallaban con `net::ERR_CONNECTION_REFUSED`.

### Causa Raíz
Vite embebe las variables de entorno en el bundle **en tiempo de compilación**, no en tiempo de ejecución. El archivo `.env` contenía:

```
VITE_API_URL=http://localhost:8000
```

Y el código usaba `||` en lugar de `??`:
```typescript
// ANTES (MAL):
apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000'
// Si VITE_API_URL='', el || hace fallback a localhost también en prod

// DESPUÉS (BIEN):
apiUrl: import.meta.env.VITE_API_URL ?? ''
// '' vacío = rutas relativas → Nginx hace el proxy correctamente
```

### Fix Completo
1. Crear `frontend/.env.production` con `VITE_API_URL=` (vacío — usa rutas relativas)
2. Cambiar **todos** los `||` por `??` donde se use `VITE_API_URL`
3. En producción, Nginx maneja `/api/*` → `http://localhost:8000`

### Protocolo Derivado
```
ANTES de hacer build de producción:
□ Verificar que .env.production existe y VITE_API_URL está vacío
□ Grep por `|| 'http://localhost'` en todo el frontend
□ Nunca usar || para valores de env que pueden ser string vacío
□ Recordar: Vite builds son inmutables — las vars quedan baked in
```

---

## PROBLEMA #2 — DNS y Nginx: La Configuración del "Último Metro"

### El Mapa Completo de Solicitudes en Producción

```
Usuario → DNS → Nginx (puerto 80/443) → PM2/FastAPI (8000) → PostgreSQL
                         ↓
                    /api/* → proxy_pass http://127.0.0.1:8000
                    /* → serve /var/www/itsme/dist (Vite build)
```

### Errores Comunes en Esta Capa

**Error 1: CORS en producción pero no en local**
- Causa: Nginx no enviaba el header `Host` correcto al backend
- Fix: `proxy_set_header Host $host;` en nginx.conf
- El backend usa el header `Origin` para validar CORS → si Nginx lo transforma, falla

**Error 2: HTTPS mixed content**
- Causa: Backend generaba URLs con `http://` hardcodeado
- Fix: Todas las URLs callback de OAuth deben usar la variable de entorno, nunca hardcoded

**Error 3: 413 Request Entity Too Large**
- Causa: Nginx rechaza uploads > 1MB por defecto
- Fix: `client_max_body_size 10M;` en nginx.conf

**Error 4: Archivos viejos del bundle no se eliminan con scp**
- Causa: `scp` copia archivos pero no borra los obsoletos
- `dist/assets/index-abc123.js` y `dist/assets/index-def456.js` coexisten
- El `index.html` apunta al nuevo pero el navegador puede cachear el viejo
- Fix: `ssh admin@servidor "rm -rf /var/www/itsme/dist/assets/*"` ANTES de scp

### Checklist de Deploy (Obligatorio)
```bash
# 1. Build local
cd frontend && npx vite build   # NUNCA tsc && vite build (rompe por errores TS menores)

# 2. Limpiar assets viejos en servidor
ssh -i ~/.ssh/google_compute_engine admin_itsme_com_mx@35.225.44.140 \
  "rm -rf /var/www/itsme/dist/assets/"

# 3. Subir
scp -i ~/.ssh/google_compute_engine -r frontend/dist/* \
  admin_itsme_com_mx@35.225.44.140:/var/www/itsme/dist/

# 4. Reiniciar backend si cambió
ssh ... "cd /opt/itsme && git pull && source .venv/bin/activate && \
  pip install -r requirements.txt && pm2 restart itsme-backend"

# 5. Verificar
curl https://itsme.com.mx/api/health
```

---

## PROBLEMA #3 — Google OAuth: El Hoyo de Seguridad que Creó Tenants Fantasma

### Síntoma
Una médico intentó "Continuar con Google" con su email de Gmail. El sistema detectó que no tenía cuenta... y en lugar de rechazarla, **le creó una cuenta nueva de Owner** sin pasar por Stripe. Tenía acceso completo gratis.

### Causa Raíz
El endpoint de OAuth tenía lógica de onboarding embebida:
```python
# ANTES (PELIGROSO):
if not result:
    # Usuario no existe → crear Owner + User + OnboardingState
    new_owner = Owner(name=name, email=email)
    db.add(new_owner)
    ...
    return token  # Token sin pago, sin subscription
```

### El Fix
```python
# DESPUÉS (CORRECTO):
if not result:
    raise HTTPException(status_code=404, detail="no_account")
# El frontend muestra: "Este correo no tiene una cuenta en It's Me.
# Regístrate en itsme.com.mx/register"
```

### Por Qué el Modelo SaaS Requiere Esto
En un SaaS con paywall:
1. El registro **siempre** pasa por el flujo de pago
2. OAuth es solo un método de **autenticación**, no de **registro**
3. Si alguien llega por OAuth sin cuenta → redirect a registro con su email pre-llenado
4. NUNCA crear entidades de negocio (Owner, Tenant, Subscription) desde OAuth

### Daño a Limpiar
```sql
-- Detectar owners creados sin subscription:
SELECT o.id, o.email, o.created_at
FROM owners o
LEFT JOIN subscriptions s ON s.owner_id = o.id
WHERE s.id IS NULL
ORDER BY o.created_at DESC;

-- Eliminar con cuidado (verificar que no tienen datos reales):
DELETE FROM onboarding_state WHERE owner_id = 'uuid';
DELETE FROM users WHERE owner_id = 'uuid';
DELETE FROM owners WHERE id = 'uuid';
```

---

## PROBLEMA #4 — Google OAuth y Multi-Email: El Caso del Médico

### Síntoma
Un médico con cuenta `dr.garcia@clinica.com` intentó "Continuar con Google" con `dr.garcia@gmail.com`. Sistema devolvía "este correo no tiene cuenta" aunque era el mismo doctor.

### El Modelo Mental Correcto

```
Un usuario en el sistema tiene:
  email (primario — el que usó para registrarse)
  google_email (opcional — su cuenta de Google para OAuth)

El login por OAuth debe buscar EN AMBOS:
  1. users WHERE email = google_email
  2. users WHERE google_email = google_email
```

### La Solución Arquitectónica

```sql
-- Agregar columna:
ALTER TABLE users ADD COLUMN google_email TEXT;
CREATE UNIQUE INDEX users_google_email_idx
  ON users (LOWER(google_email)) WHERE google_email IS NOT NULL;

-- Función SECURITY DEFINER para bypasear RLS:
CREATE OR REPLACE FUNCTION auth_get_user_by_google_email(p_google_email text)
RETURNS TABLE(...) LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  RETURN QUERY SELECT ... FROM users u
  WHERE LOWER(u.google_email) = LOWER(p_google_email);
END; $$;
```

```python
# En el login OAuth:
result = db.execute(text("SELECT ... FROM auth_get_user_by_email(:email)"), {"email": email}).first()
if not result:
    result = db.execute(text("SELECT ... FROM auth_get_user_by_google_email(:email)"), {"email": email}).first()
if not result:
    raise HTTPException(status_code=404, detail="no_account")
```

### El Flujo de Vinculación (Para Usuarios Existentes)
```
Usuario con cuenta email/password quiere añadir Google OAuth:
1. Va a Perfil → "Vincular cuenta de Google"
2. Backend genera URL OAuth con state="link_google"
3. Usuario authoriza en Google
4. Callback detecta state="link_google" → llama POST /api/auth/google/link
5. Backend verifica que ese google_email no esté vinculado a otro usuario
6. Guarda google_email en users.google_email
7. Próximo login con Google → funciona
```

---

## PROBLEMA #5 — RLS (Row-Level Security) en PostgreSQL

### Por Qué RLS en Multi-Tenant

Sin RLS, un bug en el código (olvidar `WHERE owner_id = ?`) puede filtrar datos de TODOS los tenants. Con RLS, PostgreSQL rechaza la query a nivel de base de datos aunque el código la envíe.

### El Patrón SECURITY DEFINER

El problema: las funciones de autenticación necesitan buscar usuarios SIN contexto de tenant (porque el tenant se establece DESPUÉS del login).

```sql
-- INCORRECTO: query normal falla con RLS si no hay contexto de tenant
SELECT * FROM users WHERE email = 'x@x.com';  -- RECHAZADO

-- CORRECTO: función SECURITY DEFINER omite RLS
CREATE OR REPLACE FUNCTION auth_get_user_by_email(p_email text)
RETURNS TABLE(id uuid, owner_id uuid, ...)
LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  RETURN QUERY SELECT id, owner_id, ... FROM users
  WHERE LOWER(email) = LOWER(p_email);
END; $$;
```

### Trampas de RLS

1. **Las migraciones también están sujetas a RLS** si no usas `SECURITY DEFINER` o un rol de admin
2. **Los audit logs** se escriben desde contexto de usuario → necesitan su propia función SECURITY DEFINER
3. **Los webhooks de Stripe** llegan sin contexto de tenant → siempre usar SECURITY DEFINER o deshabilitar RLS para el rol de servicio
4. **Los tests de integración** necesitan un rol `test_admin` con `BYPASS RLS` privilege

---

## PROBLEMA #6 — SMTP y Deliverability: Por Qué Los Emails Llegan al Spam

### El Stack de Deliverability

Para que los emails lleguen a la bandeja de entrada (no spam):

```
1. SPF record en DNS:
   v=spf1 include:_spf.google.com ~all
   (o el servidor SMTP que uses)

2. DKIM: firma criptográfica del servidor de correo
   → Configura en tu proveedor DNS como TXT record

3. DMARC:
   v=DMARC1; p=none; rua=mailto:dmarc@tudominio.com

4. Headers RFC-compliant en el código:
   From: "It's Me <noreply@itsme.com.mx>"  ← Display name obligatorio
   Reply-To: support@itsme.com.mx
   List-Unsubscribe: <mailto:...>
   Message-ID: <uuid@itsme.com.mx>
```

### El Bug de los Headers

```python
# ANTES (causa spam + errores en iCloud/Outlook):
msg['From'] = 'noreply@itsme.com.mx'

# DESPUÉS (RFC 5322 compliant):
from email.utils import formataddr
msg['From'] = formataddr(("It's Me", 'noreply@itsme.com.mx'))
msg['Message-ID'] = f"<{uuid.uuid4()}@itsme.com.mx>"
```

### Por Qué No Usar Gmail SMTP en Producción

- Límite: 500 emails/día (cuenta gratuita) o 2000/día (Workspace)
- La IP de tu servidor puede quedar en listas negras si envías bulk
- **Alternativas recomendadas:** SendGrid (free tier: 100/día), Resend, Amazon SES, Mailgun
- Para volumen < 1000/mes: Gmail Workspace está bien

### El Bug del Audit Log en Emails

```python
# PELIGROSO: write_audit_log dentro de _send_branded_email
# Si el tenant_id no existe en el momento del envío → FK violation → crash del email
def _send_branded_email(to, subject, body, tenant_id=None):
    # ... enviar email ...
    if tenant_id:
        write_audit_log(...)  # ← ELIMINAR DE AQUÍ
# El audit del envío se hace FUERA, en el caller, con contexto correcto
```

---

## PROBLEMA #7 — JWT en Multi-Tenant: Lo Que Debe Ir en el Token

### El Token Mínimo Correcto

```python
token_data = {
    "sub": user.email,          # Identificador estándar JWT
    "tenant_id": str(owner_id), # CRÍTICO para RLS
    "user_id": str(user.id),    # Para operaciones sobre el usuario
    "role": user.role,          # Para RBAC en frontend y backend
    "full_name": user.full_name, # Evita query extra en cada request
}
# Opcionales según rol:
if user.doctor_id:
    token_data["doctor_id"] = str(user.doctor_id)
if user.is_superuser:
    token_data["is_superuser"] = True
```

### Por Qué `doctor_id` en el Token

Los doctores son usuarios con un `doctor_id` que apunta a la tabla `doctors`. Sin esto en el token:
- Cada request del doctor haría un JOIN para encontrar su doctor_id
- Las queries filtradas por doctor (`?doctor_id=xxx`) no pueden auto-popularse
- El dashboard del doctor no sabe qué citas/pacientes son "suyos"

### Tokens de Acceso vs Refresh

```
Access Token: 30 minutos
  → Viaja en cada request como Bearer header
  → Si expira → frontend usa refresh token silenciosamente
  → Contiene todo el contexto necesario (no hace queries extra)

Refresh Token: 7 días
  → Se guarda en localStorage (o httpOnly cookie)
  → Endpoint: POST /api/auth/refresh
  → Rota el par completo (nuevo access + nuevo refresh)
  → Si refresh expira → logout forzado
```

---

## PROBLEMA #8 — React Query y Race Conditions en Multi-Role

### El Problema del Doctor Dashboard

```typescript
// ANTES (BUGGY): Fires con doctorId=undefined → query key cambia → doble fetch
const { data: patients = [] } = useQuery({
    queryKey: ['doctor-patients', doctorId],  // doctorId es undefined al inicio
    queryFn: () => api.get('/api/patients'),   // Dispara inmediatamente
});

// DESPUÉS (CORRECTO):
const { data: patients = [] } = useQuery({
    queryKey: ['doctor-patients', doctorId],
    queryFn: () => api.get('/api/patients'),
    enabled: !!doctorId,      // No dispara hasta tener doctorId
    staleTime: 30_000,        // No refetch en 30s si datos frescos
});
```

### La Jerarquía de Auth Guards

```
ProtectedRoute
  → Espera !isLoading (AuthContext hydration)
  → Espera onboardingChecked (GET /api/onboarding/state)
    → BillingGate
        → Espera billing check (GET /api/billing/status)
          → Tu componente (aquí auth YA está lista)
```

Aunque la jerarquía parece resolver el problema, **React Query puede pre-fetch** con la queryKey incorrecta si no hay `enabled`. Siempre usar:

```typescript
// En cualquier query que dependa de datos del usuario:
enabled: !!user,           // Nivel básico
enabled: !!user?.doctorId, // Si depende del doctorId específico
```

### staleTime es No-Negociable en SaaS

```typescript
// Sin staleTime: cada vez que el componente se monta → background refetch
// Con staleTime: si los datos tienen < 30s → usa cache sin refetch

// Recomendaciones por tipo de dato:
staleTime: 30_000,         // Listas de pacientes, citas del día
staleTime: 60_000 * 5,     // Catálogos (médicos, clínicas, servicios)
staleTime: 60_000 * 30,    // Info del owner, perfil del usuario
staleTime: Infinity,       // Configuración estática del tenant
```

---

## PROBLEMA #9 — Sincronización entre Módulos: Calendar y Settings

### El Síntoma

La página de Agenda mostraba Google Calendar como "Conectado". La página de Configuración mostraba el mismo calendar como "Sin conectar". Botón de conectar en Configuración no funcionaba.

### La Causa

`CalendarSyncPanel.tsx` usaba endpoints que **no existían**:
```typescript
// ANTES (endpoints inventados):
api.get('/api/calendar/sync-status')     // 404 Not Found
api.post('/api/calendar/connect')         // 404 Not Found
api.post('/api/calendar/disconnect')      // 404 Not Found

// DESPUÉS (endpoints reales del backend):
api.get('/api/integrations/google/status')        // ✓ Existe
api.get('/api/integrations/google/auth-url?mode=owner')  // ✓ Existe
```

### La Regla

> Cualquier componente reutilizable que llame a la API **debe tener un test o al menos una verificación manual de que los endpoints existen**. Los endpoints se documentan en el backend y el frontend los consume — no al revés.

---

## PROBLEMA #10 — Content Security Policy (CSP) y Google OAuth

### El Error

```
Refused to load https://accounts.google.com/o/oauth2/v2/auth because it violates CSP directive
```

### Por Qué Ocurre

Nginx (o el servidor) puede tener headers CSP configurados que bloquean redirects a dominios externos.

### La Solución

La URL de OAuth es un **redirect de navegador** (`window.location.href = url`), no una llamada fetch. No está sujeta a CSP de `connect-src`. Si aparece este error es porque:
1. El backend devuelve la URL correcta pero el frontend hace `fetch(url)` en vez de `window.location.href = url`
2. O Nginx tiene `frame-ancestors` muy restrictivo

```typescript
// CORRECTO — redirect del navegador, no fetch:
const data = await api.get('/api/integrations/google/auth-url?mode=owner');
window.location.href = data.url;  // ← Navegador hace el redirect, no CSP-blocked
```

---

## Métricas Reales del Proyecto

| Métrica | Valor |
|---------|-------|
| Sprints completados | S1 → V3.1 (15+ sprints) |
| Bugs de producción críticos resueltos | 10 (documentados arriba) |
| Archivos de código frontend | ~60 |
| Archivos de código backend | ~30 |
| Endpoints API | ~80 |
| Módulos del sistema | Pacientes, Médicos, Citas, Clínicas, Facturación, IA, Agenda, Integraciones, Auditoría |
| Líneas de código total | ~15,000 |
| Tenants en producción | Activos con clientes reales |

---

## Los 10 Mandamientos del SaaS Multi-Tenant en Producción

1. **Vite no es runtime.** Las env vars se embeben en build time. `.env.production` es obligatorio.
2. **OAuth es autenticación, no registro.** Nunca crear entidades de negocio desde un callback de OAuth.
3. **Cada usuario tiene email primario + email de OAuth.** Buscar en ambos columnas.
4. **RLS es la última línea de defensa.** Funciones SECURITY DEFINER para auth y servicios del sistema.
5. **El JWT lleva todo el contexto del usuario.** `tenant_id`, `role`, `doctor_id` — evita queries extra por request.
6. **React Query necesita `enabled` guards.** Sin ellos, las queries disparan con datos incompletos.
7. **`scp` no borra.** Limpiar assets viejos antes de subir el nuevo build.
8. **SMTP necesita SPF + DKIM + headers RFC.** Sin esto, los emails van a spam.
9. **Los endpoints del backend son la fuente de verdad.** El frontend no inventa URLs.
10. **Documentar cada problema de producción.** El próximo desarrollador (o agente IA) lo necesita.

---

*Documentado por MAVIM-ORCHESTRATOR — 2026-03-24*
*Proyecto: github.com/MerariJafet/itsme*
*Metodología: github.com/MerariJafet/MAVIM*
