# services/chat_service.py
from typing import List
from src.services.search_service import SearchService
import requests
import traceback


class ChatService:
    """
    Service for handling chat interactions with RAG: obtiene contexto relevante
    y lo pasa a un modelo de lenguaje usando Ollama.
    """
    def __init__(self):
        self.search_service = SearchService()
        # Aquí podrías parametrizar el modelo y la URL de Ollama
        self.ollama_model = "gemma3:4b"
        self.ollama_url = "http://localhost:11434/api/generate"

    def get_response(self, messages: str) -> str:
        # 1. Obtener la última pregunta del usuario
        user_query = messages
        # 2. Buscar contexto relevante usando el servicio de búsqueda
        context = self.search_service.search(user_query)
        # 3. Pasar contexto y pregunta al modelo de lenguaje (Ollama)
        response = self._call_ollama_llm(user_query, context)
        return response

    def _call_ollama_llm(self, query: str, context: List[str]) -> str:
        # Construir el prompt con contexto
        context_str = "\n".join(context)
        prompt = (
            f"Contexto relevante:\n{context_str}\n"
            f"Pregunta del usuario: {query}\n"
            f"Responde de forma concisa y clara."
        )
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "[Sin respuesta del modelo]")
        except Exception as e:
            print("Error llamando a Ollama LLM:", e)
            print("Traceback:", traceback.format_exc())
            if 'response' in locals():
                print("Status code:", response.status_code)
                print("Response text:", response.text)
            print("Payload enviado:", payload)
            return "[Error al generar respuesta con el modelo]"
