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

## Multi-Agente (v2.0)
- [ ] **Model Routing:** ¿Cada agente usa el modelo Claude correcto según SOP_08? (Opus para estrategia, Sonnet para código, Haiku para scraping).
- [ ] **Aislamiento de módulos:** ¿Ningún subagente Developer tocó archivos fuera de su módulo asignado?
- [ ] **PROGRESS_LOG.json actualizado:** ¿El log refleja el estado final real antes del cierre de sesión?
- [ ] **Sin conflictos Git:** ¿Las ramas de los agentes paralelos no tienen merge conflicts no resueltos?

## Web Intelligence / Scraping (v2.0)
- [ ] **robots.txt verificado:** ¿El scraper comprobó robots.txt antes de extraer?
- [ ] **Rate limiting activo:** ¿Hay al menos 1.5 segundos entre requests en loops de scraping?
- [ ] **Sin PII en Knowledge Store:** ¿Los datos extraídos fueron pasados por Guardrails para eliminar PII?
- [ ] **Modelo correcto para scraping:** ¿Se usó Haiku (no Opus ni Sonnet) para extracción masiva?
- [ ] **Cache TTL definido:** ¿Las entradas del Knowledge Store tienen `expires_at`?
