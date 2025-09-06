# services/search_service.py
import json
import requests
from typing import List
from src.db.connection import PostgresConnection
from src.utils import config
import logging


class SearchService:
    """
    Service for handling search queries using embeddings and pgvector.
    """
    def __init__(self):
        self.pg_connection = PostgresConnection(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )

    def get_ollama_embedding(
        self,
        query: str,
        model: str = "nomic-embed-text:v1.5",
        base_url: str = "http://localhost:11434"
    ) -> List[float]:
        url = f"{base_url}/api/embeddings"
        payload = {
            "model": model,
            "prompt": query
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["embedding"]
        except Exception as e:
            logging.error(f"Error getting embedding from Ollama: {e}")
            raise

    def search(self, query: str) -> List[str]:
        embedding = self.get_ollama_embedding(query)
        print(embedding)
        sql = (
            "SELECT name FROM mooc.courses "
            "ORDER BY embedding <=> %s "
            "LIMIT 10;"
        )
        try:
            results = self.pg_connection.execute_query(
                sql,
                (json.dumps(embedding),)
            )
            # Extraer solo los nombres de los resultados
            return [row["name"] for row in results]
        except Exception as e:
            logging.error(f"Error searching courses: {e}")
            return []
