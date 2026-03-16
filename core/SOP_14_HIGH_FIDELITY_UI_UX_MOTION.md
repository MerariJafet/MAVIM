# SOP_14 — HIGH-FIDELITY UI/UX & MOTION

> **MAVIM v3.1 — Aesthetic Layer Protocol**
> Activa este SOP antes de tocar cualquier línea de CSS, componente visual o animación.
> El "AI Slop" y el diseño genérico son **ilegales** bajo MAVIM.

---

## GSD Planning Gate

```
PROBLEM:    Los agentes de IA generan interfaces mediocres, genéricas y sin identidad visual,
            usando Shadcn sin personalización, Tailwind defaults y cero motion design.
EVIDENCE:   Observado en múltiples proyectos piloto (itsme, agente_nucleo) donde el diseño
            pasaba Gates 1-18 pero fallaba el criterio humano de "¿esto se ve profesional?".
SCOPE:      OUT: Backend APIs, auth flows, DB schema — este SOP es solo para la capa visual.
VALIDATION: La pantalla debe pasar el "Dribbble Test" — ¿parece un producto de alta gama?
CONFLICT:   Extiende SOP_02 (Design Token System) y SOP_08 (Playwright gates). No conflicta.
```

---

## Principio Rector

> **"Un UI genérico es un UI fallido. El agente que genera interfaces mediocres no ha completado su misión."**

El diseño de alta fidelidad no es opcional ni decorativo. Es la diferencia entre un producto que genera confianza y uno que se abandona. Bajo MAVIM, la calidad visual tiene el mismo peso que la corrección funcional.

---

## PROHIBICIONES ABSOLUTAS — Anti AI-Slop Law

Las siguientes prácticas están **EXPLÍCITAMENTE PROHIBIDAS** y constituyen violación de MAVIM:

### 🚫 Componentes Genéricos Sin Personalización
```tsx
// ❌ ILEGAL — Shadcn vanilla sin personalización
<Button>Save</Button>
<Card className="p-4">...</Card>
<Badge variant="default">Active</Badge>

// ✅ OBLIGATORIO — Personalización completa
<Button className="bg-[var(--primary)] hover:bg-[var(--primary-dark)]
  shadow-[0_4px_14px_var(--primary-glow)] transition-all duration-200
  hover:-translate-y-0.5 active:translate-y-0 font-semibold tracking-wide">
  Save
</Button>
```

### 🚫 Tipografías Sin Carácter
```css
/* ❌ ILEGAL */
font-family: system-ui, sans-serif;
font-size: 16px;
font-weight: 400;

/* ✅ OBLIGATORIO — Tipografía con voz */
--font-display: "Sora", "Plus Jakarta Sans", sans-serif; /* Headlines */
--font-sans: "Plus Jakarta Sans", "Inter", sans-serif;   /* Body */
--font-mono: "JetBrains Mono", "Fira Code", monospace;  /* Code/data */
```

### 🚫 Paletas de Bajo Contraste y Sin Carácter
```css
/* ❌ ILEGAL — Paleta genérica y aburrida */
--primary: #3b82f6; /* blue-500 default */
--bg: #f9fafb;      /* gray-50 default */

/* ✅ OBLIGATORIO — Paleta con personalidad e identidad */
/* Define tu paleta en base a la identidad del producto.
   Usa contrast ratio AAA para texto principal.
   Incluye colores de acento vibrantes con variables de glow/halo. */
```

### 🚫 Layouts Convencionales y Predecibles
```
❌ ILEGAL: sidebar izquierdo + contenido derecho + tabla básica
❌ ILEGAL: card grid 3 columnas iguales
❌ ILEGAL: form vertical label-input-label-input

✅ OBLIGATORIO: Layouts asimétricos, grids creativos,
   jerarquía visual clara, espaciado intencional,
   uso estratégico del espacio negativo.
```

### 🚫 Animaciones Planas o Ausentes
```
❌ ILEGAL: transition: all 0.2s ease; (sin physics)
❌ ILEGAL: opacity 0 → 1 linear
❌ ILEGAL: No hay feedback de interacción

✅ OBLIGATORIO: Spring physics para elementos interactivos
✅ OBLIGATORIO: Micro-interacciones en hover/focus/active
✅ OBLIGATORIO: Staggered entries para listas y grids
```

---

## Fase Obligatoria: DIRECCIÓN DE ARTE

**Esta fase debe ejecutarse ANTES de escribir cualquier código de componente.**

```
┌─────────────────────────────────────────────────────────────────┐
│             FLUJO MAVIM — PROYECTO NUEVO v3.1                   │
├─────────────────────────────────────────────────────────────────┤
│  SOP_09 → SOP_01 → SOP_02 → [🎨 SOP_14 ART DIRECTION] → BUILD │
│                                        ↑                         │
│                              NUEVO — obligatorio                 │
└─────────────────────────────────────────────────────────────────┘
```

### Protocolo de Dirección de Arte (4 pasos)

**Paso 1 — Definir Identidad Visual del Producto**
```markdown
Responde antes de tocar código:
1. ¿Cuál es el mood del producto? (confiable/audaz/minimalista/orgánico/futurista)
2. ¿Quién es el usuario? (sus referencias visuales, su estilo de vida)
3. ¿Qué NO debe parecer este producto? (define los anti-ejemplos)
4. ¿Qué app/sitio real usa como referencia de calidad? (3 referencias concretas)
```

**Paso 2 — Definir Sistema de Tokens Extendido**
```css
/* MANDATORY EXTENSION — más allá de los tokens base de SOP_02 */
:root {
  /* Tokens de Motion */
  --spring-bounce:  cubic-bezier(0.34, 1.56, 0.64, 1);  /* spring effect */
  --spring-soft:    cubic-bezier(0.22, 1, 0.36, 1);      /* suave */
  --spring-sharp:   cubic-bezier(0.4, 0, 0.2, 1);        /* sharp */
  --dur-micro:  80ms;
  --dur-fast:   150ms;
  --dur-normal: 250ms;
  --dur-slow:   400ms;
  --dur-enter:  500ms;

  /* Tokens de Tipografía (MANDATORY) */
  --font-display: "Sora", sans-serif;
  --font-sans:    "Plus Jakarta Sans", sans-serif;
  --font-mono:    "JetBrains Mono", monospace;
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --text-4xl:  2.25rem;
  --text-5xl:  3rem;

  /* Tokens de Identidad (personalizar por proyecto) */
  --primary-glow:   rgba(var(--primary-rgb), 0.25);
  --primary-halo:   rgba(var(--primary-rgb), 0.12);
  --surface-glass:  rgba(255, 255, 255, 0.08);
  --surface-frost:  rgba(255, 255, 255, 0.6);
  --border-subtle:  rgba(255, 255, 255, 0.06);
  --text-gradient:  linear-gradient(135deg, var(--text) 0%, var(--muted) 100%);
}
```

**Paso 3 — Seleccionar Skills de Motion**

Según la complejidad del motion design requerido:

| Nivel | Skills a Activar | Casos de Uso |
|-------|-----------------|--------------|
| **Básico** | `animation-libraries-expert` | Transiciones de página, micro-interacciones |
| **Avanzado** | `animation-libraries-expert` + Framer Motion | Gestos, drag, layout animations |
| **Pro** | `animation-libraries-expert` + GSAP | Timeline animations, ScrollTrigger |
| **3D** | `threejs-skills` + `animation-libraries-expert` | Hero 3D, partículas, WebGL |

```bash
# Activar Skills en Claude Code:
# /ui-ux-pro-max           → estándares visuales de alta fidelidad
# /animation-libraries-expert → Framer Motion + GSAP + CSS spring
# /threejs-skills          → Three.js + WebGL + R3F
```

**Paso 4 — Crear `ART_DIRECTION.md`** (entregable obligatorio)
```markdown
# Art Direction — [Nombre del Proyecto]

## Identidad Visual
- **Mood:** [elegante/audaz/minimalista/etc.]
- **Referencias:** [App 1], [App 2], [App 3]
- **Anti-referencias:** [lo que NO debe parecer]

## Paleta Seleccionada
- Primary: #XXX (ratio AA/AAA: X.X:1)
- Background: #XXX
- Accent: #XXX
- Rationale: [por qué estos colores para este usuario]

## Tipografía Seleccionada
- Display: [fuente + por qué]
- Body: [fuente + por qué]
- Mono: [fuente + por qué]

## Sistema de Motion
- Framework: [Framer Motion / GSAP / CSS]
- Spring preset: [valores cubic-bezier]
- Stagger timing: Xms entre elementos

## Layout Signature
- [Descripción del layout signature del producto]
- [Grid creativo o asimétrico principal]
```

---

## Estándares de Alta Fidelidad

### Tipografía Audaz
```css
/* Headlines — deben tener peso visual */
.headline-primary {
  font-family: var(--font-display);
  font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl));
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

/* Body — legible y refinado */
.body-base {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: 400;
  line-height: 1.65;
  letter-spacing: 0.01em;
}

/* Labels y UI text */
.label-ui {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
```

### Paletas de Alto Contraste
```css
/* REGLA: Todo texto en color --text debe tener contrast ratio >= 7:1 */
/* REGLA: Todo texto en color --muted debe tener contrast ratio >= 4.5:1 */
/* REGLA: Los colores de acento deben tener un "halo" o "glow" variable */

/* Ejemplo — paleta dark premium */
[data-theme="dark"] {
  --bg:         #080c18;   /* near-black con tinte azul */
  --surface:    #0f1629;   /* surface elevado */
  --surface-2:  #1a2240;   /* surface secundario */
  --border:     #1e2d4a;   /* borde sutil */
  --text:       #f0f4ff;   /* blanco azulado — 15.8:1 sobre --bg */
  --muted:      #8ca0c4;   /* azul medio — 5.2:1 sobre --bg */
  --primary:    #4f8ef7;   /* azul vibrante */
  --primary-rgb: 79, 142, 247;
  --accent:     #a78bfa;   /* violeta complementario */
  --accent-rgb: 167, 139, 250;
}
```

### Micro-Interacciones con Spring Physics
```tsx
/* Framer Motion — spring preset MAVIM */
const springBounce = {
  type: "spring",
  stiffness: 500,
  damping: 28,
  mass: 0.8,
};

const springSmooth = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

/* Botón con spring */
<motion.button
  whileHover={{ scale: 1.02, y: -1 }}
  whileTap={{ scale: 0.97 }}
  transition={springBounce}
>
  Submit
</motion.button>

/* Card con hover reveal */
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ ...springSmooth, delay: index * 0.06 }}
>
  <Card />
</motion.div>

/* CSS spring equivalente */
.interactive-element {
  transition: transform var(--dur-fast) var(--spring-bounce),
              box-shadow var(--dur-normal) var(--spring-soft);
}
.interactive-element:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 8px 24px var(--primary-glow);
}
.interactive-element:active {
  transform: translateY(0) scale(0.98);
}
```

### Grid/Flexbox No Convencionales
```css
/* REGLA: Los grids deben tener intención visual, no solo funcionalidad */

/* Grid asimétrico — dashboard highlight */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: auto;
  gap: 1.5rem;
}
.dashboard-grid .hero-card {
  grid-column: 1 / 2;
  grid-row: 1 / 3;
}

/* Bento grid — agrupación visual premium */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-auto-rows: minmax(120px, auto);
  gap: 1rem;
}

/* Masonry con CSS */
.masonry {
  columns: 3 280px;
  column-gap: 1.5rem;
}
.masonry > * {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}
```

---

## Integración de Skills Especializados

### ui-ux-pro-max
Activa este skill para:
- Auditar componentes existentes contra estándares de alta fidelidad
- Generar propuestas de rediseño con tokens personalizados
- Revisar contrast ratios y accesibilidad visual

### animation-libraries-expert
Activa este skill para:
- Implementar animaciones con Framer Motion (layout, gesture, exit)
- Implementar timelines complejos con GSAP + ScrollTrigger
- Orquestar animaciones staggered en listas y grids
- CSS animations con spring physics nativas

```bash
# Dependencias a instalar según el nivel de motion:
# Básico:
npm install framer-motion

# Avanzado:
npm install framer-motion gsap @gsap/react

# Pro (con ScrollTrigger):
npm install framer-motion gsap @gsap/react
# + registro en componente: gsap.registerPlugin(ScrollTrigger)
```

### threejs-skills
Activa este skill para:
- Hero sections con geometrías 3D y shaders custom
- Partículas interactivas (particles.js → Three.js)
- Modelos GLTF/GLB en landing pages
- Post-processing (bloom, chromatic aberration)

```bash
# Dependencias Three.js:
npm install three @react-three/fiber @react-three/drei
# Para postprocessing:
npm install @react-three/postprocessing
```

---

## Playwright Gates Adicionales (SOP_14 Extension)

Complementa los 18 gates de SOP_08 con validaciones estéticas:

| Gate | Test | Criterio |
|------|------|---------|
| A01 | Fuente display cargada | `document.fonts.check('700 24px "Sora"')` → true |
| A02 | Spring variable definida | `--spring-bounce` existe en `:root` |
| A03 | Contrast ratio headline | Ratio >= 7:1 en `--text` sobre `--bg` |
| A04 | Animaciones no deshabilitadas | `prefers-reduced-motion` respetado pero animaciones presentes |
| A05 | No bg-white hardcoded en componentes | 0 instancias de `bg-white` en dark mode |
| A06 | Motion tokens presentes | `--dur-fast`, `--dur-normal`, `--spring-bounce` definidos |
| A07 | Grid layout no trivial | Al menos un grid con `grid-template-columns` no uniforme |

---

## Checklist de Cumplimiento

Antes de considerar completa cualquier vista o componente:

**Art Direction:**
- [ ] `ART_DIRECTION.md` creado y aprobado
- [ ] Identidad visual definida (mood, referencias, anti-referencias)
- [ ] Paleta personalizada con contrast ratios documentados
- [ ] Tipografía seleccionada (display + sans + mono)
- [ ] Sistema de motion elegido (Framer Motion / GSAP / CSS)

**Tokens:**
- [ ] `--spring-bounce` y `--spring-soft` definidos en `:root`
- [ ] `--font-display` y `--font-sans` cargados desde Google Fonts / local
- [ ] `--primary-glow` y `--primary-halo` definidos
- [ ] `--dur-micro` → `--dur-enter` definidos

**Componentes:**
- [ ] Cero componentes Shadcn sin personalización visual
- [ ] Todos los botones tienen hover + active state con spring
- [ ] Todas las cards tienen hover elevation con shadow spring
- [ ] Listas y grids tienen staggered entry animation

**Layouts:**
- [ ] Al menos un grid creativo/asimétrico por página principal
- [ ] Jerarquía visual clara (1 elemento dominante, 2-3 secundarios)
- [ ] Uso intencional del espacio negativo
- [ ] No hay "bloques rectangulares iguales" sin variación

**Motion:**
- [ ] Page transitions implementadas
- [ ] Skeleton loaders animados (shimmer con spring)
- [ ] Micro-interacciones en todos los elementos interactivos
- [ ] `prefers-reduced-motion` respetado

**Gates Playwright:**
- [ ] Gates A01-A07 pasando
- [ ] Gates 1-18 (SOP_08) manteniendo 18/18

---

## Referencias

- `../core/SOP_02_ARCHITECTURE.md` → Design Token System base
- `../core/SOP_07_REFACTORING.md` → Cirugía estética en proyectos existentes
- `../core/SOP_08_AUTOMATED_TESTING.md` → Gates Playwright (extender con A01-A07)
- `../showcase/itsme-phase14-16/` → Caso de éxito con cirugía visual real
- Skills: `ui-ux-pro-max`, `animation-libraries-expert`, `threejs-skills`
