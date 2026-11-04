import sys
from pathlib import Path
from pprint import pprint

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hiring_ai.unified_scoring_engine import UnifiedScoringEngine


def main():
    engine = UnifiedScoringEngine()

    candidate = {
        "ats": 85,
        "screening": 80,
        "hr_interview": 90,
        "technical_interview": 88,
        "machine_test": 92,
    }

    print("\n========== DAY 51: CROSS-ROUND AGGREGATION ==========")

    for role in ["default", "technical", "non_technical"]:
        print(f"\n--- {role.upper()} ROLE ---")

        result = engine.calculate(candidate, role_type=role)
        pprint(result)


if __name__ == "__main__":
    main()