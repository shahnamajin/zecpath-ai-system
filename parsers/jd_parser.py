import re


class JobDescriptionParser:

    def __init__(self):

        # Common skill synonyms
        self.skill_synonyms = {
            "python3": "Python",
            "py": "Python",
            "js": "JavaScript",
            "javascript": "JavaScript",
            "reactjs": "React",
            "react.js": "React",
            "nodejs": "Node.js",
            "node.js": "Node.js",
            "postgres": "PostgreSQL",
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence"
        }

        self.known_skills = [
            "python",
            "java",
            "javascript",
            "django",
            "flask",
            "react",
            "node.js",
            "sql",
            "mysql",
            "postgresql",
            "mongodb",
            "aws",
            "azure",
            "docker",
            "kubernetes",
            "machine learning",
            "artificial intelligence",
            "excel",
            "power bi"
        ]

    # -----------------------------------
    # Normalize JD Text
    # -----------------------------------
    def normalize_text(self, text):

        text = text.replace("•", " ")
        text = text.replace("\t", " ")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # -----------------------------------
    # Extract Role
    # -----------------------------------
    def extract_role(self, text):

        roles = [
            "Software Engineer",
            "Python Developer",
            "Data Scientist",
            "Data Analyst",
            "Machine Learning Engineer",
            "Business Analyst",
            "HR Executive",
            "Project Manager"
        ]

        for role in roles:

            if role.lower() in text.lower():
                return role

        return "Unknown"

    # -----------------------------------
    # Extract Skills
    # -----------------------------------
    def extract_skills(self, text):

        text_lower = text.lower()

        skills = []

        for skill in self.known_skills:

            if skill in text_lower:
                skills.append(skill.title())

        for synonym, standard_skill in self.skill_synonyms.items():

            if synonym in text_lower and standard_skill not in skills:
                skills.append(standard_skill)

        return list(dict.fromkeys(skills))

    # -----------------------------------
    # Extract Experience
    # -----------------------------------
    def extract_experience(self, text):

        pattern = r"(\d+)\+?\s*(?:years|year|yrs)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return {
                "minimum_years": int(match.group(1))
            }

        return {
            "minimum_years": 0
        }

    # -----------------------------------
    # Extract Education
    # -----------------------------------
    def extract_education(self, text):

        education_keywords = [
            "B.Tech",
            "B.E",
            "M.Tech",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Sc",
            "MBA",
            "Computer Science",
            "Computer Applications"
        ]

        education = []

        for item in education_keywords:

            if item.lower() in text.lower():
                education.append(item)

        return education

    # -----------------------------------
    # Parse Complete Job Description
    # -----------------------------------
    def parse(self, text):

        normalized_text = self.normalize_text(text)

        return {
            "job_title": self.extract_role(normalized_text),

            "required_skills": self.extract_skills(
                normalized_text
            ),

            "experience_required": self.extract_experience(
                normalized_text
            ),

            "education_required": self.extract_education(
                normalized_text
            )
        }