
import pytest

from screening_ai.stability_utils import (
    calculate_weighted_score,
    choose_follow_up,
    clean_transcript,
    validate_score,
)


def test_clean_transcript():
    result = clean_transcript("  Hello\u200b   world  !  ")
    assert result == "Hello world!"


def test_validate_score():
    assert validate_score(85) == 85.0


@pytest.mark.parametrize("score", [-1, 101, float("nan"), float("inf"), True])
def test_invalid_score(score):
    with pytest.raises(ValueError):
        validate_score(score)


def test_weighted_score():
    scores = {
        "ats": 80,
        "screening": 70,
        "interview": 90,
    }
    weights = {
        "ats": 0.40,
        "screening": 0.25,
        "interview": 0.35,
    }

    assert calculate_weighted_score(scores, weights) == 81.0


def test_invalid_weights():
    with pytest.raises(ValueError):
        calculate_weighted_score(
            {"ats": 80, "interview": 90},
            {"ats": 0.4, "interview": 0.4},
        )


def test_follow_up_retry():
    assert choose_follow_up("", "unknown", attempts=0) == "retry"


def test_follow_up_clarify():
    assert choose_follow_up("Maybe", "unclear", attempts=0) == "clarify"


def test_follow_up_continue():
    assert choose_follow_up("I know Python", "answer") == "continue"


def test_follow_up_escalate():
    assert choose_follow_up("Help", "human_help") == "escalate"
    assert choose_follow_up("", "unknown", attempts=2) == "escalate"
