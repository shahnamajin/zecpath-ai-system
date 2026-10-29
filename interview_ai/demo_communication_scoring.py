"""Demo for Day 35 Communication Skill Evaluation."""

from interview_ai.communication_scorer import CommunicationScorer


SAMPLES = [
    ("COMM_001", "I worked on a Flask project. I developed the backend and integrated the database. The result was a working web application."),
    ("COMM_002", "Um, I, uh, worked on a project, you know, and basically I did some things."),
    ("COMM_003", "First, I analyzed the requirement. Then I implemented the backend using Flask. Finally, I tested the APIs and documented the result."),
    ("COMM_004", "I am good at Python and SQL and I used them in my projects for data analysis and web development."),
    ("COMM_005", "I worked with Python."),
]


def main():
    scorer = CommunicationScorer()

    print("ZECPath AI - COMMUNICATION SKILL EVALUATION DEMO")
    print("=" * 58)

    for case_id, text in SAMPLES:
        result = scorer.score(text)
        print(f"\n{case_id}")
        print(f"Response          : {text}")
        print(f"Word Count        : {result['word_count']}")
        print(f"Fluency           : {result['components']['fluency']:.2f}")
        print(f"Grammar Quality   : {result['components']['grammar_quality']:.2f}")
        print(f"Vocabulary Range  : {result['components']['vocabulary_range']:.2f}")
        print(f"Clarity           : {result['components']['clarity']:.2f}")
        print(f"Answer Structure  : {result['components']['answer_structure']:.2f}")
        print(f"Filler Control    : {result['components']['filler_control']:.2f}")
        print(f"Filler Count      : {result['filler_details']['count']}")
        print(f"Filler Rate       : {result['filler_details']['rate_per_100_words']:.2f}/100 words")
        print(f"Evidence Factor   : {result['normalization']['evidence_factor']:.2f}")
        print(f"Communication Score: {result['communication_score']:.2f}/100")
        print(f"Band              : {result['band']}")

    print("\nCOMMUNICATION SKILL EVALUATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
