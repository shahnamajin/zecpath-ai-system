import re


class FairnessEngine:

    def mask_personal_attributes(self, text):

        # Mask email
        text = re.sub(
            r"[\w\.-]+@[\w\.-]+",
            "[EMAIL]",
            text
        )

        # Mask phone numbers
        text = re.sub(
            r"\+?\d[\d\s\-]{8,}\d",
            "[PHONE]",
            text
        )

        return text
    def evaluate_bias_indicators(self, text):

        indicators = []

        bias_words = [
            "male",
            "female",
            "married",
            "single",
            "christian",
            "muslim",
            "hindu"
        ]

        lower = text.lower()

        for word in bias_words:

            pattern = r"\b" + re.escape(word) + r"\b"

            if re.search(pattern, lower):
                indicators.append(word)

        return indicators

    def keyword_penalty(self, skill_count):

        # Reduce over-dependence on excessive keyword repetition
        if skill_count > 20:
            return -5

        return 0

    def normalize_score(self, score):

        # Ensure score remains between 0 and 100
        return max(0, min(100, score))