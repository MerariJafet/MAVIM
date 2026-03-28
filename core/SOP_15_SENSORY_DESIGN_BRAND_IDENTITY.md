# SOP_15 — SENSORY DESIGN & BRAND IDENTITY

> **MAVIM v3.2 — Sensory Experience Layer**
> Activa este SOP después de SOP_14 (High-Fidelity UI/UX) para completar la capa sensorial.
> El diseño sensorial convierte software funcional en experiencia memorable.

---

## GSD Planning Gate

```
PROBLEM:    Los productos digitales que solo usan vista (visual) son inherentemente planos.
            El audio, el movimiento cinematico y el feedback háptico crean memoria muscular
            y asociaciones emocionales que aumentan la retención y el valor percibido.
EVIDENCE:   Estudios de HCI (CHI 2023) demuestran +34% retención con earcons consistentes.
            Apple, Linear, Vercel usan micro-sonidos para reforzar su identidad de marca.
SCOPE:      OUT: Música de fondo, sonidos intrusivos, loops de audio, efectos de video pesados.
            IN:  Earcons (< 200ms), motion cinematico (GSAP/CSS), haptic feedback (mobile).
VALIDATION: Test de "reconocimiento a ciegas" — usuario identifica el producto solo por audio.
CONFLICT:   Extiende SOP_14 (motion tokens). Accesibilidad: respeta prefers-reduced-motion
            y prefers-reduced-transparency. Todo audio es opt-in o respeta user preference.
```

---

## Principio Rector

> **"La excelencia sensorial no se ve — se siente. Un producto de lujo se distingue
> antes de que el usuario lea una sola palabra."**

El diseño sensorial opera en tres canales simultáneos:
- **Audio:** Earcons y señales sonoras refuerzan acciones sin interrumpir
- **Movimiento:** Física cinematica crea peso, masa e inercia perceptibles
- **Háptico:** Confirmación táctil en mobile cierra el loop sensorial

---

## Canal 1 — Audio (Earcons)

### Filosofía de los Earcons

Los earcons son señales sonoras de **< 200ms** que comunican estado sin palabras.
Son el equivalente auditivo de un micro-interacción visual.

```
Earcon → Acción asociada → Respuesta cognitiva
─────────────────────────────────────────────
click     → Interacción confirmada   → "Mi acción fue registrada"
success   → Operación completada     → "Todo salió bien"
error     → Acción fallida           → "Necesito corregir algo"
loading   → Proceso iniciado         → "El sistema está trabajando"
complete  → Proceso finalizado       → "Listo para continuar"
navigate  → Cambio de contexto       → "Estoy en un lugar nuevo"
```

### Especificación de Earcons (Web Audio API)

```typescript
// Parámetros de síntesis — identidad sonora del producto
const EARCON_SPEC = {
  // Tono de identidad: A4 (440Hz) y sus armónicos
  // Timbre: sine para pureza, triangle para calidez
  // Envelope: attack corto = precisión, decay suave = lujo

  click: {
    frequency: 880,        // A5 — brillante, confirmatorio
    type: 'sine',
    attack: 0.001,         // 1ms — instantáneo
    decay: 0.08,           // 80ms — rápido
    gain: 0.12,            // Sutil, no intrusivo
    timing: 'sync',        // Sincronizado con spring-bounce
  },
  success: {
    notes: [523, 659, 784], // C5-E5-G5 — acorde mayor ascendente
    type: 'sine',
    attack: 0.001,
    decay: 0.15,
    gain: 0.10,
    stagger: 60,           // ms entre notas
    timing: 'on-complete', // Al finalizar animación spring
  },
  error: {
    notes: [330, 220],     // E4-A3 — descenso disonante
    type: 'triangle',
    attack: 0.005,
    decay: 0.18,
    gain: 0.08,
    stagger: 80,
  },
  loading: {
    frequency: 220,        // A3 — grave, procesando
    type: 'sine',
    sweep: { from: 220, to: 330 }, // Sweep ascendente
    attack: 0.02,
    decay: 0.20,
    gain: 0.06,
  },
  complete: {
    notes: [523, 784, 1047], // C5-G5-C6 — octava perfecta
    type: 'sine',
    attack: 0.001,
    decay: 0.22,
    gain: 0.10,
    stagger: 70,
  },
  navigate: {
    frequency: 440,        // A4 — neutro, orientador
    type: 'sine',
    attack: 0.005,
    decay: 0.12,
    gain: 0.07,
  },
};
```

### Implementación Hook — `useAudio.ts`

```typescript
// MAVIM SOP_15 — Audio Hook Pattern
// Usa Web Audio API nativa — sin dependencias externas
// Respeta prefers-reduced-motion como proxy de preferencia sensorial

const useAudio = () => {
  // AudioContext lazy — se inicializa en el primer gesto del usuario
  // (requerido por navegadores modernos: autoplay policy)
  const ctx = useRef<AudioContext | null>(null);

  const getCtx = (): AudioContext => {
    if (!ctx.current) {
      ctx.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    if (ctx.current.state === 'suspended') {
      ctx.current.resume();
    }
    return ctx.current;
  };

  const play = (earcon: keyof typeof EARCON_SPEC) => {
    // 1. Respetar preferencias del usuario
    if (localStorage.getItem('itsme_sound') === 'off') return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    // 2. Síntesis programática — sin assets externos
    const ac = getCtx();
    const spec = EARCON_SPEC[earcon];
    // ... síntesis con OscillatorNode + GainNode
  };

  return { play };
};
```

### Timing de Sincronización con SOP_14

```
Spring Physics (SOP_14)     Audio Trigger (SOP_15)
──────────────────────────────────────────────────
hover  → translateY(-2px)    → ninguno (visual solo)
click  → scale(0.97)         → earcon.click (sync: 0ms delay)
        → translateY(0)
active → animation running   → earcon.loading (sync: 50ms delay)
resolve→ spring settle       → earcon.success (sync: on-complete)
error  → shake animation     → earcon.error (sync: 0ms delay)
```

---

## Canal 2 — Movimiento Cinematico

### Principios Cinematicos

El movimiento de alta fidelidad tiene **masa, inercia y peso**. Los objetos no "aparecen"
— entran con física, como objetos en el mundo real.

```
Objeto liviano (Badge, tooltip):
  spring: { stiffness: 600, damping: 25 }  → snappy, preciso

Objeto medio (Button, Card):
  spring: { stiffness: 400, damping: 30 }  → natural, fluido

Objeto pesado (Modal, Sheet, Panel):
  spring: { stiffness: 280, damping: 32 }  → grounded, premium

Objeto muy pesado (Page transition, Hero):
  spring: { stiffness: 200, damping: 28 }  → cinematico, con peso
```

### Choreography — Stagger Orquestado

```typescript
// Elementos hijos entran en secuencia — como una coreografía
const CHOREOGRAPHY = {
  list_item:    { stagger: 40ms,  base_delay: 0ms   },
  card_grid:    { stagger: 60ms,  base_delay: 80ms  },
  kpi_bento:    { stagger: 80ms,  base_delay: 100ms },
  form_fields:  { stagger: 50ms,  base_delay: 60ms  },
  modal_content:{ stagger: 30ms,  base_delay: 150ms },
};
```

### CSS Motion Cinematico

```css
/* Entrada cinematica — objetos con peso */
@keyframes cinematicEnter {
  0%   { opacity: 0; transform: translateY(24px) scale(0.94); filter: blur(3px); }
  60%  { opacity: 1; transform: translateY(-3px) scale(1.01); filter: blur(0); }
  80%  { transform: translateY(1px) scale(0.995); }
  100% { transform: translateY(0) scale(1); }
}

/* Salida cinematica */
@keyframes cinematicExit {
  0%   { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
  100% { opacity: 0; transform: translateY(-12px) scale(0.96); filter: blur(2px); }
}

/* Morph — elemento que cambia de estado */
@keyframes morphState {
  0%   { filter: blur(0) brightness(1); }
  30%  { filter: blur(1px) brightness(1.1); }
  100% { filter: blur(0) brightness(1); }
}
```

---

## Canal 3 — Feedback Háptico (Mobile)

### Web Vibration API

```typescript
// MAVIM SOP_15 — Haptic Patterns
const HAPTIC = {
  click:    () => navigator.vibrate?.(10),          // 10ms — light tap
  success:  () => navigator.vibrate?.([10, 50, 20]),// pattern: tap-pause-tap
  error:    () => navigator.vibrate?.([20, 30, 20, 30, 20]), // 3 pulsos error
  loading:  () => navigator.vibrate?.(5),           // barely perceptible
  complete: () => navigator.vibrate?.([5, 40, 10]), // subtle completion
};

// Solo activar en dispositivos táctiles
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
```

---

## Brand Identity — Sistema de Identidad Sensorial

### Vocabulario Sensorial del Producto

Cada producto debe definir su "voz sensorial" antes de implementar audio:

```markdown
## Voz Sensorial de [Producto]

Adjetivos clave: [preciso, cálido, sofisticado, rápido]
Anti-adjetivos:  [ruidoso, invasivo, genérico, distractivo]

Audio:
  Tono base: [A440 / 528Hz / 396Hz]
  Timbre: [sine=clínico/preciso | triangle=cálido | sawtooth=industrial]
  Volumen máximo: [0.15 — nunca disruptivo]

Motion:
  Estilo base: [cinematic | snappy | organic | mechanical]
  Spring base: [stiffness: X, damping: Y]

Haptic:
  Intensidad: [light | medium | none]
  Patrón: [single | double | pattern]
```

### Identidad Sonora de It's Me (Referencia)

```
Producto:     It's Me — Gestión Clínica
Tono base:    A4 (440Hz) y sus armónicos naturales (880, 1760)
Timbre:       Sine wave — clínico, preciso, limpio
Volumen:      0.06-0.12 — sutil como un estetoscopio
Asociación:   Precisión médica + calidez humana
Anti-patrón:  Sin sonidos de notificación genéricos (ding, beep)
```

---

## Reglas de Accesibilidad Sensorial

```
OBLIGATORIO:
✓ prefers-reduced-motion → desactivar animaciones cinematicas (mantener estado)
✓ prefers-reduced-motion → earcons silenciados automáticamente
✓ Sonido OFF por defecto en primer uso, ON solo tras gesto explícito
✓ Control visible de activar/desactivar sonido en UI
✓ Haptic solo en dispositivos táctiles, nunca en desktop

PROHIBIDO:
✗ Audio autoplay sin interacción del usuario (viola browser policy)
✗ Loops de sonido o música de fondo
✗ Sonidos > 200ms en micro-interacciones
✗ Haptic en acciones destructivas sin confirmación
✗ Earcons que interfieran con lectores de pantalla
```

---

## Sensory Check — Gate Final de Validación

Este gate se ejecuta DESPUÉS del Playwright smoke test (SOP_08), como paso final:

```
SENSORY CHECK PROTOCOL
─────────────────────
S01 — Audio hook no lanza errores en navegadores sin AudioContext
S02 — Earcons respetan localStorage 'sound_pref' === 'off'
S03 — prefers-reduced-motion desactiva earcons + animaciones cinematicas
S04 — AudioContext se inicializa lazy (no autoplay al cargar página)
S05 — Ganancia máxima de earcons ≤ 0.15 (medida en GainNode.gain.value)
S06 — Haptic solo se llama si navigator.vibrate está disponible
S07 — Control de sonido visible en UI (accesible con teclado)
S08 — Todas las animaciones cinematicas tienen duration < 700ms
```

```typescript
// Playwright Gate S01-S08
test('S01 — AudioContext no rompe en browsers sin soporte', async ({ page }) => {
  await page.evaluate(() => { (window as any).AudioContext = undefined; });
  await page.goto('/login');
  // No debe lanzar errores
});

test('S02 — Earcon silenciado si sound_pref = off', async ({ page }) => {
  await page.evaluate(() => localStorage.setItem('itsme_sound', 'off'));
  // Verificar que play() retorna inmediatamente sin crear AudioContext
});
```

---

## Integración con Skills

| Skill | Cuándo activar |
|-------|---------------|
| `animation-libraries-expert` | Para orquestar timing audio+motion (GSAP timeline) |
| `ui-ux-pro-max` | Para definir vocabulario sensorial del producto |
| `threejs-skills` | Para audio reactivo (AudioAnalyser + Three.js visualization) |

---

## Jerarquía en el Flujo MAVIM

```
SOP_09 → SOP_01 → SOP_02 → SOP_14 (Art Direction) → BUILD → SOP_15 (Sensory Layer)
                                                                    ↑
                                                          Post-visual, pre-release
```

SOP_15 se activa DESPUÉS de que SOP_14 está completo y los Playwright Gates 1-18 + A01-A07 pasan.

---

## Checklist de Cumplimiento

**Vocabulario Sensorial:**
- [ ] Voz sensorial del producto definida (tono, timbre, volumen, estilo motion)
- [ ] Earcon spec documentada (frecuencias, envelopes, timings)
- [ ] Verificado que audio no interfiere con lectores de pantalla

**Implementación Audio:**
- [ ] `useAudio.ts` hook implementado con Web Audio API
- [ ] AudioContext lazy-initialized (primer gesto del usuario)
- [ ] `localStorage` respetado para preferencia de sonido
- [ ] `prefers-reduced-motion` desactiva earcons
- [ ] Ganancia máxima ≤ 0.15
- [ ] Control de toggle en UI (accesible con teclado)

**Movimiento Cinematico:**
- [ ] Clases `cinematic-enter` / `cinematic-exit` definidas en CSS
- [ ] Choreography stagger aplicado en listas y grids
- [ ] Peso visual correcto por tipo de elemento (liviano/medio/pesado)

**Haptic:**
- [ ] `navigator.vibrate` con guard de disponibilidad
- [ ] Solo en dispositivos táctiles
- [ ] Patrones definidos en HAPTIC_SPEC

**Gates Playwright:**
- [ ] S01-S08 passing
- [ ] Gates A01-A07 (SOP_14) manteniendo passing
- [ ] Gates 1-18 (SOP_08) manteniendo 18/18

---

## Referencias

- `../core/SOP_14_HIGH_FIDELITY_UI_UX_MOTION.md` — Base visual (precede a SOP_15)
- `../core/SOP_08_AUTOMATED_TESTING.md` — Playwright gates base
- `../showcase/sensory-identity/` — Caso de éxito documentado
- Web Audio API: developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- Web Vibration API: developer.mozilla.org/en-US/docs/Web/API/Vibration_API
