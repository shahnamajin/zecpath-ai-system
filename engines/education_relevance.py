class EducationRelevance:

    RELEVANT_DEGREES = {
        "Software Engineer": [
            "BCA",
            "Bachelor of Computer Applications",
            "MCA",
            "Master of Computer Applications",
            "B.Tech",
            "M.Tech"
        ],

        "Data Analyst": [
            "BCA",
            "Bachelor of Computer Applications",
            "MCA",
            "Master of Computer Applications",
            "BSc",
            "MSc"
        ],

        "Data Scientist": [
            "MCA",
            "Master of Computer Applications",
            "MSc",
            "B.Tech",
            "M.Tech"
        ]
    }

    def evaluate(self, education_list, target_role):

        relevant = self.RELEVANT_DEGREES.get(target_role, [])

        score = 0
        matched = []

        for edu in education_list:

            degree = edu.get("degree_type", "")

            degree_lower = degree.lower()

            for rel in relevant:

                rel_lower = rel.lower()

                # Exact or partial match
                if rel_lower in degree_lower or degree_lower in rel_lower:

                    score = 100

                    if degree not in matched:
                        matched.append(degree)

                    break

        return {
            "education_relevance_score": score,
            "matched_degrees": matched
        }