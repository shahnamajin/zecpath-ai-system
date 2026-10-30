import copy
import json
import pytest

from screening_ai.ethics_utils import (
    load_ethics_policy,
    remove_demographic_fields,
    validate_retention_policy,
)


def test_policy_loads_and_has_pending_review_status():
    policy = load_ethics_policy()

    assert policy["review_day"] == 43
    assert policy["compliance"]["status"] == "pending_review"


def test_demographic_fields_are_removed():
    candidate = {
        "candidate_id": "TEST-001",
        "skills": ["Python", "SQL"],
        "race": "example",
        "religion": "example",
        "date_of_birth": "2000-01-01",
    }

    cleaned = remove_demographic_fields(candidate)

    assert "race" not in cleaned
    assert "religion" not in cleaned
    assert "date_of_birth" not in cleaned
    assert cleaned["skills"] == ["Python", "SQL"]


def test_nested_demographic_fields_are_removed():
    candidate = {
        "candidate_id": "TEST-002",
        "profile": {
            "gender_identity": "example",
            "skills": ["Python"],
        },
    }

    cleaned = remove_demographic_fields(candidate)

    assert "gender_identity" not in cleaned["profile"]
    assert cleaned["profile"]["skills"] == ["Python"]


def test_original_candidate_is_not_modified():
    candidate = {
        "candidate_id": "TEST-003",
        "sex": "example",
        "skills": ["Python"],
    }
    original = copy.deepcopy(candidate)

    remove_demographic_fields(candidate)

    assert candidate == original


def test_non_dictionary_candidate_is_rejected():
    with pytest.raises(ValueError):
        remove_demographic_fields(["Python"])


def test_unset_retention_period_is_rejected():
    policy = load_ethics_policy()

    with pytest.raises(ValueError, match="retention_days"):
        validate_retention_policy(policy)


def test_positive_retention_period_is_accepted():
    policy = load_ethics_policy()
    policy["data_retention"]["retention_days"] = 365

    assert validate_retention_policy(policy) == 365
