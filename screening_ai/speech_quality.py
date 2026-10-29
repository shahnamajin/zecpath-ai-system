class SpeechQualityAnalyzer:
    """
    Detects incomplete, interrupted, partial,
    or silent speech input.
    """

    INTERRUPTION_MARKERS = {
        "...",
        "--",
        "-",
    }

    PARTIAL_PATTERNS = {
        "python and sql",
        "python",
        "java",
        "sql",
        "yes",
        "no",
        "maybe",
    }

    def is_empty(self, text):
        """
        Detect silence or empty input.
        """

        return not text or not text.strip()

    def is_partial_answer(self, text, minimum_words=3):
        """
        Detect answers that are too short or appear
        to be simple incomplete responses.
        """

        if self.is_empty(text):
            return True

        normalized = text.strip().lower()

        # Remove final punctuation for comparison
        normalized = normalized.rstrip(".!?")

        # Known short-answer patterns
        if normalized in self.PARTIAL_PATTERNS:
            return True

        words = normalized.split()

        # Very short responses
        if len(words) < minimum_words:
            return True

        # Detect simple skill-list responses
        conjunctions = {"and", "&", ","}

        if len(words) <= 4 and any(
            word in conjunctions for word in words
        ):
            return True

        return False

    def is_interrupted(self, text):
        """
        Detect common interruption markers.
        """

        if self.is_empty(text):
            return False

        return any(
            marker in text
            for marker in self.INTERRUPTION_MARKERS
        )

    def classify(self, text):
        """
        Classify speech quality.
        """

        if self.is_empty(text):
            return "silence"

        if self.is_interrupted(text):
            return "interrupted"

        if self.is_partial_answer(text):
            return "partial"

        return "complete"