from fastapi import FastAPI, Body
from pydantic import BaseModel
from src.PostgresConnection import PostgresConnection
from langchain_ollama import OllamaEmbeddings
from src.search import search
from src.chat import chating_with_rag

app = FastAPI(
    title="RAG API", description="API para búsqueda de cursos", version="1.0.0"
)

# Instancia global de conexión a BD
pg_connection = PostgresConnection()
embeddings_generator = OllamaEmbeddings(
    model="nomic-embed-text", base_url="http://localhost:11434"
)


class QueryRequest(BaseModel):
    query: str


@app.on_event("startup")
async def startup_event():
    """Inicializar conexión a BD al inicio"""
    await pg_connection.connect_async()


@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar conexión a BD al finalizar"""
    await pg_connection.close_async()


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "RAG API funcionando"}


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "message": "API funcionando correctamente"}


@app.get("/search")
def search_endpoint(request: QueryRequest = Body(...)):
    """Endpoint para búsqueda de cursos usando embeddings"""
    results = search(request.query)
    return {"results": results}


@app.get("/chat")
def chat_endpoint(request: QueryRequest = Body(...)):
    """Endpoint para chat con RAG"""
    response = chating_with_rag(request.query)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
