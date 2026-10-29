from interview_ai.question_generator import HRQuestionGenerator
from interview_ai.interview_state import HRInterviewState
from interview_ai.interview_flow import HRInterviewFlow
from interview_ai.follow_up_handler import HRFollowUpHandler


def test_question_bank_loads():
    generator = HRQuestionGenerator()

    assert generator.get_question_count() == 18


def test_question_categories():
    generator = HRQuestionGenerator()

    categories = generator.get_categories()

    assert "self_introduction" in categories
    assert "career_journey" in categories
    assert "strengths_weaknesses" in categories
    assert "teamwork_culture" in categories
    assert "career_goals" in categories
    assert "availability_commitment" in categories


def test_fresher_questions():
    generator = HRQuestionGenerator()

    questions = generator.generate_questions(
        candidate_type="fresher",
        role_type="technical",
        max_questions=6
    )

    assert len(questions) == 6

    for question in questions:
        assert "fresher" in question["candidate_type"]
        assert "technical" in question["role_type"]


def test_experienced_questions():
    generator = HRQuestionGenerator()

    questions = generator.generate_questions(
        candidate_type="experienced",
        role_type="technical",
        max_questions=6
    )

    assert len(questions) == 6

    for question in questions:
        assert "experienced" in question["candidate_type"]
        assert "technical" in question["role_type"]


def test_question_ids_are_unique():
    generator = HRQuestionGenerator()

    questions = generator.generate_questions(
        candidate_type="fresher",
        role_type="technical",
        max_questions=6
    )

    ids = [
        question["question_id"]
        for question in questions
    ]

    assert len(ids) == len(set(ids))


def test_interview_state():
    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="SESSION_001"
    )

    assert state.phase == "introduction"

    state.set_question(
        question_id="HR_INTRO_001",
        question="Tell me about yourself.",
        category="self_introduction",
        follow_up_eligible=True
    )

    assert state.current_question_id == "HR_INTRO_001"
    assert state.should_follow_up() is True


def test_response_capture():
    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="SESSION_001"
    )

    state.set_question(
        question_id="HR_INTRO_001",
        question="Tell me about yourself.",
        category="self_introduction",
        follow_up_eligible=True
    )

    record = state.capture_response(
        "I am an MCA student."
    )

    assert record["response"] == "I am an MCA student."
    assert state.get_response_count() == 1
    assert state.get_last_response() == "I am an MCA student."


def test_interview_flow():
    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="SESSION_002"
    )

    flow = HRInterviewFlow(
        state=state,
        candidate_type="fresher",
        role_type="technical",
        max_questions=6
    )

    result = flow.start()

    assert result["status"] == "question"
    assert state.phase == "introduction"

    assert result["question_id"] is not None
    assert result["question"] is not None


def test_follow_up_for_short_response():
    handler = HRFollowUpHandler()

    result = handler.process_response(
        category="teamwork_culture",
        response="I worked on a project.",
        follow_up_eligible=True
    )

    assert result["follow_up_required"] is True
    assert result["follow_up_question"] is not None


def test_no_follow_up_for_detailed_response():
    handler = HRFollowUpHandler()

    result = handler.process_response(
        category="teamwork_culture",
        response=(
            "During my final year project, I worked with "
            "three team members. I handled backend development "
            "and database integration and coordinated with the "
            "frontend team."
        ),
        follow_up_eligible=True
    )

    assert result["follow_up_required"] is False
    assert result["follow_up_question"] is None


def test_follow_up_disabled():
    handler = HRFollowUpHandler()

    result = handler.process_response(
        category="availability_commitment",
        response="I can join immediately.",
        follow_up_eligible=False
    )

    assert result["follow_up_required"] is False


def test_interview_completion():
    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="SESSION_003"
    )

    state.complete_interview()

    assert state.phase == "completed"
    assert state.completed_at is not None