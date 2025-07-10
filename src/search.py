import json
import requests
from .PostgresConnection import PostgresConnection

# Configuración de la conexión a Postgres
pg_connection = PostgresConnection(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres',
)


# Función para obtener el embedding desde Ollama

def get_ollama_embedding(
    query: str,
    model: str = "nomic-embed-text",
    base_url: str = "http://localhost:11434"
):
    url = f"{base_url}/api/embeddings"
    payload = {
        "model": model,
        "prompt": query
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["embedding"]


# Función principal de búsqueda

def search(query: str):
    embedding = get_ollama_embedding(query)
    # La consulta usa el operador <=> de pgvector para similitud
    sql = (
        "SELECT name FROM mooc.courses "
        "ORDER BY embedding <=> %s "
        "LIMIT 10;"
    )
    # Asumimos que pg_connection.sql ejecuta la consulta
    # y retorna los resultados
    results = pg_connection.execute_query_sync(
        sql,
        (json.dumps(embedding),)
    )
    return results
