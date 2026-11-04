
import math
from typing import Dict


class ThresholdOptimizer:
    """
    Apply validated screening decision thresholds.

    Decisions:
        - continue: Score meets continuation threshold.
        - clarify: Response needs clarification.
        - retry: Response should be submitted again.

    The optimizer does not automatically reject candidates.
    """

    def __init__(
        self,
        continue_score: float = 70,
        clarify_score: float = 45,
        retry_score: float = 20,
    ):

        self._validate_threshold(
            "continue_score", continue_score
        )
        self._validate_threshold(
            "clarify_score", clarify_score
        )
        self._validate_threshold(
            "retry_score", retry_score
        )

        if not (
            retry_score <= clarify_score <= continue_score
        ):
            raise ValueError(
                "Thresholds must satisfy: "
                "retry_score <= clarify_score <= continue_score."
            )

        self.continue_score = float(continue_score)
        self.clarify_score = float(clarify_score)
        self.retry_score = float(retry_score)

    @staticmethod
    def _validate_threshold(name: str, value: float) -> None:
        """Validate a threshold as a finite number from 0 to 100."""

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"{name} must be a numeric value."
            )

        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(
                f"{name} must be between 0 and 100."
            )

    @staticmethod
    def _validate_score(score: float) -> None:
        """Validate candidate screening score."""

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(
                "Candidate score must be numeric."
            )

        if not math.isfinite(score) or not 0 <= score <= 100:
            raise ValueError(
                "Candidate score must be a finite number between 0 and 100."
            )

    def decide(
        self,
        score: float,
        intent: str,
        is_missing: bool = False,
        is_off_topic: bool = False,
        is_vague: bool = False,
    ) -> Dict[str, object]:
        """
        Determine the next screening action.

        Intent-based handling supplements the explicit flags.
        Explicit flags and special intents take priority over score.
        """

        # 1. Missing response
        if is_missing or intent == "missing":

            return {
                "decision": "retry",
                "reason": "Missing response",
            }

        # 2. Off-topic response
        if is_off_topic or intent == "off_topic":

            return {
                "decision": "clarify",
                "reason": "Off-topic response",
            }

        # 3. Vague response
        if is_vague or intent == "vague":

            return {
                "decision": "clarify",
                "reason": "Vague response",
            }

        # 4. Validate score before applying thresholds
        self._validate_score(score)

        # 5. Score meets continuation threshold
        if score >= self.continue_score:

            return {
                "decision": "continue",
                "reason": "Score meets continuation threshold",
            }

        # 6. Score requires clarification
        if score >= self.clarify_score:

            return {
                "decision": "clarify",
                "reason": "Score requires clarification",
            }

        # 7. Low-quality response requires retry
        if score >= self.retry_score:

            return {
                "decision": "retry",
                "reason": "Low-quality response",
            }

        # 8. Conservative fallback
        # Never automatically reject a candidate.
        return {
            "decision": "clarify",
            "reason": (
                "Low score; clarification preferred "
                "before rejection"
            ),
        }
