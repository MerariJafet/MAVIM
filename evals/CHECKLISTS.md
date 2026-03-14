# MAVIM Evaluation Checklists (The Gatekeeper)

Este documento contiene la lista de verificación técnica estricta que el agente **MAVIM-Critic** debe ejecutar y validar antes de autorizar cualquier despliegue o enviar un reporte de éxito al usuario.

## 1. Checklist de Seguridad Extrema (Zero Trust)

- [ ] **Data Bleeding / Tenant Isolation:** ¿Las consultas a la base de datos están encapsuladas con identificadores de Tenant (ej. RLS o `tenant_id` obligatorio)? Retornar "REJECTED" si una consulta masiva está expuesta.
- [ ] **Protección PII (Personal Identifiable Information):** ¿Las respuestas de la API ocultan u ofuscan contraseñas, tokens y datos sensibles?
- [ ] **Defensas contra Prompt Injection:** Toda entrada que vaya hacia un LLM debe estar delimitada por delimitadores seguros (ej. XML tags `<user_input>`) y evaluada por heurísticas de longitud e intención.
- [ ] **Access Control (Zanzibar / ReBAC):** ¿Se valida que el usuario (`actor_id`) tenga permiso explícito sobre el recurso (`resource_id`) antes de proceder con una mutación?

## 2. Checklist de Arquitectura Senior

- [ ] **Invariante de Monolito Modular:** Cero dependencias circulares entre módulos y cero `JOINs` SQL cruzados.
- [ ] **Tipos Financieros Seguros:** Si maneja transacciones o balances, NO usa floats o decimals. Utiliza *Integers* para los centavos.
- [ ] **Identificadores No-Secuenciales:** Las llaves primarias externas o expuestas al cliente deben ser obligatoriamente UUIDs, ULIDs o Snowflakes. 
- [ ] **Paginación e Indexación:** Para queries que listan recursos, se valida el uso de Paginación por Cursor (Keyset Pagination) sobre OFFSET/LIMIT, y existen índices apropiados para las llaves foráneas.

## 3. Checklist de Heurísticas UX (User Experience)

- [ ] **Feedback de Estado Inmediato:** Las operaciones que toman más de 300ms (como consultas a base de datos o llamadas LLM) muestran indicadores de carga (Spinners, Skeletons o Progress Bars).
- [ ] **Manejo de Errores Gracioso:** Los errores técnicos o excepciones (`500 Server Error`) NUNCA se muestran crudos al usuario. Presentan un mensaje amigable y orientativo.
- [ ] **Idempotencia Visual:** Los botones de "Pagar", "Enviar" o "Procesar" se deshabilitan o bloquean de inmediato tras el primer clic para evitar envíos dobles mutantes.
