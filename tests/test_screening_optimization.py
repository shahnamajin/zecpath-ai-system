from screening_ai.screening_system_tester import (
    ScreeningSystemTester,
)

from screening_ai.threshold_optimizer import (
    ThresholdOptimizer,
)

from screening_ai.false_rejection_analyzer import (
    FalseRejectionAnalyzer,
)


def test_relevant_response_continues():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=80,
        intent="experience",
    )

    assert (
        result["decision"]
        == "continue"
    )


def test_vague_response_clarifies():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=80,
        intent="vague",
        is_vague=True,
    )

    assert (
        result["decision"]
        == "clarify"
    )


def test_off_topic_response_clarifies():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=30,
        intent="off_topic",
        is_off_topic=True,
    )

    assert (
        result["decision"]
        == "clarify"
    )


def test_missing_response_retries():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=0,
        intent="missing",
        is_missing=True,
    )

    assert (
        result["decision"]
        == "retry"
    )


def test_medium_score_clarifies():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=55,
        intent="experience",
    )

    assert (
        result["decision"]
        == "clarify"
    )


def test_low_score_prefers_clarification():

    optimizer = ThresholdOptimizer()

    result = optimizer.decide(
        score=10,
        intent="experience",
    )

    assert (
        result["decision"]
        == "clarify"
    )


def test_system_accuracy():

    tester = ScreeningSystemTester()

    results = [
        {
            "case_id": "C1",
            "expected_decision": "continue",
            "predicted_decision": "continue",
            "correct": True,
        },
        {
            "case_id": "C2",
            "expected_decision": "clarify",
            "predicted_decision": "clarify",
            "correct": True,
        },
    ]

    assert (
        tester.calculate_accuracy(results)
        == 100
    )


def test_human_judgment_comparison():

    tester = ScreeningSystemTester()

    results = [
        {
            "case_id": "C1",
            "predicted_decision": "continue",
            "correct": True,
        },
        {
            "case_id": "C2",
            "predicted_decision": "clarify",
            "correct": True,
        },
    ]

    human = [
        {
            "case_id": "C1",
            "human_decision": "continue",
        },
        {
            "case_id": "C2",
            "human_decision": "clarify",
        },
    ]

    result = tester.compare_with_human_judgment(
        results,
        human,
    )

    assert (
        result["agreement_rate"]
        == 100
    )


def test_false_rejection_detection():

    analyzer = FalseRejectionAnalyzer()

    results = [
        {
            "case_id": "C1",
            "expected_decision": "continue",
            "predicted_decision": "retry",
            "expected_quality": "relevant",
        }
    ]

    result = analyzer.analyze(results)

    assert (
        result["false_rejection_count"]
        == 1
    )


def test_no_false_rejection():

    analyzer = FalseRejectionAnalyzer()

    results = [
        {
            "case_id": "C1",
            "expected_decision": "continue",
            "predicted_decision": "continue",
            "expected_quality": "relevant",
        }
    ]

    result = analyzer.analyze(results)

    assert (
        result["false_rejection_count"]
        == 0
    )