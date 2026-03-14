# MAVIM SOP_07: Refactorización Quirúrgica y Mejora

Este protocolo es **la ley suprema** cuando se trabaja sobre código existente (Brownfield). Su objetivo es elevar la calidad sin introducir regresiones.

---

## Fase 1: Deep Scan

- Lectura obligatoria del `ARCHITECTURE_CONTRACT.md` actual.
- Identificar el stack tecnológico y las fronteras de los módulos.
- **Entregable obligatorio:** Generar `IMPACT_MAP.json` detallando qué partes del sistema tocan la zona a mejorar (análisis de dependencias e impacto).
- No avanzar a la siguiente fase sin este entregable.

## Fase 2: Aislamiento

- No editar archivos directamente en `main`.
- Crear rama `refactor/[nombre-mejora]`.
- Ejecutar **Smoke Test pre-vuelo** para validar el estado base del sistema antes de cualquier cambio.

## Fase 3: Cirugía

- Implementar la mejora de forma modular siguiendo el `ARCHITECTURE_CONTRACT.md`.
- Respetar los patrones de UI Shadcn y convenciones del proyecto.
- Si se cambia una API, actualizar el contrato **de forma inmediata** antes de continuar.

## Fase 4: Re-conexión

- Validación por **MAVIM-CRITIC** mediante Smoke Test de integración Front-Back.
- Confirmar que el "puente" entre módulos sigue funcional.
- Solo tras validación exitosa se puede hacer merge a `main`.

---

## Invariantes (Reglas Inquebrantables)

- **Prohibido** hardcoding de puertos o IPs.
- **Prohibido** romper contratos de API existentes sin actualización del contrato.
- **Uso obligatorio** de variables de entorno para toda configuración sensible.
