import json
from pathlib import Path
from typing import Any, Dict, List


class HRQuestionLoader:

    REQUIRED_FIELDS = {
        "question_id",
        "category",
        "question",
        "expected_answer_type",
        "mandatory",
        "scoring_importance",
        "roles",
        "difficulty",
        "follow_up_allowed",
        "max_follow_ups",
        "order"
    }

    VALID_DIFFICULTIES = {
        "easy",
        "medium",
        "hard"
    }

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_data(self) -> Dict[str, Any]:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Question dataset not found: {self.file_path}"
            )

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def load_questions(self) -> List[Dict[str, Any]]:

        data = self.load_data()

        questions = data.get("questions", [])

        if not isinstance(questions, list):
            raise ValueError(
                "'questions' must be a list"
            )

        return questions

    def get_question_by_id(
        self,
        question_id: str
    ) -> Dict[str, Any] | None:

        for question in self.load_questions():

            if question.get("question_id") == question_id:
                return question

        return None

    def get_questions_by_category(
        self,
        category: str
    ) -> List[Dict[str, Any]]:

        return [
            question
            for question in self.load_questions()
            if question.get("category") == category
        ]

    def get_mandatory_questions(
        self
    ) -> List[Dict[str, Any]]:

        return [
            question
            for question in self.load_questions()
            if question.get("mandatory") is True
        ]

    def validate_question(
        self,
        question: Dict[str, Any]
    ) -> List[str]:

        errors = []

        missing_fields = (
            self.REQUIRED_FIELDS -
            set(question.keys())
        )

        if missing_fields:
            errors.append(
                f"Missing fields: {sorted(missing_fields)}"
            )

        scoring = question.get(
            "scoring_importance"
        )

        if not isinstance(
            scoring,
            (int, float)
        ):
            errors.append(
                "scoring_importance must be numeric"
            )
        elif not 0 <= scoring <= 1:
            errors.append(
                "scoring_importance must be between 0 and 1"
            )

        if question.get(
            "difficulty"
        ) not in self.VALID_DIFFICULTIES:
            errors.append(
                f"Invalid difficulty: "
                f"{question.get('difficulty')}"
            )

        if not isinstance(
            question.get("roles"),
            list
        ):
            errors.append(
                "roles must be a list"
            )

        if not isinstance(
            question.get("mandatory"),
            bool
        ):
            errors.append(
                "mandatory must be boolean"
            )

        if not isinstance(
            question.get("follow_up_allowed"),
            bool
        ):
            errors.append(
                "follow_up_allowed must be boolean"
            )

        if not isinstance(
            question.get("max_follow_ups"),
            int
        ):
            errors.append(
                "max_follow_ups must be integer"
            )
        elif question.get("max_follow_ups") < 0:
            errors.append(
                "max_follow_ups cannot be negative"
            )

        if not isinstance(
            question.get("order"),
            int
        ):
            errors.append(
                "order must be integer"
            )
        elif question.get("order") < 1:
            errors.append(
                "order must be greater than 0"
            )

        return errors

    def validate_dataset(self) -> Dict[str, Any]:

        questions = self.load_questions()

        errors = []
        question_ids = set()

        for index, question in enumerate(questions):

            validation_errors = (
                self.validate_question(question)
            )

            if validation_errors:

                errors.append({
                    "index": index,
                    "question_id": question.get(
                        "question_id"
                    ),
                    "errors": validation_errors
                })

            question_id = question.get(
                "question_id"
            )

            if question_id in question_ids:

                errors.append({
                    "index": index,
                    "question_id": question_id,
                    "errors": [
                        "Duplicate question_id"
                    ]
                })

            question_ids.add(question_id)

        return {
            "valid": len(errors) == 0,
            "total_questions": len(questions),
            "errors": errors
        }