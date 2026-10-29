from typing import List


class FallbackHandler:

    FALLBACK_QUESTIONS = {

        "experience": [
            "Could you briefly describe your previous work or project experience?",
            "Can you mention one project where you used these skills?"
        ],

        "skills": [
            "Could you name the main technical skills you are comfortable with?",
            "Which technologies have you worked with recently?"
        ],

        "education": [
            "Could you briefly tell me about your highest qualification?",
            "What did you specialize in during your studies?"
        ],

        "availability": [
            "When would you be available to join?",
            "How soon could you start if selected?"
        ],

        "salary_expectation": [
            "Could you share your expected salary range?",
            "What compensation range are you looking for?"
        ],

        "general": [
            "Could you please provide a little more detail?",
            "Could you briefly explain your answer?"
        ]
    }

    def get_questions(
        self,
        category: str,
    ) -> List[str]:

        return self.FALLBACK_QUESTIONS.get(
            category,
            self.FALLBACK_QUESTIONS["general"]
        )

    def get_question(
        self,
        category: str,
        attempt: int = 0,
    ) -> str:

        questions = self.get_questions(category)

        index = min(
            attempt,
            len(questions) - 1
        )

        return questions[index]