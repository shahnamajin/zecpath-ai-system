import re


class ConfidenceAnalyzer:
    """
    Analyzes observable communication signals from
    candidate transcript text.

    This module does not make psychological or personality
    judgments. It measures textual and speech-related signals.
    """

    HESITATION_MARKERS = [
        "um",
        "uh",
        "erm",
        "hmm",
        "mmm",
        "ah",
        "...",
        "--"
    ]

    UNCERTAINTY_PATTERNS = [
        "i think",
        "maybe",
        "probably",
        "perhaps",
        "i'm not sure",
        "i am not sure",
        "not sure",
        "i guess",
        "possibly",
        "i don't know",
        "i dont know",
        "might be",
        "could be"
    ]

    def count_words(self, text):
        """
        Count words in the response.
        """

        if not text:
            return 0

        return len(
            re.findall(
                r"\b[\w']+\b",
                text
            )
        )

    def detect_hesitation(self, text):
        """
        Detect hesitation markers.
        """

        if not text:
            return {
                "count": 0,
                "markers": [],
                "detected": False
            }

        text_lower = text.lower()

        markers_found = []

        for marker in self.HESITATION_MARKERS:

            if marker in text_lower:
                markers_found.append(marker)

        return {
            "count": len(markers_found),
            "markers": markers_found,
            "detected": len(markers_found) > 0
        }

    def calculate_response_length(self, text):
        """
        Categorize response length.
        """

        word_count = self.count_words(text)

        if word_count == 0:
            category = "empty"

        elif word_count <= 5:
            category = "very_short"

        elif word_count <= 15:
            category = "short"

        elif word_count <= 30:
            category = "medium"

        else:
            category = "long"

        return {
            "word_count": word_count,
            "category": category
        }

    def calculate_pace(
        self,
        text,
        duration_seconds=None
    ):
        """
        Calculate approximate speaking pace.

        Words per minute is calculated only when
        response duration is available.
        """

        word_count = self.count_words(text)

        if (
            duration_seconds is None
            or duration_seconds <= 0
        ):
            return {
                "available": False,
                "words_per_minute": None,
                "category": "unavailable"
            }

        words_per_minute = (
            word_count / duration_seconds
        ) * 60

        words_per_minute = round(
            words_per_minute,
            2
        )

        if words_per_minute < 90:
            category = "slow"

        elif words_per_minute <= 160:
            category = "normal"

        else:
            category = "fast"

        return {
            "available": True,
            "words_per_minute": words_per_minute,
            "category": category
        }

    def detect_uncertainty(self, text):
        """
        Detect uncertainty language.
        """

        if not text:
            return {
                "detected": False,
                "patterns": []
            }

        text_lower = text.lower()

        patterns_found = []

        for pattern in self.UNCERTAINTY_PATTERNS:

            if pattern in text_lower:
                patterns_found.append(pattern)

        return {
            "detected": len(patterns_found) > 0,
            "patterns": patterns_found
        }

    def calculate_communication_strength(
        self,
        hesitation,
        uncertainty,
        response_length,
        pace
    ):
        """
        Generate an observable communication-strength
        indicator from textual signals.

        Score range: 0-100.
        """

        score = 70.0

        # Hesitation signal
        if hesitation["count"] == 0:
            score += 10

        elif hesitation["count"] <= 2:
            score += 0

        else:
            score -= 10

        # Uncertainty signal
        if uncertainty["detected"]:
            score -= 10

        else:
            score += 5

        # Response length
        if response_length["category"] == "medium":
            score += 10

        elif response_length["category"] == "long":
            score += 5

        elif response_length["category"] in {
            "very_short",
            "empty"
        }:
            score -= 15

        # Pace
        if pace["available"]:

            if pace["category"] == "normal":
                score += 5

            elif pace["category"] == "fast":
                score -= 5

            elif pace["category"] == "slow":
                score -= 5

        return round(
            max(0.0, min(100.0, score)),
            2
        )

    def analyze(
        self,
        text,
        duration_seconds=None
    ):
        """
        Perform complete communication signal analysis.
        """

        hesitation = self.detect_hesitation(text)

        uncertainty = self.detect_uncertainty(text)

        response_length = (
            self.calculate_response_length(text)
        )

        pace = self.calculate_pace(
            text,
            duration_seconds
        )

        communication_strength = (
            self.calculate_communication_strength(
                hesitation,
                uncertainty,
                response_length,
                pace
            )
        )

        return {
            "hesitation": hesitation,
            "response_length": response_length,
            "response_pace": pace,
            "uncertainty": uncertainty,
            "communication_strength": communication_strength
        }