from typing import Any, Dict, List


class ConversationBuilder:

    def build_question_object(
        self,
        question: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:

        return {
            "question_id": question["question_id"],

            "prompt": {
                "text": question["question"],
                "language": language
            },

            "classification": {
                "category": question["category"],
                "expected_answer_type": (
                    question["expected_answer_type"]
                )
            },

            "evaluation": {
                "mandatory": question["mandatory"],
                "scoring_importance": (
                    question["scoring_importance"]
                )
            },

            "conversation": {
                "allow_follow_up": (
                    question["follow_up_allowed"]
                ),
                "max_follow_ups": (
                    question["max_follow_ups"]
                )
            },

            "metadata": {
                "roles": question["roles"],
                "difficulty": question["difficulty"],
                "order": question["order"]
            }
        }

    def build_conversation(
        self,
        questions: List[Dict[str, Any]],
        language: str = "en"
    ) -> List[Dict[str, Any]]:

        return [
            self.build_question_object(
                question,
                language
            )
            for question in questions
        ]