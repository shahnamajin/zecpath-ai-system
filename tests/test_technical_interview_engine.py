import pytest
from interview_ai.technical_question_selector import TechnicalQuestionSelector
from interview_ai.technical_difficulty_controller import TechnicalDifficultyController
from interview_ai.technical_interview_engine import TechnicalInterviewEngine


def test_experience_band_boundaries():
    selector = TechnicalQuestionSelector()
    assert selector.resolve_experience_band(0) == "foundational"
    assert selector.resolve_experience_band(2.99) == "foundational"
    assert selector.resolve_experience_band(3) == "intermediate"
    assert selector.resolve_experience_band(4.99) == "intermediate"
    assert selector.resolve_experience_band(5) == "advanced"


@pytest.mark.parametrize("role", ["mern_developer", "java_developer", "devops_engineer"])
def test_role_question_selection(role):
    selector = TechnicalQuestionSelector()
    selected = selector.select_questions(role, 2, max_questions=4)
    assert selected
    assert all(role in question["role_ids"] for question in selected)


def test_invalid_experience_rejected():
    selector = TechnicalQuestionSelector()
    with pytest.raises(ValueError):
        selector.resolve_experience_band(-1)


def test_difficulty_progression_is_bounded():
    controller = TechnicalDifficultyController("medium", minimum="medium", maximum="hard")
    assert controller.update("strong") == "hard"
    assert controller.update("strong") == "hard"
    assert controller.update("weak") == "medium"


def test_interview_lifecycle_and_report():
    engine = TechnicalInterviewEngine("C1", "J1", "S1", "java_developer", 2, max_questions=2)
    first = engine.start()
    assert first["status"] == "question"
    engine.submit_response("I built a small Java service and tested its endpoints.", "strong")
    second = engine.advance()
    assert second["status"] == "question"
    engine.submit_response("Java uses classes and objects.", "partial")
    completed = engine.advance()
    assert completed["status"] == "completed"
    report = engine.complete_report()
    assert report["status"] == "completed"
    assert len(report["question_history"]) == 2


def test_cannot_advance_without_response():
    engine = TechnicalInterviewEngine("C1", "J1", "S2", "mern_developer", 1, max_questions=1)
    engine.start()
    with pytest.raises(RuntimeError):
        engine.advance()
