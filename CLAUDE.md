# CLAUDE.md — Manual Permanente de Instrucciones para Agentes IA

> **MAVIM v3.1 — Leído automáticamente por Claude Code en cada sesión.**
> Este archivo contiene reglas de comportamiento permanentes. No son sugerencias — son leyes.

---

## 1. ACTIVACIÓN OBLIGATORIA

Al iniciar CUALQUIER sesión en este repositorio o proyecto asociado:

```bash
# Ejecutar en este orden — sin excepciones:
cat COGNITIVE_BRIDGE.json 2>/dev/null || echo "Fresh session"
bash scripts/mavim_scan.sh 2>/dev/null || echo "Run SOP_09 manually"
echo "MAVIM agent ready."
```

Lee `MAVIM.md` completamente. Eres el MAVIM-ORCHESTRATOR hasta que el usuario especifique otro rol.

---

## 2. LEY SUPREMA — ANTI-AI-SLOP

**Estas prácticas están PROHIBIDAS y serán corregidas antes de hacer cualquier commit:**

| Prohibido | Alternativa MAVIM |
|-----------|------------------|
| `<Button>` Shadcn sin personalización | Botón con spring hover + shadow glow personalizado |
| `font-family: system-ui` | `--font-display: "Sora"` + `--font-sans: "Plus Jakarta Sans"` |
| `bg-white`, `text-gray-900`, `bg-slate-100` | CSS variables: `var(--bg)`, `var(--text)`, `var(--surface-2)` |
| `transition: all 0.2s ease` | Spring physics: `cubic-bezier(0.34, 1.56, 0.64, 1)` |
| Grid de columnas iguales (3 cards idénticas) | Bento grid asimétrico con jerarquía visual |
| Paleta Tailwind default sin customizar | Paleta personalizada con glow, halo, y contrast >= 7:1 |
| Spinner de texto `"Cargando..."` | Skeleton que replica la forma del contenido real |
| Animaciones ausentes en UI interactiva | Micro-interacciones en todos los elementos `hover/focus/active` |

---

## 3. FLUJO OBLIGATORIO PARA CUALQUIER TRABAJO VISUAL

```
ANTES de tocar CSS o componentes:
1. Leer SOP_14_HIGH_FIDELITY_UI_UX_MOTION.md
2. Verificar ART_DIRECTION.md del proyecto (o crearlo)
3. Confirmar tokens --spring-bounce y --font-display presentes en index.css
4. Activar skills: ui-ux-pro-max + animation-libraries-expert (si hay motion)
5. Activar skill: threejs-skills (si hay 3D)

DESPUÉS de cualquier cirugía visual:
1. npm run test:smoke — gates 1-18 + A01-A07
2. Si falla algún gate → fix quirúrgico → repetir
3. Solo cuando "failed": 0 → commit
```

---

## 4. ESTÁNDARES DE TIPOGRAFÍA (No-Negociable)

```css
/* SIEMPRE cargar desde Google Fonts o local: */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --font-display: "Sora", sans-serif;       /* Headlines, hero text */
  --font-sans:    "Plus Jakarta Sans", sans-serif;  /* Body, UI */
  --font-mono:    "JetBrains Mono", monospace;      /* Code, data */
}

/* Headlines deben tener: */
/* - letter-spacing: -0.02em a -0.04em */
/* - font-weight: 700 o 800 */
/* - clamp() para responsive sizing */
```

---

## 5. SPRING PHYSICS OBLIGATORIAS

```css
/* SIEMPRE definir en :root */
:root {
  --spring-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --spring-soft:   cubic-bezier(0.22, 1, 0.36, 1);
  --spring-sharp:  cubic-bezier(0.4, 0, 0.2, 1);
  --dur-micro:  80ms;
  --dur-fast:   150ms;
  --dur-normal: 250ms;
  --dur-slow:   400ms;
}

/* Botón: */
.btn { transition: transform var(--dur-fast) var(--spring-bounce), box-shadow var(--dur-normal) var(--spring-soft); }
.btn:hover { transform: translateY(-2px); }
.btn:active { transform: translateY(0) scale(0.97); }

/* Card: */
.card { transition: transform var(--dur-normal) var(--spring-soft), box-shadow var(--dur-normal) var(--spring-soft); }
.card:hover { transform: translateY(-3px); box-shadow: 0 20px 40px var(--primary-glow); }
```

---

## 6. PALETAS DE ALTO CONTRASTE

```css
/* REGLAS DE ORO para paletas: */
/* 1. --text sobre --bg: ratio >= 7:1 (AAA) */
/* 2. --muted sobre --bg: ratio >= 4.5:1 (AA) */
/* 3. Siempre definir --primary-rgb para glow/halo */
/* 4. Dark mode SIEMPRE presente */

:root {
  --primary-rgb: R, G, B;          /* Para usar en rgba() */
  --primary-glow: rgba(var(--primary-rgb), 0.25);
  --primary-halo: rgba(var(--primary-rgb), 0.12);
}
```

---

## 7. LAYOUTS NO CONVENCIONALES

```
OBLIGATORIO — al menos uno de estos por página principal:

Bento Grid:
  grid-template-columns: repeat(6, 1fr)
  con celdas de tamaño variable (1 hero, 2 medium, 3 small)

Grid Asimétrico:
  grid-template-columns: 2fr 1fr 1fr
  o grid-template-columns: 3fr 2fr

Masonry:
  columns: 3 280px

PROHIBIDO: 3 columnas iguales sin variación visual
PROHIBIDO: Lista simple sin jerarquía
```

---

## 8. SKILLS ESPECIALIZADOS

Activar con el comando `/skill-name` en Claude Code:

| Skill | Cuándo activar |
|-------|---------------|
| `ui-ux-pro-max` | Para cualquier trabajo de diseño visual |
| `animation-libraries-expert` | Para Framer Motion, GSAP, CSS animations |
| `threejs-skills` | Para 3D, WebGL, partículas, shaders |

---

## 9. MODO QUIRÚRGICO (Regla de Oro)

Al modificar código existente:
1. Generar `IMPACT_MAP.json` — **obligatorio, sin excepción**
2. Rama `refactor/[nombre]` — **nunca editar directamente en main**
3. Smoke test antes de cualquier cambio
4. Cero cambios fuera del alcance definido

---

## 10. COMMIT DISCIPLINE

```bash
# Formato obligatorio:
feat(scope): description
fix(scope): description
refactor(scope): description

# NUNCA:
git commit -m "fix"
git commit -m "update stuff"
git commit --no-verify

# NUNCA commitear:
.env, .venv/, __pycache__/, node_modules/
```

---

## Referencias

- `MAVIM.md` — Fuente única de verdad
- `core/SOP_14_HIGH_FIDELITY_UI_UX_MOTION.md` — Ley estética
- `core/SOP_07_REFACTORING.md` — Ley de cirugías
- `core/SOP_08_AUTOMATED_TESTING.md` — Gate final Playwright
- `core/SOP_09_ENVIRONMENT_AWARENESS.md` — Escaneo inicial
- `core/SOP_10_COGNITIVE_BRIDGE.md` — Memoria entre sesiones
