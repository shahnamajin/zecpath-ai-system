"""Conversation state tracking for dynamic HR follow-up questioning."""


class DynamicFollowUpState:
    def __init__(self, candidate_id: str, session_id: str, question_id: str):
        self.candidate_id = candidate_id
        self.session_id = session_id
        self.question_id = question_id
        self.response_count = 0
        self.follow_up_count = 0
        self.trigger_history = []
        self.question_history = []
        self.current_difficulty = "base"

    def record_response(self, response: str):
        self.response_count += 1
        return self.response_count

    def record_follow_up(self, trigger: str, question: str, difficulty: str):
        self.follow_up_count += 1
        self.trigger_history.append(trigger)
        self.question_history.append(question)
        self.current_difficulty = difficulty

    def can_follow_up(self, max_follow_ups: int = 2) -> bool:
        return self.follow_up_count < max_follow_ups

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "session_id": self.session_id,
            "question_id": self.question_id,
            "response_count": self.response_count,
            "follow_up_count": self.follow_up_count,
            "trigger_history": list(self.trigger_history),
            "question_history": list(self.question_history),
            "current_difficulty": self.current_difficulty,
        }
