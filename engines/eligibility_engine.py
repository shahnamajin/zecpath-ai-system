class EligibilityEngine:
    """
    Determines candidate eligibility for AI screening
    based on ATS score and recruiter-defined rules.
    """

    def evaluate(self, candidate, rules):
        reasons = []

        # -----------------------------
        # 1. ATS SCORE CHECK
        # -----------------------------
        ats_score = candidate.get("ats_score", 0)
        minimum_score = rules.get("minimum_ats_score", 0)

        if ats_score < minimum_score:
            return self._result(
                candidate,
                "Rejected",
                reasons + [
                    f"ATS score {ats_score} is below minimum score {minimum_score}"
                ]
            )

        # -----------------------------
        # 2. MANDATORY SKILLS CHECK
        # -----------------------------
        candidate_skills = {
            skill.lower()
            for skill in candidate.get("skills", [])
        }

        mandatory_skills = rules.get("mandatory_skills", [])

        missing_skills = [
            skill for skill in mandatory_skills
            if skill.lower() not in candidate_skills
        ]

        if missing_skills:
            reasons.append(
                f"Missing mandatory skills: {', '.join(missing_skills)}"
            )

        # -----------------------------
        # 3. EXPERIENCE CHECK
        # -----------------------------
        experience = candidate.get("experience_years", 0)

        min_experience = rules.get("min_experience", 0)
        max_experience = rules.get("max_experience")

        if experience < min_experience:
            reasons.append(
                f"Experience {experience} years is below minimum "
                f"{min_experience} years"
            )

        if max_experience is not None and experience > max_experience:
            reasons.append(
                f"Experience {experience} years exceeds maximum "
                f"{max_experience} years"
            )

        # -----------------------------
        # 4. LOCATION CHECK
        # -----------------------------
        candidate_location = candidate.get("location", "")
        allowed_locations = rules.get("allowed_locations", [])

        location_met = True

        if allowed_locations:
            location_met = any(
                location.lower() in candidate_location.lower()
                for location in allowed_locations
            )

            if not location_met:
                reasons.append(
                    f"Location '{candidate_location}' is not within "
                    f"allowed locations"
                )

        # -----------------------------
        # 5. AVAILABILITY CHECK
        # -----------------------------
        availability_met = True

        if rules.get("availability_required", False):
            availability_met = candidate.get("available", False)

            if not availability_met:
                reasons.append("Candidate availability requirement not satisfied")

        # -----------------------------
        # FINAL DECISION
        # -----------------------------
        if not missing_skills and \
           experience >= min_experience and \
           (max_experience is None or experience <= max_experience) and \
           location_met and \
           availability_met:

            return self._result(
                candidate,
                "Eligible",
                ["All eligibility criteria satisfied"]
            )

        # Conditions that need recruiter verification
        return self._result(
            candidate,
            "Review",
            reasons
        )

    def _result(self, candidate, decision, reasons):
        return {
            "candidate_id": candidate.get("candidate_id"),
            "ats_score": candidate.get("ats_score", 0),
            "mandatory_skills_met": not any(
                "Missing mandatory skills" in reason
                for reason in reasons
            ),
            "experience_met": not any(
                "Experience" in reason
                for reason in reasons
            ),
            "location_met": not any(
                "Location" in reason
                for reason in reasons
            ),
            "availability_met": not any(
                "availability" in reason.lower()
                for reason in reasons
            ),
            "eligibility": decision,
            "reason": "; ".join(reasons)
        }