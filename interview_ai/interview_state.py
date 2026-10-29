from typing import Dict, List, Optional
from datetime import datetime


class HRInterviewState:
    """
    Maintains the state of an AI HR interview session.

    Tracks:
    - Candidate information
    - Job information
    - Interview phase
    - Current question
    - Candidate responses
    - Follow-up eligibility
    - Question history
    """

    VALID_PHASES = [
        "introduction",
        "core_hr",
        "role_evaluation",
        "closing",
        "completed"
    ]

    def __init__(
        self,
        candidate_id: str,
        job_id: str,
        session_id: str
    ):
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.session_id = session_id

        self.phase = "introduction"

        self.current_question_id: Optional[str] = None
        self.current_question: Optional[str] = None
        self.current_category: Optional[str] = None
        self.follow_up_eligible = False

        self.current_response: Optional[str] = None

        self.question_history: List[Dict] = []

        self.started_at = datetime.now().isoformat()
        self.completed_at: Optional[str] = None

    def set_phase(self, phase: str) -> None:
        """Change the current interview phase."""

        if phase not in self.VALID_PHASES:
            raise ValueError(
                f"Invalid interview phase: {phase}"
            )

        self.phase = phase

    def set_question(
        self,
        question_id: str,
        question: str,
        category: str,
        follow_up_eligible: bool = False
    ) -> None:
        """
        Set the current interview question.
        """

        self.current_question_id = question_id
        self.current_question = question
        self.current_category = category
        self.follow_up_eligible = follow_up_eligible

        self.current_response = None

    def capture_response(self, response: str) -> Dict:
        """
        Capture the candidate's response to the current question.
        """

        if not self.current_question_id:
            raise RuntimeError(
                "Cannot capture response without a current question."
            )

        response = response.strip()

        response_record = {
            "question_id": self.current_question_id,
            "question": self.current_question,
            "category": self.current_category,
            "response": response,
            "follow_up_eligible": self.follow_up_eligible,
            "phase": self.phase,
            "timestamp": datetime.now().isoformat()
        }

        self.current_response = response

        self.question_history.append(response_record)

        return response_record

    def should_follow_up(self) -> bool:
        """
        Determine whether the current question allows
        an AI follow-up.
        """

        return self.follow_up_eligible

    def get_last_response(self) -> Optional[str]:
        """Return the most recent candidate response."""

        if not self.question_history:
            return None

        return self.question_history[-1]["response"]

    def get_response_count(self) -> int:
        """Return the number of captured responses."""

        return len(self.question_history)

    def get_question_history(self) -> List[Dict]:
        """Return all captured question-response records."""

        return self.question_history.copy()

    def complete_interview(self) -> None:
        """Mark the interview as completed."""

        self.phase = "completed"
        self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """
        Convert the complete interview state into a dictionary.
        """

        return {
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "session_id": self.session_id,
            "phase": self.phase,
            "current_question_id": self.current_question_id,
            "current_question": self.current_question,
            "current_category": self.current_category,
            "follow_up_eligible": self.follow_up_eligible,
            "current_response": self.current_response,
            "response_count": len(self.question_history),
            "question_history": self.question_history,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }