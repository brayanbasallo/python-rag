import requests
from .search import search
import json


OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3n:e4b"


def chating_with_rag(query: str):
    chat_ollama_url = f"{OLLAMA_BASE_URL}/api/chat"
    results = search(query)
    print(results)
    cursos = ', '.join([result[0] for result in results])
    system_content = (
        "return only the answer"
        "You are a helpful assistant that can answer questions about the "
        "available courses: "
        f"{cursos} "
        "allways respond in markdown format and spanish language, "
        "if you don't know the answer, say you don't know and ask the user "
        "to provide more information"
    )
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": query}
    ]
    try:
        print("chatOllama")
        response = requests.post(
            chat_ollama_url,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages
            },
            timeout=6000
        )
        print("response (raw text)")
        print(response.text)
        # Procesar todas las líneas y concatenar los contenidos
        lines = response.text.strip().splitlines()
        content = ""
        for line in lines:
            try:
                data = json.loads(line)
                content += data.get("message", {}).get("content", "")
            except Exception as e:
                print(f"Error al parsear línea: {e}")
                continue
        print("response (final content)")
        print(content)
        return content
    except Exception as error:
        print(error)
        return {"content": "Error al procesar la consulta"}
