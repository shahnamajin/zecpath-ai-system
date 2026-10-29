from config.role_weights import ROLE_WEIGHTS


class ATSScoringEngine:

    def __init__(self):
        pass

    # -----------------------------------
    # Handle missing values safely
    # -----------------------------------
    def safe_score(self, value):

        if value is None:
            return 0

        return value

    # -----------------------------------
    # Final ATS Score Calculation
    # -----------------------------------
    def calculate(
        self,
        role,
        skill_match,
        experience_relevance,
        education_alignment,
        semantic_similarity
    ):

        weights = ROLE_WEIGHTS.get(role)

        if not weights:
            raise ValueError(
                f"No weight configuration found for role: {role}"
            )

        skill_score = self.safe_score(skill_match)
        exp_score = self.safe_score(experience_relevance)
        edu_score = self.safe_score(education_alignment)
        sem_score = self.safe_score(semantic_similarity)

        final_score = (
            skill_score * weights["skill_match"] +
            exp_score * weights["experience_relevance"] +
            edu_score * weights["education_alignment"] +
            sem_score * weights["semantic_similarity"]
        )

        final_score = round(final_score, 2)

        return {

            "role": role,

            "final_score": final_score,

            "breakdown": {

                "skill_match": {
                    "score": skill_score,
                    "weight": weights["skill_match"],
                    "contribution": round(
                        skill_score * weights["skill_match"], 2
                    )
                },

                "experience_relevance": {
                    "score": exp_score,
                    "weight": weights["experience_relevance"],
                    "contribution": round(
                        exp_score * weights["experience_relevance"], 2
                    )
                },

                "education_alignment": {
                    "score": edu_score,
                    "weight": weights["education_alignment"],
                    "contribution": round(
                        edu_score * weights["education_alignment"], 2
                    )
                },

                "semantic_similarity": {
                    "score": sem_score,
                    "weight": weights["semantic_similarity"],
                    "contribution": round(
                        sem_score * weights["semantic_similarity"], 2
                    )
                }
            },

            "recommendation": self.recommend(final_score)

        }

    # -----------------------------------
    # Recommendation Logic
    # -----------------------------------
    def recommend(self, score):

        if score >= 80:
            return "Strong Match"

        elif score >= 60:
            return "Moderate Match"

        else:
            return "Weak Match"