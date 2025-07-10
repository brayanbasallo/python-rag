# RAG: Retrieval-Augmented Generation con FastAPI, Ollama y PostgreSQL/pgvector

Este proyecto implementa un sistema de chat y búsqueda de cursos usando RAG (Retrieval-Augmented Generation), combinando FastAPI, Ollama (modelos LLM locales) y PostgreSQL con la extensión pgvector para búsquedas semánticas.

## Características

- **Chat inteligente**: Responde preguntas usando contexto relevante de una base de datos de cursos.
- **Búsqueda semántica**: Encuentra cursos similares usando embeddings y pgvector.
- **Embeddings locales**: Generación de embeddings y respuestas usando Ollama.
- **API REST**: Endpoints para chat y búsqueda.
- **Base de datos PostgreSQL**: Almacena cursos y sus embeddings vectoriales.

## Requisitos

- Python 3.13+
- Docker y Docker Compose (para la base de datos)
- Ollama instalado y corriendo localmente ([ver documentación oficial](https://ollama.com/))
- PostgreSQL con extensión pgvector

## Instalación

1. **Clona el repositorio**  
   ```bash
   git remote add origin git@github.com:brayanbasallo/python-rag.git
   cd python-rag
   ```

2. **Crea y activa un entorno virtual**  
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias**  
   ```bash
   pip install -r requirements.txt
   # O usando poetry/pdm si lo prefieres
   ```

4. **Levanta la base de datos con pgvector**  
   ```bash
   docker compose up -d
   ```

5. **Carga los datos de ejemplo**  
   ```bash
   python src/scripts/create_data.py
   ```

6. **Asegúrate de que Ollama esté corriendo**  
   ```bash
   ollama serve
   # Y que tengas el modelo necesario descargado, por ejemplo:
   ollama pull gemma3n:e4b
   ```

7. **Configura las variables de entorno** (opcional, ver `src/utils/config.py` para los defaults)

## Uso

### Ejecutar la API

```bash
uvicorn src.main:app --reload
```

La API estará disponible en [http://localhost:8000](http://localhost:8000).

### Endpoints principales

- `GET /chat`  
  **Body:**  
  ```json
  {
    "messages": "¿Qué cursos de PHP hay?"
  }
  ```
  **Respuesta:**  
  ```json
  {
    "response": "..."
  }
  ```

- `GET /search`  
  **Body:**  
  ```json
  {
    "query": "php"
  }
  ```
  **Respuesta:**  
  ```json
  {
    "results": ["Curso 1", "Curso 2", ...]
  }
  ```

## Estructura del proyecto

```
rag/
├── compose.yml
├── databases/
│   ├── 0-enable-pgvector.sql
│   └── 1-mooc.sql
├── src/
│   ├── api/
│   ├── db/
│   ├── scripts/
│   ├── services/
│   └── utils/
├── pyproject.toml
└── README.md
```

## Notas

- El modelo y la URL de Ollama se pueden parametrizar en `src/services/chat_service.py`.
- Los cursos de ejemplo están en `src/scripts/cources.json`.
- La base de datos se inicializa automáticamente con Docker Compose y los scripts SQL en `databases/`.

## Licencia

MIT


