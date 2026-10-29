from .conversation_state import ConversationContext
from .conversation_flow import ConversationFlow


def print_result(title, result):

    print("-" * 70)
    print(title)
    print(f"State : {result['state']}")
    print(f"Action: {result['action']}")
    print(f"AI    : {result['message']}")


def main():

    print("=" * 70)
    print("ZECPath AI Conversation Flow Demo")
    print("=" * 70)

    context = ConversationContext(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
    )

    flow = ConversationFlow(context)

    # Step 1: Start conversation
    result = flow.start_question(
        question_id="HR_EXP_001",
        question="Can you tell me about your experience?",
        category="experience",
    )

    print_result(
        "Step 1 - Start Conversation",
        result,
    )

    # Step 2: Silence
    result = flow.process_response(
        "",
        intent="missing",
    )

    print_result(
        "Step 2 - Silence Detected",
        result,
    )

    # Step 3: Second silence → fallback
    result = flow.process_response(
        "",
        intent="missing",
    )

    print_result(
        "Step 3 - Fallback After Silence",
        result,
    )

    # Step 4: Start another question
    result = flow.start_question(
        question_id="HR_SKILL_PY_001",
        question="Which technical skills do you use?",
        category="skills",
    )

    print_result(
        "Step 4 - New Question",
        result,
    )

    # Step 5: Confusion
    result = flow.process_response(
        "Maybe.",
        intent="vague",
    )

    print_result(
        "Step 5 - Confusion Detected",
        result,
    )

    # Step 6: Valid response
    result = flow.process_response(
        "I use Python, SQL and Flask.",
        intent="skills",
    )

    print_result(
        "Step 6 - Valid Response",
        result,
    )

    # Step 7: Repeated answer
    result = flow.process_response(
        "I use Python, SQL and Flask.",
        intent="skills",
        is_repeated=True,
    )

    print_result(
        "Step 7 - Repeated Answer",
        result,
    )

    # Step 8: Complete
    result = flow.complete()

    print_result(
        "Step 8 - Conversation Complete",
        result,
    )

    print("-" * 70)

    print("Final Context:")

    print(context.to_dict())

    print("=" * 70)

    print(
        "Conversation flow analysis completed successfully."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()