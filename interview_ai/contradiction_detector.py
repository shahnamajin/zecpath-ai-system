"""
Contradiction Pattern Detector
ZECPath AI - Day 36
"""

import re


class ContradictionDetector:
    """
    Detects simple contradiction patterns in candidate responses.

    This is a rule-based baseline detector. It focuses mainly on
    conflicting numeric claims such as years of experience, months
    of experience, and salary figures.
    """

    NUMBER_WORDS = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
    }

    def _extract_numeric_claims(self, text: str) -> list[dict]:
        """
        Extract numeric claims from text.

        Supports both:

            2 years
            two years

            5 months
            five months

            3 LPA
            5 LPA
        """

        text = (text or "").lower()

        claims = []

        # ---------------------------------------------------------
        # 1. Numeric digits
        # ---------------------------------------------------------
        digit_pattern = re.compile(
            r"\b(\d+(?:\.\d+)?)\s*"
            r"(years?|yrs?|months?|mos?|lpa)\b"
        )

        for match in digit_pattern.finditer(text):
            value = float(match.group(1))
            unit = match.group(2)

            if unit.startswith(("year", "yr")):
                normalized_unit = "years"
            elif unit.startswith(("month", "mo")):
                normalized_unit = "months"
            else:
                normalized_unit = "lpa"

            claims.append({
                "value": value,
                "unit": normalized_unit,
                "original": match.group(0)
            })

        # ---------------------------------------------------------
        # 2. Number words
        # ---------------------------------------------------------
        word_pattern = re.compile(
            r"\b("
            + "|".join(self.NUMBER_WORDS.keys())
            + r")\s*"
            r"(years?|yrs?|months?|mos?|lpa)\b"
        )

        for match in word_pattern.finditer(text):
            number_word = match.group(1)
            unit = match.group(2)

            value = self.NUMBER_WORDS[number_word]

            if unit.startswith(("year", "yr")):
                normalized_unit = "years"
            elif unit.startswith(("month", "mo")):
                normalized_unit = "months"
            else:
                normalized_unit = "lpa"

            claims.append({
                "value": float(value),
                "unit": normalized_unit,
                "original": match.group(0)
            })

        return claims

    def detect_numeric_conflicts(self, text: str) -> list[dict]:
        """
        Detect conflicting numeric claims of the same type.

        Example:

            I have two years of experience.
            I have five years of experience.

        Result:

            contradiction detected
        """

        claims = self._extract_numeric_claims(text)

        conflicts = []

        # Group claims by unit.
        grouped = {}

        for claim in claims:
            unit = claim["unit"]

            if unit not in grouped:
                grouped[unit] = []

            grouped[unit].append(claim)

        # Check each unit for different values.
        for unit, unit_claims in grouped.items():

            values = [
                claim["value"]
                for claim in unit_claims
            ]

            unique_values = list(dict.fromkeys(values))

            if len(unique_values) > 1:

                conflicts.append({
                    "type": "numeric_conflict",
                    "unit": unit,
                    "values": unique_values,
                    "claims": unit_claims,
                    "reason": "multiple_different_numeric_claims_detected"
                })

        return conflicts

    def detect_explicit_conflict_phrases(
        self,
        text: str
    ) -> list[dict]:
        """
        Detect phrases that may indicate self-correction
        or an explicit contradiction.
        """

        lowered = (text or "").lower()

        markers = [
            "but earlier i said",
            "actually",
            "on the other hand",
            "i first said",
            "i previously said",
        ]

        found = []

        for marker in markers:

            if re.search(
                r"(?<!\w)"
                + re.escape(marker)
                + r"(?!\w)",
                lowered
            ):
                found.append({
                    "type": "explicit_conflict_marker",
                    "marker": marker,
                    "reason": "possible_self_correction_or_conflict_marker"
                })

        return found

    def analyze(self, text: str) -> dict:
        """
        Run complete contradiction analysis.
        """

        numeric_conflicts = self.detect_numeric_conflicts(text)

        explicit_conflicts = (
            self.detect_explicit_conflict_phrases(text)
        )

        conflicts = (
            numeric_conflicts
            + explicit_conflicts
        )

        return {
            "detected": bool(conflicts),
            "count": len(conflicts),
            "conflicts": conflicts
        }


if __name__ == "__main__":

    detector = ContradictionDetector()

    examples = [
        "I have two years of experience. I have five years of experience.",
        "I have 2 years of experience. I have 5 years of experience.",
        "I have two years of experience with Python.",
        "I have three years of experience and five LPA salary.",
    ]

    for text in examples:

        result = detector.analyze(text)

        print("\nResponse:")
        print(text)

        print("Contradiction:")
        print(result["detected"])

        print("Details:")
        print(result["conflicts"])