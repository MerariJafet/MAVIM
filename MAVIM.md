# MAVIM Cheat Sheet (Agent Instruction Layer)
Lee esto para activarte instantáneamente:
1. **Roles:** Architect diseña bloques LEGO. Developer escribe código modular. Critic audita con Checklists.
2. **Memoria:** Lee y actualiza `PROGRESS_LOG.json` en cada turno.
3. **Secreto:** Ejecuta `setup_mavim.sh` al inicio. Prohibido filtrar el `.env`.
4. **Arquitectura:** Monolito Modular, UUIDs, Ledger para dinero, H3 para mapas.
5. **Refactoring Mode:** Si el usuario pide mejorar un código existente, carga el `core/SOP_07_REFACTORING.md`. Tu prioridad #1 es la integridad del sistema. No borres código sin antes mapear sus dependencias.
