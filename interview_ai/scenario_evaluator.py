
"""ZECPath AI - Situational Judgment Scenario Evaluation."""

import re


class ScenarioEvaluator:
    """Evaluates observable structure and clarity in scenario answers."""

    def __init__(self):
        self.weights = {
            "problem_identification": 0.20,
            "reasoning": 0.30,
            "decision_quality": 0.25,
            "communication_clarity": 0.15,
            "actionability": 0.10,
        }

    @staticmethod
    def _clamp(value):
        return round(max(0.0, min(100.0, float(value))), 2)

    def evaluate(self, answer, scenario):
        answer = (answer or "").strip()
        text = answer.lower()
        word_count = len(re.findall(r"\b[\w'-]+\b", answer))

        # Observable phrase-based baseline.
        problem = 80 if any(x in text for x in [
            "understand", "identify", "assess", "impact", "problem", "requirement"
        ]) else 55

        reasoning = 80 if any(x in text for x in [
            "because", "compare", "evidence", "trade-off", "reason", "first", "then"
        ]) else 55

        decision = 80 if any(x in text for x in [
            "prioritize", "decide", "choose", "approach", "plan", "solution"
        ]) else 55

        clarity = 80 if word_count >= 20 else 60 if word_count >= 10 else 45

        actionability = 80 if any(x in text for x in [
            "follow up", "communicate", "test", "verify", "implement", "next step"
        ]) else 55

        components = {
            "problem_identification": self._clamp(problem),
            "reasoning": self._clamp(reasoning),
            "decision_quality": self._clamp(decision),
            "communication_clarity": self._clamp(clarity),
            "actionability": self._clamp(actionability),
        }

        breakdown = {
            key: {
                "score": components[key],
                "weight": self.weights[key],
                "weighted_score": round(
                    components[key] * self.weights[key], 2
                ),
            }
            for key in components
        }

        final = self._clamp(
            sum(x["weighted_score"] for x in breakdown.values())
        )

        return {
            "scenario_id": scenario["scenario_id"],
            "category": scenario["category"],
            "components": components,
            "breakdown": breakdown,
            "final_score": final,
            "word_count": word_count,
            "interpretation": (
                "Evaluation focuses on observable problem-solving structure, "
                "reasoning, decision explanation, clarity, and actionability."
            ),
        }
