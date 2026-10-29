import re
from typing import Dict, Any


class TranscriptNormalizer:
    """
    Normalizes speech-to-text transcript data
    for downstream AI processing.
    """

    FILLER_WORDS = {
        "um",
        "uh",
        "erm",
        "hmm"
    }

    def normalize_text(self, text: str) -> str:
        """
        Normalize transcript text.
        """

        if not isinstance(text, str):
            return ""

        text = text.strip()

        # Normalize whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # Remove repeated punctuation
        text = re.sub(
            r"([.!?,])\1+",
            r"\1",
            text
        )

        # Remove leading/trailing punctuation spaces
        text = re.sub(
            r"\s+([,.!?])",
            r"\1",
            text
        )

        return text.strip()

    def remove_filler_words(
        self,
        text: str
    ) -> str:
        """
        Remove common speech fillers.
        """

        words = text.split()

        filtered_words = [
            word
            for word in words
            if word.lower().strip(
                ".,!?;"
            ) not in self.FILLER_WORDS
        ]

        return " ".join(filtered_words)

    def normalize_interaction(
        self,
        interaction: Dict[str, Any]
    ) -> Dict[str, Any]:

        normalized = interaction.copy()

        text = normalized.get(
            "text",
            ""
        )

        text = self.normalize_text(text)

        if normalized.get(
            "speaker"
        ) == "candidate":

            text = self.remove_filler_words(
                text
            )

        normalized["text"] = text

        confidence = normalized.get(
            "confidence_level"
        )

        if isinstance(
            confidence,
            (int, float)
        ):
            normalized[
                "confidence_level"
            ] = round(
                max(0, min(1, confidence)),
                3
            )

        return normalized

    def normalize_transcript(
        self,
        transcript: Dict[str, Any]
    ) -> Dict[str, Any]:

        normalized = transcript.copy()

        normalized["interactions"] = [
            self.normalize_interaction(
                interaction
            )
            for interaction in transcript.get(
                "interactions",
                []
            )
        ]

        return normalized