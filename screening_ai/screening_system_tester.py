from typing import Any, Dict, List


class ScreeningSystemTester:
    """Evaluate simulated screening cases against reference judgments."""

    def evaluate_case(
        self,
        test_case: Dict[str, Any],
        predicted_decision: str,
    ) -> Dict[str, Any]:
        """Compare an AI decision with the expected test decision."""

        expected = test_case.get(
            "expected_decision"
        )

        return {
            "case_id": test_case["case_id"],
            "expected_decision": expected,
            "predicted_decision": predicted_decision,
            "correct": (
                expected == predicted_decision
            ),
        }

    def compare_with_human_judgment(
        self,
        results: List[Dict[str, Any]],
        human_judgments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Compare AI decisions with reference human judgments."""

        human_map = {
            item["case_id"]: item["human_decision"]
            for item in human_judgments
        }

        comparisons = []

        for result in results:

            case_id = result["case_id"]

            human_decision = human_map.get(
                case_id
            )

            ai_decision = result[
                "predicted_decision"
            ]

            comparisons.append(
                {
                    "case_id": case_id,
                    "ai_decision": ai_decision,
                    "human_decision": human_decision,
                    "agreement": (
                        ai_decision == human_decision
                    ),
                }
            )

        total = len(comparisons)

        agreement_count = sum(
            1
            for item in comparisons
            if item["agreement"]
        )

        agreement_rate = (
            agreement_count / total * 100
            if total
            else 0.0
        )

        return {
            "total_cases": total,
            "agreement_count": agreement_count,
            "agreement_rate": round(
                agreement_rate,
                2,
            ),
            "comparisons": comparisons,
        }

    def calculate_accuracy(
        self,
        results: List[Dict[str, Any]],
    ) -> float:
        """Calculate AI decision accuracy."""

        if not results:
            return 0.0

        correct = sum(
            1
            for result in results
            if result.get("correct") is True
        )

        return round(
            correct / len(results) * 100,
            2,
        )