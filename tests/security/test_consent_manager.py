import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from security.consent_manager import ConsentManager


def test_consent_can_be_granted(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    manager.grant_consent("CAND_001", "ai_screening")

    assert manager.has_consent("CAND_001", "ai_screening")


def test_consent_can_be_withdrawn(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    manager.grant_consent("CAND_001", "ai_screening")
    manager.withdraw_consent("CAND_001", "ai_screening")

    assert not manager.has_consent("CAND_001", "ai_screening")


def test_withdrawal_preserves_history(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    manager.grant_consent("CAND_001", "ai_screening")
    manager.withdraw_consent("CAND_001", "ai_screening")

    history = manager.get_consent_history(
        "CAND_001", "ai_screening"
    )

    assert len(history) == 2
    assert history[0]["status"] == "granted"
    assert history[1]["status"] == "withdrawn"


def test_consent_not_granted_by_default(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    assert not manager.has_consent(
        "CAND_001", "ai_screening"
    )


def test_withdrawal_without_consent_fails(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    with pytest.raises(ValueError):
        manager.withdraw_consent("CAND_001", "ai_screening")


def test_empty_candidate_id_is_rejected(tmp_path):
    manager = ConsentManager(tmp_path / "consent.db")

    with pytest.raises(ValueError):
        manager.grant_consent("", "ai_screening")
