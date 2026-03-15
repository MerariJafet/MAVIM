# Contributing to MAVIM

**Multi-Agent VIbe coding Methodology** — Guía de Contribución

MAVIM es un proyecto vivo. Cada SOP, patrón y protocolo emergió de un problema real en producción.
Si has encontrado un fallo que MAVIM no cubre, tu contribución es bienvenida.

---

## Tipos de Contribución

| Tipo | Descripción | Rama sugerida |
|------|-------------|---------------|
| 🐛 **Bug en SOP** | Un protocolo existente tiene instrucciones incorrectas o ambiguas | `fix/sop-XX-descripcion` |
| 📋 **Nuevo SOP** | Patrón de fallo recurrente que necesita un protocolo formal | `feat/sop-13-nombre` |
| 🧩 **Nuevo Patrón** | Arquitectura o solución reutilizable para `/patterns/` | `feat/pattern-nombre` |
| 📖 **Caso de Estudio** | Proyecto real donde aplicaste MAVIM con métricas documentadas | `docs/showcase-proyecto` |
| 🛠️ **Tooling** | Script o herramienta para el ecosistema MAVIM | `feat/tool-nombre` |
| 🌐 **Traducción** | MAVIM en otro idioma | `docs/i18n-idioma` |

---

## Proceso: Antes de Empezar

### GSD Planning Gate (obligatorio para SOPs y Patrones nuevos)

Responde estas 5 preguntas antes de abrir un PR:

```
1. PROBLEM:    ¿Qué fallo específico resuelve esto? (una oración)
2. EVIDENCE:   ¿Dónde has observado este fallo? (proyecto, fecha, contexto)
3. SCOPE:      ¿Qué está explícitamente FUERA del alcance?
4. VALIDATION: ¿Cómo sabrá el agente que aplicó este protocolo correctamente?
5. CONFLICT:   ¿Entra en conflicto con algún SOP existente? (revisar SOPs 01–12)
```

Abre un **issue** con el label `[PLANNING]` y las 5 respuestas antes de hacer código.

---

## Guía Paso a Paso

### 1. Fork y configuración

```bash
git clone https://github.com/TU_USUARIO/MAVIM
cd MAVIM
bash setup.sh --local .    # instala entorno MAVIM en el propio repo
git checkout -b feat/mi-contribucion
```

### 2. Estándares de calidad

#### Para nuevos SOPs

Sigue la estructura exacta de los SOPs existentes. Cada SOP debe tener:

```markdown
# SOP_XX — NOMBRE
## Propósito
## Cuándo activar
## Protocolo (pasos numerados)
## Entregable
## Checklist de Cumplimiento
## Referencias
```

- Los números de SOP son secuenciales — nunca reutilices o saltes un número
- La sección `## Checklist de Cumplimiento` es **obligatoria**
- Las referencias cruzadas usan rutas relativas: `../core/SOP_XX_NAME.md`

#### Para patrones en `/patterns/`

```markdown
# PATTERN — NOMBRE
## Problema que resuelve
## Cuándo aplicar
## Implementación
## Anti-patrones relacionados
## Casos de uso reales
```

#### Para casos de estudio en `/showcase/`

Los casos de estudio deben incluir **métricas reales**, no estimaciones:

```markdown
# Caso: NOMBRE_PROYECTO
## Stack técnico
## Estado antes de MAVIM (con datos reales)
## SOPs aplicados y en qué orden
## Resultados con números (tests, tiempo, bugs)
## Lecciones documentadas
```

### 3. Commits

Formato: `tipo(alcance): descripción`

```bash
feat(sop): add SOP_13_OBSERVABILITY for distributed tracing
fix(sop-07): clarify IMPACT_MAP scope boundaries
docs(showcase): add case study for Node.js + Prisma stack
chore(setup): add --stack node option to setup.sh
```

### 4. Pull Request

- Título: máximo 70 caracteres, descriptivo
- Body: usa la plantilla de PR que aparece automáticamente
- El PR debe pasar la revisión del **MAVIM-CRITIC checklist** (ver abajo)

---

## MAVIM-CRITIC Checklist (para reviewers)

Antes de aprobar cualquier PR, verificar:

- [ ] El cambio soluciona un problema real documentado con evidencia
- [ ] No borra contenido de SOPs existentes (solo añade o crea nuevas secciones)
- [ ] Si es un SOP nuevo: tiene los 6 apartados obligatorios incluyendo Checklist
- [ ] Las referencias cruzadas usan rutas relativas correctas
- [ ] No introduce dependencias de un agente específico (Claude, GPT, etc.)
- [ ] Caso de estudio: incluye métricas reales, no estimaciones
- [ ] Commit messages siguen el formato `tipo(alcance): descripción`

---

## Reportar un Bug en un SOP

Abre un issue con:

- **Label:** `bug`
- **Título:** `[SOP-XX] Descripción del problema`
- **Body:**
  ```
  SOP afectado: SOP_XX_NOMBRE
  Sección: (número de sección o línea)
  Comportamiento actual: (qué dice el SOP)
  Comportamiento esperado: (qué debería decir)
  Evidencia: (caso real donde el SOP falló)
  ```

---

## Proponer un Nuevo Protocolo

Abre un issue con:

- **Label:** `enhancement`
- **Título:** `[PATTERN] Nombre del anti-patrón`
- **Body:** Las 5 respuestas del GSD Planning Gate

Si la comunidad valida el problema (≥2 reacciones 👍), procede con el PR.

---

## Preguntas

- **Dudas sobre un SOP:** Abre un issue con label `question`
- **Discusión general:** Usa GitHub Discussions
- **Casos de uso:** Comparte en el issue `[SHOWCASE] Comunidad`

---

*MAVIM v3.0 — Forjado en producción. Mejorado por la comunidad.*
*github.com/MerariJafet/MAVIM*
