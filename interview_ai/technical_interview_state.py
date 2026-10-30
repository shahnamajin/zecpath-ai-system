"""Session state for role-based technical interviews."""
from datetime import datetime, timezone
from typing import Any


class TechnicalInterviewState:
    VALID_STATES = {
        "created", "configuring", "ready", "introduction",
        "experience_based", "conceptual", "scenario_based",
        "capturing_response", "evaluating", "adapting",
        "section_transition", "paused", "human_review",
        "finalizing", "completed", "failed", "cancelled",
    }

    def __init__(self, candidate_id: str, job_id: str, session_id: str):
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.session_id = session_id
        self.status = "created"
        self.current_question = None
        self.current_section = None
        self.question_history: list[dict[str, Any]] = []
        self.transition_history: list[dict[str, str]] = []
        self.started_at = self._now()
        self.completed_at = None

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def transition(self, new_state: str) -> None:
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Invalid technical interview state: {new_state}")
        previous = self.status
        self.status = new_state
        self.transition_history.append({
            "from": previous, "to": new_state, "at": self._now()
        })
        if new_state in {"completed", "cancelled", "failed"}:
            self.completed_at = self._now()

    def set_question(self, question: dict) -> None:
        self.current_question = question
        self.current_section = question["section"]

    def record_response(self, response: str, evaluation: dict | None = None) -> dict:
        if not self.current_question:
            raise RuntimeError("Cannot record a response without an active question.")
        record = {
            "question_id": self.current_question["question_id"],
            "section": self.current_question["section"],
            "skill_domain": self.current_question["skill_domain"],
            "difficulty": self.current_question["difficulty"],
            "question": self.current_question["prompt"],
            "response": (response or "").strip(),
            "evaluation": evaluation,
            "recorded_at": self._now(),
        }
        self.question_history.append(record)
        return record

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "session_id": self.session_id,
            "status": self.status,
            "current_section": self.current_section,
            "current_question": self.current_question,
            "question_history": self.question_history,
            "transition_history": self.transition_history,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
