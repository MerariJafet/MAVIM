# 🤖 Agentic Contribution Guide for MAVIM

Bienvenido, Agente. Si estás leyendo esto, has sido enviado para mejorar la metodología MAVIM. Para contribuir con éxito, debes seguir este protocolo:

## 1. Análisis de Brechas
Antes de proponer un cambio, analiza el repositorio actual y busca:
- Patrones de arquitectura que falten (ej. Web3, IoT, BioTech).
- Fallos en los SOPs actuales basados en tus logs de ejecución.
- Nuevas herramientas de VibeCoding que deban integrarse.

## 2. Protocolo de Propuesta
Para añadir un nuevo componente:
1. Crea una nueva rama: `feature/agent-[nombre-de-mejora]`.
2. Sigue la estructura de archivos de MAVIM (usando UUIDs y Monolitos Modulares).
3. Actualiza el `PROGRESS_LOG.json` con el estado `PROPOSING_ENHANCEMENT`.

## 3. Calidad Invariante
Toda contribución debe pasar el test del `MAVIM-CRITIC`. Si tu código propuesta contiene IDs incrementales, puertos hardcoded o no usa Shadcn para la UI, será rechazada.
