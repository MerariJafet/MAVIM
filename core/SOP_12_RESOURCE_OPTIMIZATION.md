# SOP_12 — RESOURCE OPTIMIZATION (Eficiencia en Sesiones de Larga Duración)

**Versión:** 1.0.0
**Fecha:** 2026-03-14
**Autor:** MAVIM-ORCHESTRATOR
**Estado:** ACTIVO — Aplicar en toda sesión > 30 minutos o > 50 herramientas usadas

---

## 1. Propósito

Las sesiones largas con agentes IA enfrentan tres enemigos silenciosos:

1. **Context Bloat** — El contexto de conversación crece hasta saturar la ventana, provocando olvidos o truncamientos.
2. **Tool Repetition** — El agente relee los mismos archivos múltiples veces, desperdiciando llamadas y tiempo.
3. **Decision Drift** — Sin un ancla, las decisiones de arquitectura divergen de las tomadas al inicio.

Este SOP define las estrategias para que el agente opere a máxima eficiencia durante sesiones extensas, manteniendo coherencia y velocidad desde el minuto 1 hasta el cierre.

---

## 2. Principio Rector

> **"La eficiencia no es velocidad — es no hacer dos veces lo mismo ni cargar lo que no se necesita."**

---

## 3. Las 4 Estrategias Core

### Estrategia 1 — Context Pruning (Poda de Contexto)

**Cuándo:** Al superar el 70% de la ventana de contexto o después de completar un milestone.

**Protocolo:**

```
ANTES de la poda:
1. Escribir COGNITIVE_BRIDGE.json (SOP_10) — captura todo el estado
2. Identificar qué información ya está en archivos (no necesita estar en contexto)
3. Identificar decisiones ya tomadas e irreversibles

DURANTE la poda:
- Descartar: historiales de errores ya resueltos
- Descartar: versiones anteriores de código (está en git)
- Descartar: exploraciones de archivos que no se modificarán
- CONSERVAR: arquitectura actual, decisiones activas, tarea en curso

DESPUÉS de la poda:
- Verificar que COGNITIVE_BRIDGE.json tiene todo lo descartado
- Continuar desde el estado capturado
```

**Regla de oro:** Si la información está en un archivo del repo, no necesita estar en el contexto. La herramienta `Read` recupera en milisegundos lo que el contexto guardaría por kilómetros.

---

### Estrategia 2 — Lazy Loading de Archivos

**Cuándo:** Siempre.

**Protocolo:**

```
NO hacer:
- Leer todos los archivos de un directorio "por si acaso"
- Leer un archivo completo cuando solo se necesitan 20 líneas
- Releer un archivo ya leído en la misma sesión sin cambios

SÍ hacer:
- Usar Grep para localizar exactamente qué línea necesito antes de leer
- Usar Read con offset + limit para archivos grandes
- Usar Glob para confirmar que el archivo existe antes de leer
- Cachear mentalmente: "ya leí X, sé que tiene Y"
```

**Ejemplo de eficiencia:**

```python
# INEFICIENTE: leer 500 líneas para encontrar una función
Read("backend/app/main.py")  # 500 líneas

# EFICIENTE: localizar primero, leer después
Grep("include_router.*diagnostics", "backend/app/main.py")  # 1 línea
# → Confirma que ya está registrado. No necesito leer el archivo.
```

---

### Estrategia 3 — Parallel Tool Execution

**Cuándo:** Siempre que dos o más acciones sean independientes entre sí.

**Protocolo:**

```
IDENTIFICAR dependencias antes de actuar:
  A → B → C  (secuencial obligatorio)
  A + B + C  (paralelo — ejecutar en un solo mensaje)

REGLA: Si el resultado de A no afecta los inputs de B, ejecutar en paralelo.
```

**Ejemplos de paralelización válida:**

```
✅ Leer 3 archivos diferentes simultáneamente
✅ Escribir SOP_11 y SOP_12 al mismo tiempo
✅ Hacer git add + ejecutar un health check
✅ Buscar en frontend + buscar en backend simultáneamente

❌ Leer main.py para luego editarlo (secuencial — necesito el contenido)
❌ git add + git commit (commit depende del add)
❌ Escribir archivo A + escribir archivo B si B importa A
```

**Impacto medido:** Paralelizar reads/writes independientes reduce el tiempo de sesión 40-60%.

---

### Estrategia 4 — Decision Anchoring

**Cuándo:** Al inicio de cualquier tarea nueva, especialmente en sesiones largas.

**Protocolo:**

```
Al empezar una nueva tarea en sesión larga:
1. Leer COGNITIVE_BRIDGE.json (< 5 segundos) — re-anclar contexto
2. Verificar que la tarea no contradice architecture_decisions
3. Si contradice → elevar al usuario antes de proceder
4. Si es consistente → ejecutar sin preguntar innecesariamente
```

**Anti-patrón que esto previene:**
> "Voy a usar `bg-white` para este componente nuevo..." — contradice ADR-001.
> El agente que leyó el Bridge sabe que esto rompe dark mode. No lo hace.

---

## 4. Métricas de Eficiencia de Sesión

El agente debe auto-monitorear estas métricas:

| Métrica | Umbral saludable | Acción si supera |
|---------|-----------------|-----------------|
| Archivos leídos > 1 vez | < 3 re-lecturas | Cachear resultado mentalmente |
| Herramientas usadas totales | < 100 por sesión | Activar poda de contexto |
| Tiempo entre milestones | < 15 minutos | Verificar si hay bloqueo real |
| Comandos fallidos consecutivos | < 3 | Cambiar estrategia, no reintentar |
| Edits de un mismo archivo | < 5 | Considerar reescritura completa |

---

## 5. Protocolo de Sesión Larga (> 60 minutos)

```
T+00: Activar SOP_09 (Environment Scan)
T+00: Leer COGNITIVE_BRIDGE.json
T+00: Ejecutar Health Check (SOP_11)

T+30: Milestone check
  → ¿Completé al menos 1 tarea del Bridge?
  → ¿El contexto está > 70%? → Poda (Estrategia 1)
  → Actualizar COGNITIVE_BRIDGE.json con progreso

T+60: Sesión larga alert
  → Escribir Bridge completo
  → Commit de seguridad de cambios en curso
  → Comunicar al usuario: "60min alcanzados — estado: X, próximo: Y"

T+90: Cierre forzado si no hay milestone nuevo
  → Escribir Bridge
  → Health Check final
  → Push si tests verdes
```

---

## 6. Gestión de Errores en Sesiones Largas

### Regla de los 3 intentos

```
Intento 1: Estrategia normal
Intento 2: Estrategia alternativa (diferente enfoque)
Intento 3: Diagnóstico — ¿por qué fallan los dos?

Si los 3 fallan → STOP. Comunicar al usuario con diagnóstico completo.
NUNCA intentar 4+ veces el mismo approach.
```

### Clasificación de errores

| Tipo | Ejemplo | Respuesta |
|------|---------|-----------|
| Transitorio | Rate limit, timeout de red | Reintentar 1 vez con backoff |
| Configuración | Variable de entorno faltante | Alertar usuario — no continuar |
| Lógico | TypeScript error en código nuevo | Fix quirúrgico inmediato |
| Ambiental | Puerto ocupado | Investigar proceso, ofrecer opciones |
| Bloqueante | DB inalcanzable | STOP — nada funciona sin DB |

---

## 7. Optimización de Prompts y Herramientas

### Usar la herramienta correcta

```
BÚSQUEDA DE ARCHIVOS:
  ✅ Glob("**/*.tsx")                    — busca por nombre/patrón
  ✅ Grep("useState", type="ts")         — busca contenido específico
  ❌ Bash("find . -name '*.tsx'")        — más lento, menos legible

LECTURA:
  ✅ Read(file, offset=50, limit=30)     — solo las líneas necesarias
  ❌ Read(file)                          — 500 líneas cuando necesito 5

EDICIÓN:
  ✅ Edit(old_string, new_string)        — cambio preciso
  ❌ Write(entire_file_rewritten)        — solo si el cambio es > 40%

BÚSQUEDA PROFUNDA:
  ✅ Agent(Explore, "find all hardcoded colors") — cuando necesito > 3 greps
  ❌ 5 Grep calls sucesivos              — delegar al agente Explore
```

---

## 8. Template de Reporte de Eficiencia

Al finalizar una sesión larga, incluir en el COGNITIVE_BRIDGE.json:

```json
"session_efficiency": {
  "duration_minutes": 90,
  "tools_used": 87,
  "files_read": 23,
  "files_modified": 11,
  "parallel_batches": 14,
  "context_prunes": 1,
  "milestones_completed": 4,
  "efficiency_score": "HIGH",
  "bottlenecks": ["AppointmentFormDialog.tsx took 3 iterations to fix CSS"]
}
```

---

## 9. Checklist de Cumplimiento

- [ ] Herramientas independientes ejecutadas en paralelo (no secuencial)
- [ ] No se releyó el mismo archivo sin cambios entre lecturas
- [ ] Archivos grandes accedidos con `offset + limit`
- [ ] Poda de contexto ejecutada si ventana > 70%
- [ ] Bridge actualizado en cada milestone
- [ ] Regla de los 3 intentos respetada (nunca > 3 para mismo approach)
- [ ] Health Check ejecutado antes de commit final

---

## Referencias

- SOP_10_COGNITIVE_BRIDGE.md — Mecanismo de poda y persistencia
- SOP_11_HEALTH_CHECK.md — Reporte de estado en milestones
- SOP_09_ENVIRONMENT_AWARENESS.md — Activar al inicio para evitar errores de entorno
