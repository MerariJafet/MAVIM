# MAVIM Deployment: Zero to Production
El código debe estar listo para internet desde el minuto 1.

## 1. Dockerization
- Generar un `Dockerfile` multi-stage para producción (optimizado para tamaño).
- Crear un `docker-compose.yml` que levante la App + PostgreSQL + Redis localmente.

## 2. CI/CD (GitHub Actions)
- Crear `.github/workflows/deploy.yml` que ejecute:
  1. Linting y Tests.
  2. Build de producción.
  3. Despliegue automático a Vercel (Front) o Railway/Fly.io (Back).
