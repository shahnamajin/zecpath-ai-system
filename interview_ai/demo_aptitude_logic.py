
"""Day 38 - Aptitude Logic Design Demo."""

from interview_ai.aptitude_logic_engine import AptitudeLogicEngine


def main():
    engine = AptitudeLogicEngine()

    print("ZECPath AI - APTITUDE LOGIC DESIGN DEMO")
    print("=" * 58)

    reasoning_answers = [
        (
            "APT_LOGIC_001",
            "A-B-C because Task A must happen before B, and B must happen before C."
        ),
        (
            "APT_LOGIC_002",
            "I would prioritize the production bug because it has higher impact. "
            "I would communicate the trade-off and complete the routine work afterward."
        ),
        (
            "APT_LOGIC_003",
            "First I would check recent changes and collect evidence. Then I would "
            "isolate the bottleneck, test the hypothesis, apply a fix, and verify the result."
        ),
    ]

    questions = {
        q["question_id"]: q for q in engine.load_reasoning_questions()["questions"]
    }

    reasoning_results = []

    for qid, answer in reasoning_answers:
        result = engine.evaluate_reasoning(answer)
        reasoning_results.append(result)

        print(f"\n{qid}")
        print(f"Answer       : {answer}")
        print(f"Reasoning    : {result['final_score']:.2f}/100")
        print(f"Word Count   : {result['word_count']}")
        print(f"Interpretation: {result['interpretation']}")

    scenario = engine.load_scenarios()["scenarios"][0]

    scenario_answer = (
        "I would first understand both viewpoints and identify the project requirement. "
        "Then I would compare the evidence and trade-offs, agree on an actionable approach, "
        "communicate the decision clearly, and follow up on the outcome."
    )

    scenario_result = engine.evaluate_scenario(
        scenario_answer,
        scenario
    )

    print("\nSITUATIONAL JUDGMENT")
    print(f"Scenario ID  : {scenario['scenario_id']}")
    print(f"Category     : {scenario['category']}")
    print(f"Score        : {scenario_result['final_score']:.2f}/100")
    print(f"Word Count   : {scenario_result['word_count']}")

    overall = engine.get_overall_score(
        reasoning_results,
        [scenario_result]
    )

    print("\nFINAL APTITUDE / LOGIC RESULT")
    print(f"Overall Score: {overall:.2f}/100")
    print("\nAPTITUDE LOGIC DESIGN COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
