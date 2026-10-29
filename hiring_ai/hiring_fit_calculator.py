from hiring_ai.unified_scoring_engine import UnifiedScoringEngine


class HiringFitCalculator:
    def __init__(self):
        self.engine = UnifiedScoringEngine()

    def calculate_hiring_fit(
        self,
        ats_score,
        screening_score,
        hr_interview_score,
        role_type="default"
    ):
        result = self.engine.calculate(
            ats_score=ats_score,
            screening_score=screening_score,
            hr_interview_score=hr_interview_score,
            role_type=role_type
        )

        return result["hiring_fit_percentage"]