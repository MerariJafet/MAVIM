# MAVIM SOP_07: Refactorización Quirúrgica y Mejora
Este protocolo es la **ley suprema** cuando se trabaja sobre código existente. Su omisión invalida cualquier PR.

## 1. Fase de Descubrimiento (Deep Scan)
- Leer el `ARCHITECTURE_CONTRACT.md` actual.
- Identificar el stack tecnológico y las fronteras de los módulos.
- **Entregable obligatorio:** generar `IMPACT_MAP.json` detallando dependencias, archivos afectados y contratos de API de la zona a intervenir. Sin este archivo, la cirugía no puede comenzar.

## 2. Fase de Aislamiento
- No editar archivos en `main`. Crear una rama `refactor/[nombre-mejora]`.
- Ejecutar un **Smoke Test inicial** que confirme que el sistema base funciona antes de cualquier edición.
- Implementar un Test Unitario que valide el comportamiento actual (para asegurar que no se pierda funcionalidad).

## 3. Fase de Cirugía
- Aplicar la mejora siguiendo los patrones de MAVIM (Shadcn, UUIDs, etc.).
- Si se cambia una API, actualizar el `ARCHITECTURE_CONTRACT.md` inmediatamente.

## 4. Fase de Re-conexión y Smoke Test de Integración (OBLIGATORIO)
- El rol **MAVIM-CRITIC** debe validar la comunicación Front-Back mediante un `INTEGRATION_SMOKE_TEST` exitoso.
- Sin smoke test verde, el merge a `main` está prohibido.
