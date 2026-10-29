from interview_ai.communication_analyzer import CommunicationAnalyzer
from interview_ai.communication_scorer import CommunicationScorer


def test_fluency_is_available():
    result = CommunicationAnalyzer().analyze(
        "I worked on a project. I developed the backend."
    )
    assert 0 <= result["fluency"] <= 100


def test_grammar_score_range():
    result = CommunicationAnalyzer().analyze(
        "I developed the backend and tested the application."
    )
    assert 0 <= result["grammar_quality"] <= 100


def test_vocabulary_score_range():
    result = CommunicationAnalyzer().analyze(
        "I developed backend services using Python and Flask."
    )
    assert 0 <= result["vocabulary_range"] <= 100


def test_clarity_score_range():
    result = CommunicationAnalyzer().analyze(
        "I analyzed the requirement and explained the solution clearly."
    )
    assert 0 <= result["clarity"] <= 100


def test_structure_score_range():
    result = CommunicationAnalyzer().analyze(
        "First, I analyzed the requirement. Then, I implemented the solution. Finally, I tested it."
    )
    assert 0 <= result["answer_structure"] <= 100


def test_filler_words_are_detected():
    result = CommunicationAnalyzer().analyze(
        "Um, I worked on a project, you know, and basically I tested it."
    )
    assert result["filler_details"]["count"] >= 3


def test_filler_rate_is_normalized():
    result = CommunicationAnalyzer().analyze(
        "Um I worked on a project."
    )
    assert result["filler_details"]["rate_per_100_words"] > 0


def test_strong_structured_response_has_good_band():
    text = (
        "First, I analyzed the requirement. Then I implemented the backend using Flask. "
        "Finally, I tested the APIs and documented the result."
    )
    result = CommunicationScorer().score(text)
    assert result["communication_score"] >= 65
    assert result["band"] in {"good", "strong"}


def test_filler_heavy_response_scores_lower():
    scorer = CommunicationScorer()
    clean = scorer.score(
        "I developed the backend and integrated the database. The application was tested successfully."
    )
    filler = scorer.score(
        "Um, I, uh, basically developed the backend, you know, and actually integrated the database."
    )
    assert filler["communication_score"] < clean["communication_score"]


def test_short_answer_gets_evidence_adjustment():
    result = CommunicationScorer().score("I know Python.")
    assert result["normalization"]["length_adjustment_applied"] is True
    assert result["normalization"]["evidence_factor"] < 1.0


def test_score_is_always_normalized():
    samples = [
        "",
        "Yes",
        "I worked on a project.",
        "I developed a Flask application and integrated MySQL and REST APIs."
    ]
    scorer = CommunicationScorer()
    for text in samples:
        result = scorer.score(text)
        assert 0 <= result["communication_score"] <= 100


def test_weights_sum_to_one():
    weights = CommunicationScorer.WEIGHTS
    assert abs(sum(weights.values()) - 1.0) < 0.0001
