import json
from langchain_ollama import OllamaEmbeddings
from src.db.connection import PostgresConnection
from src.utils import config


def main():
    # Cargar cursos desde JSON
    with open("src/scripts/cources.json", "r", encoding="utf-8") as f:
        courses = json.load(f)

    # Crear conexión a PostgreSQL
    pg_connection = PostgresConnection(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT
    )

    # Crear generador de embeddings
    embeddings_generator = OllamaEmbeddings(
        model="nomic-embed-text:v1.5", base_url="http://localhost:11434"
    )

    try:
        # Conectar a la base de datos
        pg_connection.connect()

        # Procesar cada curso
        for course in courses:
            # Generar embedding para el nombre del curso
            embedding = embeddings_generator.embed_documents(
                [course["name"]]
            )

            # Insertar en la base de datos
            query = """
                INSERT INTO mooc.courses (id, name, embedding)
                VALUES (%s, %s, %s);
            """
            pg_connection.execute_non_query(
                query, (course["id"], course["name"], json.dumps(embedding[0]))
            )

            print(f"Procesado curso: {course['name']}")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        # Cerrar conexión
        pg_connection.close()


if __name__ == "__main__":
    main()
