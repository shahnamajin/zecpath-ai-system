import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from security.audit_logger import AuditLogger
from security.access_control import AccessControl


def test_audit_event_is_persisted(tmp_path):
    db_path = tmp_path / "audit.db"
    logger = AuditLogger(db_path)

    logger.log_event(
        actor_id="USER_001",
        actor_role="recruiter",
        action="score.reviewed",
        resource_type="candidate",
        resource_id="CAND_001",
        metadata={"source": "screening"}
    )

    events = logger.get_events()

    assert len(events) == 1
    assert events[0]["action"] == "score.reviewed"


def test_sensitive_metadata_is_excluded(tmp_path):
    logger = AuditLogger(tmp_path / "audit.db")

    logger.log_event(
        actor_id="USER_001",
        actor_role="admin",
        action="report.generated",
        resource_type="report",
        metadata={
            "status": "completed",
            "transcript": "Sensitive candidate conversation"
        }
    )

    events = logger.get_events()

    assert "transcript" not in events[0]["metadata"]
    assert "completed" in events[0]["metadata"]


def test_recruiter_can_read_candidates():
    access = AccessControl()

    assert access.has_permission(
        "recruiter", "candidate.read"
    )


def test_candidate_cannot_manage_security():
    access = AccessControl()

    assert not access.has_permission(
        "candidate", "security.manage"
    )


def test_unauthorized_action_raises_error():
    access = AccessControl()

    with pytest.raises(PermissionError):
        access.require_permission(
            "candidate", "security.manage"
        )