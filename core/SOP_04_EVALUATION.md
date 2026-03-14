# MAVIM SOP 04: Evaluation Phase (The Gatekeeper)

**Objetivo:** Actuar como el control de calidad final riguroso antes de que el usuario interactúe con el resultado o de que el código sea empujado y desplegado a producción.

## Checklist de Validación Obligatorio

El agente MAVIM-Critic o el evaluador automatizado debe validar los siguientes puntos:

### 1. UX/UI Check (Experiencia de Usuario)
- ¿La interfaz cumple con las heurísticas de usabilidad modernas?
- ¿Se han implementado indicadores visuales para estados de espera (loading spinners, skeletons)?
- ¿Se manejan y muestran mensajes de error claros y amigables para el usuario?

### 2. Security Check (Seguridad y Privacidad)
- ¿Existe algún riesgo de inyección de prompts (Prompt Injection) en las entradas de usuario?
- ¿Se están protegiendo o enmascarando los datos personales identificables (PII)?
- ¿Están correctamente implementados los guardrails contra extracciones indebidas de información?

### 3. Logic Check (Consistencia Funcional)
- ¿El código generado cumple al 100% con los requisitos estipulados originalmente en el `INTENT_MANIFEST.md`?

### 4. Evals (Métricas Automáticas)
- Implementación de pruebas automatizadas y métricas utilizando frameworks de evaluación para IA (ej. `DSPy`, `RAGAS`) para validar que el Quality Assurance es medible y consistente.
