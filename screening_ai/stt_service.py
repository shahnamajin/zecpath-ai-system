import os
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class SpeechToTextService:
    """
    Speech-to-text service for Zecpath voice screening.

    Uses OpenAI transcription models when an API key is available.
    """

    SUPPORTED_EXTENSIONS = {
        ".flac",
        ".mp3",
        ".mp4",
        ".mpeg",
        ".mpga",
        ".m4a",
        ".ogg",
        ".wav",
        ".webm",
    }

    def __init__(
        self,
        model="gpt-4o-transcribe",
        language="en",
    ):
        self.model = model
        self.language = language

        api_key = os.getenv("OPENAI_API_KEY")

        if OpenAI is None:
            raise ImportError(
                "OpenAI package is not installed. "
                "Run: pip install openai"
            )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)

    def validate_audio_file(self, audio_path):
        """
        Validate that the audio file exists and uses a supported format.
        """

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported audio format: {path.suffix}"
            )

        if path.stat().st_size == 0:
            raise ValueError("Audio file is empty.")

        return True

    def transcribe(self, audio_path):
        """
        Convert audio into text.
        """

        self.validate_audio_file(audio_path)

        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=self.language,
            )

        return {
            "text": transcription.text,
            "model": self.model,
            "language": self.language,
            "source_file": str(audio_path),
        }