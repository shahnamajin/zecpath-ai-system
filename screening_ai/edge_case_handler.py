from typing import Dict

from screening_ai.audio_quality_analyzer import AudioQualityAnalyzer
from screening_ai.language_mixing_detector import LanguageMixingDetector
from screening_ai.safety_fallback import SafetyFallback


class EdgeCaseHandler:
    """Handle common screening edge cases."""

    def __init__(self):
        self.audio_analyzer = AudioQualityAnalyzer()
        self.language_detector = LanguageMixingDetector()
        self.safety_fallback = SafetyFallback()

    def handle(
        self,
        transcript: str,
        audio_quality: float = 100.0,
        noise_level: float = 0.0,
        retry_count: int = 0,
        clarification_count: int = 0
    ) -> Dict:

        audio = self.audio_analyzer.analyze(
            audio_quality,
            noise_level
        )

        language = self.language_detector.detect(transcript)

        # Poor audio
        if audio["quality"] == "poor":
            if self.safety_fallback.should_fallback(
                retry_count,
                clarification_count,
                "poor_audio"
            ):
                return self.safety_fallback.create_fallback(
                    "repeated_poor_audio"
                )

            return {
                "action": "retry",
                "reason": "poor_audio",
                "message": (
                    "I'm having difficulty hearing you. "
                    "Could you please repeat your answer?"
                ),
                "audio": audio,
                "language": language
            }

        # Background noise
        if audio["noise_status"] == "high":
            if clarification_count >= 2:
                return self.safety_fallback.create_fallback(
                    "repeated_background_noise"
                )

            return {
                "action": "clarify",
                "reason": "background_noise",
                "message": (
                    "There seems to be some background noise. "
                    "Could you please repeat your answer clearly?"
                ),
                "audio": audio,
                "language": language
            }

        # Missing answer
        if not transcript or not transcript.strip():
            if self.safety_fallback.should_fallback(
                retry_count,
                clarification_count,
                "missing_answer"
            ):
                return self.safety_fallback.create_fallback(
                    "repeated_missing_answer"
                )

            return {
                "action": "retry",
                "reason": "missing_answer",
                "message": (
                    "I didn't receive an answer. "
                    "Could you please respond to the question?"
                ),
                "audio": audio,
                "language": language
            }

        # Language mixing
        if language["mixed"]:
            if clarification_count >= 2:
                return self.safety_fallback.create_fallback(
                    "repeated_language_mixing"
                )

            return {
                "action": "clarify",
                "reason": "language_mixing",
                "message": (
                    "I detected multiple languages in the response. "
                    "Could you please repeat your answer clearly?"
                ),
                "audio": audio,
                "language": language
            }

        # Very short / unclear response
        if len(transcript.strip().split()) < 3:
            if clarification_count >= 2:
                return self.safety_fallback.create_fallback(
                    "repeated_unclear_answer"
                )

            return {
                "action": "clarify",
                "reason": "unclear_answer",
                "message": (
                    "Could you provide a little more detail "
                    "about your answer?"
                ),
                "audio": audio,
                "language": language
            }

        return {
            "action": "continue",
            "reason": "normal_response",
            "message": "Response received successfully.",
            "audio": audio,
            "language": language
        }