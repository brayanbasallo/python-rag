# db/connection.py

import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, List, Optional


class PostgresConnection:
    """
    Manages PostgreSQL database connections and queries.
    """
    def __init__(
        self, host: str, database: str, user: str, password: str,
        port: int = 5432
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self) -> None:
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            logging.info("PostgreSQL connection established.")
        except Exception as e:
            logging.error(f"Error connecting to PostgreSQL: {e}")
            raise

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            logging.info("PostgreSQL connection closed.")

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Any]:
        if not self.connection:
            self.connect()
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result

    def execute_non_query(
        self, query: str, params: Optional[tuple] = None
    ) -> None:
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
