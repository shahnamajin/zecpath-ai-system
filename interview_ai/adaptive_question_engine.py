"""Adaptive questioning layer built on the dynamic follow-up engine."""

from .dynamic_follow_up_engine import DynamicFollowUpEngine


class AdaptiveQuestionEngine:
    DIFFICULTY_BY_TRIGGER = {
        "clarification": "simple",
        "deepening": "medium",
        "example_based": "medium",
        "scenario_based": "advanced",
    }

    def __init__(self):
        self.engine = DynamicFollowUpEngine()

    def adapt(self, response: str, question_id: str, history=None, follow_up_count=0):
        result = self.engine.process_response(
            response=response,
            question_id=question_id,
            question_history=history or [],
            follow_up_count=follow_up_count,
        )
        trigger = result.get("trigger")
        result["difficulty"] = (
            self.DIFFICULTY_BY_TRIGGER.get(trigger) if trigger else None
        )
        return result
