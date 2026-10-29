from screening_ai.conversation_state import (
    ConversationState,
    ConversationContext,
)

from screening_ai.conversation_flow import (
    ConversationFlow,
)


def create_flow():

    context = ConversationContext(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
    )

    flow = ConversationFlow(context)

    flow.start_question(
        question_id="HR_EXP_001",
        question="Tell me about your experience.",
        category="experience",
    )

    return flow


def test_initial_question():

    flow = create_flow()

    assert (
        flow.context.state
        == ConversationState.ASKING
    )


def test_valid_response_moves_to_next_question():

    flow = create_flow()

    result = flow.process_response(
        "I have two years of Python experience.",
        intent="experience",
    )

    assert result["action"] == "next_question"

    assert (
        flow.context.state
        == ConversationState.NEXT_QUESTION
    )


def test_silence_triggers_retry():

    flow = create_flow()

    result = flow.process_response(
        "",
        intent="missing",
    )

    assert result["action"] == "retry"

    assert (
        flow.context.state
        == ConversationState.RETRY
    )


def test_second_silence_triggers_fallback():

    flow = create_flow()

    flow.process_response(
        "",
        intent="missing",
    )

    result = flow.process_response(
        "",
        intent="missing",
    )

    assert result["action"] == "fallback"

    assert (
        flow.context.state
        == ConversationState.FALLBACK
    )


def test_confusion_triggers_clarification():

    flow = create_flow()

    result = flow.process_response(
        "Maybe.",
        intent="vague",
    )

    assert result["action"] == "clarify"

    assert (
        flow.context.state
        == ConversationState.CLARIFICATION
    )


def test_second_confusion_triggers_fallback():

    flow = create_flow()

    flow.process_response(
        "Maybe.",
        intent="vague",
    )

    result = flow.process_response(
        "I don't know.",
        intent="vague",
    )

    assert result["action"] == "fallback"


def test_repeated_answer_triggers_clarification():

    flow = create_flow()

    result = flow.process_response(
        "I work with Python.",
        intent="skills",
        is_repeated=True,
    )

    assert result["action"] == "clarify"


def test_second_repeated_answer_triggers_fallback():

    flow = create_flow()

    flow.process_response(
        "I work with Python.",
        intent="skills",
        is_repeated=True,
    )

    result = flow.process_response(
        "I work with Python.",
        intent="skills",
        is_repeated=True,
    )

    assert result["action"] == "fallback"


def test_conversation_completion():

    flow = create_flow()

    result = flow.complete()

    assert result["action"] == "complete"

    assert (
        flow.context.state
        == ConversationState.COMPLETED
    )


def test_context_serialization():

    flow = create_flow()

    data = flow.context.to_dict()

    assert data["candidate_id"] == "CAND_1001"

    assert data["job_id"] == "JOB_2001"

    assert "state" in data