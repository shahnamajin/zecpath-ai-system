
"""ZECPath AI - Logical Reasoning Scoring Model."""

import re


class LogicalReasoningScorer:
    """Scores observable reasoning quality on a 0-100 scale."""

    def __init__(self):
        self.weights = {
            "problem_identification": 0.20,
            "reasoning": 0.30,
            "decision_quality": 0.25,
            "clarity": 0.15,
            "actionability": 0.10,
        }

    @staticmethod
    def _clamp(value):
        return round(max(0.0, min(100.0, float(value))), 2)

    @staticmethod
    def _count_words(text):
        return len(re.findall(r"\b[\w'-]+\b", text or ""))

    def score(self, answer, signals=None):
        """
        Score an answer using explicit observable signals.

        signals may contain component scores from an upstream analyzer.
        If omitted, a transparent heuristic baseline is used.
        """
        answer = (answer or "").strip()
        signals = signals or {}

        word_count = self._count_words(answer)

        components = {
            "problem_identification": signals.get(
                "problem_identification",
                70 if word_count >= 15 else 50
            ),
            "reasoning": signals.get(
                "reasoning",
                75 if any(x in answer.lower()
                           for x in ["because", "therefore", "first", "then", "why"])
                else 55
            ),
            "decision_quality": signals.get(
                "decision_quality",
                75 if any(x in answer.lower()
                           for x in ["prioritize", "impact", "risk", "trade-off"])
                else 60
            ),
            "clarity": signals.get(
                "clarity",
                75 if word_count >= 12 else 50
            ),
            "actionability": signals.get(
                "actionability",
                75 if any(x in answer.lower()
                           for x in ["would", "plan", "check", "test", "follow up"])
                else 55
            ),
        }

        components = {
            key: self._clamp(value)
            for key, value in components.items()
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

        final_score = self._clamp(
            sum(item["weighted_score"] for item in breakdown.values())
        )

        return {
            "components": components,
            "breakdown": breakdown,
            "final_score": final_score,
            "word_count": word_count,
            "interpretation": (
                "The score reflects observable reasoning characteristics "
                "in the supplied response; it is not a measure of general intelligence."
            ),
        }
