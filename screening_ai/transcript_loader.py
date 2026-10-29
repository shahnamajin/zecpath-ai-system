import json
from pathlib import Path
from typing import Any, Dict


class TranscriptLoader:
    """
    Loads voice screening transcript data.
    """

    REQUIRED_FIELDS = {
        "transcript_id",
        "candidate_id",
        "job_id",
        "session_id",
        "language",
        "started_at",
        "ended_at",
        "interactions"
    }

    INTERACTION_REQUIRED_FIELDS = {
        "interaction_id",
        "question_id",
        "speaker",
        "timestamp",
        "text",
        "confidence_level",
        "sequence"
    }

    VALID_SPEAKERS = {
        "ai",
        "candidate"
    }

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> Dict[str, Any]:
        """
        Load transcript JSON.
        """

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Transcript file not found: {self.file_path}"
            )

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def validate(self, transcript: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate transcript structure and metadata.
        """

        errors = []

        missing_fields = (
            self.REQUIRED_FIELDS -
            set(transcript.keys())
        )

        if missing_fields:
            errors.append({
                "type": "missing_fields",
                "fields": sorted(missing_fields)
            })

        interactions = transcript.get(
            "interactions",
            []
        )

        if not isinstance(interactions, list):
            errors.append({
                "type": "invalid_interactions",
                "message": "interactions must be a list"
            })

            return {
                "valid": False,
                "errors": errors
            }

        interaction_ids = set()

        for index, interaction in enumerate(
            interactions
        ):

            missing = (
                self.INTERACTION_REQUIRED_FIELDS -
                set(interaction.keys())
            )

            if missing:
                errors.append({
                    "type": "missing_interaction_fields",
                    "index": index,
                    "fields": sorted(missing)
                })

            speaker = interaction.get("speaker")

            if speaker not in self.VALID_SPEAKERS:
                errors.append({
                    "type": "invalid_speaker",
                    "index": index,
                    "speaker": speaker
                })

            confidence = interaction.get(
                "confidence_level"
            )

            if not isinstance(
                confidence,
                (int, float)
            ):
                errors.append({
                    "type": "invalid_confidence",
                    "index": index
                })

            elif not 0 <= confidence <= 1:
                errors.append({
                    "type": "confidence_out_of_range",
                    "index": index
                })

            interaction_id = interaction.get(
                "interaction_id"
            )

            if interaction_id in interaction_ids:
                errors.append({
                    "type": "duplicate_interaction_id",
                    "interaction_id": interaction_id
                })

            interaction_ids.add(interaction_id)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "interaction_count": len(interactions)
        }

    def get_candidate_responses(
        self,
        transcript: Dict[str, Any]
    ):
        """
        Return only candidate responses.
        """

        return [
            interaction
            for interaction in transcript.get(
                "interactions",
                []
            )
            if interaction.get("speaker") == "candidate"
        ]

    def get_ai_questions(
        self,
        transcript: Dict[str, Any]
    ):
        """
        Return only AI questions.
        """

        return [
            interaction
            for interaction in transcript.get(
                "interactions",
                []
            )
            if interaction.get("speaker") == "ai"
        ]