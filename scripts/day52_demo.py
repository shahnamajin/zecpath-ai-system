import sys
from pathlib import Path
from pprint import pprint

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hiring_ai.final_recommendation_engine import (
    FinalRecommendationEngine
)


def main():
    engine = FinalRecommendationEngine()

    candidate_score = {
        "status": "completed",
        "hiring_fit_percentage": 87.40,
        "missing_stages": [],
        "completed_stages": [
            "ats",
            "screening",
            "hr_interview",
            "technical_interview",
            "machine_test"
        ]
    }

    scenarios = [
        {
            "name": "Strong Candidate",
            "risks": []
        },
        {
            "name": "Integrity Concern",
            "risks": [{
                "category": "integrity",
                "severity": "high",
                "status": "unverified",
                "description": "Unusual tab switching during assessment."
            }]
        },
        {
            "name": "Behavioral Observation",
            "risks": [{
                "category": "behavior",
                "severity": "medium",
                "status": "observed",
                "description": "Repeated changes in gaze direction."
            }]
        }
    ]

    print("\n========== DAY 52: FINAL RECOMMENDATION AI ==========")

    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")

        result = engine.recommend(
            candidate_score,
            risk_factors=scenario["risks"]
        )

        pprint(result)


if __name__ == "__main__":
    main()