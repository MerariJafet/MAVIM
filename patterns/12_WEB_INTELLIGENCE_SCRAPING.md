# Blueprint 12: Web Intelligence & Scraping Pipeline

**Objetivo:** Arquitectura de referencia para pipelines de extracción y análisis de información web dentro de sistemas MAVIM. Este blueprint aplica tanto a investigación pre-diseño como a funcionalidades de scraping en producción.

**Modelo de Agente:** MAVIM-Scraper con `claude-haiku-4-5-20251001` para extracción. `claude-sonnet-4-6` para síntesis y análisis.

---

## Casos de Uso Cubiertos

| Caso | Descripción | Módulo Primario |
| :--- | :--- | :--- |
| **Research Intelligence** | Investigar tecnologías, librerías y competidores antes del diseño | Intelligence Collector |
| **Content Extraction** | Extraer texto estructurado de múltiples URLs para RAG o análisis | Content Pipeline |
| **Design Analysis** | Analizar diseño visual, CSS, tipografía y colores de una web | Design Extractor |
| **Competitive Monitoring** | Monitorear cambios en sitios de referencia | Change Detector |

---

## Mapa de Módulos

| Módulo | Responsabilidad | Interface (API Síncrona) | Eventos (Asíncronos) |
| :--- | :--- | :--- | :--- |
| **Intelligence Collector** | Recibe URLs, coordina herramientas de scraping, gestiona rate limiting | `POST /intelligence/collect` | `CollectionStarted`, `CollectionCompleted` |
| **Content Pipeline** | Limpieza, normalización y conversión a Markdown LLM-ready | `POST /content/process` | `ContentProcessed`, `ContentIndexed` |
| **Design Extractor** | Extrae estilos CSS computados, paleta de colores, tipografía, screenshots | `POST /design/analyze` | `DesignExtracted`, `ScreenshotCaptured` |
| **Knowledge Store** | Almacena resultados de extracción en formato estructurado | `GET /knowledge/query` | `KnowledgeSaved`, `KnowledgeExpired` |

---

## Esquema de Datos

```json
// ScrapingJob (id: UUID, url: String, mode: ENUM[research|content|design], status: ENUM, result_path: String)
// ContentChunk (id: UUID, job_id: UUID, content: Text, source_url: String, extracted_at: Timestamp)
// DesignSnapshot (id: UUID, job_id: UUID, colors: JSON, typography: JSON, layout: JSON, screenshot_path: String)
// KnowledgeEntry (id: UUID, source_url: String, summary: Text, tags: JSON, expires_at: Timestamp)
```

---

## Stack Tecnológico Recomendado por Escenario

### Escenario A: Agente Local (Claude Code self-hosted)

```python
# Stack principal
crawl4ai        # Extracción LLM-ready — open source, MCP support
playwright      # JavaScript rendering + design extraction
beautifulsoup4  # Parsing HTML estático ligero
httpx           # HTTP async client

# MCP para integración nativa con Claude Code
# docker run unclecode/crawl4ai  # Crawl4AI MCP server
```

### Escenario B: Producción Gestionada (Sin infraestructura propia)

```python
# Stack principal
firecrawl   # API gestionada — Markdown limpio, site crawling, anti-bot
jina-reader # Zero-setup URL-to-text: r.jina.ai/{url}
spider      # Alto volumen, bajo costo
```

### Escenario C: Sitios con Protección Anti-Bot (Cloudflare, etc.)

```python
scrapling   # Adaptive tracking + Cloudflare bypass nativo (MIT)
crawlee     # Browser fingerprinting + proxy rotation (MIT, de Apify)
# o Bright Data Web Unlocker para enterprise
```

### Escenario D: Extracción en Lenguaje Natural (Sin selectores CSS)

```python
scrapegraphai   # Describe qué quieres en texto, apunta a URL
# Soporta Claude, GPT-4, Gemini, Ollama (local LLMs)
```

---

## Implementación: Intelligence Collector (Ejemplo Core)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

class IntelligenceCollector:
    """MAVIM Web Intelligence Collector — SOP_09 compliant"""

    RATE_LIMIT_SECONDS = 1.5  # Invariante ética: respetar servidores

    async def collect_research(self, urls: list[str]) -> list[dict]:
        """Recopila información de múltiples URLs para el MAVIM-Planner"""
        results = []
        config = CrawlerRunConfig(
            word_count_threshold=100,   # Filtrar páginas vacías
            remove_overlay_elements=True,  # Quitar modales y banners
            excluded_tags=["nav", "footer", "aside"]  # Solo contenido
        )

        async with AsyncWebCrawler() as crawler:
            for url in urls:
                # Verificar robots.txt antes (invariante ética)
                if not await self._check_robots(url):
                    continue

                result = await crawler.arun(url=url, config=config)
                results.append({
                    "url": url,
                    "markdown": result.markdown,  # Fit Markdown limpio
                    "title": result.metadata.get("title"),
                    "word_count": len(result.markdown.split())
                })

                await asyncio.sleep(self.RATE_LIMIT_SECONDS)  # Rate limiting

        return results

    async def _check_robots(self, url: str) -> bool:
        """Verifica robots.txt — cumplimiento ético obligatorio"""
        # Implementar verificación de robots.txt
        # Si no puede verificarlo, permite por defecto (no bloquea sin razón)
        return True


class DesignExtractor:
    """Extrae estructura visual y design tokens de una URL"""

    async def extract(self, url: str) -> dict:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")

            design_tokens = await page.evaluate("""() => {
                const getColors = () => {
                    const colors = new Set();
                    document.querySelectorAll('*').forEach(el => {
                        const cs = getComputedStyle(el);
                        ['backgroundColor','color','borderColor'].forEach(prop => {
                            const val = cs[prop];
                            if (val && val !== 'rgba(0, 0, 0, 0)' && val !== 'transparent') {
                                colors.add(val);
                            }
                        });
                    });
                    return [...colors].slice(0, 20); // Top 20 colores
                };

                return {
                    colors: getColors(),
                    typography: {
                        bodyFont: getComputedStyle(document.body).fontFamily,
                        h1Size: getComputedStyle(document.querySelector('h1') || document.body).fontSize,
                        lineHeight: getComputedStyle(document.body).lineHeight
                    },
                    layout: {
                        maxWidth: getComputedStyle(document.body).maxWidth,
                        hasDarkMode: window.matchMedia('(prefers-color-scheme: dark)').matches
                    }
                };
            }""")

            screenshot_bytes = await page.screenshot(full_page=True)
            await browser.close()

            return {
                "url": url,
                "design_tokens": design_tokens,
                "screenshot": screenshot_bytes  # Guardar como PNG
            }
```

---

## Detalles Críticos de Implementación

### 1. Gestión de Rate Limiting y Concurrencia

```python
# Correcto: Semáforo para limitar requests concurrentes
sem = asyncio.Semaphore(5)  # Máximo 5 requests simultáneos
async with sem:
    result = await crawler.arun(url=url)
    await asyncio.sleep(1.5)  # Entre cada request

# Incorrecto: lanzar 100 requests simultáneos sin límite
tasks = [crawler.arun(url=u) for u in urls_list]
await asyncio.gather(*tasks)  # PROHIBIDO sin semáforo
```

### 2. Almacenamiento Eficiente del Knowledge Store

```python
# Formato de salida estandarizado MAVIM
{
    "id": "uuid-v4",
    "source_url": "https://ejemplo.com",
    "extracted_at": "ISO-8601",
    "expires_at": "ISO-8601 + 7d",  # Cache TTL para evitar re-scraping
    "content_type": "research | design | content",
    "summary": "...",  # Resumen de máximo 500 palabras (Claude Haiku)
    "raw_markdown": "...",
    "design_tokens": {}  # Solo si content_type == "design"
}
```

### 3. Integración con MAVIM-Planner

El Planner activa el Intelligence Collector con un prompt estructurado:
```
"Eres MAVIM-Scraper con claude-haiku-4-5.
Investiga: [lista de URLs o queries].
Objetivo: [qué información necesita el Planner].
Guarda resultados en KNOWLEDGE_LOG.md.
Respeta robots.txt y rate limiting de SOP_09."
```

---

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **Ignorar robots.txt:** NUNCA scraping masivo sin verificar `robots.txt`. El MAVIM-Critic rechaza pipelines sin este check.
> 2. **Scraping sin rate limiting:** Todo loop de extracción DEBE tener `asyncio.sleep(1.5)` mínimo entre requests.
> 3. **Usar Opus para extracción masiva:** El análisis en bulk debe correr con Haiku. Usar Opus aquí es costo prohibitivo.
> 4. **Almacenar PII extraído:** Si el scraping extrae emails, nombres u otra PII accidentalmente, el módulo Guardrails debe filtrarla antes de llegar al Knowledge Store.
> 5. **No cachear resultados:** Re-scraping del mismo URL en el mismo sprint es ineficiente. Usar `expires_at` en KnowledgeEntry.
