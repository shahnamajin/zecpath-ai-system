from typing import Dict


class AudioQualityAnalyzer:
    """Analyze basic audio-quality signals for screening conversations."""

    def analyze(
        self,
        audio_quality: float,
        noise_level: float = 0.0
    ) -> Dict:
        audio_quality = max(0.0, min(100.0, audio_quality))
        noise_level = max(0.0, min(100.0, noise_level))

        if audio_quality < 30:
            quality = "poor"
        elif audio_quality < 60:
            quality = "weak"
        else:
            quality = "good"

        if noise_level >= 70:
            noise_status = "high"
        elif noise_level >= 40:
            noise_status = "moderate"
        else:
            noise_status = "low"

        return {
            "audio_quality": audio_quality,
            "noise_level": noise_level,
            "quality": quality,
            "noise_status": noise_status,
            "usable": audio_quality >= 30
        }