import pytest

from interview_ai.technical_scoring_engine import TechnicalScoringEngine


@pytest.fixture
def engine():
    return TechnicalScoringEngine()


@pytest.fixture
def question():
    return {
        "question_id": "JAVA-CON-001",
        "skill_domain": "java_language",
        "section": "conceptual",
        "question_type": "conceptual",
        "difficulty": "medium",
        "prompt": "Explain Java collections."
    }


def test_conceptual_weighted_score(engine, question):
    result = engine.score_answer(
        question,
        {
            "accuracy": 4,
            "depth": 3,
            "logical_reasoning": 3,
            "real_world_applicability": 2
        },
        evidence_coverage=0.75
    )

    assert result["normalized_score"] == 82.5
    assert result["answer_depth"] == "deep"
    assert len(result["dimension_breakdown"]) == 4


def test_shallow_answer_detection(engine, question):
    result = engine.score_answer(
        question,
        {
            "accuracy": 3,
            "depth": 1,
            "logical_reasoning": 1,
            "real_world_applicability": 1
        },
        evidence_coverage=0.25
    )

    assert result["answer_depth"] == "shallow"


def test_evidence_coverage_developing(engine, question):
    result = engine.score_answer(
        question,
        {
            "accuracy": 3,
            "depth": 3,
            "logical_reasoning": 3,
            "real_world_applicability": 2
        },
        evidence_coverage=0.55
    )

    assert result["answer_depth"] == "developing"


def test_skill_breakdown(engine):
    answers = [
        {"skill_domain": "java", "normalized_score": 80},
        {"skill_domain": "java", "normalized_score": 90},
        {"skill_domain": "sql", "normalized_score": 70}
    ]

    result = engine.build_skill_breakdown(answers)

    assert result["java"]["average_score"] == 85
    assert result["java"]["question_count"] == 2
    assert result["sql"]["question_count"] == 1
    assert result["sql"]["average_score"] == 70


def test_report_requires_scored_answers(engine):
    with pytest.raises(ValueError):
        engine.build_report(
            "C1",
            "J1",
            "S1",
            "java_developer",
            2,
            []
        )


def test_invalid_dimension_score_rejected(engine, question):
    with pytest.raises(ValueError):
        engine.score_answer(
            question,
            {
                "accuracy": 5,
                "depth": 2,
                "logical_reasoning": 2,
                "real_world_applicability": 2
            }
        )


def test_question_type_weights_change_by_type(engine, question):
    q = dict(
        question,
        question_type="scenario_based",
        section="scenario_based"
    )

    result = engine.score_answer(
        q,
        {
            "accuracy": 3,
            "depth": 3,
            "logical_reasoning": 4,
            "real_world_applicability": 4
        }
    )

    assert result["normalized_score"] == 90.0
    assert result["question_type"] == "scenario_based"
    assert result["dimension_breakdown"][2]["weight"] == 0.35