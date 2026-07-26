import sqlite3
from pathlib import Path
from typing import Any, Optional


class DBService:
    def __init__(self, db_path: str = "./data/chess/chess.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS elo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uin INTEGER UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    rate INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS pgn (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    white_uin INTEGER NOT NULL,
                    black_uin INTEGER NOT NULL,
                    white_name TEXT NOT NULL,
                    black_name TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()

    def create_elo(self, uin: int, name: str, rate: int = 500) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO elo (uin, name, rate)
                VALUES (?, ?, ?)
                ON CONFLICT(uin) DO UPDATE SET
                    name=excluded.name,
                    rate=excluded.rate,
                    updated_at=CURRENT_TIMESTAMP;
                """,
                (uin, name, rate),
            )
            conn.commit()

    def get_elo_rate_by_uin(self, uin: int) -> Optional[int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT rate FROM elo WHERE uin = ?", (uin,))
            row = cursor.fetchone()
            return row["rate"] if row else None

    def get_highest_rate_list(self) -> list[dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, rate FROM elo ORDER BY rate DESC LIMIT 10"
            )
            rows = cursor.fetchall()
            return [{"name": row["name"], "rate": row["rate"]} for row in rows]

    def update_elo_by_uin(self, uin: int, name: str, rate: int) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE elo
                SET name = ?, rate = ?, updated_at = CURRENT_TIMESTAMP
                WHERE uin = ?
                """,
                (name, rate, uin),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    """
                    INSERT INTO elo (uin, name, rate)
                    VALUES (?, ?, ?)
                    """,
                    (uin, name, rate),
                )
            conn.commit()

    def clean_elo_by_uin(self, uin: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE elo
                SET rate = 100, updated_at = CURRENT_TIMESTAMP
                WHERE uin = ?
                """,
                (uin,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def create_pgn(
        self,
        data: str,
        white_uin: int,
        black_uin: int,
        white_name: str,
        black_name: str,
    ) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pgn (data, white_uin, black_uin, white_name, black_name)
                VALUES (?, ?, ?, ?, ?)
                """,
                (data, white_uin, black_uin, white_name, black_name),
            )
            conn.commit()
