import logging
from pathlib import Path

import aiosqlite

DB_PATH = Path(__file__).parent.parent.parent / "chat_history.db"

logger = logging.getLogger(__name__)

_db: aiosqlite.Connection | None = None


async def init_db() -> None:
    global _db
    _db = await aiosqlite.connect(DB_PATH)
    await _db.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            session TEXT    NOT NULL,
            role    TEXT    NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT    NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    await _db.execute(
        "CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session)"
    )
    await _db.commit()
    logger.info("Database initialised at %s", DB_PATH)


async def close_db() -> None:
    global _db
    if _db:
        await _db.close()
        _db = None


async def get_history(session_id: str, limit: int = 20) -> list[dict]:
    assert _db is not None, "Database not initialised"
    async with _db.execute(
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
    ) as cursor:
        rows = await cursor.fetchall()
    return [{"role": row[0], "content": row[1]} for row in rows]


async def save_message(session_id: str, role: str, content: str) -> None:
    assert _db is not None, "Database not initialised"
    await _db.execute(
        "INSERT INTO messages (session, role, content) VALUES (?, ?, ?)",
        (session_id, role, content),
    )
    await _db.commit()
