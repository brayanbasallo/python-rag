import json
import asyncio
from langchain_ollama import OllamaEmbeddings
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.PostgresConnection import PostgresConnection


async def main():
    # Cargar cursos desde JSON
    with open("src/scripts/cources.json", "r", encoding="utf-8") as f:
        courses = json.load(f)

    # Crear conexión a PostgreSQL
    pg_connection = PostgresConnection()

    # Crear generador de embeddings
    embeddings_generator = OllamaEmbeddings(
        model="nomic-embed-text", base_url="http://localhost:11434"
    )

    try:
        # Conectar a la base de datos
        await pg_connection.connect_async()

        # Procesar cada curso
        for course in courses:
            # Generar embedding para el nombre del curso
            embedding = await embeddings_generator.aembed_documents(
                    [course["name"]]
                )

            # Insertar en la base de datos
            query = """
                INSERT INTO mooc.courses (id, name, embedding)
                VALUES ($1, $2, $3);
            """
            await pg_connection.execute_query_async(
                query, (course["id"], course["name"], json.dumps(embedding[0]))
            )

            print(f"Procesado curso: {course['name']}")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        # Cerrar conexión
        await pg_connection.close_async()


if __name__ == "__main__":
    asyncio.run(main())
