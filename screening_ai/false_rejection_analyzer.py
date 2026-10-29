from typing import Any, Dict, List


class FalseRejectionAnalyzer:
    """Identify cases where potentially relevant answers were rejected."""

    def analyze(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        false_rejections = []

        for result in results:

            expected = result.get(
                "expected_decision"
            )

            predicted = result.get(
                "predicted_decision"
            )

            quality = result.get(
                "expected_quality"
            )

            if (
                quality == "relevant"
                and predicted in {
                    "retry",
                    "reject",
                }
                and expected == "continue"
            ):

                false_rejections.append(
                    {
                        "case_id":
                            result["case_id"],
                        "expected":
                            expected,
                        "predicted":
                            predicted,
                    }
                )

        return {
            "false_rejection_count":
                len(false_rejections),

            "false_rejections":
                false_rejections,
        }