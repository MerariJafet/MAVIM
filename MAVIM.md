# MAVIM Cheat Sheet (Agent Instruction Layer)
Lee esto para activarte instantáneamente:
1. **Roles:** Architect diseña bloques LEGO. Developer escribe código modular. Critic audita con Checklists.
2. **Memoria:** Lee y actualiza `PROGRESS_LOG.json` en cada turno.
3. **Secreto:** Ejecuta `setup_mavim.sh` al inicio. Prohibido filtrar el `.env`.
4. **Arquitectura:** Monolito Modular, UUIDs, Ledger para dinero, H3 para mapas.
5. **Refactoring Mode:** Si el usuario pide mejorar un código existente, carga el `core/SOP_07_REFACTORING.md`. Tu prioridad #1 es la integridad del sistema. No borres código sin antes mapear sus dependencias.

## Modo Quirúrgico
Cuando se trabaje sobre código existente, el `SOP_07_REFACTORING.md` es la **ley suprema**. Orden de operaciones:
1. Generar `IMPACT_MAP.json` — **primer entregable obligatorio, sin excepción.**
2. Aislar en rama `refactor/[nombre]` y ejecutar Smoke Test base.
3. Operar con precisión quirúrgica: cero cambios fuera del alcance definido.
4. Validar con `INTEGRATION_SMOKE_TEST` antes de cualquier merge a `main`.

## Modo E2E — Auto-Mejora con IA
Después de cada cirugía visual, activar el **SOP_08_AUTOMATED_TESTING**. Orden:
1. `npm run test:smoke` — 18 gates Playwright en Chromium real.
2. Leer `playwright-report/mavim-trace.json` — UUID `run_id` + `failure_summary`.
3. Si hay fallos: aplicar fix quirúrgico (SOP_07), repetir desde paso 1.
4. **Sólo cuando `"failed": 0`** → commit + push.
5. El job `e2e-smoke` en CI es el árbitro final antes de merge a `main`.

> **Principio:** Si Playwright falla, la cirugía no está terminada.
> El UUID `correlation_id` de cada fallo vincula el test con los logs del backend.
