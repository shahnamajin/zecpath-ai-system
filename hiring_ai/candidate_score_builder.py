from datetime import datetime, timezone
from uuid import uuid4

from hiring_ai.unified_scoring_engine import UnifiedScoringEngine


class CandidateScoreBuilder:
    def __init__(self):
        self.engine = UnifiedScoringEngine()

    def build(
        self,
        candidate_id,
        job_id,
        ats_score,
        screening_score,
        hr_interview_score,
        technical_interview_score,
        machine_test_score,
        role_type="default",
    ):
        scores = {
            "ats": ats_score,
            "screening": screening_score,
            "hr_interview": hr_interview_score,
            "technical_interview": technical_interview_score,
            "machine_test": machine_test_score,
        }

        result = self.engine.calculate(scores, role_type)

        return {
            "score_id": str(uuid4()),
            "candidate_id": candidate_id,
            "job_id": job_id,
            "role_type": result["role_type"],
            "evaluation_rounds": result["scores"],
            "weights": result["weights"],
            "weighted_contributions": result[
                "weighted_contributions"
            ],
            "hiring_fit_percentage": result[
                "hiring_fit_percentage"
            ],
            "completed_stages": result["completed_stages"],
            "missing_stages": result["missing_stages"],
            "completion_percentage": result[
                "completion_percentage"
            ],
            "status": result["status"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }