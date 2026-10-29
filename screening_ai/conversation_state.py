from enum import Enum
from typing import Dict, Any


class ConversationState(str, Enum):

    START = "START"
    ASKING = "ASKING"
    WAITING_FOR_RESPONSE = "WAITING_FOR_RESPONSE"
    PROCESSING_RESPONSE = "PROCESSING_RESPONSE"

    CLARIFICATION = "CLARIFICATION"
    RETRY = "RETRY"
    FALLBACK = "FALLBACK"

    NEXT_QUESTION = "NEXT_QUESTION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ConversationContext:

    def __init__(
        self,
        candidate_id: str,
        job_id: str,
    ):

        self.candidate_id = candidate_id
        self.job_id = job_id

        self.state = ConversationState.START

        self.current_question_id = None
        self.current_question = None
        self.current_category = "general"

        self.retry_count = 0
        self.clarification_count = 0
        self.repeat_count = 0

        self.previous_answer = None

    def to_dict(self) -> Dict[str, Any]:

        return {
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "state": self.state.value,
            "current_question_id":
                self.current_question_id,
            "current_question":
                self.current_question,
            "current_category":
                self.current_category,
            "retry_count":
                self.retry_count,
            "clarification_count":
                self.clarification_count,
            "repeat_count":
                self.repeat_count,
            "previous_answer":
                self.previous_answer
        }