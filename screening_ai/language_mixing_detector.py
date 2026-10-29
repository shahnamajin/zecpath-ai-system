import re
from typing import Dict


class LanguageMixingDetector:
    """Detect likely language mixing in a candidate response."""

    def detect(self, text: str) -> Dict:
        if not text or not text.strip():
            return {
                "mixed": False,
                "languages_detected": [],
                "confidence": 0.0
            }

        latin_words = re.findall(r"[A-Za-z]+", text)
        malayalam_chars = re.findall(r"[\u0D00-\u0D7F]", text)

        languages = []

        if latin_words:
            languages.append("latin")
        if malayalam_chars:
            languages.append("malayalam")

        mixed = len(languages) > 1

        confidence = 0.9 if mixed else 0.0

        return {
            "mixed": mixed,
            "languages_detected": languages,
            "confidence": confidence
        }