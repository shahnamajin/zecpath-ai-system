from screening_ai.audio_quality_analyzer import AudioQualityAnalyzer
from screening_ai.language_mixing_detector import LanguageMixingDetector
from screening_ai.edge_case_handler import EdgeCaseHandler
from screening_ai.robust_screening_flow import RobustScreeningFlow
from screening_ai.safety_fallback import SafetyFallback


def test_poor_audio_triggers_retry():
    handler = EdgeCaseHandler()

    result = handler.handle(
        transcript="",
        audio_quality=20
    )

    assert result["action"] == "retry"


def test_background_noise_triggers_clarification():
    handler = EdgeCaseHandler()

    result = handler.handle(
        transcript="I work with Python and SQL.",
        audio_quality=80,
        noise_level=80
    )

    assert result["action"] == "clarify"


def test_language_mixing_is_detected():
    detector = LanguageMixingDetector()

    result = detector.detect(
        "I know Python and കുറച്ച് Java."
    )

    assert result["mixed"] is True


def test_missing_answer_triggers_retry():
    handler = EdgeCaseHandler()

    result = handler.handle(
        transcript="",
        audio_quality=95
    )

    assert result["action"] == "retry"


def test_normal_response_continues():
    handler = EdgeCaseHandler()

    result = handler.handle(
        transcript="I have two years of experience with Python.",
        audio_quality=95,
        noise_level=10
    )

    assert result["action"] == "continue"


def test_short_response_requires_clarification():
    handler = EdgeCaseHandler()

    result = handler.handle(
        transcript="Python developer.",
        audio_quality=95
    )

    assert result["action"] == "clarify"


def test_retry_counter_increases():
    flow = RobustScreeningFlow()

    result = flow.process_response(
        transcript="",
        audio_quality=20
    )

    assert result["action"] == "retry"
    assert result["retry_count"] == 1


def test_safe_fallback_after_repeated_audio_failure():
    fallback = SafetyFallback(max_retries=2)

    result = fallback.should_fallback(
        retry_count=2,
        clarification_count=0,
        failure_type="poor_audio"
    )

    assert result is True


def test_safe_fallback_message():
    fallback = SafetyFallback()

    result = fallback.create_fallback("repeated_failure")

    assert result["action"] == "safe_fallback"
    assert "difficulty" in result["message"]


def test_flow_reset():
    flow = RobustScreeningFlow()

    flow.process_response(
        transcript="",
        audio_quality=20
    )

    flow.reset()

    assert flow.retry_count == 0
    assert flow.clarification_count == 0