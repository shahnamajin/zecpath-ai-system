from typing import Dict


class ThresholdOptimizer:
    """Apply configurable screening decision thresholds."""

    def __init__(
        self,
        continue_score: float = 70,
        clarify_score: float = 45,
        retry_score: float = 20,
    ):

        self.continue_score = continue_score
        self.clarify_score = clarify_score
        self.retry_score = retry_score

    def decide(
        self,
        score: float,
        intent: str,
        is_missing: bool = False,
        is_off_topic: bool = False,
        is_vague: bool = False,
    ) -> Dict[str, object]:

        # Missing answers should be retried
        if is_missing:

            return {
                "decision": "retry",
                "reason": "Missing response",
            }

        # Off-topic answers should be clarified
        if is_off_topic:

            return {
                "decision": "clarify",
                "reason": "Off-topic response",
            }

        # Vague answers should be clarified
        if is_vague:

            return {
                "decision": "clarify",
                "reason": "Vague response",
            }

        # Relevant answers should not be
        # rejected only because of a low score.
        if score >= self.continue_score:

            return {
                "decision": "continue",
                "reason": "Score meets continuation threshold",
            }

        if score >= self.clarify_score:

            return {
                "decision": "clarify",
                "reason": "Score requires clarification",
            }

        if score >= self.retry_score:

            return {
                "decision": "retry",
                "reason": "Low-quality response",
            }

        return {
            "decision": "clarify",
            "reason": (
                "Low score; clarification preferred "
                "before rejection"
            ),
        }