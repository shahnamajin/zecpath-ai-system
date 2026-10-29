class ScreeningScorer:
    """
    Calculates individual screening parameters:
    clarity, relevance, completeness and consistency.
    """

    def __init__(self):
        self.weights = {
            "clarity": 0.25,
            "relevance": 0.30,
            "completeness": 0.25,
            "consistency": 0.20,
        }

    def score_clarity(self, text, intent, quality):
        """
        Score how clearly the candidate communicates.
        """

        if not text or quality.get("is_missing"):
            return 0.0

        if quality.get("is_vague"):
            return 30.0

        words = text.strip().split()

        word_count = len(words)

        if word_count <= 2:
            return 40.0

        if word_count <= 5:
            return 60.0

        if word_count <= 15:
            return 85.0

        return 95.0

    def score_relevance(self, intent, quality):
        """
        Score how relevant the answer is to the question.
        """

        if quality.get("is_missing"):
            return 0.0

        if quality.get("is_off_topic"):
            return 10.0

        if quality.get("is_vague"):
            return 40.0

        if intent in {
            "introduction",
            "education",
            "experience",
            "skills",
            "availability",
            "salary_expectation",
            "location",
        }:
            return 95.0

        return 50.0

    def score_completeness(
        self,
        text,
        entities,
        intent,
        quality
    ):
        """
        Score whether the candidate has provided sufficient information.
        """

        if not text or quality.get("is_missing"):
            return 0.0

        if quality.get("is_vague"):
            return 20.0

        if quality.get("is_off_topic"):
            return 10.0

        score = 50.0

        skills = entities.get("skills", [])

        experience = entities.get(
            "experience",
            {}
        )

        availability = entities.get(
            "availability",
            {}
        )

        salary = entities.get(
            "salary_expectation",
            {}
        )

        if intent == "skills":

            if len(skills) >= 3:
                score = 100.0

            elif len(skills) == 2:
                score = 85.0

            elif len(skills) == 1:
                score = 70.0

            else:
                score = 40.0

        elif intent == "experience":

            if experience.get("years") is not None:

                if experience.get("types"):
                    score = 100.0
                else:
                    score = 85.0

            elif experience.get("types"):
                score = 70.0

            else:
                score = 40.0

        elif intent == "availability":

            if (
                availability.get(
                    "immediately_available"
                )
                or availability.get("notice_period")
            ):
                score = 95.0
            else:
                score = 40.0

        elif intent == "salary_expectation":

            if salary.get("mentioned"):
                score = 95.0
            else:
                score = 30.0

        else:

            word_count = len(
                text.strip().split()
            )

            if word_count >= 15:
                score = 95.0
            elif word_count >= 8:
                score = 80.0
            elif word_count >= 4:
                score = 65.0
            else:
                score = 40.0

        return min(score, 100.0)

    def score_consistency(
        self,
        entities,
        previous_context=None
    ):
        """
        Score consistency with previously known candidate information.

        If no previous context exists, a neutral score is returned.
        """

        if not previous_context:
            return 80.0

        consistency_score = 100.0

        current_skills = set(
            entities.get("skills", [])
        )

        previous_skills = set(
            previous_context.get(
                "skills",
                []
            )
        )

        if previous_skills and current_skills:

            if not current_skills.intersection(
                previous_skills
            ):
                consistency_score -= 30.0

        current_experience = entities.get(
            "experience",
            {}
        )

        previous_experience = previous_context.get(
            "experience",
            {}
        )

        current_years = current_experience.get(
            "years"
        )

        previous_years = previous_experience.get(
            "years"
        )

        if (
            current_years is not None
            and previous_years is not None
        ):

            if abs(
                current_years - previous_years
            ) > 1.0:

                consistency_score -= 30.0

        return max(
            0.0,
            consistency_score
        )

    def calculate_weighted_score(
        self,
        clarity,
        relevance,
        completeness,
        consistency
    ):
        """
        Calculate weighted score out of 100.
        """

        score = (
            clarity * self.weights["clarity"]
            + relevance * self.weights["relevance"]
            + completeness * self.weights["completeness"]
            + consistency * self.weights["consistency"]
        )

        return round(
            max(0.0, min(100.0, score)),
            2
        )

    def score_answer(
        self,
        text,
        intent,
        entities,
        quality,
        previous_context=None
    ):
        """
        Generate a complete per-question score.
        """

        clarity = self.score_clarity(
            text,
            intent,
            quality
        )

        relevance = self.score_relevance(
            intent,
            quality
        )

        completeness = self.score_completeness(
            text,
            entities,
            intent,
            quality
        )

        consistency = self.score_consistency(
            entities,
            previous_context
        )

        total_score = self.calculate_weighted_score(
            clarity,
            relevance,
            completeness,
            consistency
        )

        return {
            "clarity": clarity,
            "relevance": relevance,
            "completeness": completeness,
            "consistency": consistency,
            "total_score": total_score
        }