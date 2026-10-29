from interview_ai.question_generator import HRQuestionGenerator


def display_questions(title, questions):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    for index, question in enumerate(questions, start=1):
        print(f"\n{index}. {question['question']}")
        print(f"   ID: {question['question_id']}")
        print(f"   Category: {question['category']}")
        print(f"   Difficulty: {question['difficulty']}")
        print(
            f"   Follow-up Eligible: "
            f"{question['follow_up_eligible']}"
        )


def main():
    generator = HRQuestionGenerator()

    print("\nZECPath AI - HR INTERVIEW QUESTION GENERATOR")
    print("=" * 60)

    print(f"Total Questions in Bank: {generator.get_question_count()}")

    print("\nAvailable Categories:")
    for category in generator.get_categories():
        print(f"- {category}")

    # --------------------------------------------------
    # Fresher Technical
    # --------------------------------------------------

    fresher_technical = generator.generate_questions(
        candidate_type="fresher",
        role_type="technical",
        max_questions=6
    )

    display_questions(
        "FRESHER - TECHNICAL ROLE",
        fresher_technical
    )

    # --------------------------------------------------
    # Experienced Technical
    # --------------------------------------------------

    experienced_technical = generator.generate_questions(
        candidate_type="experienced",
        role_type="technical",
        max_questions=6
    )

    display_questions(
        "EXPERIENCED - TECHNICAL ROLE",
        experienced_technical
    )

    # --------------------------------------------------
    # Fresher Non-Technical
    # --------------------------------------------------

    fresher_non_technical = generator.generate_questions(
        candidate_type="fresher",
        role_type="non_technical",
        max_questions=6
    )

    display_questions(
        "FRESHER - NON-TECHNICAL ROLE",
        fresher_non_technical
    )

    print("\n" + "=" * 60)
    print("HR QUESTION GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()