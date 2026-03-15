# SOP_08 — AUTOMATED TESTING WITH AI-DRIVEN SELF-IMPROVEMENT

**Versión:** 1.0.0
**Fecha:** 2026-03-14
**Autor:** MAVIM-ORCHESTRATOR (generado durante cirugía visual de It's Me)
**Estado:** ACTIVO — Integrado al MAVIM-CRITIC como gate final obligatorio

---

## 1. Propósito

Este SOP define el protocolo oficial de MAVIM para implementar, ejecutar y auto-mejorar suites de pruebas E2E automatizadas usando IA. Establece que **ninguna cirugía puede considerarse terminada** sin pasar el MAVIM-CRITIC E2E Gate.

El proceso documentado aquí emergió de la cirugía visual del proyecto It's Me (2026-03), donde un bucle de mejora continua con Playwright detectó y corrigió automáticamente un fallo real (colores hardcodeados en el componente `Badge`) que habría pasado desapercibido en revisión manual.

---

## 2. Principio Rector

> **"El test es el único árbitro. Si Playwright falla, la cirugía no está terminada."**

La IA puede generar código correcto, pero solo las pruebas con navegador real pueden verificar que el sistema integrado se comporta como se espera en las condiciones de producción.

---

## 3. Stack Obligatorio

| Componente | Tecnología | Razón |
|------------|-----------|-------|
| Test runner | Playwright | Navegador Chromium real, no jsdom |
| Modo | Headless | Reproducible en CI sin display server |
| Observabilidad | MAVIM UUID Reporter | Trazabilidad de fallos con correlation_id |
| CI integration | GitHub Actions job `e2e-smoke` | Gate automático antes de merge |
| Reporte | JSON + HTML + mavim-trace.json | Auditoría y correlación con backend logs |

---

## 4. Instalación (Cirugía Nueva)

```bash
# En el directorio frontend del proyecto
npm install --save-dev @playwright/test
npx playwright install chromium --with-deps

# Crear estructura
mkdir -p e2e/reporter
```

Archivos mínimos requeridos:
```
frontend/
├── playwright.config.ts          # Config con MAVIM reporter
├── e2e/
│   ├── reporter/
│   │   └── mavim-reporter.ts    # UUID trace reporter
│   ├── smoke.spec.ts            # Gates de shell y rutas
│   └── forms.spec.ts            # Gates de formularios y dark mode
```

---

## 5. Los 18 Gates Obligatorios del MAVIM-CRITIC

Todo proyecto con frontend React + Shadcn DEBE implementar estos gates. Son el mínimo para aprobar la cirugía:

### Suite A — Frontend Shell (gates 01-09)

| Gate | Descripción | Por qué es crítico |
|------|-------------|-------------------|
| 01 | React monta sin errores de consola | Base de toda la app |
| 02 | CSS vars Shadcn definidas (`--bg`, `--surface`, `--primary`, `--danger`) | El design system existe |
| 03 | `data-theme=dark` cambia `--bg` a oscuro | Dark mode funciona |
| 04 | Login: inputs + submit visibles | Flujo de entrada funcional |
| 05 | Card: `border-color` resuelto (no transparent) | Shadcn Card renderiza |
| 06 | Sin HTTP 5xx en JS chunks | Build íntegro |
| 07 | Anti-FOUC: tema antes de React | UX sin parpadeo |
| 08-09 | Rutas protegidas redirigen sin token | Auth guard activo |

### Suite B — Forms & Dark Mode (gates 10-18)

| Gate | Descripción | Qué detecta |
|------|-------------|------------|
| 10 | Login sin `bg-slate-*` en dark mode | Colores hardcodeados escapados |
| 11 | Error de login usa `--danger` | CSS var en estados de error |
| 12 | Dialog paciente: ≥3 Shadcn inputs | Formularios migrados |
| 13 | Dialog doctor: sin errores consola | Integración form completa |
| 14 | Dialogs sin hardcoded en dark mode | Dark mode global en modals |
| 15-16 | Páginas usan Skeleton (no texto) | Loading states modernos |
| 17 | Topbar tiene toggle dark mode | Feature visible y funcional |
| 18 | `/app/clinics` CSS vars + Skeleton | Page completa migrada |

---

## 6. MAVIM UUID Reporter — Trazabilidad Avanzada

### Problema que resuelve

Cuando un test E2E falla, el desarrollador necesita:
1. Saber exactamente qué falló y dónde
2. Correlacionar el fallo con los logs del backend
3. Tener un ID único para buscar en los logs estructurados

### Arquitectura del UUID Reporter

```typescript
// Cada test recibe dos UUIDs:
{
  "test_id": "uuid-del-test-específico",        // ID de esta ejecución del test
  "correlation_id": "uuid-para-backend-logs",   // Buscar en logs con X-Correlation-Id
  "suite": "MAVIM-CRITIC — Login Form",
  "title": "10 · Login form usa CSS vars",
  "status": "failed",
  "error": {
    "message": "Colores hardcodeados...",
    "location": "e2e/forms.spec.ts:59"
  }
}
```

### Archivo de salida: `playwright-report/mavim-trace.json`

```json
{
  "run_id": "uuid-del-run-completo",
  "started_at": "2026-03-14T10:00:00Z",
  "total": 18,
  "passed": 17,
  "failed": 1,
  "failure_summary": "[a1b2c3d4] MAVIM-CRITIC — Login Form › Gate 10: bg-slate-100 found",
  "tests": [...]
}
```

### Correlación con backend

El header `X-MAVIM-Test: playwright` se inyecta en todas las requests durante las pruebas. El backend puede filtrar logs con:

```bash
# Ver solo requests de pruebas Playwright
docker logs it-me-backend | jq 'select(.headers["x-mavim-test"] == "playwright")'

# Buscar por correlation_id de un fallo específico
docker logs it-me-backend | jq 'select(.correlation_id == "a1b2c3d4-...")'
```

---

## 7. Bucle de Auto-Mejora con IA

Este es el proceso que generó este SOP. Documentar para reproducirlo en cualquier proyecto:

```
┌─────────────────────────────────────────────────────────┐
│                MAVIM AUTO-IMPROVEMENT LOOP               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. ORCHESTRATOR escribe código (cirugía)                │
│       ↓                                                  │
│  2. Playwright corre 18 gates en Chromium real           │
│       ↓                                                  │
│  3. ¿Algún gate falla?                                   │
│       ├─ NO  → MAVIM-CRITIC aprueba → push               │
│       └─ SÍ  → mavim-trace.json captura UUID + error     │
│                    ↓                                     │
│  4. ORCHESTRATOR lee el failure_summary                  │
│       ↓                                                  │
│  5. Identifica la causa raíz en el código                │
│       ↓                                                  │
│  6. Aplica fix quirúrgico (SOP_07)                       │
│       ↓                                                  │
│  7. Vuelve al paso 2                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Ejemplo real (It's Me, 2026-03-14)

**Iteración 1:** Gate 10 falla
```
Error: div[inline-flex items-center rounded-full...] has "bg-slate-100"
correlation_id: a1b2c3d4-...
```

**Análisis ORCHESTRATOR:** El error apunta al componente `Badge`. La variante `muted` tenía `bg-slate-100` hardcodeado.

**Fix aplicado:**
```typescript
// ANTES
muted: "border-transparent bg-slate-100 text-slate-700"

// DESPUÉS
muted: "border-transparent bg-[var(--surface-2)] text-[var(--muted)]"
```

**Iteración 2:** 18/18 gates pasan → cirugía aprobada.

**Tiempo total del bucle:** < 2 minutos.

---

## 8. Integración CI/CD

```yaml
# .github/workflows/ci.yml
e2e-smoke:
  name: MAVIM-CRITIC — Frontend E2E Smoke
  runs-on: ubuntu-latest
  needs: frontend-build
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: "20" }
    - run: npm ci
      working-directory: frontend
    - run: npx playwright install chromium --with-deps
      working-directory: frontend
    - run: npm run dev &
      working-directory: frontend
      env: { VITE_API_URL: http://localhost:8000 }
    - name: Wait for Vite
      run: for i in $(seq 1 20); do curl -sf http://localhost:5173/ && break || sleep 1; done
    - name: Run E2E gates
      run: npx playwright test --reporter=list
      working-directory: frontend
    - name: Upload MAVIM trace on failure
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: mavim-trace
        path: frontend/playwright-report/
```

---

## 9. Checklist de Cumplimiento

Antes de declarar una cirugía visual terminada, verificar:

- [ ] `npm run test:smoke` pasa **18/18** gates
- [ ] `playwright-report/mavim-trace.json` existe y tiene `"failed": 0`
- [ ] No hay `bg-white`, `bg-slate-*`, `bg-gray-*` en componentes renderizados (gate 10 + 14)
- [ ] Todos los formularios usan Shadcn `<Input>`, `<Label>`, `<Button>`, `<Dialog>`
- [ ] Dark mode verificado con `data-theme=dark` en Chromium real
- [ ] Anti-FOUC: `data-theme` aplicado antes de `ReactDOM.createRoot()`
- [ ] Estados de carga usan `<Skeleton>` (no texto "Cargando...")
- [ ] Badge y variantes de color usan CSS vars (no clases hardcodeadas)
- [ ] CI job `e2e-smoke` verde en la rama

---

## 10. Expansión futura

Para proyectos con backend activo en pruebas, añadir:

```typescript
// e2e/api-contracts.spec.ts
test('backend health retorna 200', async ({ request }) => {
    const res = await request.get('http://localhost:8000/health');
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.status).toBe('ok');
});

test('auth rechaza credenciales inválidas con 401', async ({ request }) => {
    const res = await request.post('http://localhost:8000/api/auth/login', {
        form: { username: 'x@x.com', password: 'wrong' }
    });
    expect(res.status()).toBe(401);
});
```

Esto unifica el smoke backend (antes en bash) con el E2E de Playwright, centralizando toda la trazabilidad en `mavim-trace.json`.

---

## Referencias

- SOP_07_REFACTORING.md — Metodología de cirugía quirúrgica (prerequisito)
- IMPACT_MAP.json — Formato del mapa de impacto inicial
- MAVIM.md — Modo Quirúrgico y jerarquía de SOPs
- Caso de estudio: `itsme/docs/TECHNICAL.md` sección "Playwright E2E"
