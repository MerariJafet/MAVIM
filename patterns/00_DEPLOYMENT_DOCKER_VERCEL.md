# Patrón 00: Deployment & Infrastructure (Zero to Prod)

**Objetivo:** Asegurar que el ciclo escrito por el agente termine con código vivo y accesible en internet (Production Ready), no solo durmiendo en un repositorio local.

## 1. Contenedores (El Backend)
Todo servidor, API, o Worker de procesamiento asíncrono (ej. Python FastAPI, Node/Express, Temporal Workers) DEBE estar Dockerizado desde el inicio.
- **Entregable:** Generar un `Dockerfile` optimizado (Multi-stage build).
- **Prohibido:** Copiar basura (`node_modules`, `.venv`). Se debe generar un `.dockerignore` estricto que excluya `.env` e historiales.

## 2. Edge / Serverless (El Frontend & Meta-Frameworks)
Para frameworks full-stack modernos como Next.js, Nuxt, o SvelteKit:
- **Entregable:** La configuración debe estar preparada para **Vercel** o plataformas Edge.
- El agente escribirá un `vercel.json` si se requieren reescrituras complejas o encabezados de seguridad CORS iniciales.

## 3. CI/CD Automático (Continuous Integration)
El repositorio NO está completo sin automatización de despliegues.
- **Entregable:** El agente debe crear el archivo `.github/workflows/deploy.yml` (o equivalente).
- **Regla:** El workflow debe incluir un paso de validación (`npm run typecheck`, `npm run lint`, `pytest`) ANTES de empujar la imagen al Registry o gatillar la API de despliegue de Vercel/Railway. Si la CI falla, el Critic bloqueará la entrega.
