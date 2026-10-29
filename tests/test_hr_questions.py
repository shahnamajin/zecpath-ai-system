from pathlib import Path

from screening_ai.question_loader import HRQuestionLoader
from screening_ai.question_selector import HRQuestionSelector
from screening_ai.conversation_builder import ConversationBuilder


DATASET_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "hr_screening"
    / "hr_questions.json"
)


def create_loader():
    return HRQuestionLoader(
        str(DATASET_PATH)
    )


def test_questions_load():

    loader = create_loader()

    questions = loader.load_questions()

    assert len(questions) > 0


def test_question_schema():

    loader = create_loader()

    questions = loader.load_questions()

    for question in questions:

        assert "question_id" in question
        assert "category" in question
        assert "question" in question
        assert "expected_answer_type" in question
        assert "mandatory" in question
        assert "scoring_importance" in question
        assert "roles" in question
        assert "difficulty" in question
        assert "follow_up_allowed" in question
        assert "max_follow_ups" in question
        assert "order" in question


def test_question_ids_are_unique():

    loader = create_loader()

    questions = loader.load_questions()

    ids = [
        question["question_id"]
        for question in questions
    ]

    assert len(ids) == len(set(ids))


def test_scoring_range():

    loader = create_loader()

    questions = loader.load_questions()

    for question in questions:

        score = question[
            "scoring_importance"
        ]

        assert 0 <= score <= 1


def test_dataset_validation():

    loader = create_loader()

    result = loader.validate_dataset()

    assert result["valid"] is True
    assert result["total_questions"] == 24
    assert result["errors"] == []


def test_category_filter():

    loader = create_loader()

    questions = (
        loader.get_questions_by_category(
            "skills"
        )
    )

    assert len(questions) > 0

    for question in questions:

        assert question["category"] == "skills"


def test_mandatory_questions():

    loader = create_loader()

    questions = (
        loader.get_mandatory_questions()
    )

    assert len(questions) > 0

    for question in questions:

        assert question["mandatory"] is True


def test_role_filter():

    loader = create_loader()

    questions = loader.load_questions()

    selector = HRQuestionSelector(
        questions
    )

    python_questions = (
        selector.get_questions_for_role(
            "python_developer"
        )
    )

    assert len(python_questions) > 0


def test_python_question_exists():

    loader = create_loader()

    questions = loader.load_questions()

    selector = HRQuestionSelector(
        questions
    )

    python_questions = (
        selector.get_questions_for_role(
            "python_developer"
        )
    )

    ids = [
        question["question_id"]
        for question in python_questions
    ]

    assert "HR_SKILL_PY_001" in ids


def test_screening_sequence_order():

    loader = create_loader()

    questions = loader.load_questions()

    selector = HRQuestionSelector(
        questions
    )

    sequence = (
        selector.build_screening_sequence(
            "python_developer"
        )
    )

    assert len(sequence) > 0

    categories = [
        question["category"]
        for question in sequence
    ]

    assert categories[0] == "introduction"

    assert categories.index(
        "introduction"
    ) < categories.index("education")

    assert categories.index(
        "education"
    ) < categories.index("experience")

    assert categories.index(
        "experience"
    ) < categories.index("skills")

    assert categories.index(
        "skills"
    ) < categories.index("location")

    assert categories.index(
        "location"
    ) < categories.index("salary")

    assert categories.index(
        "salary"
    ) < categories.index("notice_period")


def test_first_questions_are_in_correct_order():

    loader = create_loader()

    questions = loader.load_questions()

    selector = HRQuestionSelector(
        questions
    )

    sequence = (
        selector.build_screening_sequence(
            "python_developer"
        )
    )

    assert sequence[0]["question_id"] == "HR_INT_001"
    assert sequence[1]["question_id"] == "HR_INT_002"
    assert sequence[2]["question_id"] == "HR_INT_003"


def test_conversation_builder():

    loader = create_loader()

    questions = loader.load_questions()

    builder = ConversationBuilder()

    conversation = (
        builder.build_conversation(
            questions[:3]
        )
    )

    assert len(conversation) == 3

    first = conversation[0]

    assert "question_id" in first
    assert "prompt" in first
    assert "classification" in first
    assert "evaluation" in first
    assert "conversation" in first
    assert "metadata" in first

    assert (
        first["prompt"]["language"]
        == "en"
    )