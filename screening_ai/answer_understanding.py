from .intent_classifier import IntentClassifier
from .answer_extractor import AnswerExtractor


class AnswerUnderstandingEngine:
    """
    Converts candidate responses into semantic,
    AI-processable answer objects.
    """

    def __init__(self):

        self.classifier = IntentClassifier()
        self.extractor = AnswerExtractor()

    def understand(
        self,
        candidate_id,
        job_id,
        question_id,
        question_category,
        text,
        confidence_level=1.0,
    ):
        """
        Understand and structure a candidate answer.
        """

        intent = self.classifier.classify(
            text,
            question_category=question_category,
        )

        skills = self.extractor.extract_skills(text)

        experience = self.extractor.extract_experience(text)

        availability = (
            self.extractor.extract_availability(text)
        )

        salary = self.extractor.extract_salary(text)

        return {
            "candidate_id": candidate_id,

            "job_id": job_id,

            "question_id": question_id,

            "answer": {
                "raw_text": text,
                "intent": intent,
                "confidence_level": round(
                    confidence_level,
                    3
                )
            },

            "entities": {
                "skills": skills,

                "experience": experience,

                "availability": availability,

                "salary_expectation": salary,
            },

            "quality": {
                "is_missing": (
                    intent == "missing"
                ),

                "is_vague": (
                    intent == "vague"
                ),

                "is_off_topic": (
                    intent == "off_topic"
                ),
            }
        }