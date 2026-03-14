# MAVIM SOP 05: Resilience Phase

**Objetivo:** Garantizar que el sistema sobreviva a fallos transitorios en servicios externos o de Inteligencia Artificial (LLMs) sin degradar la experiencia del usuario y sin saturar los recursos del servidor.

## Protocolos de Resiliencia Obligatorios

Ninguna llamada a una API externa (especialmente a proveedores de LLM como OpenAI, Anthropic, Gemini o APIs de pago financiero) debe hacerse al descubierto.

### 1. Circuit Breakers (Cortacircuitos)
- Implementar el patrón **Circuit Breaker**. Si una API falla consecutivamente (ej. 3 veces seguidas), el circuito se "abre" y corta la comunicación temporalmente.
- En estado "Abierto", el sistema debe devolver un error inmediato (`503 Service Unavailable`) o utilizar un flujo de degradación de servicio (Fallback) en lugar de seguir esperando `timeouts` largos.

### 2. Retries con Backoff Exponencial
- Para errores transitorios de red (`429 Too Many Requests` o `502 Bad Gateway`), implementar un **Retry** automático.
- **Importante:** Utilizar **Backoff Exponencial con Jitter**. Si el LLM bloquea por cuota, no reintentar a velocidad fija. Reintenta a `1s`, luego a `2s`, `4s`, `8s`, sumando un factor aleatorio (Jitter) para no crear tormentas de reintentos sincrónicos ("Thundering Herd Problem").

### 3. Timeouts Estrictos
- Jamás permitir que el hilo de ejecución principal (Main Thread o Worker) se quede esperando infinitamente. 
- Toda solicitud a un External API o Base de Datos externa debe tener un `timeout` agresivo y configurado.

> [!CAUTION]
> Es vital que el `AI Gateway` maneje estas políticas de forma global, en lugar de esparcir bloques `try/catch` manuales en los controladores. NUNCA satures los Workers esperando la inferencia sincrónica de un LLM saturado.
