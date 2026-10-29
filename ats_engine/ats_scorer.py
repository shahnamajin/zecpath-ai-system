
import json
from datetime import datetime


class ATSScorer:
    """Calculate ATS scores from candidate profiles and job descriptions."""

    @staticmethod
    def _normalize_skills(candidate_skills):
        """Convert supported skill formats into normalized skill strings."""
        normalized = []

        def add_skill(value):
            if isinstance(value, str):
                skill = value.strip().lower()
                if skill:
                    normalized.append(skill)

            elif isinstance(value, dict):
                # Handle common skill object formats.
                for key in ("name", "skill", "skill_name", "value"):
                    if key in value and isinstance(value[key], str):
                        add_skill(value[key])
                        return

                # Handle dictionaries that group skills by category.
                for nested_value in value.values():
                    add_skill(nested_value)

            elif isinstance(value, (list, tuple, set)):
                for item in value:
                    add_skill(item)

        add_skill(candidate_skills)

        # Remove duplicates while preserving order.
        return list(dict.fromkeys(normalized))

    def score(self, candidate, job_path):
        """Score a candidate against a JSON job description."""

        # Load job description.
        with open(job_path, "r", encoding="utf-8") as file:
            job = json.load(file)

        # Validate required candidate fields.
        required_candidate_fields = [
            "candidate_id",
            "skills",
            "education",
            "projects",
            "experience",
            "certifications",
        ]

        missing_fields = [
            field
            for field in required_candidate_fields
            if field not in candidate
        ]

        if missing_fields:
            raise ValueError(
                f"Candidate data is missing fields: {missing_fields}"
            )

        # Normalize candidate skills, supporting nested dictionaries.
        candidate_skills = self._normalize_skills(candidate["skills"])

        # Normalize required job skills.
        required_skills = self._normalize_skills(
            job.get("required_skills", [])
        )

        if not required_skills:
            raise ValueError(
                "Job description must contain at least one required skill."
            )

        # Match skills.
        matched_skills = [
            skill for skill in required_skills
            if skill in candidate_skills
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill not in candidate_skills
        ]

        # Skill score: 40 marks.
        skills_score = int(
            (len(matched_skills) / len(required_skills)) * 40
        )

        # Education score: 20 marks.
        education_score = 20 if candidate["education"] else 0

        # Project score: 20 marks.
        projects = candidate["projects"] or []

        if len(projects) >= 2:
            project_score = 20
        elif len(projects) == 1:
            project_score = 10
        else:
            project_score = 0

        # Experience score: 10 marks.
        experience_score = 10 if candidate["experience"] else 0

        # Certification score: 10 marks.
        certifications = candidate["certifications"] or []
        certification_score = 10 if certifications else 0

        # Overall score: maximum 100 marks.
        overall_score = (
            skills_score
            + education_score
            + project_score
            + experience_score
            + certification_score
        )

        # Recommendation.
        if overall_score >= 80:
            recommendation = "Shortlist"
        elif overall_score >= 60:
            recommendation = "Review"
        else:
            recommendation = "Reject"

        # Final ATS report.
        report = {
            "candidate_id": candidate["candidate_id"],
            "job_id": job.get("job_id"),
            "scores": {
                "skills": skills_score,
                "education": education_score,
                "projects": project_score,
                "experience": experience_score,
                "certifications": certification_score,
            },
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": recommendation,
            "score_breakdown": {
                "skills": (
                    f"{len(matched_skills)}/{len(required_skills)} "
                    "required skills matched."
                ),
                "education": (
                    "Education details found."
                    if education_score
                    else "Education not found."
                ),
                "projects": f"{len(projects)} project(s) identified.",
                "experience": (
                    "Professional experience found."
                    if experience_score
                    else "No professional experience found."
                ),
                "certifications": (
                    f"{len(certifications)} certification(s) identified."
                ),
            },
            "ai_metadata": {
                "model": "ATS Scorer V2",
                "version": "2.0",
                "processed_at": datetime.now().isoformat(),
            },
        }

        return report
