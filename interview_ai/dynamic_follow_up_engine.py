"""Dynamic follow-up decision engine for the ZECPath HR Interview system."""

from .response_quality_analyzer import ResponseQualityAnalyzer
from .question_repetition_checker import QuestionRepetitionChecker


class DynamicFollowUpEngine:
    """
    Selects an adaptive follow-up trigger from a candidate response.

    Trigger priority:
    1. Empty / very short / uncertain response -> clarification
    2. General claim -> example-based
    3. Short but meaningful response -> deepening
    4. Detailed/confident response -> scenario-based
    """

    FOLLOW_UP_TEMPLATES = {
        "clarification": [
            "Could you please explain that in a little more detail?"
        ],
        "deepening": [
            "What was your specific responsibility in that situation?"
        ],
        "example_based": [
            "Can you give me a specific example of that?"
        ],
        "scenario_based": [
            "Suppose you faced a challenging situation related to this. How would you handle it?"
        ],
    }

    def __init__(self, max_follow_ups_per_question: int = 2):
        self.analyzer = ResponseQualityAnalyzer()
        self.repetition_checker = QuestionRepetitionChecker()
        self.max_follow_ups_per_question = max_follow_ups_per_question

    def decide_trigger(self, response: str) -> dict:
        analysis = self.analyzer.analyze(response)
        text = analysis["response"].lower()

        if analysis["quality"] in {"empty", "very_short", "uncertain"}:
            trigger = "clarification"
        elif analysis["vague"] and any(
            phrase in text for phrase in ("good at", "strong in", "excellent at", "team player")
        ):
            trigger = "example_based"
        elif analysis["quality"] == "vague":
            trigger = "deepening"
        elif analysis["word_count"] < 13:
            trigger = "deepening"
        elif analysis["confidence"] == "confident":
            trigger = "scenario_based"
        else:
            trigger = "deepening"

        return {
            "trigger": trigger,
            "analysis": analysis,
            "reason": {
                "clarification": "response_incomplete_or_uncertain",
                "deepening": "response_needs_more_detail",
                "example_based": "general_claim_needs_example",
                "scenario_based": "detailed_confident_response",
            }[trigger],
        }

    def generate_follow_up(self, trigger: str, history: list[str] | None = None) -> str | None:
        history = history or []
        candidates = self.repetition_checker.filter_new(
            self.FOLLOW_UP_TEMPLATES.get(trigger, []), history
        )
        return candidates[0] if candidates else None

    def process_response(
        self,
        response: str,
        question_id: str,
        question_history: list[str] | None = None,
        follow_up_count: int = 0,
        follow_up_eligible: bool = True,
    ) -> dict:
        history = question_history or []

        if not follow_up_eligible:
            return {
                "action": "continue",
                "trigger": None,
                "reason": "follow_up_not_eligible",
                "question": None,
                "question_id": question_id,
                "follow_up_count": follow_up_count,
            }

        if follow_up_count >= self.max_follow_ups_per_question:
            return {
                "action": "continue",
                "trigger": None,
                "reason": "follow_up_limit_reached",
                "question": None,
                "question_id": question_id,
                "follow_up_count": follow_up_count,
            }

        decision = self.decide_trigger(response)
        question = self.generate_follow_up(decision["trigger"], history)

        if question is None:
            return {
                "action": "continue",
                "trigger": decision["trigger"],
                "reason": "repeated_follow_up_prevented",
                "question": None,
                "question_id": question_id,
                "follow_up_count": follow_up_count,
            }

        return {
            "action": "follow_up",
            "trigger": decision["trigger"],
            "reason": decision["reason"],
            "question": question,
            "question_id": question_id,
            "follow_up_count": follow_up_count + 1,
            "analysis": decision["analysis"],
        }
