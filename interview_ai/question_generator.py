import json
from pathlib import Path
from typing import List, Dict, Optional


class HRQuestionGenerator:
    """
    Role-based HR interview question generator.

    Selects questions based on:
    - Candidate type
    - Role type
    - Interview category
    - Previously asked questions
    """

    def __init__(self, question_bank_path: Optional[str] = None):
        if question_bank_path is None:
            question_bank_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "hr_interview"
                / "hr_question_bank.json"
            )

        self.question_bank_path = Path(question_bank_path)
        self.questions = self._load_question_bank()

    def _load_question_bank(self) -> List[Dict]:
        """Load questions from the JSON question bank."""

        if not self.question_bank_path.exists():
            raise FileNotFoundError(
                f"Question bank not found: {self.question_bank_path}"
            )

        with open(self.question_bank_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("questions", [])

    def filter_questions(
        self,
        candidate_type: str,
        role_type: str,
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter questions based on candidate type,
        role type and optional category.
        """

        candidate_type = candidate_type.lower().strip()
        role_type = role_type.lower().strip()

        filtered = []

        for question in self.questions:

            candidate_types = [
                value.lower()
                for value in question.get("candidate_type", [])
            ]

            role_types = [
                value.lower()
                for value in question.get("role_type", [])
            ]

            if candidate_type not in candidate_types:
                continue

            if role_type not in role_types:
                continue

            if category:
                if question.get("category") != category:
                    continue

            filtered.append(question)

        return filtered

    def generate_questions(
        self,
        candidate_type: str,
        role_type: str,
        categories: Optional[List[str]] = None,
        max_questions: int = 10
    ) -> List[Dict]:
        """
        Generate a role-based HR interview question list.

        Questions are selected category by category to maintain
        balanced interview coverage.
        """

        if categories is None:
            categories = [
                "self_introduction",
                "career_journey",
                "strengths_weaknesses",
                "teamwork_culture",
                "career_goals",
                "availability_commitment"
            ]

        selected_questions = []
        used_question_ids = set()

        for category in categories:

            category_questions = self.filter_questions(
                candidate_type=candidate_type,
                role_type=role_type,
                category=category
            )

            for question in category_questions:

                question_id = question.get("question_id")

                if question_id in used_question_ids:
                    continue

                selected_questions.append(question)
                used_question_ids.add(question_id)

                break

            if len(selected_questions) >= max_questions:
                break

        return selected_questions[:max_questions]

    def get_follow_up_eligible_questions(
        self,
        questions: List[Dict]
    ) -> List[Dict]:
        """Return only questions that allow follow-up questions."""

        return [
            question
            for question in questions
            if question.get("follow_up_eligible", False)
        ]

    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """Find a question using its question ID."""

        for question in self.questions:
            if question.get("question_id") == question_id:
                return question

        return None

    def get_categories(self) -> List[str]:
        """Return all available question categories."""

        categories = []

        for question in self.questions:
            category = question.get("category")

            if category and category not in categories:
                categories.append(category)

        return categories

    def get_question_count(self) -> int:
        """Return total number of questions."""

        return len(self.questions)