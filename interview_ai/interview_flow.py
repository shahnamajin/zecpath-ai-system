from typing import Dict, List, Optional

from interview_ai.interview_state import HRInterviewState
from interview_ai.question_generator import HRQuestionGenerator


class HRInterviewFlow:
    """
    Controls the overall HR interview conversation flow.

    Phases:
    1. Introduction
    2. Core HR
    3. Role-based Evaluation
    4. Closing
    5. Completed
    """

    PHASES = [
        "introduction",
        "core_hr",
        "role_evaluation",
        "closing",
        "completed"
    ]

    def __init__(
        self,
        state: HRInterviewState,
        candidate_type: str,
        role_type: str,
        max_questions: int = 6
    ):
        self.state = state
        self.candidate_type = candidate_type
        self.role_type = role_type
        self.max_questions = max_questions

        self.question_generator = HRQuestionGenerator()

        self.questions: List[Dict] = []
        self.current_index = 0

        self._generate_questions()

    def _generate_questions(self) -> None:
        """Generate questions for the candidate profile."""

        self.questions = self.question_generator.generate_questions(
            candidate_type=self.candidate_type,
            role_type=self.role_type,
            max_questions=self.max_questions
        )

    def start(self) -> Dict:
        """Start the HR interview."""

        self.state.set_phase("introduction")

        return self.next_question()

    def next_question(self) -> Dict:
        """Move to the next interview question."""

        if self.current_index >= len(self.questions):
            self.state.set_phase("closing")

            return {
                "status": "closing",
                "message": (
                    "Thank you for your responses. "
                    "We are moving to the closing phase."
                )
            }

        question = self.questions[self.current_index]

        self.current_index += 1

        category = question["category"]

        if category == "self_introduction":
            self.state.set_phase("introduction")

        elif category in [
            "career_journey",
            "strengths_weaknesses",
            "teamwork_culture",
            "career_goals",
            "availability_commitment"
        ]:
            self.state.set_phase("core_hr")

        self.state.set_question(
            question_id=question["question_id"],
            question=question["question"],
            category=question["category"],
            follow_up_eligible=question["follow_up_eligible"]
        )

        return {
            "status": "question",
            "question_id": question["question_id"],
            "question": question["question"],
            "category": question["category"],
            "phase": self.state.phase,
            "follow_up_eligible": question["follow_up_eligible"]
        }

    def submit_response(self, response: str) -> Dict:
        """Capture the candidate's response."""

        record = self.state.capture_response(response)

        return {
            "status": "response_captured",
            "question_id": record["question_id"],
            "response": record["response"],
            "follow_up_eligible": record["follow_up_eligible"],
            "phase": record["phase"]
        }

    def can_follow_up(self) -> bool:
        """Check whether the current question supports a follow-up."""

        return self.state.should_follow_up()

    def start_role_evaluation(self) -> Dict:
        """Move the interview into role-based evaluation."""

        self.state.set_phase("role_evaluation")

        return {
            "status": "role_evaluation",
            "message": "Role-based evaluation phase started."
        }

    def close_interview(self) -> Dict:
        """Move to closing and complete the interview."""

        self.state.set_phase("closing")

        return {
            "status": "closing",
            "message": "HR interview is moving to the closing phase."
        }

    def complete(self) -> Dict:
        """Complete the interview."""

        self.state.complete_interview()

        return {
            "status": "completed",
            "message": "HR interview completed successfully."
        }

    def get_progress(self) -> Dict:
        """Return current interview progress."""

        total = len(self.questions)

        completed = len(self.state.get_question_history())

        return {
            "current_phase": self.state.phase,
            "questions_completed": completed,
            "total_questions": total,
            "remaining_questions": max(total - completed, 0)
        }