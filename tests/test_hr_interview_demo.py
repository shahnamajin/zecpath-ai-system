from interview_ai.hr_interview_demo import recommendation_for


def test_strong_score_requires_human_review():
    label, _ = recommendation_for(
        85, {"strong": 80, "moderate": 60, "review": 40}
    )
    assert label == "recommend_for_human_review"


def test_low_score_is_not_auto_rejected():
    label, rationale = recommendation_for(
        25, {"strong": 80, "moderate": 60, "review": 40}
    )
    assert label == "human_review_required"
    assert "do not automatically reject" in rationale


def test_invalid_threshold_order_raises():
    try:
        recommendation_for(
            70, {"strong": 60, "moderate": 80, "review": 40}
        )
    except ValueError:
        return
    raise AssertionError("Invalid threshold order should raise ValueError")
