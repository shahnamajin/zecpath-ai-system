
import pytest

from hiring_ai.unified_scoring_engine import UnifiedScoringEngine
from hiring_ai.hiring_fit_calculator import HiringFitCalculator
from hiring_ai.candidate_score_builder import CandidateScoreBuilder


# --------------------------------------------------
# FIXTURES
# --------------------------------------------------

@pytest.fixture
def engine():
    return UnifiedScoringEngine()


@pytest.fixture
def complete_scores():
    return {
        "ats": 85,
        "screening": 80,
        "hr_interview": 90,
        "technical_interview": 88,
        "machine_test": 92,
    }


# --------------------------------------------------
# EXISTING SCORING TESTS
# --------------------------------------------------

def test_default_weights_total_one(engine):
    weights = engine.get_weights("default")

    assert set(weights) == engine.REQUIRED_COMPONENTS
    assert sum(weights.values()) == pytest.approx(1.0)


def test_technical_role_weights(engine):
    weights = engine.get_weights("technical")

    assert weights["technical_interview"] == 0.30
    assert sum(weights.values()) == pytest.approx(1.0)


def test_non_technical_role_weights(engine):
    weights = engine.get_weights("non_technical")

    assert weights["hr_interview"] == 0.25
    assert sum(weights.values()) == pytest.approx(1.0)


def test_five_stage_hiring_fit(engine, complete_scores):
    result = engine.calculate(complete_scores)

    assert result["hiring_fit_percentage"] == pytest.approx(87.40)
    assert result["status"] == "completed"
    assert result["completion_percentage"] == 100


def test_incomplete_candidate(engine):
    scores = {
        "ats": 85,
        "screening": 80,
        "hr_interview": 90,
        "technical_interview": 88,
    }

    result = engine.calculate(scores)

    assert result["status"] == "incomplete"
    assert result["hiring_fit_percentage"] is None
    assert result["missing_stages"] == ["machine_test"]


def test_none_score_is_incomplete(engine, complete_scores):
    complete_scores["machine_test"] = None

    result = engine.calculate(complete_scores)

    assert result["status"] == "incomplete"
    assert result["hiring_fit_percentage"] is None


@pytest.mark.parametrize(
    "score",
    [-1, 101, float("inf"), float("-inf"), float("nan"), True],
)
def test_invalid_scores_rejected(engine, complete_scores, score):
    complete_scores["ats"] = score

    with pytest.raises(ValueError):
        engine.calculate(complete_scores)


def test_invalid_weights_rejected(engine):
    engine.role_config["roles"]["invalid"] = {
        "ats": 0.5,
        "screening": 0.2,
        "hr_interview": 0.1,
        "technical_interview": 0.1,
        "machine_test": 0.2,
    }

    with pytest.raises(ValueError):
        engine.calculate(
            {
                "ats": 80,
                "screening": 80,
                "hr_interview": 80,
                "technical_interview": 80,
                "machine_test": 80,
            },
            "invalid",
        )


def test_calculator_returns_percentage(complete_scores):
    calculator = HiringFitCalculator()

    result = calculator.calculate_hiring_fit(
        ats_score=complete_scores["ats"],
        screening_score=complete_scores["screening"],
        hr_interview_score=complete_scores["hr_interview"],
        technical_interview_score=complete_scores[
            "technical_interview"
        ],
        machine_test_score=complete_scores["machine_test"],
    )

    assert result == pytest.approx(87.40)


def test_candidate_score_object(complete_scores):
    builder = CandidateScoreBuilder()

    result = builder.build(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        ats_score=complete_scores["ats"],
        screening_score=complete_scores["screening"],
        hr_interview_score=complete_scores["hr_interview"],
        technical_interview_score=complete_scores[
            "technical_interview"
        ],
        machine_test_score=complete_scores["machine_test"],
    )

    assert result["candidate_id"] == "CAND_1001"
    assert result["job_id"] == "JOB_2001"
    assert result["hiring_fit_percentage"] == pytest.approx(87.40)
    assert result["status"] == "completed"
    assert len(result["evaluation_rounds"]) == 5
    assert len(result["weighted_contributions"]) == 5
    assert result["completion_percentage"] == 100


def test_boundary_scores(engine):
    scores = {
        component: 100
        for component in engine.REQUIRED_COMPONENTS
    }

    result = engine.calculate(scores)
    assert result["hiring_fit_percentage"] == 100

    scores = {
        component: 0
        for component in engine.REQUIRED_COMPONENTS
    }

    result = engine.calculate(scores)
    assert result["hiring_fit_percentage"] == 0


def test_role_selection_case_insensitive(engine, complete_scores):
    lower = engine.calculate(complete_scores, "technical")
    upper = engine.calculate(complete_scores, "TECHNICAL")

    assert (
        lower["hiring_fit_percentage"]
        == upper["hiring_fit_percentage"]
    )


# --------------------------------------------------
# DAY 54: CROSS-ROUND CONSISTENCY TESTS
# --------------------------------------------------

def test_repeated_calculation_is_consistent(engine, complete_scores):
    """Identical inputs must produce identical results."""

    first_result = engine.calculate(complete_scores)
    second_result = engine.calculate(complete_scores)

    assert first_result == second_result


def test_score_calculation_is_independent_of_input_order(
    engine, complete_scores
):
    """Dictionary insertion order must not change the result."""

    reversed_scores = dict(
        reversed(list(complete_scores.items()))
    )

    first_result = engine.calculate(complete_scores)
    second_result = engine.calculate(reversed_scores)

    assert (
        first_result["hiring_fit_percentage"]
        == second_result["hiring_fit_percentage"]
    )

    assert (
        first_result["weighted_contributions"]
        == second_result["weighted_contributions"]
    )


def test_role_specific_scores_are_consistent(engine, complete_scores):
    """Each role must use its configured weights consistently."""

    technical_first = engine.calculate(
        complete_scores, "technical"
    )

    technical_second = engine.calculate(
        complete_scores, "technical"
    )

    non_technical = engine.calculate(
        complete_scores, "non_technical"
    )

    assert technical_first == technical_second

    assert technical_first["hiring_fit_percentage"] == pytest.approx(
        87.30
    )

    assert non_technical["hiring_fit_percentage"] == pytest.approx(
        86.75
    )

    assert (
        technical_first["hiring_fit_percentage"]
        != non_technical["hiring_fit_percentage"]
    )


def test_incomplete_evaluation_remains_consistent(engine):
    """Missing evaluation stages must never become zero scores."""

    incomplete_scores = {
        "ats": 85,
        "screening": 80,
        "hr_interview": 90,
        "technical_interview": None,
        "machine_test": 92,
    }

    first_result = engine.calculate(incomplete_scores)
    second_result = engine.calculate(incomplete_scores)

    assert first_result == second_result

    assert first_result["status"] == "incomplete"
    assert first_result["hiring_fit_percentage"] is None
    assert first_result["completion_percentage"] == 80

    assert first_result["missing_stages"] == [
        "technical_interview"
    ]
