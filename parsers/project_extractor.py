class ProjectExtractor:

    def extract(self, text):

        projects = []

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        current_project = None

        for line in lines:

            # New project
            if "–" in line and "Technologies" not in line:

                if current_project:
                    projects.append(current_project)

                title, category = line.split("–", 1)

                current_project = {
                    "title": title.strip(),
                    "category": category.strip(),
                    "technologies": [],
                    "description": []
                }

            elif line.startswith("Technologies:"):

                techs = line.replace("Technologies:", "").strip()

                current_project["technologies"] = [
                    tech.strip() for tech in techs.split(",")
                ]

            elif line.startswith("•"):

                current_project["description"].append(
                    line.replace("•", "").strip()
                )

            else:
                # Continue previous description if line doesn't start with a bullet
                if current_project and current_project["description"]:
                    current_project["description"][-1] += " " + line

        if current_project:
            projects.append(current_project)

        return projects