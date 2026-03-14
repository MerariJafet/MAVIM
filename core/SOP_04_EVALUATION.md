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

### 4. Validación de Puente (The Smoke Test)
- **Regla Genérica:** El `CRITIC` tiene prohibido aprobar un proyecto si los módulos (ej. Front y Back) no se "saludan" entre sí.
- **Prueba Obligatoria:** Se debe ejecutar un Smoke Test de integración (vía script o comando de terminal) que valide que el punto A puede recibir una respuesta exitosa del punto B usando las variables expuestas en el Contrato de Entorno.

### 5. Evals (Métricas Automáticas)
- Implementación de pruebas automatizadas y métricas utilizando frameworks de evaluación para IA (ej. `DSPy`, `RAGAS`) para validar que el Quality Assurance es medible y consistente.
