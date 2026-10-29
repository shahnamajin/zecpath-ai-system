from interview_ai.interview_state import HRInterviewState
from interview_ai.interview_flow import HRInterviewFlow


def main():
    print("\nZECPath AI - HR INTERVIEW FLOW DEMO")
    print("=" * 65)

    state = HRInterviewState(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        session_id="HR_SESSION_002"
    )

    flow = HRInterviewFlow(
        state=state,
        candidate_type="fresher",
        role_type="technical",
        max_questions=6
    )

    # --------------------------------------------------
    # Start interview
    # --------------------------------------------------

    first_question = flow.start()

    print("\nINTERVIEW STARTED")
    print("-" * 65)

    print(f"Phase     : {first_question['phase']}")
    print(f"Question  : {first_question['question']}")
    print(f"Question ID: {first_question['question_id']}")

    # --------------------------------------------------
    # Simulated responses
    # --------------------------------------------------

    responses = [
        "I am an MCA student with experience in Python and data analysis.",
        "My education gave me a strong foundation in programming and software development.",
        "My strengths are adaptability, discipline and learning ability.",
        "I have worked on projects where I collaborated with other team members.",
        "I want to build my career as a software professional.",
        "I am available to join according to the requirements of the company."
    ]

    print("\nHR INTERVIEW")
    print("-" * 65)

    for index, response in enumerate(responses, start=1):

        # Capture response for current question
        result = flow.submit_response(response)

        print(f"\nQuestion {index}")
        print(f"Question ID : {result['question_id']}")
        print(f"Response    : {result['response']}")
        print(f"Phase       : {result['phase']}")
        print(
            f"Follow-up   : "
            f"{result['follow_up_eligible']}"
        )

        # Get next question
        next_result = flow.next_question()

        if next_result["status"] == "question":
            print(f"Next Question: {next_result['question']}")
        else:
            print(f"Status: {next_result['status']}")

    # --------------------------------------------------
    # Role evaluation
    # --------------------------------------------------

    evaluation = flow.start_role_evaluation()

    print("\nROLE-BASED EVALUATION")
    print("-" * 65)
    print(f"Status  : {evaluation['status']}")
    print(f"Message : {evaluation['message']}")

    # --------------------------------------------------
    # Closing
    # --------------------------------------------------

    closing = flow.close_interview()

    print("\nCLOSING")
    print("-" * 65)
    print(f"Status  : {closing['status']}")
    print(f"Message : {closing['message']}")

    # --------------------------------------------------
    # Complete
    # --------------------------------------------------

    completed = flow.complete()

    print("\nFINAL RESULT")
    print("-" * 65)
    print(f"Status       : {completed['status']}")
    print(f"Candidate ID : {state.candidate_id}")
    print(f"Session ID   : {state.session_id}")
    print(f"Responses    : {state.get_response_count()}")
    print(f"Final Phase  : {state.phase}")

    print("\nHR INTERVIEW FLOW COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()