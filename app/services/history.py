import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "chat_history.db"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            session   TEXT    NOT NULL,
            role      TEXT    NOT NULL,
            content   TEXT    NOT NULL,
            created   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    return conn


def get_history(session_id: str, limit: int = 20) -> list[dict]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT role, content FROM (
                SELECT role, content, created
                FROM messages
                WHERE session = ?
                ORDER BY created DESC
                LIMIT ?
            ) ORDER BY created ASC
            """,
            (session_id, limit),
        ).fetchall()
    return [{"role": row[0], "content": row[1]} for row in rows]


def save_message(session_id: str, role: str, content: str) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO messages (session, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )
        conn.commit()
