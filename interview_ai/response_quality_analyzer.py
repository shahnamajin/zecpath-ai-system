"""Analyze candidate responses for adaptive HR interview follow-up decisions."""

import re


class ResponseQualityAnalyzer:
    """Classify response completeness, vagueness, and confidence signals."""

    VAGUE_PHRASES = (
        "many things", "many projects", "some projects", "etc", "and so on",
        "i am good at", "i am strong in", "i know", "i have experience"
    )
    UNCERTAINTY_PHRASES = (
        "i think", "maybe", "probably", "perhaps", "i guess",
        "i'm not sure", "i am not sure", "possibly", "i don't know"
    )

    def analyze(self, response: str) -> dict:
        text = (response or "").strip()
        words = re.findall(r"\b[\w+#.-]+\b", text.lower())
        word_count = len(words)

        if not text:
            quality = "empty"
        elif word_count <= 3:
            quality = "very_short"
        elif self._is_uncertain(text):
            quality = "uncertain"
        elif self._is_vague(text):
            quality = "vague"
        elif word_count < 13:
            quality = "moderate"
        else:
            quality = "detailed"

        confidence = "uncertain" if self._is_uncertain(text) else (
            "confident" if word_count >= 13 else "neutral"
        )

        return {
            "response": text,
            "word_count": word_count,
            "quality": quality,
            "confidence": confidence,
            "vague": self._is_vague(text),
            "uncertain": self._is_uncertain(text),
        }

    def _is_vague(self, text: str) -> bool:
        lowered = text.lower()
        return any(p in lowered for p in self.VAGUE_PHRASES)

    def _is_uncertain(self, text: str) -> bool:
        lowered = text.lower()
        return any(p in lowered for p in self.UNCERTAINTY_PHRASES)
