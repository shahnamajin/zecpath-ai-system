import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POLICY = PROJECT_ROOT / "config" / "security_policy.json"


class RetentionManager:

    def __init__(self, policy_path=None):
        path = Path(policy_path or DEFAULT_POLICY)

        with open(path, "r", encoding="utf-8-sig") as file:
            self.policy = json.load(file)

        self.retention = self.policy.get("retention", {})

    def get_retention_days(self, category):
        days = self.retention.get(f"{category}_days")

        if days is None:
            return None

        if isinstance(days, bool) or not isinstance(days, int) or days < 0:
            raise ValueError(
                f"Invalid retention period for {category}."
            )

        return days

    def is_expired(self, category, created_at, reference_time=None):
        days = self.get_retention_days(category)

        if days is None:
            return False

        try:
            created = datetime.fromisoformat(created_at)
        except (TypeError, ValueError):
            raise ValueError("created_at must be a valid ISO timestamp.")

        if created.tzinfo is None:
            raise ValueError("created_at must include timezone information.")

        now = reference_time or datetime.now(timezone.utc)

        if now.tzinfo is None:
            raise ValueError("reference_time must include timezone information.")

        return now >= created + timedelta(days=days)

    def evaluate_records(self, category, records, reference_time=None):
        if not isinstance(records, list):
            raise ValueError("records must be a list.")

        expired = []
        retained = []

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each record must be a dictionary.")

            if "created_at" not in record:
                raise ValueError("Record is missing created_at.")

            if self.is_expired(
                category,
                record["created_at"],
                reference_time
            ):
                expired.append(record)
            else:
                retained.append(record)

        return {
            "category": category,
            "retention_days": self.get_retention_days(category),
            "expired_count": len(expired),
            "retained_count": len(retained),
            "expired_records": expired,
            "retained_records": retained,
            "deletion_enabled": self.retention.get(
                "delete_expired_records", False
            )
        }

    def delete_expired(self, evaluation, dry_run=True):
        if not isinstance(evaluation, dict):
            raise ValueError("evaluation must be a dictionary.")

        expired = evaluation.get("expired_records")

        if not isinstance(expired, list):
            raise ValueError("Invalid retention evaluation.")

        if dry_run:
            return {
                "deleted": False,
                "dry_run": True,
                "eligible_count": len(expired)
            }

        if not self.retention.get("delete_expired_records", False):
            raise PermissionError(
                "Automatic deletion is disabled in the retention policy."
            )

        # This manager only evaluates records.
        # Actual deletion must be implemented by the owning storage system.
        raise NotImplementedError(
            "Connect deletion to the relevant storage backend before enabling it."
        )
