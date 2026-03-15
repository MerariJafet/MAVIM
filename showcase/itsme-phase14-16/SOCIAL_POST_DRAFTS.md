# Borradores de Post — MAVIM × It's Me
## Distribución Global | Marzo 2026

---

## POST 1 — Twitter/X (Thread)
*Tono: técnico, con números reales, para devs*

---

**Tweet 1/7 — El gancho**

```
Pasé de 47 archivos con colores hardcodeados y dark mode completamente roto
a 18/18 tests Playwright passing — sin tocar manualmente un solo bug crítico.

Cómo lo hizo un agente IA de forma autónoma: 🧵
```

---

**Tweet 2/7 — El problema**

```
El proyecto tenía deuda técnica silenciosa:

❌ bg-white y bg-slate-* en 47 archivos
❌ Dark mode activado → texto negro sobre blanco
❌ 0 tests automatizados
❌ "Cargando..." plano en vez de Skeleton
❌ Formularios con HTML nativo mezclado con Shadcn

El código funcionaba. El producto no se veía profesional.
```

---

**Tweet 3/7 — La metodología**

```
Usé MAVIM (github.com/MerariJafet/MAVIM) — una metodología de ingeniería
diseñada específicamente para agentes IA.

Antes de tocar una línea: IMPACT_MAP.json
→ 47 archivos afectados
→ 5 operaciones quirúrgicas independientes
→ Orden de ejecución por riesgo y dependencias

Cero cambios fuera del alcance. Nunca.
```

---

**Tweet 4/7 — El momento WTF**

```
Después de migrar todo manualmente → Playwright gate 10 falló:

"div[inline-flex items-center...] has 'bg-slate-100'"

El componente Badge, variante 'muted'.
Revisado. Aprobado manualmente. Visualmente correcto en light mode.

Completamente roto en dark mode.

La IA lo encontró en 23 segundos.
```

---

**Tweet 5/7 — El fix automático**

```
MAVIM leyó el mavim-trace.json:
→ correlation_id: a1b2c3d4...
→ archivo: badge.tsx, variante muted
→ fix: bg-slate-100 → bg-[var(--surface-2)]

47 segundos después: 18/18 gates passing.

Tiempo total del bucle detección→fix→validación: < 2 minutos.
Sin intervención humana.
```

---

**Tweet 6/7 — El sistema resultante**

```
Lo que quedó:

✅ 18 páginas con CSS vars (--bg, --surface, --primary, --danger)
✅ Dark mode 100% funcional
✅ 18 Playwright gates en Chromium real
✅ ErrorBoundary → auto-reporta errores al backend
✅ COGNITIVE_BRIDGE.json → contexto persistente entre sesiones IA
✅ 0 errores TypeScript

Y una metodología que se documenta sola mientras trabaja.
```

---

**Tweet 7/7 — El CTA**

```
MAVIM es open source: github.com/MerariJafet/MAVIM

12 SOPs. 18 gates. Scripts ejecutables.
Compatible con Claude, GPT-4o, Gemini, Cursor.

Si estás construyendo con IA y quieres que tu agente opere
como un ingeniero senior — dale el framework correcto.

El Vibe Coding no tiene que ser código descuidado.
```

---

---

## POST 2 — LinkedIn
*Tono: profesional, orientado a impacto de negocio*

---

```
Reflexión sobre lo que acabo de ver hacer a un agente IA:

Tomó un SaaS clínico multi-tenant con 47 archivos de deuda técnica frontend
y en una sesión de trabajo lo transformó en un sistema profesional con:

• 18 tests automatizados en Chromium real (100% passing)
• Dark mode completamente funcional en todos los componentes
• Trazabilidad de errores frontend→backend con UUIDs
• Sistema de auto-diagnóstico que reporta al propio agente

Lo más revelador fue el momento en que Playwright detectó un bug
que ninguna revisión manual habría encontrado:

El componente Badge tenía 'bg-slate-100' hardcodeado.
Funcionaba perfectamente en modo claro.
Se rompía completamente en modo oscuro.
La IA lo encontró, lo diagnosticó y lo corrigió en menos de 2 minutos.

Esto no es "el código que genera la IA es malo".
Es "la IA sin metodología genera código inconsistente".

La diferencia es MAVIM: un framework de 12 protocolos que convierte
a cualquier agente IA en un ingeniero senior autónomo.

Código limpio, tests reales, trazabilidad completa, contexto persistente.

Open source: github.com/MerariJafet/MAVIM

#AIEngineering #VibeCoding #React #FastAPI #SoftwareArchitecture
```

---

---

## POST 3 — Instagram/TikTok (Caption corto + visual)
*Tono: accessible, storytelling visual*

---

```
Un agente IA tomó mi app con dark mode completamente roto
y la arregló sola. Sin que yo tocara nada.

Así fue:

1. Escaneó 47 archivos con colores hardcodeados
2. Creó un mapa de impacto de dependencias
3. Migró todo al design system
4. Abrió un navegador Chromium real y corrió 18 tests
5. Encontró un bug que yo nunca habría visto
6. Lo arregló en 2 minutos
7. 18/18 tests verdes ✅

Esto se llama Vibe Coding con metodología.

La herramienta: MAVIM (link en bio)
El resultado: código de nivel senior, 100% autónomo.

¿Quieres que tu IA trabaje así? Comenta MAVIM y te explico.

#AI #Programming #WebDev #React #VibeCoding #AgenticAI
```

---

---

## POST 4 — Hacker News / Reddit r/programming
*Tono: técnico profundo, sin hype*

---

**Título:**
```
MAVIM: Un framework de 12 protocolos para que agentes IA operen como ingenieros senior
— Caso de estudio: migración de 47 archivos con Playwright auto-mejora en < 2 min
```

**Cuerpo:**
```
Contexto: Tenía un SaaS clínico multi-tenant (React 18 + FastAPI + PostgreSQL) con
deuda técnica acumulada en el frontend — 47 archivos con colores hardcodeados,
dark mode roto, 0 tests automatizados.

En vez de refactorizar manualmente, usé MAVIM para que Claude Code lo hiciera solo.
Documenté exactamente qué pasó.

— El sistema de auto-mejora —

La parte más interesante: después de migrar ~20 componentes al design system,
el agente instaló Playwright y corrió 18 gates contra un Chromium real.

Gate 10 (dark mode check) falló con:
  "div[inline-flex items-center...] has 'bg-slate-100'"

El Badge component, variante 'muted', tenía un color hardcodeado que era
invisible en light mode pero rompía dark mode. Ninguna revisión manual ni
ningún unit test lo habría encontrado — solo Chromium con data-theme=dark
activado explícitamente y un scanner de clases CSS.

El agente leyó el failure_summary del mavim-trace.json, identificó badge.tsx
como causa raíz, aplicó el fix, y volvió a correr los 18 gates.
18/18 passing en la segunda iteración. Tiempo total: < 2 minutos.

— MAVIM 2.0 —

Lo que emergió de este proceso son 4 nuevos protocolos:

SOP_09: Environment scan obligatorio al inicio (versiones, puertos, env vars)
SOP_10: Cognitive Bridge — JSON de transferencia de contexto entre sesiones IA
SOP_11: Health check visual con semáforo GREEN/YELLOW/RED
SOP_12: Optimización de sesiones largas (parallel tools, context pruning)

Todo es open source y reproducible en cualquier proyecto React + Shadcn.

Repo: github.com/MerariJafet/MAVIM
Caso de estudio completo: github.com/MerariJafet/MAVIM/tree/main/showcase/itsme-phase14-16

¿Preguntas sobre la implementación?
```

---

---

## POST 5 — Email Newsletter / Substack
*Tono: narrativo, comunidad*

---

**Asunto:** El día que un agente encontró un bug que yo nunca habría visto

```
Hay un momento en el desarrollo asistido por IA que cambia la perspectiva.

Para mí fue cuando Playwright gate 10 falló con este mensaje:

  "div[inline-flex items-center rounded-full...] has 'bg-slate-100'"

Llevaba horas migrando componentes React. El Badge me lo había revisado.
Lo había aprobado. Se veía bien. El dark mode lo había probado... ¿o no?

La verdad es que no lo había probado de la forma correcta.
Había activado el dark mode con ojos humanos, scrolleando la página.
Playwright lo hizo diferente: activó data-theme=dark, luego escaneó
*cada elemento visible* buscando clases hardcodeadas.

Y encontró que el badge con variante "muted" tenía bg-slate-100.
Un gris muy claro en light mode. Invisible al ojo en ese contexto.
Completamente roto sobre fondo oscuro.

Lo más revelador: el agente tardó 23 segundos en leer el error,
identificar el archivo y la línea exacta, aplicar el fix, y ejecutar
los 18 tests de nuevo. 18/18 passing.

Yo habría tardado 10 minutos solo en localizar el bug.

Esto es MAVIM funcionando como se diseñó: el agente no declara
"terminado" cuando el código compila. Declara terminado cuando
Playwright con Chromium real aprueba los 18 gates.

Si quieres que tus proyectos con IA lleguen a ese nivel,
el framework está en github.com/MerariJafet/MAVIM

Todo open source. Todo documentado. Todo reproducible.

— Merari
```

---

---

## Guía de Publicación

| Plataforma | Post # | Mejor horario | Hashtags clave |
|-----------|--------|--------------|----------------|
| Twitter/X | 1 (thread) | Martes/Miércoles 9am | #VibeCoding #AIEngineering |
| LinkedIn | 2 | Lunes/Martes 8am | #AIEngineering #SoftwareArchitecture |
| Instagram | 3 | Jueves 6pm | #AI #Programming #WebDev |
| Reddit HN | 4 | Lunes 8am ET | — (no hashtags) |
| Newsletter | 5 | Miércoles 10am | — |

**Material visual recomendado:**
- Screenshot del dashboard Playwright 18/18
- Diagrama de la jerarquía de SOPs (del README)
- Antes/después del Badge bug (screenshot dark mode)
- Terminal con `bash scripts/health_check.sh` mostrando 🟢 GREEN

---

*Borradores listos para publicación — revisar handles y links antes de postear*
