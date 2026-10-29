
import pytest

from hiring_ai.unified_scoring_engine import UnifiedScoringEngine
from hiring_ai.hiring_fit_calculator import HiringFitCalculator
from hiring_ai.candidate_score_builder import CandidateScoreBuilder


@pytest.fixture
def engine():
    return UnifiedScoringEngine()


# 1. Default scoring weights
def test_default_weights_total_one(engine):
    weights = engine.get_weights("default")

    assert weights == {
        "ats": 0.40,
        "screening": 0.25,
        "hr_interview": 0.35,
    }
    assert sum(weights.values()) == pytest.approx(1.0)


# 2. Technical role weights
def test_technical_role_weights(engine):
    weights = engine.get_weights("technical")

    assert weights == {
        "ats": 0.45,
        "screening": 0.30,
        "hr_interview": 0.25,
    }
    assert sum(weights.values()) == pytest.approx(1.0)


# 3. Non-technical role weights
def test_non_technical_role_weights(engine):
    weights = engine.get_weights("non_technical")

    assert weights == {
        "ats": 0.25,
        "screening": 0.30,
        "hr_interview": 0.45,
    }
    assert sum(weights.values()) == pytest.approx(1.0)


# 4. Default hiring-fit calculation
def test_hiring_fit_calculation(engine):
    result = engine.calculate(
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
        role_type="default",
    )

    assert result["hiring_fit_percentage"] == pytest.approx(81.0)


# 5. Technical role calculation
def test_technical_role_adjustment(engine):
    result = engine.calculate(
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
        role_type="technical",
    )

    assert result["hiring_fit_percentage"] == pytest.approx(79.5)


# 6. Non-technical role calculation
def test_non_technical_role_adjustment(engine):
    result = engine.calculate(
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
        role_type="non_technical",
    )

    assert result["hiring_fit_percentage"] == pytest.approx(81.5)


# 7. Invalid scores must be rejected
@pytest.mark.parametrize(
    "score",
    [-1, 101, float("inf"), float("-inf"), float("nan")],
)
def test_invalid_score_rejected(engine, score):
    with pytest.raises(ValueError):
        engine.calculate(score, 70, 80)


# 8. Boolean values are not valid scores
def test_boolean_score_rejected(engine):
    with pytest.raises(ValueError):
        engine.calculate(True, 70, 80)


# 9. Hiring-fit calculator
def test_calculator_returns_percentage():
    calculator = HiringFitCalculator()

    result = calculator.calculate_hiring_fit(
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
    )

    assert result == pytest.approx(81.0)


# 10. Unified candidate score object
def test_candidate_score_object():
    builder = CandidateScoreBuilder()

    result = builder.build(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        ats_score=80,
        screening_score=70,
        hr_interview_score=90,
    )

    assert result["candidate_id"] == "CAND_1001"
    assert result["job_id"] == "JOB_2001"
    assert result["role_type"] == "default"
    assert result["hiring_fit_percentage"] == pytest.approx(81.0)
    assert result["status"] == "completed"
    assert result["score_id"]
    assert result["created_at"]

    assert set(result["evaluation_rounds"]) == {
        "ats",
        "screening",
        "hr_interview",
    }


# 11. Invalid weights must be rejected
def test_invalid_weights_are_rejected(engine):
    engine.role_config["roles"]["invalid"] = {
        "ats": 0.5,
        "screening": 0.3,
        "hr_interview": 0.3,
    }

    with pytest.raises(ValueError):
        engine.calculate(80, 70, 90, "invalid")


# 12. Negative weights must be rejected
def test_negative_weights_are_rejected(engine):
    engine.role_config["roles"]["invalid"] = {
        "ats": 0.8,
        "screening": -0.1,
        "hr_interview": 0.3,
    }

    with pytest.raises(ValueError):
        engine.calculate(80, 70, 90, "invalid")


# 13. Boundary scores are valid
def test_boundary_scores(engine):
    result = engine.calculate(
        ats_score=100,
        screening_score=0,
        hr_interview_score=100,
        role_type="default",
    )

    assert result["hiring_fit_percentage"] == pytest.approx(75.0)


# 14. Role selection is case-insensitive
def test_role_selection_is_case_insensitive(engine):
    lower = engine.calculate(80, 70, 90, "technical")
    upper = engine.calculate(80, 70, 90, "TECHNICAL")

    assert (
        lower["hiring_fit_percentage"]
        == upper["hiring_fit_percentage"]
    )
