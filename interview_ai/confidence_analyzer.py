"""Confidence and hesitation signal analyzer for ZECPath AI."""

import re
from .sentiment_scoring_engine import SentimentScoringEngine


class ConfidenceAnalyzer:
    HESITATION_MARKERS = {"um", "uh", "erm", "hmm", "mmm", "...", "--"}
    UNCERTAINTY_PHRASES = (
        "i think", "maybe", "probably", "perhaps", "i guess",
        "i'm not sure", "i am not sure", "possibly", "i don't know",
        "might be", "could be"
    )

    def __init__(self):
        self.sentiment = SentimentScoringEngine()

    def words(self, text: str) -> list[str]:
        return re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", (text or "").lower())

    def detect_hesitation(self, text: str) -> dict:
        lowered = (text or "").lower()
        words = self.words(text)
        found = []

        for marker in self.HESITATION_MARKERS:
            if marker in {"...", "--"}:
                found.extend(re.findall(re.escape(marker), lowered))
            else:
                found.extend(re.findall(r"\b" + re.escape(marker) + r"\b", lowered))

        count = len(found)
        rate = round((count / len(words) * 100), 2) if words else 0.0

        return {
            "count": count,
            "rate_per_100_words": rate,
            "markers": found,
            "level": (
                "high" if rate > 10 else
                "moderate" if rate > 4 else
                "low"
            )
        }

    def detect_uncertainty(self, text: str) -> dict:
        lowered = (text or "").lower()
        found = [
            phrase for phrase in self.UNCERTAINTY_PHRASES
            if re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", lowered)
        ]

        return {
            "count": len(found),
            "phrases": found,
            "level": (
                "high" if len(found) >= 2 else
                "moderate" if len(found) == 1 else
                "low"
            )
        }

    def detect_repeated_words(self, text: str) -> dict:
        words = self.words(text)
        repeated = []
        for i in range(1, len(words)):
            if words[i] == words[i - 1]:
                repeated.append(words[i])

        return {
            "count": len(repeated),
            "words": repeated,
            "detected": bool(repeated)
        }

    def estimate_response_pace(self, text: str, duration_seconds: float | None = None) -> dict:
        words = self.words(text)
        if not duration_seconds or duration_seconds <= 0:
            return {
                "available": False,
                "wpm": None,
                "pace": "not_available"
            }

        wpm = len(words) / duration_seconds * 60
        pace = "slow" if wpm < 90 else "normal" if wpm <= 160 else "fast"

        return {
            "available": True,
            "wpm": round(wpm, 2),
            "pace": pace
        }

    def analyze(self, text: str, duration_seconds: float | None = None) -> dict:
        words = self.words(text)
        hesitation = self.detect_hesitation(text)
        uncertainty = self.detect_uncertainty(text)
        repetition = self.detect_repeated_words(text)
        sentiment = self.sentiment.analyze(text)
        pace = self.estimate_response_pace(text, duration_seconds)

        return {
            "word_count": len(words),
            "hesitation": hesitation,
            "uncertainty": uncertainty,
            "repetition": repetition,
            "sentiment": sentiment,
            "pace": pace
        }
