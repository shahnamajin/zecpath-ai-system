from datetime import datetime
from config.role_similarity import ROLE_SIMILARITY


class ExperienceRelevance:

    def __init__(self):
        pass

    # -----------------------------------
    # Convert year string to integer
    # -----------------------------------
    def year(self, value):

        if not value:
            return None

        value = value.strip()

        if value.lower() == "present":
            return datetime.now().year

        try:
            return int(value[-4:])
        except:
            return None

    # -----------------------------------
    # Calculate Total Experience
    # -----------------------------------
    def total_experience(self, experiences):

        total = 0

        for exp in experiences:

            start = self.year(exp.get("start_date"))
            end = self.year(exp.get("end_date"))

            if start and end:
                total += end - start

        return f"{total} Years"

    # -----------------------------------
    # Detect Employment Gaps
    # -----------------------------------
    def detect_gaps(self, experiences):

        gaps = []

        if len(experiences) < 2:
            return gaps

        sorted_exp = sorted(
            experiences,
            key=lambda x: self.year(x.get("start_date")) or 9999
        )

        for i in range(len(sorted_exp) - 1):

            current_end = self.year(sorted_exp[i].get("end_date"))
            next_start = self.year(sorted_exp[i + 1].get("start_date"))

            if current_end and next_start:

                if next_start > current_end:

                    gaps.append({
                        "from": current_end,
                        "to": next_start,
                        "duration": f"{next_start - current_end} Years"
                    })

        return gaps

    # -----------------------------------
    # Detect Overlapping Jobs
    # -----------------------------------
    def detect_overlap(self, experiences):

        if len(experiences) < 2:
            return False

        sorted_exp = sorted(
            experiences,
            key=lambda x: self.year(x.get("start_date")) or 9999
        )

        for i in range(len(sorted_exp) - 1):

            current_end = self.year(sorted_exp[i].get("end_date"))
            next_start = self.year(sorted_exp[i + 1].get("start_date"))

            if current_end and next_start:

                if next_start < current_end:
                    return True

        return False

    # -----------------------------------
    # Calculate Role Relevance
    # -----------------------------------
    def relevance_score(self, experiences, target_role):

        score = 0
        matched_roles = []

        target_lower = target_role.lower()

        for exp in experiences:

            role = exp.get("designation", "")
            role_lower = role.lower()

            # Exact or partial match
            if target_lower in role_lower or role_lower in target_lower:

                score = 100

                if role not in matched_roles:
                    matched_roles.append(role)

                continue

            # Similar roles
            similar_roles = ROLE_SIMILARITY.get(target_role, [])

            for sim in similar_roles:

                sim_lower = sim.lower()

                if sim_lower in role_lower or role_lower in sim_lower:

                    score = max(score, 90)

                    if role not in matched_roles:
                        matched_roles.append(role)

                    break

        return score, matched_roles

    # -----------------------------------
    # Generate Final Report
    # -----------------------------------
    def generate(self, experiences, target_role):

        score, matched = self.relevance_score(
            experiences,
            target_role
        )

        report = {

            "total_experience": self.total_experience(experiences),

            "gaps": self.detect_gaps(experiences),

            "overlap": self.detect_overlap(experiences),

            "relevance_score": score,

            "matching_roles": matched

        }

        return report