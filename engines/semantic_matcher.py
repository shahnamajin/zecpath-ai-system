from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # -----------------------------------
    # Convert text to embedding
    # -----------------------------------
    def embed(self, text):

        return self.model.encode([text])

    # -----------------------------------
    # Compute semantic similarity
    # -----------------------------------
    def similarity(self, text1, text2):

        emb1 = self.embed(text1)
        emb2 = self.embed(text2)

        score = cosine_similarity(
            emb1,
            emb2
        )[0][0]

        return round(float(score) * 100, 2)

    # -----------------------------------
    # Recommendation logic
    # -----------------------------------
    def recommend(self, score):

        if score >= 80:
            return "Strong Match"

        elif score >= 60:
            return "Moderate Match"

        else:
            return "Weak Match"

    # -----------------------------------
    # Resume ↔ JD overall matching
    # -----------------------------------
    def match(self, resume, jd):

        score = self.similarity(resume, jd)

        return {

            "overall_similarity": score,

            "recommendation": self.recommend(score)

        }

    # -----------------------------------
    # Section-wise semantic matching
    # -----------------------------------
    def section_match(
        self,
        resume_skills,
        jd_skills,
        resume_exp,
        jd_exp,
        resume_projects,
        jd_projects
    ):

        return {

            "skills_similarity": self.similarity(
                resume_skills,
                jd_skills
            ),

            "experience_similarity": self.similarity(
                resume_exp,
                jd_exp
            ),

            "project_similarity": self.similarity(
                resume_projects,
                jd_projects
            )

        }