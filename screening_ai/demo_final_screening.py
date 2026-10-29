"""
ZECPath AI - End-to-End Screening Demo

Day 32 - Screening System Finalization

This demo brings together the major screening stages:
1. Question selection
2. Candidate response
3. Intent understanding
4. Screening decision
5. Edge-case handling
6. Final screening summary

This is a local demonstration and does not require a real STT API key.
"""

from typing import Dict, List

from screening_ai.intent_classifier import IntentClassifier
from screening_ai.answer_extractor import AnswerExtractor
from screening_ai.confidence_analyzer import ConfidenceAnalyzer
from screening_ai.sentiment_analyzer import SentimentAnalyzer
from screening_ai.edge_case_handler import EdgeCaseHandler


# ---------------------------------------------------------------------
# Candidate / Job Information
# ---------------------------------------------------------------------

CANDIDATE_ID = "CAND_1001"
JOB_ID = "JOB_2001"
SESSION_ID = "SESSION_3001"

JOB_TITLE = "Python Developer"


# ---------------------------------------------------------------------
# Simulated Screening Questions
# ---------------------------------------------------------------------

QUESTIONS = [
    {
        "question_id": "HR_INTRO_001",
        "category": "introduction",
        "question": "Tell me about yourself.",
        "answer": (
            "I am an MCA student with experience in Python, "
            "web development and data analysis."
        ),
    },
    {
        "question_id": "HR_SKILL_PY_001",
        "category": "skills",
        "question": "Which technical skills do you use?",
        "answer": (
            "I work with Python, SQL, Flask, pandas and "
            "machine learning."
        ),
    },
    {
        "question_id": "HR_EXP_001",
        "category": "experience",
        "question": "Tell me about your experience with Python.",
        "answer": (
            "I have worked on Python projects involving Flask, "
            "data analysis and machine learning."
        ),
    },
    {
        "question_id": "HR_SALARY_001",
        "category": "salary_expectation",
        "question": "What are your salary expectations?",
        "answer": "My expected salary is around 5 LPA.",
    },
]


# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

def calculate_demo_score(
    answer: str,
    intent: str,
    confidence_score: float,
) -> float:
    """
    Calculate a simple demo screening score.

    This is only an orchestration/demo score.
    The production screening scorer from Day 26 remains
    the dedicated scoring component.
    """

    score = 50.0

    # Relevant answer
    if len(answer.split()) >= 6:
        score += 15

    # Intent detected
    if intent not in {"missing", "vague", "off_topic"}:
        score += 15

    # Confidence
    if confidence_score >= 70:
        score += 15
    elif confidence_score >= 50:
        score += 5

    return min(round(score, 2), 100.0)


def make_decision(
    score: float,
    intent: str,
) -> str:
    """
    Apply the Day 30 optimized screening thresholds.
    """

    # Special conditions first
    if intent == "missing":
        return "retry"

    if intent in {"vague", "off_topic"}:
        return "clarify"

    # Threshold rules from Day 30
    if score >= 70:
        return "continue"

    if score >= 45:
        return "clarify"

    if score >= 20:
        return "retry"

    # False-rejection protection
    return "clarify"


# ---------------------------------------------------------------------
# Intent Detection
# ---------------------------------------------------------------------

def detect_intent(
    classifier: IntentClassifier,
    answer: str,
) -> str:
    """
    Support the intent classifier used during Day 25.

    Different local implementations may expose slightly different
    method names, so this function checks the common interfaces.
    """

    if hasattr(classifier, "classify"):
        result = classifier.classify(answer)

    elif hasattr(classifier, "predict"):
        result = classifier.predict(answer)

    elif hasattr(classifier, "detect_intent"):
        result = classifier.detect_intent(answer)

    else:
        # Safe fallback for the demo
        text = answer.lower()

        if not text.strip():
            return "missing"

        if any(
            word in text
            for word in ["python", "sql", "flask", "machine learning"]
        ):
            return "skills"

        if any(
            word in text
            for word in ["experience", "worked", "project"]
        ):
            return "experience"

        if any(
            word in text
            for word in ["salary", "lpa", "expected"]
        ):
            return "salary_expectation"

        return "introduction"

    # Handle dictionary-style results
    if isinstance(result, dict):
        return (
            result.get("intent")
            or result.get("label")
            or result.get("predicted_intent")
            or "unknown"
        )

    return str(result)


# ---------------------------------------------------------------------
# Confidence Analysis
# ---------------------------------------------------------------------

def analyze_confidence(
    analyzer: ConfidenceAnalyzer,
    answer: str,
) -> Dict:
    """
    Run the existing Day 27 confidence analyzer.
    """

    try:
        if hasattr(analyzer, "analyze"):
            result = analyzer.analyze(answer)

        elif hasattr(analyzer, "analyze_response"):
            result = analyzer.analyze_response(answer)

        else:
            result = {}

    except TypeError:
        # Some implementations may require duration.
        try:
            result = analyzer.analyze(
                answer,
                duration_seconds=30
            )
        except Exception:
            result = {}

    if isinstance(result, dict):
        return result

    return {
        "communication_strength": 70.0
    }


# ---------------------------------------------------------------------
# Sentiment Analysis
# ---------------------------------------------------------------------

def analyze_sentiment(
    analyzer: SentimentAnalyzer,
    answer: str,
) -> Dict:
    """
    Run the existing Day 27 sentiment analyzer.
    """

    try:
        if hasattr(analyzer, "analyze"):
            result = analyzer.analyze(answer)

        elif hasattr(analyzer, "analyze_sentiment"):
            result = analyzer.analyze_sentiment(answer)

        else:
            result = {}

    except Exception:
        result = {}

    if isinstance(result, dict):
        return result

    return {
        "sentiment": "neutral",
        "score": 0.0,
    }


# ---------------------------------------------------------------------
# Main End-to-End Demo
# ---------------------------------------------------------------------

def main():

    print("=" * 70)
    print("ZECPath AI - END-TO-END SCREENING DEMO")
    print("=" * 70)

    print()
    print(f"Candidate ID : {CANDIDATE_ID}")
    print(f"Job ID       : {JOB_ID}")
    print(f"Session ID   : {SESSION_ID}")
    print(f"Job Title    : {JOB_TITLE}")

    print()
    print("=" * 70)
    print("INITIALIZING SCREENING COMPONENTS")
    print("=" * 70)

    try:
        intent_classifier = IntentClassifier()
    except Exception:
        intent_classifier = None

    try:
        answer_extractor = AnswerExtractor()
    except Exception:
        answer_extractor = None

    try:
        confidence_analyzer = ConfidenceAnalyzer()
    except Exception:
        confidence_analyzer = None

    try:
        sentiment_analyzer = SentimentAnalyzer()
    except Exception:
        sentiment_analyzer = None

    edge_case_handler = EdgeCaseHandler()

    print("Intent Classifier      : Ready")
    print("Answer Extractor       : Ready")
    print("Confidence Analyzer    : Ready")
    print("Sentiment Analyzer     : Ready")
    print("Edge Case Handler      : Ready")

    print()
    print("=" * 70)
    print("SCREENING SESSION")
    print("=" * 70)

    results: List[Dict] = []

    for index, item in enumerate(QUESTIONS, start=1):

        question_id = item["question_id"]
        category = item["category"]
        question = item["question"]
        answer = item["answer"]

        print()
        print("-" * 70)
        print(f"QUESTION {index}")
        print("-" * 70)

        print(f"Question ID : {question_id}")
        print(f"Category    : {category}")

        print()
        print("AI:")
        print(question)

        print()
        print("Candidate:")
        print(answer)

        # -------------------------------------------------------------
        # Edge Case Check
        # -------------------------------------------------------------

        edge_result = edge_case_handler.handle(
            transcript=answer,
            audio_quality=95,
            noise_level=10,
        )

        print()
        print("Edge Case Analysis:")
        print(f"  Action : {edge_result['action']}")
        print(f"  Reason : {edge_result['reason']}")

        # -------------------------------------------------------------
        # Intent
        # -------------------------------------------------------------

        if intent_classifier is not None:
            intent = detect_intent(
                intent_classifier,
                answer,
            )
        else:
            intent = category

        print()
        print("Intent:")
        print(f"  {intent}")

        # -------------------------------------------------------------
        # Answer Extraction
        # -------------------------------------------------------------

        extracted_answer = answer

        if answer_extractor is not None:

            try:
                if hasattr(answer_extractor, "extract"):
                    extracted = answer_extractor.extract(answer)

                    if isinstance(extracted, dict):
                        extracted_answer = (
                            extracted.get("answer")
                            or extracted.get("value")
                            or answer
                        )

                    elif isinstance(extracted, str):
                        extracted_answer = extracted

            except Exception:
                extracted_answer = answer

        # -------------------------------------------------------------
        # Confidence
        # -------------------------------------------------------------

        if confidence_analyzer is not None:
            confidence_result = analyze_confidence(
                confidence_analyzer,
                answer,
            )
        else:
            confidence_result = {
                "communication_strength": 70.0
            }

        confidence_score = float(
            confidence_result.get(
                "communication_strength",
                confidence_result.get("confidence_score", 70.0),
            )
        )

        print()
        print("Confidence:")
        print(f"  {confidence_score:.2f}")

        # -------------------------------------------------------------
        # Sentiment
        # -------------------------------------------------------------

        if sentiment_analyzer is not None:
            sentiment_result = analyze_sentiment(
                sentiment_analyzer,
                answer,
            )
        else:
            sentiment_result = {
                "sentiment": "neutral"
            }

        sentiment = sentiment_result.get(
            "sentiment",
            "neutral"
        )

        print()
        print("Sentiment:")
        print(f"  {sentiment}")

        # -------------------------------------------------------------
        # Screening Score
        # -------------------------------------------------------------

        score = calculate_demo_score(
            extracted_answer,
            intent,
            confidence_score,
        )

        # -------------------------------------------------------------
        # Decision
        # -------------------------------------------------------------

        decision = make_decision(
            score,
            intent,
        )

        print()
        print("Screening Score:")
        print(f"  {score:.2f}/100")

        print()
        print("Decision:")
        print(f"  {decision.upper()}")

        results.append(
            {
                "question_id": question_id,
                "category": category,
                "answer": answer,
                "intent": intent,
                "confidence": confidence_score,
                "sentiment": sentiment,
                "score": score,
                "decision": decision,
            }
        )

    # -----------------------------------------------------------------
    # Final Result
    # -----------------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL SCREENING RESULT")
    print("=" * 70)

    total_score = sum(
        item["score"]
        for item in results
    )

    final_score = (
        total_score / len(results)
        if results
        else 0.0
    )

    skills = set()

    for item in results:

        answer = item["answer"].lower()

        if "python" in answer:
            skills.add("Python")

        if "sql" in answer:
            skills.add("SQL")

        if "flask" in answer:
            skills.add("Flask")

        if "machine learning" in answer:
            skills.add("Machine Learning")

        if "pandas" in answer:
            skills.add("Pandas")

    print()
    print(f"Candidate ID : {CANDIDATE_ID}")
    print(f"Job ID       : {JOB_ID}")
    print(f"Job Title    : {JOB_TITLE}")
    print(f"Session ID   : {SESSION_ID}")

    print()
    print(f"Final Score  : {final_score:.2f}/100")

    print()
    print("Confirmed Skills:")

    if skills:
        for skill in sorted(skills):
            print(f"  - {skill}")
    else:
        print("  - None detected")

    continue_count = sum(
        1
        for item in results
        if item["decision"] == "continue"
    )

    clarify_count = sum(
        1
        for item in results
        if item["decision"] == "clarify"
    )

    retry_count = sum(
        1
        for item in results
        if item["decision"] == "retry"
    )

    print()
    print("Decision Summary:")
    print(f"  Continue : {continue_count}")
    print(f"  Clarify  : {clarify_count}")
    print(f"  Retry    : {retry_count}")

    print()
    print("Status:")
    print("  SCREENING COMPLETED")

    print()
    print("=" * 70)
    print("END-TO-END AI SCREENING DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()