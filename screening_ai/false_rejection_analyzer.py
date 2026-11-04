
class FalseRejectionAnalyzer:
    """
    Analyzes screening decisions by comparing expected decisions
    with predicted decisions.

    Supported decisions:
        continue, clarify, retry, reject

    Calculates:
        - Accuracy
        - Precision
        - Recall
        - F1 score
        - False positives
        - False negatives
        - False rejections

    Binary classification:
        Positive class: continue
        Negative class: clarify, retry, reject
    """

    VALID_DECISIONS = {
        "continue",
        "clarify",
        "retry",
        "reject"
    }

    def analyze(self, results):
        """
        Analyze expected and predicted screening decisions.

        Required fields:
            expected_decision
            predicted_decision

        Optional fields:
            case_id
            expected_quality
        """

        if not isinstance(results, list):
            raise ValueError("Results must be a list.")

        false_positives = []
        false_negatives = []
        false_rejections = []

        total_cases = len(results)
        correct_predictions = 0

        true_positives = 0
        true_negatives = 0

        for index, result in enumerate(results):

            if not isinstance(result, dict):
                raise ValueError(
                    f"Result at index {index} must be a dictionary."
                )

            expected = result.get("expected_decision")
            predicted = result.get("predicted_decision")

            if expected not in self.VALID_DECISIONS:
                raise ValueError(
                    f"Invalid expected decision: {expected}"
                )

            if predicted not in self.VALID_DECISIONS:
                raise ValueError(
                    f"Invalid predicted decision: {predicted}"
                )

            case_id = result.get(
                "case_id",
                f"CASE_{index + 1}"
            )

            # Overall correct predictions
            if expected == predicted:
                correct_predictions += 1

            # True positive: expected and predicted continue
            if expected == "continue" and predicted == "continue":
                true_positives += 1

            # True negative: both decisions are not continue
            elif expected != "continue" and predicted != "continue":
                true_negatives += 1

            # False positive: predicted continue incorrectly
            if expected != "continue" and predicted == "continue":

                false_positives.append({
                    "case_id": case_id,
                    "expected": expected,
                    "predicted": predicted
                })

            # False negative: failed to continue when expected
            if expected == "continue" and predicted != "continue":

                false_negatives.append({
                    "case_id": case_id,
                    "expected": expected,
                    "predicted": predicted
                })

            # False rejection: relevant answer incorrectly retried/rejected
            if (
                result.get("expected_quality") == "relevant"
                and expected == "continue"
                and predicted in {"retry", "reject"}
            ):

                false_rejections.append({
                    "case_id": case_id,
                    "expected": expected,
                    "predicted": predicted
                })

        # Accuracy: correct predictions across all decision categories
        accuracy_percentage = (
            correct_predictions / total_cases * 100
            if total_cases > 0 else 0.0
        )

        # Precision: TP / (TP + FP)
        precision = (
            true_positives /
            (true_positives + len(false_positives))
            if (true_positives + len(false_positives)) > 0
            else 0.0
        )

        # Recall: TP / (TP + FN)
        recall = (
            true_positives /
            (true_positives + len(false_negatives))
            if (true_positives + len(false_negatives)) > 0
            else 0.0
        )

        # F1 score
        f1_score = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        return {
            "total_cases": total_cases,
            "correct_predictions": correct_predictions,

            "accuracy_percentage": round(
                accuracy_percentage, 2
            ),

            "false_positive_count": len(false_positives),
            "false_positives": false_positives,

            "false_negative_count": len(false_negatives),
            "false_negatives": false_negatives,

            "false_rejection_count": len(false_rejections),
            "false_rejections": false_rejections,

            "true_positives": true_positives,
            "true_negatives": true_negatives,

            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4)
        }
