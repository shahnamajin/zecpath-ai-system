from interview_ai.response_quality_analyzer import ResponseQualityAnalyzer
from interview_ai.question_repetition_checker import QuestionRepetitionChecker
from interview_ai.dynamic_follow_up_engine import DynamicFollowUpEngine
from interview_ai.adaptive_question_engine import AdaptiveQuestionEngine


def test_empty_response_clarification():
    result = DynamicFollowUpEngine().decide_trigger("")
    assert result["trigger"] == "clarification"


def test_short_response_clarification():
    result = DynamicFollowUpEngine().decide_trigger("Yes")
    assert result["trigger"] == "clarification"


def test_vague_response_deepening():
    result = DynamicFollowUpEngine().decide_trigger("I worked on a project.")
    assert result["trigger"] == "deepening"


def test_meaningful_short_response_deepening():
    result = DynamicFollowUpEngine().decide_trigger("I developed a Flask application.")
    assert result["trigger"] == "deepening"


def test_general_claim_example_based():
    result = DynamicFollowUpEngine().decide_trigger("I am good at teamwork.")
    assert result["trigger"] == "example_based"


def test_confident_detailed_response_scenario():
    result = DynamicFollowUpEngine().decide_trigger(
        "I designed the backend architecture, implemented REST APIs, integrated MySQL and deployed the application."
    )
    assert result["trigger"] == "scenario_based"


def test_question_repetition_is_detected():
    checker = QuestionRepetitionChecker()
    q = "What was your specific responsibility in that situation?"
    assert checker.is_repeated(q, [q])


def test_repeated_follow_up_is_blocked():
    engine = DynamicFollowUpEngine()
    q = "What was your specific responsibility in that situation?"
    assert engine.generate_follow_up("deepening", [q]) is None


def test_follow_up_limit():
    result = DynamicFollowUpEngine().process_response(
        "I developed a Flask application.",
        "HR_CAREER_001",
        follow_up_count=2
    )
    assert result["reason"] == "follow_up_limit_reached"


def test_follow_up_disabled():
    result = DynamicFollowUpEngine().process_response(
        "Yes",
        "HR_AVAIL_001",
        follow_up_eligible=False
    )
    assert result["action"] == "continue"


def test_adaptive_difficulty():
    engine = AdaptiveQuestionEngine()
    result = engine.adapt(
        "I designed the backend architecture, implemented REST APIs, integrated MySQL and deployed the application.",
        "HR_SKILL_001"
    )
    assert result["difficulty"] == "advanced"
    assert result["trigger"] == "scenario_based"


def test_response_analyzer_fields():
    result = ResponseQualityAnalyzer().analyze("I worked with Python and Flask.")
    assert result["word_count"] > 0
    assert "quality" in result
    assert "confidence" in result
