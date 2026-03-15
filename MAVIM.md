# MAVIM v2.0 — Agent Instruction Layer
> La primera metodología de ingeniería que se auto-mejora con cada sesión de trabajo.

Lee esto para activarte instantáneamente:
1. **Roles:** Architect diseña bloques LEGO. Developer escribe código modular. Critic audita con Checklists.
2. **Memoria:** Lee y actualiza `PROGRESS_LOG.json` en cada turno.
3. **Secreto:** Ejecuta `setup_mavim.sh` al inicio. Prohibido filtrar el `.env`.
4. **Arquitectura:** Monolito Modular, UUIDs, Ledger para dinero, H3 para mapas.
5. **Refactoring Mode:** Si el usuario pide mejorar un código existente, carga el `core/SOP_07_REFACTORING.md`. Tu prioridad #1 es la integridad del sistema. No borres código sin antes mapear sus dependencias.

---

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

## Modo Consciente — Environment Awareness (v2.0)
Al iniciar cualquier sesión nueva, activar el **SOP_09_ENVIRONMENT_AWARENESS**. Orden:
1. `bash scripts/mavim_scan.sh` — genera `ENVIRONMENT_SNAPSHOT.json` en < 60s.
2. Verificar `status: GREEN/YELLOW/RED` antes de operar.
3. Resolver todos los warnings antes de iniciar cirugía.
4. Si el status es RED → comunicar al usuario y esperar corrección.

> **Principio:** Un agente que no conoce su entorno opera con alucinaciones de infraestructura.

## Modo Bridge — Transición entre IAs (v2.0)
Al finalizar sesión o cambiar de modelo, activar el **SOP_10_COGNITIVE_BRIDGE**. Orden:
1. `python3 scripts/write_bridge.py` — genera `COGNITIVE_BRIDGE.json`.
2. El agente entrante lee el Bridge ANTES de cualquier acción.
3. Verificar `state.health` y ejecutar `handoff_instructions.first_actions`.
4. Anunciar al usuario: estado del sistema + próximo paso.

> **Principio:** El conocimiento de un agente no debe morir con su sesión.

---

## Jerarquía de SOPs (v2.0)

```
SOP_09 ENVIRONMENT_AWARENESS  ← Activar primero en sesión nueva
SOP_10 COGNITIVE_BRIDGE       ← Leer al inicio, escribir al finalizar
    ↓
SOP_07 REFACTORING            ← Ley suprema en cirugías
SOP_08 AUTOMATED_TESTING      ← Gate final obligatorio
    ↓
SOP_01..06                    ← Arquitectura, síntesis, evaluación, resiliencia
```

## Índice de SOPs

| SOP | Nombre | Cuándo activar |
|-----|--------|---------------|
| 01 | INTENTION | Al definir un nuevo feature |
| 02 | ARCHITECTURE | Al diseñar módulos o sistemas |
| 03 | SYNTHESIS | Al integrar componentes |
| 04 | EVALUATION | Al revisar calidad del código |
| 05 | RESILIENCE | Al diseñar manejo de errores |
| 06 | CONTINUITY | Al planificar sprints |
| 07 | REFACTORING | **Al modificar código existente** |
| 08 | AUTOMATED_TESTING | **Después de toda cirugía** |
| 09 | ENVIRONMENT_AWARENESS | **Al inicio de sesión** |
| 10 | COGNITIVE_BRIDGE | **Al inicio y fin de sesión** |
