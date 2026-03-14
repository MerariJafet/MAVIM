# MAVIM Evaluation Checklists

## UX / Heurísticas de Usabilidad
- [ ] **Visibilidad del Estado:** ¿Hay Spinners o Skeletons en procesos largos?
- [ ] **Prevención de Errores:** ¿Los formularios tienen validación inline?
- [ ] **Consistencia:** ¿Se usan los mismos componentes de UI en todos los módulos?

## Seguridad y Robustez
- [ ] **PII Isolation:** ¿Los datos sensibles están encriptados en reposo?
- [ ] **Prompt Injection:** ¿Las entradas del usuario al LLM están saneadas?
- [ ] **Idempotencia:** ¿Qué pasa si el webhook de pago llega 2 veces? (Debe estar manejado).
