# MAVIM Evaluation Checklists

## UX / Heurísticas de Usabilidad
- [ ] **Visibilidad del Estado:** ¿Hay Spinners o Skeletons en procesos largos?
- [ ] **Prevención de Errores:** ¿Los formularios tienen validación inline?
- [ ] **Consistencia:** ¿Se usan los mismos componentes de UI en todos los módulos?
- [ ] **Pureza de Componentes (Visual DNA):** El `CRITIC` debe verificar que el `DEVELOPER` no use etiquetas HTML base `<button class="...">` para elementos que ya existen en el Sistema de Diseño (ej. Shadcn). Se deben exigir importaciones formales. Si se detecta "código sucio", el proyecto se rechaza.

## Seguridad y Robustez
- [ ] **PII Isolation:** ¿Los datos sensibles están encriptados en reposo?
- [ ] **Prompt Injection:** ¿Las entradas del usuario al LLM están saneadas?
- [ ] **Idempotencia:** ¿Qué pasa si el webhook de pago llega 2 veces? (Debe estar manejado).
