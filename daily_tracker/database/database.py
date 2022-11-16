"""
Maintain the backend SQLite database.
"""
import pathlib
import sqlite3
from typing import Iterable


class DatabaseConnector:
    """Implements the `execute_file` method on a SQLite3 connection."""
    def __init__(self, filepath: str):
        self.filepath = pathlib.Path(filepath).resolve()
        self.connection = sqlite3.connect(self.filepath)
        self._create_backend()

    @property
    def engine(self) -> str:
        """
        The database connection to be used with Pandas and SQLAlchemy.
        """
        return r"sqlite:///" + str(self.filepath).replace("\\", r"/")

    def execute(self, sql: str, parameters: Iterable) -> sqlite3.Cursor:
        """
        Shortcut to the execute method on the SQLite connection object.
        """
        return self.connection.execute(sql, parameters)

    def _create_backend(self) -> None:
        """
        Create the backend if it doesn't already exist.
        """
        if not(
            self.connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = 'tracker'
                """
            ).fetchone()
        ):
            self.run_query_from_file("daily_tracker/database/create.sql")

    def run_query_from_file(self, filepath: str) -> sqlite3.Cursor:
        """
        Open a file and execute the query inside it.
        """
        with open(filepath, "r") as f:
            return self.connection.executescript(f.read())
