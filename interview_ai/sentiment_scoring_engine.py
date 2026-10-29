"""Transparent sentiment scoring baseline for ZECPath AI."""

import re


class SentimentScoringEngine:
    POSITIVE_WORDS = {
        "confident", "success", "successful", "achieved", "improved",
        "completed", "enjoy", "enjoyed", "good", "strong", "effective",
        "excellent", "proud", "comfortable", "handled", "solved"
    }

    NEGATIVE_WORDS = {
        "bad", "failed", "failure", "difficult", "worried", "nervous",
        "confused", "uncertain", "problem", "problems", "stressed",
        "stress", "afraid", "unable", "weak", "hate", "mistake"
    }

    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", (text or "").lower())

    def analyze(self, text: str) -> dict:
        words = self.tokenize(text)
        positive = [w for w in words if w in self.POSITIVE_WORDS]
        negative = [w for w in words if w in self.NEGATIVE_WORDS]

        total = len(words)
        if total == 0:
            score = 0.0
            sentiment = "neutral"
        else:
            raw = (len(positive) - len(negative)) / max(1, total)
            score = round(max(-1.0, min(1.0, raw * 5)), 2)
            if score > 0.10:
                sentiment = "positive"
            elif score < -0.10:
                sentiment = "negative"
            else:
                sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": score,
            "positive_indicators": positive,
            "negative_indicators": negative,
            "word_count": total
        }
