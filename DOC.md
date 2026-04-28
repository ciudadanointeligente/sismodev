# Monitor o Sismo - Especificación Técnica

## 1. Concepto

Plataforma de monitoreo que analiza y clasifica leyes, noticias y eventos de un país específico según parámetros de derechos humanos y derechos democráticos. Utiliza LlamaParse para el procesamiento inteligente de documentos y clasificación automática.

## 2. Arquitectura General

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   APIs Públicas │────▶│   Django App     │────▶│   LlamaParse    │
│  (Legislación,  │     │  (Backend/API)   │     │(Análisis c/ LLM)│
│   Noticias)     │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   Frontend/API   │
                        │   (Dashboard)    │
                        └──────────────────┘
```

## 3. Estructura del Proyecto Django

```
monitor_leyes/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── legislation/          # Monitoreo de leyes
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services/
│   │   │   ├── api_clients/  # Clientes para APIs legislativas
│   │   │   └── parsers/      # Parsers específicos
│   │   └── tasks.py          # Tareas async
│   │
│   ├── news/                # Monitoreo de noticias
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services/
│   │   └── tasks.py
│   │
│   ├── events/               # Monitoreo de eventos
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services/
│   │   └── tasks.py
│   │
│   ├── analysis/             # Análisis con LlamaParse
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services/
│   │   │   └── llamaparse_service.py
│   │   └── classification.py # Clasificación derechos humanos/democráticos
│   │
│   └── dashboard/            # API pública del dashboard
│       ├── views.py
│       └── serializers.py
│
├── core/                     # Configuración compartida
│   ├── models.py
│   ├── api_clients/          # Clientes HTTP genéricos
│   ├── rate_limiter.py
│   └── validators.py
│
├── scripts/
│   └── fetch_data.py         # Script de fetch manual
│
├── tests/
│   ├── legislation/
│   ├── news/
│   ├── events/
│   └── analysis/
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## 4. Modelos de Datos

### 4.1 Legislation (Leyes)

```python
class Law:
    id: UUID
    title: str
    summary: str
    full_text: TextField
    law_number: str
    jurisdiction: str
    publication_date: date
    effective_date: date
    source_url: URL
    source_api: str
    status: str  # draft, published, repealed
    category: str
    raw_data: JSONField
    created_at: datetime
    updated_at: datetime

class LawAnalysis:
    id: UUID
    law: FK(Law)
    human_rights_score: float  # 0-100
    democratic_score: float   # 0-100
    concerns: JSONField
    recommendations: JSONField
    analyzed_at: datetime
    llamaparse_response: JSONField
```

### 4.2 News (Noticias)

```python
class NewsArticle:
    id: UUID
    title: str
    content: TextField
    summary: str
    source: str
    source_url: URL
    author: str
    published_at: datetime
    country: str
    tags: JSONField
    related_laws: ManyToMany(Law)
    raw_data: JSONField
    created_at: datetime

class NewsAnalysis:
    id: UUID
    article: FK(NewsArticle)
    human_rights_impact: float
    democratic_impact: float
    sentiment: str
    key_concerns: JSONField
    analyzed_at: datetime
```

### 4.3 Events (Eventos)

```python
class LegislativeEvent:
    id: UUID
    title: str
    description: TextField
    event_type: str  # vote, hearing, committee, etc.
    date: datetime
    location: str
    related_laws: ManyToMany(Law)
    participants: JSONField
    outcome: str
    source_url: URL
    raw_data: JSONField
    created_at: datetime
```

### 4.4 Clasificación de Derechos

```python
class HumanRightsParameter:
    id: UUID
    name: str
    description: str
    weight: float
    category: str  # civil, political, economic, social

class DemocraticParameter:
    id: UUID
    name: str
    description: str
    weight: float
    category: str  # participation, accountability, transparency
```

## 5. APIs Externas a Integrar

### 5.1 APIs Legislativas (ejemplo para Chile)

- **Micrositios Legislativos**: API del Congreso/Senado
- **Boletín Oficial**: API de publicación de leyes
- **INFOLEG**: Base de datos legislativa

### 5.2 APIs de Noticias

- **NewsAPI**: Agregador de noticias
- **GDELT**: Global Database of Events, Language, and Tone
- **Media Cloud**: Análisis de medios

### 5.3 Configuración de APIs

```python
# config/settings.py
EXTERNAL_APIS = {
    'legislation': {
        'api_name': 'api_leychile',
        'base_url': 'https://www.leychile.cl/Consulta/obtxml?opt=3&cantidad=5',
        'rate_limit': 30,  # requests per minute
        'auth_token': env('LEYCHILE_TOKEN'),
    },
    'news': {
        'api_name': 'newsapi',
        'base_url': 'https://newsapi.org/v2',
        'rate_limit': 100,
        'api_key': env('NEWSAPI_KEY'),
    },
    'gdelt': {
        'base_url': 'https://api.gdeltproject.org',
        'rate_limit': 1000,
    }
}
```

## 6. Servicio LlamaParse

### 6.1 Flujo de Análisis

```
1. Raw Content (PDF/HTML) → LlamaParse → Structured Text
2. Structured Text → Classification Engine
3. Classification → Human Rights Score (0-100)
4. Classification → Democratic Score (0-100)
5. Analysis Results → Stored in DB
```

### 6.2 Prompt de Clasificación

```python
ANALYSIS_PROMPT = """
Analiza el siguiente documento legislative/noticia/evento.
Evalúa según estos criterios de derechos humanos y democráticos:

DERECHOS HUMANOS:
- Derecho a la vida y integridad
- Libertad de expresión y prensa
- Derecho a la privacidad
- Acceso a la justicia
- No discriminación
- Derechos laborales
- Derecho a la educación y salud

DERECHOS DEMOCRÁTICOS:
- Participación ciudadana
- Transparencia governmental
- Rendición de cuentas
- Separación de poderes
- Estado de derecho
- Protección de minorías
- Libertad de asociación

Devuelve en JSON:
{
    "human_rights_score": 0-100,
    "democratic_score": 0-100,
    "violations_detected": ["lista"],
    "concerns": ["lista"],
    "recommendations": ["lista"]
}
"""
```

### 6.3 Implementación

```python
# apps/analysis/services/llamaparse_service.py
import httpx

class LlamaParseService:
    def __init__(self):
        self.api_key = settings.LLAMAPARSE_API_KEY
        self.base_url = "https://api.cloud.llamaparse.com"

    async def parse_document(self, file_url: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/parse",
                json={"url": file_url},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()

    async def analyze_content(self, content: str, parameters: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                json={
                    "content": content,
                    "prompt": ANALYSIS_PROMPT,
                    "parameters": parameters
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
```

## 7. API Endpoints

### 7.1 Laws

```
GET    /api/v1/laws/                  # Listar leyes
GET    /api/v1/laws/{id}/             # Detalle de ley
GET    /api/v1/laws/{id}/analysis/    # Análisis de ley
GET    /api/v1/laws/search/           # Búsqueda con filtros
POST   /api/v1/laws/{id}/reanalyze/   # Re-analizar
```

### 7.2 News

```
GET    /api/v1/news/                  # Listar noticias
GET    /api/v1/news/{id}/             # Detalle
GET    /api/v1/news/{id}/analysis/    # Análisis
GET    /api/v1/news/search/           # Búsqueda
```

### 7.3 Events

```
GET    /api/v1/events/                # Listar eventos
GET    /api/v1/events/{id}/           # Detalle
GET    /api/v1/events/calendar/       # Calendario de eventos
```

### 7.4 Analysis & Dashboard

```
GET    /api/v1/dashboard/summary/      # Resumen general
GET    /api/v1/dashboard/human-rights/ # Métricas derechos humanos
GET    /api/v1/dashboard/democratic/   # Métricas democráticas
GET    /api/v1/parameters/            # Parámetros de clasificación
```

## 8. Tareas Periódicas (Celery)

```python
# Fetch desde APIs cada hora
@celery_app.task
def fetch_legislation():
    """Obtiene nuevas leyes de APIs legislativas"""

@celery_app.task
def fetch_news():
    """Obtiene noticias del país seleccionado"""

@celery_app.task
def fetch_events():
    """Obtiene eventos legislativos"""

# Análisis asíncrono
@celery_app.task
def analyze_new_content():
    """Envía contenido nuevo a LlamaParse"""

# Limpieza
@celery_app.task
def cleanup_old_raw_data():
    """Elimina datos crudos después de 30 días"""
```

## 9. Variables de Entorno

```bash
# .env.example
DEBUG=True
COUNTRY=CL  # Código del país a monitorear

# APIs Externas
INFOLEG_TOKEN=
NEWSAPI_KEY=
GDELT_API_KEY=

# LlamaParse
LLAMAPARSE_API_KEY=

# Base de datos
DATABASE_URL=postgres://user:pass@localhost:5432/monitor_leyes

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

## 10. Stack Técnico

- **Backend**: Django 4.2+ + Django REST Framework
- **Base de datos**: PostgreSQL
- **Cache/Queue**: Redis + Celery
- **Análisis**: LlamaParse API
- **APIs externas**: httpx + asyncio
- **Frontend**: API REST (cliente externo)

## 11. Flujo de Datos Completo

```
1. Scheduler (Celery Beat) activa fetch_legislation/fetch_news/fetch_events
2. API clients obtienen datos de fuentes externas
3. Datos crudos se guardan en modelos raw_data JSONField
4. Se encola analyze_new_content para cada ítem nuevo
5. LlamaParse procesa y clasifica el contenido
6. Resultados de análisis se almacenan
7. Dashboard/API expone datos procesados
```
