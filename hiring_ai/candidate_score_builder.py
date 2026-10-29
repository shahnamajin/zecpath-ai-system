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
        role_type="default"
    ):
        result = self.engine.calculate(
            ats_score,
            screening_score,
            hr_interview_score,
            role_type
        )

        return {
            "score_id": str(uuid4()),
            "candidate_id": candidate_id,
            "job_id": job_id,
            "role_type": role_type,
            "evaluation_rounds": result["scores"],
            "weights": result["weights"],
            "weighted_contributions": result[
                "weighted_contributions"
            ],
            "hiring_fit_percentage": result[
                "hiring_fit_percentage"
            ],
            "status": result["status"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }