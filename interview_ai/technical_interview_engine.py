"""Orchestrator for ZECPath role-based technical interview sessions."""
from interview_ai.technical_interview_state import TechnicalInterviewState
from interview_ai.technical_question_selector import TechnicalQuestionSelector
from interview_ai.technical_difficulty_controller import TechnicalDifficultyController


SECTION_STATES = {
    "introduction": "introduction",
    "experience_based": "experience_based",
    "conceptual": "conceptual",
    "scenario_based": "scenario_based",
}


class TechnicalInterviewEngine:
    def __init__(self, candidate_id, job_id, session_id, role_id, experience_years,
                 max_questions=12, selector=None):
        self.selector = selector or TechnicalQuestionSelector()
        self.role = self.selector.get_role(role_id)
        self.experience_band = self.selector.resolve_experience_band(experience_years)
        self.questions = self.selector.select_questions(
            role_id=role_id, experience_years=experience_years,
            max_questions=max_questions
        )
        if not self.questions:
            raise ValueError(f"No questions available for role {role_id} and experience {experience_years}")
        baseline = next(
            b["baseline_difficulty"] for b in self.selector.hierarchy["experience_bands"]
            if b["id"] == self.experience_band
        )
        self.difficulty = TechnicalDifficultyController(
            baseline=baseline,
            minimum=baseline,
            maximum="expert"
        )
        self.state = TechnicalInterviewState(candidate_id, job_id, session_id)
        self.index = 0
        self.state.transition("configuring")
        self.state.transition("ready")

    def start(self):
        if self.state.status != "ready":
            raise RuntimeError("Interview can only start from ready state")
        return self.next_question()

    def next_question(self):
        if self.state.status in {"completed", "cancelled", "failed"}:
            raise RuntimeError(f"Interview is terminal: {self.state.status}")
        if self.index >= len(self.questions):
            self.state.transition("finalizing")
            self.state.transition("completed")
            return {"status": "completed", "message": "Technical interview completed."}
        question = self.questions[self.index]
        self.index += 1
        self.state.set_question(question)
        self.state.transition(SECTION_STATES[question["section"]])
        self.state.transition("capturing_response")
        return {
            "status": "question",
            "question_id": question["question_id"],
            "section": question["section"],
            "skill_domain": question["skill_domain"],
            "difficulty": question["difficulty"],
            "prompt": question["prompt"],
            "experience_band": self.experience_band,
            "progress": {"current": self.index, "total": len(self.questions)},
        }

    def submit_response(self, response, evaluation_status="insufficient", evaluation=None):
        if self.state.status != "capturing_response":
            raise RuntimeError("No response is currently expected")
        self.state.transition("evaluating")
        record = self.state.record_response(response, evaluation=evaluation)
        next_difficulty = self.difficulty.update(evaluation_status)
        self.state.transition("adapting")
        return {
            "status": "response_recorded",
            "question_id": record["question_id"],
            "evaluation_status": evaluation_status,
            "next_difficulty": next_difficulty,
            "next_action": "request_next_question",
        }

    def advance(self):
        if self.state.status != "adapting":
            raise RuntimeError("Call submit_response before advancing")
        self.state.transition("section_transition")
        return self.next_question()

    def pause(self):
        if self.state.status not in {"capturing_response", "evaluating", "adapting"}:
            raise RuntimeError("Interview cannot be paused from its current state")
        self.state.transition("paused")
        return {"status": "paused"}

    def resume(self):
        if self.state.status != "paused":
            raise RuntimeError("Only a paused interview can be resumed")
        self.state.transition("capturing_response")
        return {"status": "resumed", "question_id": self.state.current_question["question_id"]}

    def complete_report(self):
        if self.state.status != "completed":
            raise RuntimeError("Interview must be completed before requesting its report")
        return self.state.to_dict()
