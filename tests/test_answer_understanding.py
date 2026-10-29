from screening_ai.intent_classifier import IntentClassifier
from screening_ai.answer_extractor import AnswerExtractor
from screening_ai.answer_understanding import (
    AnswerUnderstandingEngine
)


def test_skills_intent():

    classifier = IntentClassifier()

    result = classifier.classify(
        "I have experience with Python and SQL.",
        question_category="skills"
    )

    assert result == "skills"


def test_experience_intent():

    classifier = IntentClassifier()

    result = classifier.classify(
        "I completed a six month internship.",
        question_category="experience"
    )

    assert result == "experience"


def test_availability_intent():

    classifier = IntentClassifier()

    result = classifier.classify(
        "I can join immediately.",
        question_category="availability"
    )

    assert result == "availability"


def test_salary_intent():

    classifier = IntentClassifier()

    result = classifier.classify(
        "I expect 5 LPA.",
        question_category="salary_expectation"
    )

    assert result == "salary_expectation"


def test_missing_intent():

    classifier = IntentClassifier()

    assert classifier.classify("") == "missing"


def test_vague_intent():

    classifier = IntentClassifier()

    assert classifier.classify("Yes.") == "vague"


def test_off_topic_intent():

    classifier = IntentClassifier()

    result = classifier.classify(
        "I enjoy watching movies on weekends."
    )

    assert result == "off_topic"


def test_skill_extraction():

    extractor = AnswerExtractor()

    skills = extractor.extract_skills(
        "I have used Python, SQL and Flask."
    )

    assert "python" in skills
    assert "sql" in skills
    assert "flask" in skills


def test_experience_extraction():

    extractor = AnswerExtractor()

    result = extractor.extract_experience(
        "I have two years of work experience."
    )

    assert result["years"] == 2.0
    assert "work" in result["types"]


def test_availability_extraction():

    extractor = AnswerExtractor()

    result = extractor.extract_availability(
        "I can join in 2 weeks."
    )

    assert result["notice_period"] == "2 weeks"


def test_salary_extraction():

    extractor = AnswerExtractor()

    result = extractor.extract_salary(
        "I expect 5 LPA."
    )

    assert result["mentioned"] is True
    assert result["values"][0]["value"] == 5.0


def test_structured_answer():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_SKILL_PY_001",
        question_category="skills",
        text="I have experience with Python and SQL.",
        confidence_level=0.95,
    )

    assert result["candidate_id"] == "CAND_1001"

    assert result["job_id"] == "JOB_2001"

    assert result["question_id"] == "HR_SKILL_PY_001"

    assert result["answer"]["intent"] == "skills"

    assert "python" in result["entities"]["skills"]

    assert "sql" in result["entities"]["skills"]

    assert result["quality"]["is_off_topic"] is False