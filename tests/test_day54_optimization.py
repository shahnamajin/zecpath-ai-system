
import pytest

from screening_ai.false_rejection_analyzer import (
    FalseRejectionAnalyzer,
)


def test_detects_false_positive():
    analyzer = FalseRejectionAnalyzer()

    result = analyzer.analyze([
        {
            "case_id": "FP01",
            "expected_decision": "clarify",
            "predicted_decision": "continue",
        }
    ])

    assert result["false_positive_count"] == 1


def test_detects_false_negative():
    analyzer = FalseRejectionAnalyzer()

    result = analyzer.analyze([
        {
            "case_id": "FN01",
            "expected_decision": "continue",
            "predicted_decision": "retry",
            "expected_quality": "relevant",
        }
    ])

    assert result["false_negative_count"] == 1
    assert result["false_rejection_count"] == 1


def test_calculates_perfect_classification():
    analyzer = FalseRejectionAnalyzer()

    result = analyzer.analyze([
        {
            "case_id": "C01",
            "expected_decision": "continue",
            "predicted_decision": "continue",
        },
        {
            "case_id": "C02",
            "expected_decision": "clarify",
            "predicted_decision": "clarify",
        },
    ])

    assert result["accuracy_percentage"] == 100
    assert result["f1_score"] == 1


def test_empty_dataset():
    result = FalseRejectionAnalyzer().analyze([])

    assert result["total_cases"] == 0
    assert result["accuracy_percentage"] == 0


def test_invalid_decision_rejected():
    analyzer = FalseRejectionAnalyzer()

    with pytest.raises(ValueError):
        analyzer.analyze([
            {
                "expected_decision": "unknown",
                "predicted_decision": "continue",
            }
        ])
