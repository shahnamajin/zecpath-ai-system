from hiring_ai.unified_scoring_engine import UnifiedScoringEngine


class HiringFitCalculator:

    def __init__(self):
        self.engine = UnifiedScoringEngine()

    def calculate_hiring_fit(
        self,
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

        result = self.engine.calculate(
            scores=scores,
            role_type=role_type,
        )

        return result["hiring_fit_percentage"]