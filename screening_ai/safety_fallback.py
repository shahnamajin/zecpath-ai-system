from typing import Dict


class SafetyFallback:
    """Provide controlled fallback behavior after repeated failures."""

    def __init__(
        self,
        max_retries: int = 2,
        max_clarifications: int = 2
    ):
        self.max_retries = max_retries
        self.max_clarifications = max_clarifications

    def should_fallback(
        self,
        retry_count: int,
        clarification_count: int,
        failure_type: str
    ) -> bool:
        if failure_type in {
            "poor_audio",
            "missing_answer",
            "unclear_answer",
            "unsupported_language"
        }:
            if retry_count >= self.max_retries:
                return True

        if clarification_count >= self.max_clarifications:
            return True

        return False

    def create_fallback(self, reason: str) -> Dict:
        return {
            "action": "safe_fallback",
            "reason": reason,
            "message": (
                "I'm having difficulty understanding the response. "
                "We can move to the next question or continue this question later."
            )
        }