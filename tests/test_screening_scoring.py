from screening_ai.screening_scorer import ScreeningScorer
from screening_ai.score_aggregator import ScoreAggregator
from screening_ai.screening_scoring_engine import (
    ScreeningScoringEngine
)


def test_clarity_score():

    scorer = ScreeningScorer()

    score = scorer.score_clarity(
        "I have experience with Python and SQL.",
        "skills",
        {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert score > 0
    assert score <= 100


def test_relevance_score():

    scorer = ScreeningScorer()

    score = scorer.score_relevance(
        "skills",
        {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert score == 95.0


def test_off_topic_relevance():

    scorer = ScreeningScorer()

    score = scorer.score_relevance(
        "off_topic",
        {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": True
        }
    )

    assert score == 10.0


def test_missing_answer_score():

    scorer = ScreeningScorer()

    result = scorer.score_answer(
        text="",
        intent="missing",
        entities={},
        quality={
            "is_missing": True,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert result["clarity"] == 0.0
    assert result["relevance"] == 0.0
    assert result["completeness"] == 0.0


def test_skill_completeness():

    scorer = ScreeningScorer()

    score = scorer.score_completeness(
        text="I know Python, SQL and Flask.",
        entities={
            "skills": [
                "python",
                "sql",
                "flask"
            ]
        },
        intent="skills",
        quality={
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert score == 100.0


def test_experience_completeness():

    scorer = ScreeningScorer()

    score = scorer.score_completeness(
        text="I have two years of work experience.",
        entities={
            "skills": [],
            "experience": {
                "years": 2.0,
                "types": ["work"]
            }
        },
        intent="experience",
        quality={
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert score == 100.0


def test_salary_completeness():

    scorer = ScreeningScorer()

    score = scorer.score_completeness(
        text="I expect 5 LPA.",
        entities={
            "salary_expectation": {
                "mentioned": True,
                "values": [
                    {
                        "value": 5.0,
                        "unit": "lpa"
                    }
                ]
            }
        },
        intent="salary_expectation",
        quality={
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    )

    assert score == 95.0


def test_score_normalization():

    aggregator = ScoreAggregator()

    assert aggregator.normalize_score(120) == 100.0
    assert aggregator.normalize_score(-10) == 0.0
    assert aggregator.normalize_score(75) == 75.0


def test_score_aggregation():

    aggregator = ScoreAggregator()

    result = aggregator.aggregate(
        [
            {"total_score": 80},
            {"total_score": 60},
            {"total_score": 100}
        ]
    )

    assert result["total_questions"] == 3
    assert result["average_score"] == 80.0
    assert result["normalized_score"] == 80.0


def test_question_scoring():

    engine = ScreeningScoringEngine()

    answer = {
        "answer": {
            "raw_text": (
                "I have experience with Python and SQL."
            ),
            "intent": "skills",
            "confidence_level": 0.95
        },

        "entities": {
            "skills": [
                "python",
                "sql"
            ],
            "experience": {
                "years": None,
                "types": []
            },
            "availability": {
                "immediately_available": False,
                "notice_period": None
            },
            "salary_expectation": {
                "mentioned": False,
                "values": []
            }
        },

        "quality": {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    }

    result = engine.score_question(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_SKILL_001",
        question_category="skills",
        answer_data=answer
    )

    assert result["candidate_id"] == "CAND_1001"
    assert result["job_id"] == "JOB_2001"
    assert result["scores"]["total_score"] > 0
    assert result["scores"]["total_score"] <= 100


def test_explainable_output():

    engine = ScreeningScoringEngine()

    answer = {
        "answer": {
            "raw_text": "I have experience with Python.",
            "intent": "skills",
            "confidence_level": 0.95
        },

        "entities": {
            "skills": ["python"]
        },

        "quality": {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False
        }
    }

    result = engine.score_question(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_SKILL_001",
        question_category="skills",
        answer_data=answer
    )

    assert "explanation" in result
    assert len(result["explanation"]) > 0


def test_final_screening_score():

    engine = ScreeningScoringEngine()

    question_results = [
        {
            "question_id": "Q1",
            "scores": {
                "total_score": 80
            }
        },
        {
            "question_id": "Q2",
            "scores": {
                "total_score": 60
            }
        }
    ]

    result = engine.calculate_final_score(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_results=question_results
    )

    assert result["final_screening_score"] == 70.0
    assert result["score_summary"]["total_questions"] == 2