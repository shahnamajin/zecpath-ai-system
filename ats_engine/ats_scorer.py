import json
from datetime import datetime


class ATSScorer:

    def score(self, candidate, job_path):

        # -----------------------------
        # Load Job Description
        # -----------------------------
        with open(job_path, "r", encoding="utf-8") as file:
            job = json.load(file)

        # -----------------------------
        # Candidate Skills
        # -----------------------------
        candidate_skills = []

        for category in candidate["skills"].values():
            candidate_skills.extend(category)

        candidate_skills = [
            skill.lower().strip()
            for skill in candidate_skills
        ]

        # -----------------------------
        # Required Skills
        # -----------------------------
        required_skills = [
            skill.lower().strip()
            for skill in job["required_skills"]
        ]

        matched_skills = []
        missing_skills = []

        for skill in required_skills:

            if skill in candidate_skills:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

        # -----------------------------
        # Skill Score (40 Marks)
        # -----------------------------
        skills_score = int(
            (len(matched_skills) / len(required_skills)) * 40
        )

        # -----------------------------
        # Education Score (20 Marks)
        # -----------------------------
        education_score = 20 if candidate["education"] else 0

        # -----------------------------
        # Project Score (20 Marks)
        # -----------------------------
        if len(candidate["projects"]) >= 2:
            project_score = 20
        elif len(candidate["projects"]) == 1:
            project_score = 10
        else:
            project_score = 0

        # -----------------------------
        # Experience Score (10 Marks)
        # -----------------------------
        experience_score = 10 if candidate["experience"] else 0

        # -----------------------------
        # Certification Score (10 Marks)
        # -----------------------------
        certification_score = (
            10 if candidate["certifications"] else 0
        )

        # -----------------------------
        # Overall Score
        # -----------------------------
        overall_score = (
            skills_score
            + education_score
            + project_score
            + experience_score
            + certification_score
        )

        # -----------------------------
        # Recommendation
        # -----------------------------
        if overall_score >= 80:
            recommendation = "Shortlist"

        elif overall_score >= 60:
            recommendation = "Review"

        else:
            recommendation = "Reject"

        # -----------------------------
        # Final ATS Report
        # -----------------------------
        report = {

            "candidate_id": candidate["candidate_id"],

            "job_id": job["job_id"],

            "scores": {

                "skills": skills_score,

                "education": education_score,

                "projects": project_score,

                "experience": experience_score,

                "certifications": certification_score

            },

            "overall_score": overall_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "recommendation": recommendation,

            "score_breakdown": {

                "skills":
                    f"{len(matched_skills)}/{len(required_skills)} required skills matched.",

                "education":
                    "Education details found."
                    if education_score
                    else "Education not found.",

                "projects":
                    f"{len(candidate['projects'])} project(s) identified.",

                "experience":
                    "Professional experience found."
                    if experience_score
                    else " No professional experience found.",

                "certifications":
                    f"{len(candidate['certifications'])} certification(s) identified."

            },

            "ai_metadata": {

                "model": "ATS Scorer V2",

                "version": "2.0",

                "processed_at": datetime.now().isoformat()

            }

        }

        return report