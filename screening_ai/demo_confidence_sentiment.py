from .confidence_analyzer import ConfidenceAnalyzer
from .sentiment_analyzer import SentimentAnalyzer
from .behavioral_analyzer import BehavioralAnalyzer


def print_result(index, result, text):

    print("\n" + "-" * 70)

    print(f"Response {index}")

    print(f"Text: {text}")

    communication = (
        result["communication_signals"]
    )

    hesitation = communication[
        "hesitation"
    ]

    length = communication[
        "response_length"
    ]

    pace = communication[
        "response_pace"
    ]

    uncertainty = communication[
        "uncertainty"
    ]

    print(
        f"Hesitation: "
        f"{hesitation['detected']}"
    )

    print(
        f"Hesitation Count: "
        f"{hesitation['count']}"
    )

    print(
        f"Hesitation Markers: "
        f"{hesitation['markers']}"
    )

    print(
        f"Response Length: "
        f"{length['word_count']} words "
        f"({length['category']})"
    )

    print(
        f"Response Pace: "
        f"{pace['category']}"
    )

    if pace["words_per_minute"] is not None:

        print(
            f"Words Per Minute: "
            f"{pace['words_per_minute']}"
        )

    print(
        f"Uncertainty: "
        f"{uncertainty['detected']}"
    )

    print(
        f"Uncertainty Patterns: "
        f"{uncertainty['patterns']}"
    )

    print(
        f"Communication Strength: "
        f"{communication['communication_strength']}/100"
    )

    sentiment = result["sentiment"]

    print(
        f"Sentiment: "
        f"{sentiment['sentiment']}"
    )

    print(
        f"Sentiment Score: "
        f"{sentiment['sentiment_score']}"
    )

    print(
        f"Positive Indicators: "
        f"{sentiment['positive_indicators']}"
    )

    print(
        f"Negative Indicators: "
        f"{sentiment['negative_indicators']}"
    )

    contradiction = result[
        "contradiction"
    ]

    print(
        f"Contradiction: "
        f"{contradiction['detected']}"
    )

    if contradiction["details"]:

        for detail in contradiction["details"]:

            print(
                f"  - {detail}"
            )


def main():

    print("=" * 70)
    print(
        "ZECPath Confidence & Sentiment Signal Analysis Demo"
    )
    print("=" * 70)

    confidence_analyzer = (
        ConfidenceAnalyzer()
    )

    sentiment_analyzer = (
        SentimentAnalyzer()
    )

    behavioral_analyzer = (
        BehavioralAnalyzer(
            confidence_analyzer,
            sentiment_analyzer
        )
    )

    test_responses = [

        {
            "text": (
                "I am confident that I can work "
                "with Python and SQL."
            ),
            "duration": 8
        },

        {
            "text": (
                "Um, I think maybe I can work "
                "with Python."
            ),
            "duration": 7
        },

        {
            "text": (
                "I don't know much about Java "
                "and I have no experience with it."
            ),
            "duration": 10
        },

        {
            "text": (
                "I have two years of Python experience."
            ),
            "duration": 5
        },

        {
            "text": (
                "Um, uh, I worked on a project."
            ),
            "duration": 6
        }
    ]

    for index, item in enumerate(
        test_responses,
        start=1
    ):

        result = behavioral_analyzer.analyze(
            text=item["text"],
            duration_seconds=item["duration"]
        )

        print_result(
            index,
            result,
            item["text"]
        )

    print("\n" + "=" * 70)
    print(
        "Confidence and sentiment analysis completed successfully."
    )
    print("=" * 70)


if __name__ == "__main__":
    main()