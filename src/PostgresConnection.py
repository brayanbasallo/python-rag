import asyncpg
import psycopg2
from typing import Optional
import os


class PostgresConnection:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres",
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.async_connection = None

    def get_connection_string(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )

    def connect_sync(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            return self.connection
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    async def connect_async(self):
        try:
            self.async_connection = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            return self.async_connection
        except asyncpg.PostgresError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def close_sync(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    async def close_async(self):
        if self.async_connection:
            await self.async_connection.close()
            self.async_connection = None

    def execute_query_sync(self, query: str, params: Optional[tuple] = None):
        if not self.connection:
            self.connect_sync()

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount

    async def execute_query_async(
        self,
        query: str,
        params: Optional[tuple] = None,
    ) -> Optional[asyncpg.Record | int]:
        if not self.async_connection:
            await self.connect_async()

        if query.strip().upper().startswith("SELECT"):
            return await self.async_connection.fetch(
                query, *params if params else ()
                )
        else:
            return await self.async_connection.execute(
                query, *params if params else ()
                )

    @classmethod
    def from_env(cls) -> "PostgresConnection":
        return cls(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        )
