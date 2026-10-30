"""Role-, section-, experience- and difficulty-aware technical question selector."""
import json
from pathlib import Path


class TechnicalQuestionSelector:
    def __init__(self, role_domains_path=None, hierarchy_path=None, question_bank_path=None):
        root = Path(__file__).resolve().parent.parent
        data_dir = root / "data" / "technical_interview"
        self.role_domains_path = Path(role_domains_path or data_dir / "role_skill_domains.json")
        self.hierarchy_path = Path(hierarchy_path or data_dir / "question_hierarchy.json")
        self.question_bank_path = Path(question_bank_path or data_dir / "technical_question_bank.json")
        self.roles = self._load(self.role_domains_path)["roles"]
        self.hierarchy = self._load(self.hierarchy_path)
        self.questions = self._load(self.question_bank_path)["questions"]
        self._validate_question_bank()

    @staticmethod
    def _load(path):
        if not path.exists():
            raise FileNotFoundError(f"Technical interview data file not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _validate_question_bank(self):
        required = {"question_id", "role_ids", "skill_domain", "section",
                    "experience_bands", "difficulty", "prompt", "expected_evidence"}
        ids = set()
        for question in self.questions:
            missing = required - question.keys()
            if missing:
                raise ValueError(f"Question missing fields {sorted(missing)}")
            if question["question_id"] in ids:
                raise ValueError(f"Duplicate question_id: {question['question_id']}")
            ids.add(question["question_id"])

    def resolve_experience_band(self, years):
        if isinstance(years, bool) or not isinstance(years, (int, float)) or years < 0:
            raise ValueError("experience_years must be a non-negative number")
        for band in self.hierarchy["experience_bands"]:
            lower = band["min_years_inclusive"]
            upper = band["max_years_exclusive"]
            if years >= lower and (upper is None or years < upper):
                return band["id"]
        raise ValueError(f"No experience band configured for {years} years")

    def get_role(self, role_id):
        for role in self.roles:
            if role["role_id"] == role_id:
                return role
        raise ValueError(f"Unsupported role_id: {role_id}")

    def select_questions(self, role_id, experience_years, sections=None,
                         max_questions=12, used_question_ids=None):
        if max_questions < 1:
            raise ValueError("max_questions must be at least 1")
        role = self.get_role(role_id)
        band = self.resolve_experience_band(experience_years)
        sections = sections or ["introduction", "experience_based", "conceptual", "scenario_based"]
        allowed_domains = set(role["core_domains"] + role["supporting_domains"] + role["optional_domains"])
        used = set(used_question_ids or [])
        selected = []
        for section in sections:
            eligible = [
                q for q in self.questions
                if role_id in q["role_ids"]
                and q["skill_domain"] in allowed_domains
                and q["section"] == section
                and band in q["experience_bands"]
                and q["question_id"] not in used
            ]
            eligible.sort(key=lambda q: (
                q["difficulty"] != self.hierarchy["experience_bands"][
                    next(i for i, item in enumerate(self.hierarchy["experience_bands"]) if item["id"] == band)
                ]["baseline_difficulty"],
                q["question_id"],
            ))
            for question in eligible:
                selected.append(dict(question))
                used.add(question["question_id"])
                if len(selected) >= max_questions:
                    return selected
        return selected
