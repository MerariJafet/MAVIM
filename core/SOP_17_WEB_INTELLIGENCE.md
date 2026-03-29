# MAVIM SOP 09: Web Intelligence (Scraping, Extracción y Análisis)

**Objetivo:** Proveer a los agentes MAVIM la capacidad de investigar, extraer información y analizar la estructura y diseño de páginas web como parte nativa del flujo de trabajo. Este SOP aplica tanto para investigación previa al diseño (MAVIM-Planner) como para extracción de datos en producción.

**Modelo Recomendado:** `claude-haiku-4-5-20251001` para extracción masiva. `claude-sonnet-4-6` para análisis y síntesis de lo extraído.

---

## Las 3 Modalidades de Web Intelligence

| Modalidad | Descripción | Rol MAVIM |
| :--- | :--- | :--- |
| **Research Mode** | Investigar tecnologías, competidores, librerías y benchmarks antes de diseñar | MAVIM-Planner |
| **Content Extraction** | Extraer texto, datos estructurados y metadatos de páginas web | MAVIM-Scraper (sub-rol) |
| **Design Analysis** | Extraer estructura visual, CSS, tipografía, colores y layout | MAVIM-Architect + Scraper |

---

## Arsenal de Herramientas Recomendadas (Investigación 2026)

### Categoría A: Open Source — AI-Optimizado (Recomendación Principal)

#### 1. Crawl4AI ⭐ (Mejor para agentes Claude locales)
- **Repo:** `github.com/unclecode/crawl4ai` — Apache 2.0, 62,800+ stars
- **Por qué MAVIM lo usa:** Produce "Fit Markdown" — contenido filtrado y listo para LLMs, sin ruido de navegación, ads ni boilerplate.
- **Capacidades clave:**
  - Extracción LLM-ready con filtrado BM25 automático
  - Soporte de JavaScript / SPAs con Playwright integrado
  - Extracción por CSS/XPath sin necesidad de LLM
  - Anti-bot bypass y gestión de pool de browsers
  - **MCP server oficial** — se conecta directamente a Claude Code via Docker
- **Instalación:**
  ```bash
  pip install crawl4ai
  crawl4ai-setup  # instala browser drivers
  ```
- **Uso básico:**
  ```python
  import asyncio
  from crawl4ai import AsyncWebCrawler

  async def scrape(url):
      async with AsyncWebCrawler() as crawler:
          result = await crawler.arun(url=url)
          return result.markdown  # Markdown limpio listo para el LLM
  ```

#### 2. Scrapling (Mejor para sitios que cambian estructura frecuentemente)
- **Repo:** `github.com/D4Vinci/Scrapling` — MIT, 20,000+ stars
- **Por qué MAVIM lo usa:** Tracking adaptativo de elementos — si el sitio cambia su HTML, el scraper se auto-ajusta.
- **Capacidades clave:**
  - Rastreo adaptativo de elementos (no falla con rediseños del sitio)
  - Bypass nativo de Cloudflare
  - **MCP server integrado** desde v0.4 (Feb 2026) — Claude, Cursor y otros lo usan directamente
- **Instalación:** `pip install scrapling`

#### 3. Playwright (Mejor para extracción de diseño y sites JS complejos)
- **Repo:** `github.com/microsoft/playwright-python` — Apache 2.0
- **Por qué MAVIM lo usa:** Acceso completo al DOM renderizado, estilos computados, geometría de layout y screenshots.
- **Capacidades clave:**
  - Extracción de estilos CSS computados: `page.eval_on_selector(el, "getComputedStyle(el)")`
  - Screenshots de alta fidelidad: `page.screenshot(full_page=True)`
  - Árbol de accesibilidad semántico: `page.accessibility.snapshot()`
  - Intercepción de red, emulación móvil
  - **MCP server oficial:** `@playwright/mcp` (npm)
- **Instalación:**
  ```bash
  pip install playwright
  playwright install chromium  # solo el browser necesario
  ```

#### 4. ScrapeGraphAI (Mejor para extracción en lenguaje natural)
- **Repo:** `github.com/ScrapeGraphAI/Scrapegraph-ai` — MIT
- **Por qué MAVIM lo usa:** Describe en lenguaje natural qué extraer — cero selectores CSS.
- **Capacidades clave:**
  - `SmartScraperGraph`: describe el dato en texto, apunta a una URL
  - Soporta OpenAI, Anthropic Claude, Ollama (modelos locales), Groq
  - **MCP server disponible** — Claude Desktop y Cursor lo consumen directamente
  - Usa Playwright internamente para rendering JS

#### 5. BeautifulSoup4 + HTTPX (Mejor para sitios estáticos simples)
- **Repo:** `pypi.org/project/beautifulsoup4` — MIT
- **Cuándo usarlo:** Sitios HTML estático sin JS. Más rápido y liviano que Playwright para estos casos.
- **Instalación:** `pip install beautifulsoup4 httpx`

---

### Categoría B: Servicios Gestionados (Cuando no quieres infraestructura)

#### Firecrawl (Primer integración oficial Claude MCP)
- **Repo MCP:** `github.com/firecrawl/firecrawl-mcp-server`
- **Plugin Claude Code:** `github.com/firecrawl/firecrawl-claude-plugin`
- **Licencia:** AGPL-3.0 (self-host) / API comercial gestionada
- **Capacidades:**
  - Convierte cualquier URL o sitio completo a Markdown limpio o JSON estructurado
  - Crawl completo de sitios + mapeo de subdominios
  - Navegación agéntica "FIRE-1" para sitios complejos
  - Anti-bot + proxy rotation integrados
- **Costo:** Free tier disponible; paid para volumen alto

#### Jina AI Reader (Más simple — zero setup)
- **Uso:** Prepend `r.jina.ai/` a cualquier URL
- **Ejemplo:** `curl https://r.jina.ai/https://ejemplo.com`
- **Cuándo:** Prototipos rápidos, una sola URL, sin configuración

---

## MCP Servers para Claude Code (Integración Nativa)

> Estos MCP servers permiten que Claude Code tenga capacidad de scraping **nativa** sin código adicional.

| MCP Server | Comando de Instalación | Notas |
| :--- | :--- | :--- |
| **Firecrawl MCP** | `claude mcp add firecrawl` | Managed; mejor para equipos sin infra |
| **Playwright MCP** | `npm install @playwright/mcp` | Open source; Microsoft oficial |
| **Crawl4AI MCP** | Docker: `docker run unclecode/crawl4ai` | Self-hosted; gratuito; mejor para local |
| **ScrapeGraphAI MCP** | `pip install scrapegraphai` | Extracción en lenguaje natural |
| **Scrapling MCP** | Built-in `scrapling --mcp` | Local; adaptativo; anti-bot |

---

## Protocolo de Extracción de Diseño Web (Design Extraction)

Para el caso de uso "analizar el diseño y estructura de una página web":

### Paso 1: Screenshot y Estructura Visual
```python
from playwright.async_api import async_playwright

async def extract_design(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Captura visual
        screenshot = await page.screenshot(full_page=True)

        # Estilos computados del body
        body_styles = await page.evaluate("""() => {
            const el = document.body;
            const cs = getComputedStyle(el);
            return {
                fontFamily: cs.fontFamily,
                fontSize: cs.fontSize,
                backgroundColor: cs.backgroundColor,
                color: cs.color,
                maxWidth: cs.maxWidth
            };
        }""")

        # Paleta de colores (todos los backgrounds del DOM)
        colors = await page.evaluate("""() => {
            const els = document.querySelectorAll('*');
            const colors = new Set();
            els.forEach(el => {
                const cs = getComputedStyle(el);
                if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') colors.add(cs.backgroundColor);
                if (cs.color) colors.add(cs.color);
            });
            return [...colors];
        }""")

        # Árbol semántico
        accessibility = await page.accessibility.snapshot()

        await browser.close()
        return {
            "screenshot": screenshot,
            "body_styles": body_styles,
            "color_palette": colors,
            "semantic_structure": accessibility
        }
```

### Paso 2: Análisis con Claude
Una vez extraído el diseño, enviarlo a Claude Sonnet para síntesis:
```
"Analiza los estilos computados y paleta de colores extraídos.
Identifica: design system subyacente (Material, Tailwind, Bootstrap),
paleta de colores primaria/secundaria/acento, tipografía, y
si hay componentes reutilizables identificables."
```

---

## Reglas de Uso Ético (Invariantes)

> [!CAUTION]
> El MAVIM-Critic rechazará cualquier implementación que viole estas reglas.

1. **`robots.txt` primero:** Antes de scraping masivo, verificar y respetar `https://sitio.com/robots.txt`.
2. **Rate limiting obligatorio:** Mínimo 1-2 segundos entre requests para no saturar servidores. Usar `asyncio.sleep()` o el throttling integrado de Crawl4AI/Scrapy.
3. **Sin datos personales:** No almacenar PII extraído de páginas públicas sin consentimiento.
4. **User-Agent honesto:** No impersonar otros browsers para evasión maliciosa. Si se necesita bypass de Cloudflare, usar herramientas con disclaimer ético (Scrapling, Crawl4AI).
5. **Uso académico/investigación:** Este módulo es para investigación, benchmarking, análisis de diseño y construcción de datasets propios. No para scraping masivo de competidores con fines de copia directa.

---

## Checklist del MAVIM-Critic para Web Intelligence

- [ ] ¿El scraper respeta `robots.txt` del dominio objetivo?
- [ ] ¿Hay rate limiting implementado?
- [ ] ¿Los datos extraídos son necesarios para la tarea y no incluyen PII innecesario?
- [ ] ¿El modelo usado es Haiku/Sonnet (no Opus) para extracción masiva?
- [ ] ¿Los resultados se guardan en un formato estructurado (`KNOWLEDGE_LOG.md` o JSON)?
- [ ] ¿El scraping se ejecuta de forma asíncrona para no bloquear el flujo principal?

---

## Integración con el Flujo MAVIM

```
MAVIM-Planner (Opus)
    └── Activa MAVIM-Scraper (Haiku) vía SOP_09
            ├── Investiga tecnologías / competidores
            ├── Extrae estructura y diseño de referencia
            └── Guarda en KNOWLEDGE_LOG.md
                    └── MAVIM-Architect (Opus) consume el log para tomar decisiones informadas
```
