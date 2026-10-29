from typing import Dict

from screening_ai.edge_case_handler import EdgeCaseHandler


class RobustScreeningFlow:
    """Screening flow with edge-case and failure protection."""

    def __init__(self):
        self.edge_case_handler = EdgeCaseHandler()

        self.retry_count = 0
        self.clarification_count = 0

    def process_response(
        self,
        transcript: str,
        audio_quality: float = 100.0,
        noise_level: float = 0.0
    ) -> Dict:

        result = self.edge_case_handler.handle(
            transcript=transcript,
            audio_quality=audio_quality,
            noise_level=noise_level,
            retry_count=self.retry_count,
            clarification_count=self.clarification_count
        )

        action = result["action"]

        if action == "retry":
            self.retry_count += 1

        elif action == "clarify":
            self.clarification_count += 1

        elif action == "continue":
            self.retry_count = 0
            self.clarification_count = 0

        elif action == "safe_fallback":
            self.retry_count = 0
            self.clarification_count = 0

        return {
            **result,
            "retry_count": self.retry_count,
            "clarification_count": self.clarification_count
        }

    def reset(self):
        self.retry_count = 0
        self.clarification_count = 0