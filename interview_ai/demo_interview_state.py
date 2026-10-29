from interview_ai.interview_state import HRInterviewState


def main():
    print("\nZECPath AI - HR INTERVIEW STATE DEMO")
    print("=" * 60)

    # Create interview session
    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="HR_SESSION_001"
    )

    print("\nINTERVIEW SESSION")
    print(f"Candidate ID : {state.candidate_id}")
    print(f"Job ID       : {state.job_id}")
    print(f"Session ID   : {state.session_id}")
    print(f"Phase        : {state.phase}")

    # --------------------------------------------------
    # Question 1
    # --------------------------------------------------

    state.set_question(
        question_id="HR_INTRO_001",
        question="Tell me about yourself.",
        category="self_introduction",
        follow_up_eligible=True
    )

    print("\nQUESTION 1")
    print(f"Question ID  : {state.current_question_id}")
    print(f"Question     : {state.current_question}")
    print(f"Category     : {state.current_category}")
    print(f"Follow-up    : {state.should_follow_up()}")

    response = state.capture_response(
        "I am an MCA student with experience in Python, "
        "web development and data analysis."
    )

    print("\nRESPONSE CAPTURED")
    print(f"Response     : {response['response']}")
    print(f"Phase        : {response['phase']}")

    # --------------------------------------------------
    # Move to Core HR
    # --------------------------------------------------

    state.set_phase("core_hr")

    state.set_question(
        question_id="HR_SW_001",
        question="What are your greatest strengths?",
        category="strengths_weaknesses",
        follow_up_eligible=True
    )

    print("\nQUESTION 2")
    print(f"Question ID  : {state.current_question_id}")
    print(f"Question     : {state.current_question}")
    print(f"Category     : {state.current_category}")
    print(f"Follow-up    : {state.should_follow_up()}")

    state.capture_response(
        "My strengths are adaptability, discipline "
        "and learning ability."
    )

    # --------------------------------------------------
    # Display history
    # --------------------------------------------------

    print("\nINTERVIEW HISTORY")
    print("-" * 60)

    for index, item in enumerate(
        state.get_question_history(),
        start=1
    ):
        print(f"\n{index}. {item['question_id']}")
        print(f"   Question : {item['question']}")
        print(f"   Response : {item['response']}")
        print(f"   Phase    : {item['phase']}")

    # --------------------------------------------------
    # Complete interview
    # --------------------------------------------------

    state.set_phase("closing")
    state.complete_interview()

    print("\nFINAL STATE")
    print("-" * 60)

    final_state = state.to_dict()

    print(f"Candidate ID : {final_state['candidate_id']}")
    print(f"Job ID       : {final_state['job_id']}")
    print(f"Session ID   : {final_state['session_id']}")
    print(f"Phase        : {final_state['phase']}")
    print(f"Responses    : {final_state['response_count']}")

    print("\nHR INTERVIEW STATE MANAGEMENT COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()