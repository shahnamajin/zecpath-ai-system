import pytest

from hiring_ai.final_recommendation_engine import (
    FinalRecommendationEngine
)


@pytest.fixture
def engine():
    return FinalRecommendationEngine()


@pytest.fixture
def completed_candidate():
    return {
        "status": "completed",
        "hiring_fit_percentage": 87.40,
        "missing_stages": [],
        "completed_stages": [
            "ats",
            "screening",
            "hr_interview",
            "technical_interview",
            "machine_test"
        ]
    }


def test_high_score_recommends_selected(engine, completed_candidate):
    result = engine.recommend(completed_candidate)

    assert result["recommendation"] == "selected"
    assert result["recommendation_label"] == "Selected"


def test_medium_score_recommends_review(engine, completed_candidate):
    completed_candidate["hiring_fit_percentage"] = 70

    result = engine.recommend(completed_candidate)

    assert result["recommendation"] == "hold_review"


def test_low_score_recommends_rejected(engine, completed_candidate):
    completed_candidate["hiring_fit_percentage"] = 45

    result = engine.recommend(completed_candidate)

    assert result["recommendation"] == "rejected"


def test_incomplete_candidate_requires_review(engine):
    candidate = {
        "status": "incomplete",
        "hiring_fit_percentage": None,
        "missing_stages": ["machine_test"]
    }

    result = engine.recommend(candidate)

    assert result["recommendation"] == "hold_review"
    assert result["requires_human_review"] is True


def test_integrity_concern_routes_to_review(engine, completed_candidate):
    risks = [{
        "category": "integrity",
        "severity": "high",
        "status": "unverified",
        "description": "Unusual tab switching."
    }]

    result = engine.recommend(completed_candidate, risks)

    assert result["recommendation"] == "hold_review"
    assert result["requires_human_review"] is True


def test_behavior_does_not_change_hiring_score(engine, completed_candidate):
    risks = [{
        "category": "behavior",
        "severity": "high",
        "status": "observed",
        "description": "Repeated gaze changes."
    }]

    result = engine.recommend(completed_candidate, risks)

    assert result["hiring_fit_score"] == 87.40
    assert result["recommendation"] == "selected"
    assert result["requires_human_review"] is True


def test_confidence_score_is_bounded(engine, completed_candidate):
    result = engine.recommend(completed_candidate)

    assert 0 <= result["confidence_score"] <= 100


def test_invalid_score_rejected(engine, completed_candidate):
    completed_candidate["hiring_fit_percentage"] = 120

    with pytest.raises(ValueError):
        engine.recommend(completed_candidate)
@pytest.mark.parametrize(
    "invalid_score",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_non_finite_score_rejected(
    engine, completed_candidate, invalid_score
):
    completed_candidate["hiring_fit_percentage"] = invalid_score

    with pytest.raises(ValueError):
        engine.recommend(completed_candidate)