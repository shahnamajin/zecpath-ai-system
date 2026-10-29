"""Demo for Day 34 Dynamic Follow-Up Logic."""

from interview_ai.adaptive_question_engine import AdaptiveQuestionEngine


CASES = [
    ("CASE_001", ""),
    ("CASE_002", "Yes"),
    ("CASE_003", "I worked on a project."),
    ("CASE_004", "I developed a Flask application."),
    ("CASE_005", "I am good at teamwork."),
    ("CASE_006", "I developed a Flask application and integrated MySQL, REST APIs, authentication and deployment."),
    ("CASE_007", "I designed the backend architecture, implemented REST APIs, integrated MySQL and deployed the application."),
]


def main():
    engine = AdaptiveQuestionEngine()
    history = []

    print("ZECPath AI - DYNAMIC FOLLOW-UP LOGIC DEMO")
    print("=" * 55)

    for case_id, response in CASES:
        result = engine.adapt(
            response=response,
            question_id="HR_TEAM_001",
            history=history,
        )
        print(f"\n{case_id}")
        print(f"Response   : {response or '<empty>'}")
        print(f"Trigger    : {result['trigger']}")
        print(f"Difficulty : {result['difficulty']}")
        print(f"Action     : {result['action']}")
        print(f"Reason     : {result['reason']}")
        print(f"Follow-up  : {result['question'] or 'None'}")

        if result["question"]:
            history.append(result["question"])

    # Explicit repetition protection demonstration
    repeated = engine.engine.generate_follow_up(
        "deepening",
        ["What was your specific responsibility in that situation?"]
    )
    print("\nREPETITION CHECK")
    print("Repeated question blocked:", repeated is None)
    print("\nDYNAMIC FOLLOW-UP LOGIC DEMO COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
