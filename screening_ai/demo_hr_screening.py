from pathlib import Path
from pprint import pprint

from question_loader import HRQuestionLoader
from question_selector import HRQuestionSelector
from conversation_builder import ConversationBuilder


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = (
    BASE_DIR
    / "data"
    / "hr_screening"
    / "hr_questions.json"
)


def main():

    print("=" * 60)
    print("ZECPath HR Screening Dataset Demo")
    print("=" * 60)

    loader = HRQuestionLoader(
        str(DATASET)
    )

    questions = loader.load_questions()

    print(
        f"\nTotal questions: {len(questions)}"
    )

    validation = loader.validate_dataset()

    print(
        f"Dataset valid: {validation['valid']}"
    )

    if not validation["valid"]:

        print("\nValidation errors:")

        pprint(validation["errors"])

        return

    role = "python_developer"

    selector = HRQuestionSelector(
        questions
    )

    role_questions = (
        selector.build_screening_sequence(role)
    )

    print(f"\nRole: {role}")

    print(
        f"Questions selected: "
        f"{len(role_questions)}"
    )

    print("\nScreening sequence:")
    print("-" * 60)

    for number, question in enumerate(
        role_questions,
        start=1
    ):

        print(
            f"{number}. "
            f"[{question['category']}] "
            f"{question['question']}"
        )

    builder = ConversationBuilder()

    conversation = builder.build_conversation(
        role_questions
    )

    print("\nConversation-ready object:")
    print("-" * 60)

    pprint(
        conversation[0],
        sort_dicts=False
    )


if __name__ == "__main__":
    main()