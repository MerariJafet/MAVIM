# CHANGELOG — It's Me × MAVIM
## Evolución Automatizada: Fase 14 → Fase 16

> Generado por MAVIM-ORCHESTRATOR | 2026-03-14
> Fuente: `git log` + análisis de impacto MAVIM-CRITIC

---

## [v2.0.0] — 2026-03-14 — MAVIM 2.0 Integration

### Resumen
La mayor actualización desde el lanzamiento. Transición de un frontend con deuda técnica crítica a un sistema profesional con auto-validación, trazabilidad UUID y metodología documentada.

---

### ✨ Features Nuevas

#### Sistema de Auto-Diagnóstico
- **`/api/diagnostics/frontend-error`** — Endpoint para recepción de errores de React con `correlation_id` UUID
- **`/api/diagnostics/errors`** — Query de errores para consumo del agente IA
- **`/api/diagnostics/snapshot`** — Health snapshot completo: DB, env vars, proceso, warnings
- **`/api/diagnostics/health`** — Health check rápido para Playwright y CI

#### ErrorBoundary con Trazabilidad
- Auto-reporta errores de React al backend sin intervención humana
- Captura `unhandledrejection` (promesas no capturadas) vía `window.addEventListener`
- Muestra `correlation_id` en UI para debugging
- Diseño actualizado a CSS vars (dark mode compatible)

#### MAVIM Infrastructure Scripts
- **`scripts/mavim_scan.sh`** — SOP_09: Environment snapshot en < 60s (GREEN/YELLOW/RED)
- **`scripts/write_bridge.py`** — SOP_10: Cognitive Bridge entre sesiones IA
- **`scripts/health_check.sh`** — SOP_11: Dashboard visual CODE/TESTS/API/UX

#### Playwright E2E — 18 Gates MAVIM-CRITIC
- `e2e/smoke.spec.ts` — Gates 01–09: shell, CSS vars, dark mode, rutas protegidas
- `e2e/forms.spec.ts` — Gates 10–18: forms, dialogs, dark mode, skeletons
- `e2e/reporter/mavim-reporter.ts` — UUID trace reporter con `correlation_id` por test
- CI/CD: job `e2e-smoke` como gate final antes de merge

#### COGNITIVE_BRIDGE.json + ENVIRONMENT_SNAPSHOT.json
- Artefactos vivos en la raíz del proyecto
- Actualizados automáticamente al final de cada sesión
- Portabilidad total entre Claude, GPT-4o, Gemini, agentes locales

---

### 🎨 Visual Migration (Design System)

#### CSS Variables Design System
Todos los colores hardcodeados reemplazados con tokens del design system:

| Token | Uso |
|-------|-----|
| `--bg` | Fondo base de la aplicación |
| `--surface` | Cards, modales, paneles |
| `--surface-2` | Inputs, hover states, código |
| `--border` | Todos los bordes |
| `--text` | Texto principal |
| `--muted` | Texto secundario, placeholders |
| `--primary` | CTA, links, acciones principales |
| `--danger` | Errores, eliminaciones, alertas críticas |

#### Páginas Migradas (18 total)
- `Services.tsx` — PageHeader, Card, Skeleton, CSS vars
- `Consultorios.tsx` — PageHeader, Skeleton grid, CSS vars
- `Clinics.tsx` — PageHeader, EmptyState, Skeleton, CSS vars
- `Notifications.tsx` — Skeleton rows, CSS vars en badges de tipo
- `Settings.tsx` — CSS vars en todas las cards de configuración
- `PatientDashboard.tsx` — CSS vars completo
- `PatientLogin.tsx` — Shadcn Input/Label/Button
- `RegisterOwner.tsx` — Shadcn Input/Label/Button
- `Login.tsx` — Error state con `--danger` CSS var
- `dashboard/Payments.tsx` — CSS vars, sin emerald/blue hardcoded
- + 8 páginas adicionales (Calendar, Welcome, OAuthCallback...)

#### Componentes Migrados
- **`badge.tsx`** — 5 variantes con CSS vars (fix crítico detectado por Playwright)
- **`DoctorFormDialog.tsx`** — Rewrite completo con Shadcn Dialog/Input/Label
- **`ServiceFormDialog.tsx`** — Rewrite completo
- **`ConsultorioFormDialog.tsx`** — Rewrite completo
- **`AppointmentFormDialog.tsx`** — Batch replacement (700+ líneas)
- **`ClinicSelector.tsx`** — Skeleton en loading state

#### Skeleton Loading States
Reemplazado en 6 páginas: Services, Consultorios, Clinics, Doctors, Notifications, ClinicSelector

---

### 🐛 Bug Fixes

- **`badge.tsx` variante `muted`** — `bg-slate-100` hardcodeado → `bg-[var(--surface-2)]`
  - *Detectado por:* Playwright gate 10 (auto-mejora — sin intervención humana)
  - *Impacto:* Dark mode roto en todos los badges de tipo `muted`

- **`AgentActivity.tsx`** — Badge variant `"outline"` inválido → `"muted"`
  - *Error:* TypeScript TS2322 — variant no existía en el tipo
  - *Fix:* Variant correcto + CSS var para color

- **`Login.tsx`** — Error div con `bg-rose-50 border-rose-200 text-rose-600`
  - *Fix:* `bg-[var(--danger)]/10 border-[var(--danger)]/20 text-[var(--danger)]`

- **`playwright.config.ts`** — `extraHTTPHeaders: { 'X-MAVIM-Test': 'playwright' }` global
  - *Causa del bug:* Custom header enviado a Google Fonts CDN → CORS preflight rechazado
  - *Fix:* Eliminado header global; inyectar solo per-request en API tests
  - *Impacto corregido:* Gates 01, 04, 06 fallaban por falsos positivos de CORS

- **Git credential helper** — Ruta inválida (`/VMarx Dione DB/gh` no encontrado)
  - *Fix:* `gh auth setup-git` reconfigura al gh de `/usr/bin/gh`

---

### 🏗️ Backend

- Structured JSON logging con `ContextVar` para `correlation_id`
- `X-Correlation-Id` response header en todas las respuestas
- Nuevo router `diagnostics.py` — sin modificar routers existentes (additive only)
- Logs filtrados en `/api/diagnostics/errors` para consumo del agente

---

### 📦 Dependencies

```json
// Agregadas (devDependencies)
"@playwright/test": "^1.58.2"
```

```bash
# Browsers instalados
chromium (Playwright)
```

---

### 🔄 CI/CD

```yaml
# Nuevo job en .github/workflows/ci.yml
e2e-smoke:
  name: MAVIM-CRITIC — Frontend E2E Smoke
  # Gate final antes de merge a main
  # Bloquea si cualquiera de los 18 gates falla
```

---

## [v1.13.0] — 2026-03-13 — Patient Profile & Enhanced Appointments

### Features
- Patient Profile Overlay — vista detallada sin navegación
- Enhanced appointment flow con persistencia de datos
- Row action buttons en tablas de pacientes y citas
- Button contrast improvements (accesibilidad)

---

## [v1.12.0] — 2026-03-10 — Premium Frontend Complete

### Features
- App Shell completo: Sidebar + Topbar + navegación
- Dashboard KPIs con datos reales del backend
- Quick Actions conectadas a form dialogs reales
- Patients y Calendar modules con UI premium
- Empty states premium para Settings

---

## [v1.11.0] — 2026-02-15 — Sprint 6.2: Integrations

### Features
- Email SMTP con Gmail support + MessageLog
- Telegram bot con control de acceso y user linking
- Environment validation + demo fast mode para reminders

---

## [v1.10.0] — 2026-02-10 — Sprint 6.1: Security Hardening

### Features
- Argon2 password hashing (reemplaza bcrypt)
- SECURITY DEFINER para audit logging con RLS
- JWT con expiración configurable

---

## Notas del ORCHESTRATOR

### Sobre el proceso de migración

La migración visual de 47 archivos fue el mayor riesgo de esta fase. La estrategia fue:

1. **Primero el design system** — definir todos los tokens CSS antes de tocar componentes
2. **Componentes antes que páginas** — migrar Badge, Button, Input primero para que las páginas hereden
3. **Archivos grandes con scripts** — `AppointmentFormDialog.tsx` (700+ líneas) fue procesado con Python batch replacement para garantizar cobertura total
4. **Validar después de cada grupo** — no esperar al final para descubrir regresiones

### Sobre la detección automática del Badge bug

El bug del Badge es el ejemplo más poderoso del valor de MAVIM. El componente había pasado:
- Revisión manual durante la migración ✗ (no detectado)
- Revisión de TypeScript (tsc) ✗ (válido sintácticamente)
- Revisión visual en light mode ✗ (se veía bien)

Solo Playwright con `data-theme=dark` activado explícitamente + scan de clases hardcodeadas lo encontró. Esto es lo que significa "validación real" en MAVIM.

---

*CHANGELOG generado por MAVIM-ORCHESTRATOR*
*Para reportar un cambio no documentado: abrir issue en github.com/MerariJafet/MAVIM*
