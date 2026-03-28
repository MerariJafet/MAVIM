# MAVIM SOP_02 — Architecture Phase (The LEGO Map)

**Versión:** 2.0.0
**Actualización:** 2026-03-14 — Integración GSD Planning Gate + UI/UX Pro Max standards
**Estado:** ACTIVO

---

## 1. Propósito

Establecer una base técnica robusta, escalable y mantenible antes de escribir una sola línea de código. Este SOP es el más importante de MAVIM: define la arquitectura que todos los demás SOPs darán por sentada.

> **Principio:** Una arquitectura bien definida hace que el código se escriba solo. Una arquitectura mal definida hace que todo el código sea deuda técnica desde el primer commit.

---

## 2. GSD Planning Gate (Obligatorio Pre-Arquitectura)

Antes de diseñar cualquier módulo, el agente DEBE responder estas 5 preguntas. Sin ellas, el trabajo de arquitectura no comienza.

```
1. PROBLEM   ¿Qué problema de negocio específico resuelve este sistema?
             (una sola frase, no lista de features)

2. EVIDENCE  ¿Dónde está el usuario o proceso que tiene ese problema hoy?
             (fuente concreta: ticket, conversación, pain point documentado)

3. SCOPE     ¿Qué está explícitamente FUERA del alcance de la v1?
             (listar 3–5 cosas que NO se harán para mantener el foco)

4. VALIDATION ¿Cómo sabrá el agente que la arquitectura es correcta?
              (criterio medible: "el smoke test pasa", "el diagrama no tiene ciclos")

5. CONFLICT  ¿Conflicta esto con algún módulo o SOP existente?
             (revisar SOPs 01–12 y módulos ya construidos)
```

**Output obligatorio:** `ARCHITECTURE_CONTRACT.md` con las 5 respuestas + los artefactos de la sección 3.

---

## 3. Reglas de Oro Arquitectónicas

### 3.1 Patrón Principal: Monolito Modular

Toda aplicación construida con MAVIM **DEBE** seguir el patrón de **Monolito Modular**.

```
app/
├── modules/
│   ├── auth/          ← Autónomo: sus datos, su lógica
│   ├── billing/       ← Autónomo: sus datos, su lógica
│   ├── inventory/     ← Autónomo: sus datos, su lógica
│   └── core/          ← Shared primitives únicamente
├── shared/
│   ├── events.py      ← Domain events bus
│   └── types.py       ← Shared type definitions
└── main.py
```

**Razón:** Los microservicios multiplican la complejidad operacional antes de que exista masa crítica de usuarios. El monolito modular da la misma separación de concerns sin el overhead de red.

### 3.2 Identificadores Universales

- **SIEMPRE** `UUID v4` como Primary Keys para entidades de dominio expuestas
- **NUNCA** IDs auto-incrementales numéricos — revelan volumen y orden de creación
- **NUNCA** IDs predecibles en URLs públicas

### 3.3 Comunicación Inter-módulo

Los módulos se comunican exclusivamente mediante:

| Tipo | Mecanismo | Cuándo |
|------|-----------|--------|
| Síncrono | Interfaces públicas explícitas (contratos) | Lectura de datos, queries |
| Asíncrono | Domain Events (emit/subscribe) | Efectos secundarios, notificaciones |

**PROHIBIDO:** JOINs directos entre tablas de módulos diferentes en la base de datos.

### 3.4 El Contrato de Entorno

```markdown
# ARCHITECTURE_CONTRACT.md (obligatorio)

## Puertos de red
- Frontend: 5173 (Vite dev) / 3000 (prod)
- Backend:  8000 (FastAPI / Express)
- DB:       5432 (PostgreSQL)
- Cache:    6379 (Redis)

## Variables de entorno críticas
- DATABASE_URL, SECRET_KEY, VITE_API_URL
- [lista completa sin valores]

## Prefijos de rutas
- API pública:  /api/v1/
- Auth:         /api/auth/
- Admin:        /api/admin/
- Webhooks:     /api/webhooks/
```

**Prohibición:** Cero valores hardcodeados (`localhost:8080`) en lógica de negocio. Todo desde `.env`.

---

## 4. Patrones de Datos por Dominio

### 4.1 Dinero — Ledger Pattern (obligatorio)

```sql
-- NUNCA: UPDATE accounts SET balance = balance - 100
-- SIEMPRE: append-only ledger
CREATE TABLE ledger_entries (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id  UUID NOT NULL REFERENCES accounts(id),
    amount      BIGINT NOT NULL,  -- centavos, nunca FLOAT
    direction   TEXT CHECK (direction IN ('debit', 'credit')),
    reference   UUID,             -- ID de la transacción origen
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
-- Balance = SUM de entries para el account
```

### 4.2 Multi-tenancy — Row Level Security

```sql
-- Cada tabla de dominio lleva tenant_id
ALTER TABLE patients ADD COLUMN clinic_id UUID NOT NULL;

-- RLS en PostgreSQL — nunca filtrar solo en la aplicación
CREATE POLICY tenant_isolation ON patients
    USING (clinic_id = current_setting('app.current_tenant')::UUID);
```

### 4.3 Geolocalización — H3 Indexing

```python
# NUNCA: lat/lng sin índice espacial
# SIEMPRE: H3 resolution 9 para operaciones de proximidad
import h3
h3_index = h3.geo_to_h3(lat, lng, resolution=9)
```

---

## 5. UI/UX Pro Max Standards (Frontend Architecture)

Todo proyecto con interfaz de usuario construido con MAVIM debe cumplir estos estándares antes de que el MAVIM-Critic lo apruebe.

### 5.1 Design Token System (obligatorio)

```css
/* index.css — tokens mínimos requeridos */
:root {
  --bg:        #ffffff;
  --surface:   #f8fafc;
  --surface-2: #f1f5f9;
  --border:    #e2e8f0;
  --text:      #0f172a;
  --muted:     #64748b;
  --primary:   #2563eb;
  --danger:    #dc2626;
  --success:   #16a34a;
  --warning:   #d97706;
  --ring:      rgba(37, 99, 235, 0.4);
  --r-sm:      6px;
  --r-md:      10px;
  --r-lg:      16px;
}

[data-theme="dark"] {
  --bg:        #0f172a;
  --surface:   #1e293b;
  --surface-2: #334155;
  --border:    #475569;
  --text:      #f8fafc;
  --muted:     #94a3b8;
}
```

**Regla absoluta:** Cero colores hardcodeados (`bg-white`, `text-gray-900`, `bg-slate-100`) en componentes. Todo vía CSS vars. Violación detectada por Playwright gate 10.

### 5.2 Component Hierarchy

```
Nivel 1 — Primitivos (atoms):
  Button [primary | secondary | ghost | destructive]
  Input, Label, Textarea, Select
  Badge [default | success | warning | danger | info | muted]

Nivel 2 — Composites (molecules):
  Card (surface + border + shadow)
  Dialog (Radix/Shadcn — siempre, nunca div custom)
  Toast / Alert

Nivel 3 — Patterns (organisms):
  PageHeader (title + subtitle + actions)
  EmptyState (icon + mensaje + CTA)
  DataTable (con Skeleton loading)
  FormDialog (Dialog + Form + validation)

Nivel 4 — Templates:
  AppShell (Sidebar + Topbar + content area)
  AuthLayout (card centrado + branding)
```

### 5.3 Skeleton-First Loading

```tsx
// NUNCA
{loading && <p>Cargando...</p>}

// SIEMPRE — Skeleton que replica el shape del contenido real
{loading && (
  <div className="grid grid-cols-3 gap-4">
    {Array.from({ length: 6 }).map((_, i) => (
      <Skeleton key={i} className="h-32 rounded-[var(--r-md)]" />
    ))}
  </div>
)}
```

### 5.4 Navigation Standards

- Máximo 5 items en sidebar principal
- El item activo siempre visualmente distinguible con `--primary`
- Breadcrumb para rutas anidadas > 2 niveles
- Back navigation siempre predecible (no `history.go(-1)` en flujos críticos)

### 5.5 Anti-FOUC Pattern

```tsx
// main.tsx — ANTES de ReactDOM.createRoot()
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

---

## 6. Patrones de Arquitectura por Tipo de Producto

| Tipo | Pattern | Referencia |
|------|---------|-----------|
| SaaS Multi-Tenant | Monolito Modular + RLS | [04_SAAS_MULTITENANT.md](../patterns/04_SAAS_MULTITENANT.md) |
| E-Commerce | Catálogo + Ledger + Inventario | [01_ECOMMERCE.md](../patterns/01_ECOMMERCE.md) |
| Marketplace | Ledger doble entrada + Escrow | [02_MARKETPLACE_ADVANCED.md](../patterns/02_MARKETPLACE_ADVANCED.md) |
| AI App | RAG aislado + Prompt injection prevention | [10_AI_APP_MODULAR.md](../patterns/10_AI_APP_MODULAR.md) |
| Logística | H3 + Surge Pricing + Batch Matching | [08_ONDEMAND_LOGISTICS.md](../patterns/08_ONDEMAND_LOGISTICS.md) |

---

## 7. Integración con el Flujo MAVIM

```
SOP_09 (Environment Scan)
    ↓ entorno verificado
SOP_01 (Intention)    ← INTENT_MANIFEST: problema + actores + DoD definidos
    ↓ intención clara
SOP_02 (Architecture) ← ESTÁS AQUÍ — requiere INTENT_MANIFEST como prerequisito
    ↓ ARCHITECTURE_CONTRACT.md + GSD Gate completado
SOP_07 (Refactoring)  → respeta los module boundaries de SOP_02
    ↓
SOP_08 (E2E Testing)  → valida la UI architecture (gates 02, 03, 10, 14)
```

> **Nota:** SOP_01 es obligatorio antes de SOP_02. No es posible arquitecturar sin conocer la intención.

---

## 8. Checklist de Cumplimiento

Antes de considerar la arquitectura "definida":

- [ ] GSD Planning Gate completado (5 preguntas respondidas)
- [ ] `ARCHITECTURE_CONTRACT.md` creado con puertos, vars y prefijos
- [ ] Estructura de módulos definida (sin JOINs cross-module)
- [ ] UUIDs v4 en todas las PKs de entidades expuestas
- [ ] Ledger pattern definido para cualquier módulo de dinero
- [ ] RLS configurado si hay multi-tenancy
- [ ] Design token system (`index.css`) creado con los 10 tokens mínimos
- [ ] `data-theme=dark` override definido para todos los tokens
- [ ] Componentes de Nivel 1 y 2 identificados (no reinventar primitivos)
- [ ] Anti-FOUC pattern incluido en `main.tsx`
- [ ] Pattern de Skeleton-first definido para todas las rutas asíncronas

---

## Referencias

- [SOP_01_INTENTION.md](SOP_01_INTENTION.md) — Define el INTENT_MANIFEST antes de arquitecturar
- [SOP_07_REFACTORING.md](SOP_07_REFACTORING.md) — Respeta boundaries al refactorizar
- [SOP_08_AUTOMATED_TESTING.md](SOP_08_AUTOMATED_TESTING.md) — Valida la UI architecture
- [SOP_09_ENVIRONMENT_AWARENESS.md](SOP_09_ENVIRONMENT_AWARENESS.md) — Pre-requisito del environment
- [patterns/COMMON_TRAPS.md](../patterns/COMMON_TRAPS.md) — Anti-patrones prohibidos
- [showcase/itsme-phase14-16/IMPACT_MAP.json](../showcase/itsme-phase14-16/IMPACT_MAP.json) — Ejemplo real de aplicación
