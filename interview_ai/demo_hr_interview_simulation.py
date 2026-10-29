
"""Day 40 - HR Interview Simulation Demo."""

import json
from pathlib import Path

from interview_ai.hr_interview_simulator import HRInterviewSimulator


def main():
    simulator = HRInterviewSimulator()
    results = simulator.run_all()
    comparisons = simulator.compare_manual_evaluation()
    metrics = simulator.evaluation_metrics()
    issues = simulator.identify_inconsistencies()
    recommendations = simulator.recommendations()

    print("ZECPath AI - HR INTERVIEW SIMULATION DEMO")
    print("=" * 62)

    for item in comparisons:
        print(f"\n{item['session_id']} | {item['candidate_type'].upper()}")
        print(f"Candidate ID        : {item['candidate_id']}")
        print(f"AI Score            : {item['ai_score']:.2f}/100")
        print(f"Manual Score        : {item['manual_score']:.2f}/100")
        print(f"Score Difference    : {item['score_difference']:+.2f}")
        print(f"AI Decision         : {item['ai_decision']}")
        print(f"Manual Decision     : {item['manual_decision']}")
        print(f"Decision Agreement  : {item['decision_agreement']}")

    print("\nSIMULATION ACCURACY EVALUATION")
    print(f"Sessions Tested             : {metrics['session_count']}")
    print(f"Decision Accuracy            : {metrics['decision_accuracy']:.2f}%")
    print(f"Scores Within ±5 Points      : {metrics['score_within_tolerance']:.2f}%")
    print(f"Mean Absolute Score Difference: {metrics['mean_absolute_score_difference']:.2f}")
    print(f"Decision Disagreements       : {metrics['decision_disagreements']}")

    print("\nSCORING INCONSISTENCIES")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("- None detected")

    print("\nIMPROVEMENT RECOMMENDATIONS")
    for recommendation in recommendations:
        print(f"- {recommendation}")

    output = (
        Path(__file__).resolve().parent.parent
        / "data/hr_simulation/hr_interview_test_report.json"
    )

    report = {
        "simulation_results": results,
        "manual_comparison": comparisons,
        "accuracy_evaluation": metrics,
        "scoring_inconsistencies": issues,
        "improvement_recommendations": recommendations
    }

    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\nReport Export               : {output.name}")
    print("\nHR INTERVIEW SIMULATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
