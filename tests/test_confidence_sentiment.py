from screening_ai.confidence_analyzer import (
    ConfidenceAnalyzer
)

from screening_ai.sentiment_analyzer import (
    SentimentAnalyzer
)

from screening_ai.behavioral_analyzer import (
    BehavioralAnalyzer
)


def create_behavioral_analyzer():

    confidence = ConfidenceAnalyzer()

    sentiment = SentimentAnalyzer()

    return BehavioralAnalyzer(
        confidence,
        sentiment
    )


def test_hesitation_detection():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.detect_hesitation(
        "Um, I worked on a Python project."
    )

    assert result["detected"] is True
    assert result["count"] >= 1
    assert "um" in result["markers"]


def test_no_hesitation():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.detect_hesitation(
        "I have experience with Python."
    )

    assert result["detected"] is False


def test_response_length():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.calculate_response_length(
        "I have experience with Python and SQL."
    )

    assert result["word_count"] > 0
    assert result["category"] in {
        "very_short",
        "short",
        "medium",
        "long"
    }


def test_response_pace():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.calculate_pace(
        "I have experience with Python and SQL.",
        duration_seconds=5
    )

    assert result["available"] is True
    assert result["words_per_minute"] > 0


def test_pace_without_duration():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.calculate_pace(
        "I have experience with Python."
    )

    assert result["available"] is False
    assert result["words_per_minute"] is None


def test_uncertainty_detection():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.detect_uncertainty(
        "I think maybe I can work with Python."
    )

    assert result["detected"] is True
    assert len(result["patterns"]) > 0


def test_no_uncertainty():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.detect_uncertainty(
        "I have two years of Python experience."
    )

    assert result["detected"] is False


def test_positive_sentiment():

    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "I am confident and excited about this opportunity."
    )

    assert result["sentiment"] == "positive"
    assert result["sentiment_score"] > 0


def test_negative_sentiment():

    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "I have poor experience and I am worried."
    )

    assert result["sentiment"] == "negative"
    assert result["sentiment_score"] < 0


def test_neutral_sentiment():

    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "I have two years of Python experience."
    )

    assert result["sentiment"] == "neutral"
    assert result["sentiment_score"] == 0.0


def test_contradiction_detection():

    analyzer = create_behavioral_analyzer()

    result = analyzer.detect_contradictions(
        current_entities={
            "experience": {
                "years": 5.0
            }
        },
        previous_context={
            "experience": {
                "years": 2.0
            }
        }
    )

    assert result["detected"] is True
    assert len(result["details"]) > 0


def test_no_contradiction():

    analyzer = create_behavioral_analyzer()

    result = analyzer.detect_contradictions(
        current_entities={
            "experience": {
                "years": 2.0
            }
        },
        previous_context={
            "experience": {
                "years": 2.0
            }
        }
    )

    assert result["detected"] is False


def test_communication_strength():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.analyze(
        "I have experience with Python and SQL.",
        duration_seconds=5
    )

    assert (
        0
        <= result["communication_strength"]
        <= 100
    )


def test_complete_behavioral_analysis():

    analyzer = create_behavioral_analyzer()

    result = analyzer.analyze(
        text="I am confident in my Python skills.",
        duration_seconds=5
    )

    assert "communication_signals" in result
    assert "sentiment" in result
    assert "contradiction" in result

    assert (
        "communication_strength"
        in result["communication_signals"]
    )


def test_empty_response_analysis():

    analyzer = create_behavioral_analyzer()

    result = analyzer.analyze(
        text="",
        duration_seconds=None
    )

    assert (
        result["communication_signals"]
        ["response_length"]["word_count"]
        == 0
    )

    assert (
        result["communication_signals"]
        ["response_pace"]["available"]
        is False
    )