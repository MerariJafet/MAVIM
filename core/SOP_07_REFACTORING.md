# MAVIM SOP: Surgical Refactoring & Improvement
Este protocolo es OBLIGATORIO cuando se trabaja sobre código existente.

## 1. Fase de Descubrimiento (Deep Scan)
- Leer el `ARCHITECTURE_CONTRACT.md` actual.
- Identificar el stack tecnológico y las fronteras de los módulos.
- Generar un `IMPACT_ANALYSIS.json` detallando qué partes del sistema tocan la zona a mejorar.

## 2. Fase de Aislamiento
- No editar archivos en `main`. Crear una rama `refactor/[nombre-mejora]`.
- Implementar un Test Unitario que valide el comportamiento actual (para asegurar que no se pierda funcionalidad).

## 3. Fase de Cirugía
- Aplicar la mejora siguiendo los patrones de MAVIM (Shadcn, UUIDs, etc.).
- Si se cambia una API, actualizar el `ARCHITECTURE_CONTRACT.md` inmediatamente.

## 4. Fase de Re-conexión y Smoke Test
- Ejecutar el `INTEGRATION_SMOKE_TEST` para asegurar que el "puente" entre módulos sigue vivo.
