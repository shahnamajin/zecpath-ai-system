from typing import Any, Dict, List


class HRQuestionSelector:
    """
    Selects and orders HR screening questions based on role.
    """

    CATEGORY_ORDER = [
        "introduction",
        "education",
        "experience",
        "skills",
        "location",
        "salary",
        "notice_period"
    ]

    def __init__(self, questions: List[Dict[str, Any]]):
        self.questions = questions

    def get_questions_for_role(
        self,
        role: str
    ) -> List[Dict[str, Any]]:
        role = role.lower().strip()

        return [
            question
            for question in self.questions
            if (
                "all" in [
                    r.lower()
                    for r in question.get("roles", [])
                ]
                or role in [
                    r.lower()
                    for r in question.get("roles", [])
                ]
            )
        ]

    def get_mandatory_questions_for_role(
        self,
        role: str
    ) -> List[Dict[str, Any]]:
        return [
            question
            for question in self.get_questions_for_role(role)
            if question.get("mandatory") is True
        ]

    def get_questions_by_category(
        self,
        role: str,
        category: str
    ) -> List[Dict[str, Any]]:
        return [
            question
            for question in self.get_questions_for_role(role)
            if question.get("category") == category
        ]

    def prioritize_questions(
        self,
        questions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Prioritize questions by scoring importance.
        This method is useful for analysis, but is NOT used
        to determine the natural conversation order.
        """

        return sorted(
            questions,
            key=lambda q: q.get(
                "scoring_importance",
                0
            ),
            reverse=True
        )

    def build_screening_sequence(
        self,
        role: str
    ) -> List[Dict[str, Any]]:
        """
        Build a natural HR screening conversation.

        The order field controls the conversation flow.
        Scoring importance does not override the natural flow.
        """

        questions = self.get_questions_for_role(role)

        sequence = []

        for category in self.CATEGORY_ORDER:

            category_questions = [
                question
                for question in questions
                if question.get("category") == category
            ]

            category_questions.sort(
                key=lambda q: q.get("order", 999)
            )

            sequence.extend(category_questions)

        return sequence