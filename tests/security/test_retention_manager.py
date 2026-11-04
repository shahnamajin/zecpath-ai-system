import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import json
import pytest

from security.retention_manager import RetentionManager


def create_policy(tmp_path, days=30, enabled=False):
    policy = {
        "retention": {
            "resume_days": days,
            "delete_expired_records": enabled
        }
    }

    path = tmp_path / "policy.json"
    path.write_text(json.dumps(policy), encoding="utf-8")
    return path


def test_unset_retention_does_not_expire_records(tmp_path):
    path = create_policy(tmp_path, days=None)
    manager = RetentionManager(path)

    assert manager.get_retention_days("resume") is None


def test_old_record_is_expired(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30)
    )

    created = datetime.now(timezone.utc) - timedelta(days=40)

    assert manager.is_expired(
        "resume", created.isoformat()
    )


def test_recent_record_is_retained(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30)
    )

    created = datetime.now(timezone.utc) - timedelta(days=5)

    assert not manager.is_expired(
        "resume", created.isoformat()
    )


def test_evaluate_records_counts_correctly(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30)
    )

    now = datetime.now(timezone.utc)

    records = [
        {"id": "OLD", "created_at": (now - timedelta(days=40)).isoformat()},
        {"id": "NEW", "created_at": (now - timedelta(days=5)).isoformat()}
    ]

    result = manager.evaluate_records("resume", records)

    assert result["expired_count"] == 1
    assert result["retained_count"] == 1


def test_dry_run_does_not_delete(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30)
    )

    evaluation = {
        "expired_records": [{"id": "OLD"}]
    }

    result = manager.delete_expired(evaluation, dry_run=True)

    assert result["dry_run"] is True
    assert result["deleted"] is False
    assert result["eligible_count"] == 1


def test_automatic_deletion_is_disabled(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30, enabled=False)
    )

    with pytest.raises(PermissionError):
        manager.delete_expired(
            {"expired_records": [{"id": "OLD"}]},
            dry_run=False
        )


def test_naive_timestamp_is_rejected(tmp_path):
    manager = RetentionManager(
        create_policy(tmp_path, days=30)
    )

    with pytest.raises(ValueError):
        manager.is_expired(
            "resume", "2026-01-01T00:00:00"
        )
