"""Behavioral confidence signal engine for ZECPath AI."""

from .confidence_analyzer import ConfidenceAnalyzer
from .contradiction_detector import ContradictionDetector


class BehavioralSignalEngine:
    """
    Produces a behavioral confidence score from observable transcript signals.

    This is not a psychological or medical assessment. It summarizes textual/
    conversational indicators such as hesitation, uncertainty, repetition,
    sentiment, contradiction patterns, and response stability.
    """

    WEIGHTS = {
        "hesitation_control": 0.25,
        "uncertainty_control": 0.20,
        "repetition_control": 0.15,
        "contradiction_control": 0.20,
        "sentiment_signal": 0.10,
        "response_stability": 0.10,
    }

    def __init__(self):
        self.analyzer = ConfidenceAnalyzer()
        self.contradictions = ContradictionDetector()

    def _hesitation_score(self, data: dict) -> float:
        rate = data["hesitation"]["rate_per_100_words"]
        return max(0.0, min(100.0, 100 - rate * 4))

    def _uncertainty_score(self, data: dict) -> float:
        count = data["uncertainty"]["count"]
        return max(0.0, min(100.0, 100 - count * 25))

    def _repetition_score(self, data: dict) -> float:
        count = data["repetition"]["count"]
        return max(0.0, min(100.0, 100 - count * 25))

    def _contradiction_score(self, contradiction: dict) -> float:
        return max(0.0, 100 - contradiction["count"] * 35)

    def _sentiment_score(self, sentiment: dict) -> float:
        # Map [-1, 1] to a bounded signal around 50.
        return round(max(0.0, min(100.0, 50 + sentiment["score"] * 50)), 2)

    def _stability_score(self, data: dict) -> float:
        word_count = data["word_count"]
        if word_count == 0:
            return 0.0
        # Avoid treating very short answers as strong evidence.
        return 100.0 if word_count >= 8 else 70.0

    def score(self, text: str, duration_seconds: float | None = None) -> dict:
        signals = self.analyzer.analyze(text, duration_seconds)
        contradiction = self.contradictions.analyze(text)

        components = {
            "hesitation_control": round(self._hesitation_score(signals), 2),
            "uncertainty_control": round(self._uncertainty_score(signals), 2),
            "repetition_control": round(self._repetition_score(signals), 2),
            "contradiction_control": round(self._contradiction_score(contradiction), 2),
            "sentiment_signal": round(self._sentiment_score(signals["sentiment"]), 2),
            "response_stability": round(self._stability_score(signals), 2),
        }

        raw_score = sum(
            components[key] * weight
            for key, weight in self.WEIGHTS.items()
        )
        final_score = round(max(0.0, min(100.0, raw_score)), 2)

        if final_score >= 80:
            band = "high_behavioral_confidence"
        elif final_score >= 60:
            band = "moderate_behavioral_confidence"
        elif final_score >= 40:
            band = "low_behavioral_confidence"
        else:
            band = "very_low_behavioral_confidence"

        stress_indicators = []
        if signals["hesitation"]["level"] == "high":
            stress_indicators.append("high_hesitation")
        if signals["uncertainty"]["level"] in {"high", "moderate"}:
            stress_indicators.append("high_uncertainty")
        if signals["repetition"]["detected"]:
            stress_indicators.append("repeated_words")
        if signals["sentiment"]["sentiment"] == "negative":
            stress_indicators.append("negative_sentiment")
        if contradiction["detected"]:
            stress_indicators.append("contradictory_response")
        if 0 < signals["word_count"] < 4:
            stress_indicators.append("very_short_response")

        return {
            "behavioral_confidence_score": final_score,
            "band": band,
            "components": components,
            "weights": self.WEIGHTS.copy(),
            "signals": signals,
            "contradiction": contradiction,
            "stress_indicators": stress_indicators,
            "interpretation_note": (
                "Behavioral/textual indicators only; not a definitive measurement "
                "of emotional state, stress, personality, or psychological condition."
            ),
        }
