from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import aiosqlite

@dataclass
class Reminder:
    id: str
    text: str
    due_at: datetime
    advisor: str
    source: str        # "conversation" | "manual" | "calendar"
    urgency: str       # "normal" | "urgent"
    sent: bool = False
    created_at: datetime = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class ReminderStore:
    """Async SQLite-backed reminder store."""
    
    def __init__(self, db_path: str = "data/scheduler.db"):
        self.db_path = db_path
    
    async def initialize(self) -> None:
        """Create tables if they don't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    due_at TEXT NOT NULL,
                    advisor TEXT NOT NULL,
                    source TEXT NOT NULL,
                    urgency TEXT NOT NULL DEFAULT 'normal',
                    sent INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            await db.commit()
    
    async def add(self, reminder: Reminder) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO reminders (id, text, due_at, advisor, source, urgency, sent, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (reminder.id, reminder.text, reminder.due_at.isoformat(),
                 reminder.advisor, reminder.source, reminder.urgency,
                 1 if reminder.sent else 0, reminder.created_at.isoformat())
            )
            await db.commit()
    
    async def get_due(self, now: datetime | None = None) -> list[Reminder]:
        """Return all unsent reminders due before now."""
        if now is None:
            now = datetime.utcnow()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM reminders WHERE sent=0 AND due_at <= ?",
                (now.isoformat(),)
            ) as cursor:
                rows = await cursor.fetchall()
        return [self._row_to_reminder(r) for r in rows]
    
    async def mark_sent(self, reminder_id: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE reminders SET sent=1 WHERE id=?", (reminder_id,))
            await db.commit()
    
    async def list_all(self, limit: int = 50) -> list[Reminder]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM reminders ORDER BY due_at DESC LIMIT ?", (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
        return [self._row_to_reminder(r) for r in rows]
    
    def _row_to_reminder(self, row: aiosqlite.Row) -> Reminder:
        return Reminder(
            id=row["id"],
            text=row["text"],
            due_at=datetime.fromisoformat(row["due_at"]),
            advisor=row["advisor"],
            source=row["source"],
            urgency=row["urgency"],
            sent=bool(row["sent"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )
