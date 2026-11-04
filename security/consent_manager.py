import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = PROJECT_ROOT / "data" / "security" / "consent.db"


class ConsentManager:

    def __init__(self, database_path=None):
        self.database_path = Path(database_path or DEFAULT_DB)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS consent_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('granted', 'withdrawn')),
                    timestamp TEXT NOT NULL
                )
            """)

    def _validate(self, candidate_id, purpose):
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("candidate_id must be a non-empty string.")

        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("purpose must be a non-empty string.")

    def _record_event(self, candidate_id, purpose, status):
        self._validate(candidate_id, purpose)
        timestamp = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                INSERT INTO consent_events (
                    candidate_id, purpose, status, timestamp
                )
                VALUES (?, ?, ?, ?)
            """, (candidate_id, purpose, status, timestamp))

        return timestamp

    def grant_consent(self, candidate_id, purpose):
        return self._record_event(candidate_id, purpose, "granted")

    def withdraw_consent(self, candidate_id, purpose):
        if not self.has_consent(candidate_id, purpose):
            raise ValueError("No active consent exists for this purpose.")

        return self._record_event(candidate_id, purpose, "withdrawn")

    def has_consent(self, candidate_id, purpose):
        self._validate(candidate_id, purpose)

        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute("""
                SELECT status
                FROM consent_events
                WHERE candidate_id = ? AND purpose = ?
                ORDER BY id DESC
                LIMIT 1
            """, (candidate_id, purpose)).fetchone()

        return row is not None and row[0] == "granted"

    def get_consent_history(self, candidate_id, purpose):
        self._validate(candidate_id, purpose)

        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute("""
                SELECT candidate_id, purpose, status, timestamp
                FROM consent_events
                WHERE candidate_id = ? AND purpose = ?
                ORDER BY id ASC
            """, (candidate_id, purpose)).fetchall()

        return [dict(row) for row in rows]
