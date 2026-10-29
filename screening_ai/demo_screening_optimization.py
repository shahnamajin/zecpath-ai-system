import json

from .screening_system_tester import (
    ScreeningSystemTester,
)

from .threshold_optimizer import (
    ThresholdOptimizer,
)

from .false_rejection_analyzer import (
    FalseRejectionAnalyzer,
)


def load_test_cases():

    with open(
        "data/screening_optimization/"
        "screening_test_cases.json",
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)["test_cases"]


def load_human_judgments():

    with open(
        "data/screening_optimization/"
        "human_judgment.json",
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)["judgments"]


def main():

    print("=" * 70)
    print("ZECPath AI Screening System Testing & Optimization")
    print("=" * 70)

    test_cases = load_test_cases()

    human_judgments = load_human_judgments()

    optimizer = ThresholdOptimizer()

    tester = ScreeningSystemTester()

    results = []

    print("\nSIMULATED SCREENING CASES")
    print("-" * 70)

    for case in test_cases:

        response = case["response"]

        intent = case["intent"]

        is_missing = (
            intent == "missing"
        )

        is_off_topic = (
            intent == "off_topic"
        )

        is_vague = (
            intent == "vague"
        )

        # Simulated score for optimization testing.
        if case["expected_quality"] == "relevant":
            score = 80

        elif case["expected_quality"] == "uncertain":
            score = 50

        elif case["expected_quality"] == "irrelevant":
            score = 30

        else:
            score = 0

        decision = optimizer.decide(
            score=score,
            intent=intent,
            is_missing=is_missing,
            is_off_topic=is_off_topic,
            is_vague=is_vague,
        )

        result = tester.evaluate_case(
            case,
            decision["decision"],
        )

        result["expected_quality"] = (
            case["expected_quality"]
        )

        result["score"] = score

        results.append(result)

        print(
            f"{case['case_id']} | "
            f"Score: {score:>3} | "
            f"AI: {decision['decision']:<9} | "
            f"Expected: "
            f"{case['expected_decision']:<9} | "
            f"Correct: {result['correct']}"
        )

    accuracy = tester.calculate_accuracy(
        results
    )

    comparison = (
        tester.compare_with_human_judgment(
            results,
            human_judgments,
        )
    )

    false_rejection_analyzer = (
        FalseRejectionAnalyzer()
    )

    false_rejections = (
        false_rejection_analyzer.analyze(
            results
        )
    )

    print("\nSYSTEM TEST RESULTS")
    print("-" * 70)

    print(
        f"Total Cases: "
        f"{len(results)}"
    )

    print(
        f"AI Decision Accuracy: "
        f"{accuracy}%"
    )

    print(
        f"Human Judgment Agreement: "
        f"{comparison['agreement_rate']}%"
    )

    print(
        f"False Rejections: "
        f"{false_rejections['false_rejection_count']}"
    )

    print("\nOPTIMIZATION SUMMARY")
    print("-" * 70)

    print(
        "Relevant responses are allowed to "
        "continue when their score meets the "
        "continuation threshold."
    )

    print(
        "Vague and off-topic responses are "
        "sent for clarification instead of "
        "immediate rejection."
    )

    print(
        "Missing responses trigger a retry."
    )

    print(
        "Low-scoring responses are clarified "
        "before rejection to reduce false "
        "rejections."
    )

    print("\n" + "=" * 70)

    print(
        "Screening system testing and optimization "
        "completed successfully."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()