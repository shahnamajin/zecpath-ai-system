import re


class TranscriptCleaner:
    """
    Cleans raw speech-to-text output before AI processing.
    """

    FILLER_WORDS = {
        "um",
        "uh",
        "erm",
        "hmm",
        "mmm",
        "ah",
        "like",
        "you know",
    }

    def clean_whitespace(self, text):
        """
        Remove unnecessary whitespace.
        """

        text = text.strip()
        text = re.sub(r"\s+", " ", text)

        return text

    def remove_filler_words(self, text):
        """
        Remove common speech filler words and
        clean punctuation left behind by their removal.
        """

        if not text:
            return ""

        # Remove multi-word filler first
        text = re.sub(
            r"\byou\s+know\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Remove single-word fillers
        for filler in self.FILLER_WORDS:
            if filler == "you know":
                continue

            pattern = rf"\b{re.escape(filler)}\b"

            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE,
            )

        # Remove punctuation left directly after a removed filler
        text = re.sub(r"^\s*[,;:]\s*", "", text)

        # Clean spaces before punctuation
        text = re.sub(r"\s+([,.!?;:])", r"\1", text)

        # Remove duplicate punctuation
        text = re.sub(r"([,.!?;:]){2,}", r"\1", text)

        return self.clean_whitespace(text)

    def normalize_case(self, text):
        """
        Normalize the first character of the transcript.
        """

        text = text.strip()

        if not text:
            return text

        return text[0].upper() + text[1:]

    def normalize_punctuation(self, text):
        """
        Normalize punctuation and spacing.
        """

        text = text.strip()

        # Remove spaces before punctuation
        text = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            text,
        )

        # Collapse repeated punctuation
        text = re.sub(
            r"([,.!?;:]){2,}",
            r"\1",
            text,
        )

        # Remove punctuation at the beginning
        text = re.sub(
            r"^[,;:]\s*",
            "",
            text,
        )

        return self.clean_whitespace(text)

    def clean(self, text):
        """
        Complete transcript cleaning pipeline.
        """

        if text is None:
            return ""

        text = self.clean_whitespace(text)
        text = self.remove_filler_words(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_case(text)

        return text