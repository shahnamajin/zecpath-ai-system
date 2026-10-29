from typing import Dict, Any


class ScreeningInteraction:

    def __init__(
        self,
        candidate_id: str,
        job_id: str,
        question_id: str,
        interaction_id: str,
        timestamp: str,
        speaker: str,
        text: str,
        confidence_level: float,
        sequence: int
    ):

        self.candidate_id = candidate_id
        self.job_id = job_id
        self.question_id = question_id
        self.interaction_id = interaction_id
        self.timestamp = timestamp
        self.speaker = speaker
        self.text = text
        self.confidence_level = confidence_level
        self.sequence = sequence

    def to_dict(self) -> Dict[str, Any]:

        return {
            "interaction_id": self.interaction_id,
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "question_id": self.question_id,
            "timestamp": self.timestamp,
            "speaker": self.speaker,
            "text": self.text,
            "confidence_level": self.confidence_level,
            "sequence": self.sequence
        }

    def is_low_confidence(
        self,
        threshold: float = 0.70
    ) -> bool:

        return self.confidence_level < threshold