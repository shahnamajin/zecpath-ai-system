import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = PROJECT_ROOT / "logs" / "security_audit.db"

SENSITIVE_KEYS = {
    "password", "token", "secret", "resume_text",
    "transcript", "raw_answer", "email", "phone", "address"
}


class AuditLogger:

    def __init__(self, database_path=None):
        self.database_path = Path(database_path or DEFAULT_DB)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actor_id TEXT NOT NULL,
                    actor_role TEXT NOT NULL,
                    action TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT,
                    outcome TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT
                )
            """)

    def _sanitize_metadata(self, metadata):
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary.")

        sanitized = {}

        for key, value in metadata.items():
            if key.lower() in SENSITIVE_KEYS:
                continue

            if isinstance(value, (str, int, float, bool)) or value is None:
                sanitized[key] = value
            else:
                sanitized[key] = "[omitted]"

        return sanitized

    def log_event(
        self,
        actor_id,
        actor_role,
        action,
        resource_type,
        resource_id=None,
        outcome="success",
        metadata=None
    ):
        required = {
            "actor_id": actor_id,
            "actor_role": actor_role,
            "action": action,
            "resource_type": resource_type,
            "outcome": outcome
        }

        for field, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be a non-empty string.")

        if resource_id is not None and not isinstance(resource_id, str):
            raise ValueError("resource_id must be a string or None.")

        safe_metadata = self._sanitize_metadata(metadata or {})
        timestamp = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                INSERT INTO audit_events (
                    actor_id, actor_role, action, resource_type,
                    resource_id, outcome, timestamp, metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                actor_id,
                actor_role,
                action,
                resource_type,
                resource_id,
                outcome,
                timestamp,
                json.dumps(safe_metadata)
            ))

        return timestamp

    def get_events(self, limit=100):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer.")

        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT * FROM audit_events
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()

        return [dict(row) for row in rows]
