"""Communication scoring model for ZECPath AI."""

from .communication_analyzer import CommunicationAnalyzer


class CommunicationScorer:
    WEIGHTS = {
        "fluency": 0.20,
        "grammar_quality": 0.20,
        "vocabulary_range": 0.15,
        "clarity": 0.20,
        "answer_structure": 0.15,
        "filler_control": 0.10,
    }

    def __init__(self):
        self.analyzer = CommunicationAnalyzer()

    def normalize_component(self, value: float) -> float:
        return round(max(0.0, min(100.0, value)), 2)

    def score(self, text: str) -> dict:
        metrics = self.analyzer.analyze(text)
        components = {
            key: self.normalize_component(metrics[key])
            for key in self.WEIGHTS
        }

        raw = sum(components[key] * weight for key, weight in self.WEIGHTS.items())

        # Length normalization: avoid allowing a very short answer to receive
        # a fully representative score based on too little evidence.
        word_count = metrics["word_count"]
        if word_count < 5:
            evidence_factor = 0.70
        elif word_count < 8:
            evidence_factor = 0.85
        else:
            evidence_factor = 1.00

        final_score = round(max(0.0, min(100.0, raw * evidence_factor)), 2)

        if final_score >= 80:
            band = "strong"
        elif final_score >= 65:
            band = "good"
        elif final_score >= 50:
            band = "moderate"
        else:
            band = "needs_improvement"

        return {
            "communication_score": final_score,
            "band": band,
            "word_count": word_count,
            "components": components,
            "weights": self.WEIGHTS.copy(),
            "normalization": {
                "evidence_factor": evidence_factor,
                "length_adjustment_applied": evidence_factor < 1.0,
            },
            "filler_details": metrics["filler_details"],
        }
