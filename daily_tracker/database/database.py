"""
Maintain the backend SQLite database.
"""
import pathlib
import sqlite3


class DatabaseConnector:
    """Implements the `execute_file` method on a SQLite3 connection."""
    def __init__(self, filepath: str):
        self.filepath = pathlib.Path(filepath).resolve()
        self.connection = sqlite3.connect(self.filepath)
        self._create_table()

    def _create_table(self) -> None:
        """
        Create the tracker table if it doesn't already exist.
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
        with open(filepath, 'r') as f:
            return self.connection.executescript(f.read())
