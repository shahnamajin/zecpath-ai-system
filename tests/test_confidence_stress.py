from interview_ai.confidence_analyzer import ConfidenceAnalyzer
from interview_ai.sentiment_scoring_engine import SentimentScoringEngine
from interview_ai.contradiction_detector import ContradictionDetector
from interview_ai.behavioral_signal_engine import BehavioralSignalEngine


def test_hesitation_detection():
    result = ConfidenceAnalyzer().analyze("Um, I worked on a project, uh, with Python.")
    assert result["hesitation"]["count"] == 2


def test_uncertainty_detection():
    result = ConfidenceAnalyzer().analyze("I think maybe I can do it.")
    assert result["uncertainty"]["count"] == 2


def test_repeated_words_detection():
    result = ConfidenceAnalyzer().analyze("I worked worked on the backend.")
    assert result["repetition"]["detected"] is True
    assert result["repetition"]["count"] == 1


def test_pace_calculation():
    result = ConfidenceAnalyzer().analyze(
        "I worked on a Python project with Flask and SQL.",
        duration_seconds=6
    )
    assert result["pace"]["available"] is True
    assert result["pace"]["wpm"] > 0


def test_sentiment_positive():
    result = SentimentScoringEngine().analyze(
        "I successfully completed the project and solved the problem."
    )
    assert result["sentiment"] == "positive"


def test_sentiment_negative():
    result = SentimentScoringEngine().analyze(
        "I was nervous and confused about the difficult problem."
    )
    assert result["sentiment"] == "negative"


def test_numeric_contradiction_detection():
    result = ContradictionDetector().analyze(
        "I have two years of experience. I have five years of experience."
    )
    assert result["detected"] is True


def test_no_contradiction_for_single_numeric_claim():
    result = ContradictionDetector().analyze(
        "I have two years of experience with Python."
    )
    assert result["detected"] is False


def test_behavioral_score_range():
    result = BehavioralSignalEngine().score(
        "I have worked with Python and Flask for two years.",
        duration_seconds=8
    )
    assert 0 <= result["behavioral_confidence_score"] <= 100


def test_uncertain_response_has_stress_indicator():
    result = BehavioralSignalEngine().score(
        "Um, I think maybe I can do it, but I'm not sure."
    )
    assert "high_uncertainty" in result["stress_indicators"]


def test_repetition_is_reflected():
    result = BehavioralSignalEngine().score(
        "I worked worked on the backend backend."
    )
    assert "repeated_words" in result["stress_indicators"]


def test_contradiction_is_reflected():
    result = BehavioralSignalEngine().score(
        "I have two years of experience. I have five years of experience."
    )
    assert "contradictory_response" in result["stress_indicators"]


def test_weights_sum_to_one():
    weights = BehavioralSignalEngine.WEIGHTS
    assert abs(sum(weights.values()) - 1.0) < 0.0001


def test_interpretation_note_present():
    result = BehavioralSignalEngine().score("I completed the project successfully.")
    assert "not a definitive measurement" in result["interpretation_note"]
