from interview_ai.follow_up_handler import HRFollowUpHandler


def main():
    print("\nZECPath AI - HR FOLLOW-UP HANDLER DEMO")
    print("=" * 65)

    handler = HRFollowUpHandler()

    # --------------------------------------------------
    # Short response
    # --------------------------------------------------

    print("\nCASE 1 - SHORT RESPONSE")
    print("-" * 65)

    response = "I worked on a college project."

    result = handler.process_response(
        category="teamwork_culture",
        response=response,
        follow_up_eligible=True
    )

    print(f"Response          : {response}")
    print(
        f"Follow-up Required: "
        f"{result['follow_up_required']}"
    )
    print(
        f"Follow-up Question: "
        f"{result['follow_up_question']}"
    )
    print(f"Reason            : {result['reason']}")

    # --------------------------------------------------
    # Detailed response
    # --------------------------------------------------

    print("\nCASE 2 - DETAILED RESPONSE")
    print("-" * 65)

    response = (
        "During my final year project, I worked with three team "
        "members. I was responsible for the backend development "
        "and database integration. I also coordinated with the "
        "frontend team to integrate the modules."
    )

    result = handler.process_response(
        category="teamwork_culture",
        response=response,
        follow_up_eligible=True
    )

    print(f"Response          : {response}")
    print(
        f"Follow-up Required: "
        f"{result['follow_up_required']}"
    )
    print(
        f"Follow-up Question: "
        f"{result['follow_up_question']}"
    )
    print(f"Reason            : {result['reason']}")

    # --------------------------------------------------
    # Follow-up disabled
    # --------------------------------------------------

    print("\nCASE 3 - FOLLOW-UP NOT ELIGIBLE")
    print("-" * 65)

    response = "I can join immediately."

    result = handler.process_response(
        category="availability_commitment",
        response=response,
        follow_up_eligible=False
    )

    print(f"Response          : {response}")
    print(
        f"Follow-up Required: "
        f"{result['follow_up_required']}"
    )
    print(
        f"Follow-up Question: "
        f"{result['follow_up_question']}"
    )
    print(f"Reason            : {result['reason']}")

    print("\n" + "=" * 65)
    print("HR FOLLOW-UP HANDLING COMPLETED SUCCESSFULLY")
    print("=" * 65)


if __name__ == "__main__":
    main()