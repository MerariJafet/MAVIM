# MAVIM Showcase — Casos de Éxito

Esta carpeta documenta implementaciones reales de MAVIM en producción.
Cada caso incluye: mapa de impacto, resultados de tests, changelog automatizado
y materiales de comunicación.

---

## Casos Documentados

### [It's Me — Fases 14–16](./itsme-phase14-16/)
**SaaS Clínico Multi-Tenant | React 18 + FastAPI + PostgreSQL**

La primera implementación documentada del ciclo completo de MAVIM:
desde deuda técnica crítica hasta sistema profesional con auto-validación.

| Archivo | Contenido |
|---------|-----------|
| [CASE_STUDY.md](./itsme-phase14-16/CASE_STUDY.md) | Caso de éxito completo con diagnóstico, cirugía y resultados |
| [IMPACT_MAP.json](./itsme-phase14-16/IMPACT_MAP.json) | Mapa de dependencias pre-cirugía (SOP_07) |
| [PLAYWRIGHT_RESULTS.md](./itsme-phase14-16/PLAYWRIGHT_RESULTS.md) | 18/18 gates + historial del bucle de auto-mejora |
| [CHANGELOG.md](./itsme-phase14-16/CHANGELOG.md) | Evolución completa Fase 14→16 |
| [SOCIAL_POST_DRAFTS.md](./itsme-phase14-16/SOCIAL_POST_DRAFTS.md) | 5 posts para Twitter, LinkedIn, Reddit, Newsletter |

**Resultado clave:** Playwright detectó y corrigió automáticamente un bug de dark mode
en el componente Badge en < 2 minutos — sin intervención humana.

---

## Contribuir un Caso

¿Usaste MAVIM en tu proyecto? Documenta el caso:

```
showcase/
└── tu-proyecto-nombre/
    ├── CASE_STUDY.md        # Diagnóstico + cirugía + resultados
    ├── IMPACT_MAP.json      # Mapa de dependencias pre-surgery
    ├── PLAYWRIGHT_RESULTS.md # Resultados de tests
    └── CHANGELOG.md         # Evolución del proyecto
```

Abre un PR con el título: `showcase: [nombre-proyecto] — [descripción breve]`
