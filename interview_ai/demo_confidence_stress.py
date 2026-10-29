"""Day 36 demo: Confidence & Stress Indicators."""

from interview_ai.behavioral_signal_engine import BehavioralSignalEngine


SAMPLES = [
    (
        "CONF_001",
        "I have worked with Python and Flask for two years. I built APIs and deployed applications.",
        35
    ),
    (
        "CONF_002",
        "Um, I think maybe I worked on some projects, but I'm not sure.",
        20
    ),
    (
        "CONF_003",
        "I worked worked on a Python project and I handled the backend backend.",
        25
    ),
    (
        "CONF_004",
        "I don't know. Maybe I can do it.",
        12
    ),
    (
        "CONF_005",
        "I have two years of experience. I have five years of experience.",
        18
    ),
]


def main():
    engine = BehavioralSignalEngine()

    print("ZECPath AI - CONFIDENCE & STRESS INDICATORS DEMO")
    print("=" * 58)

    for case_id, text, duration in SAMPLES:
        result = engine.score(text, duration)

        print(f"\n{case_id}")
        print(f"Response                 : {text}")
        print(f"Hesitation Count         : {result['signals']['hesitation']['count']}")
        print(f"Hesitation Rate          : {result['signals']['hesitation']['rate_per_100_words']:.2f}/100 words")
        print(f"Uncertainty Count        : {result['signals']['uncertainty']['count']}")
        print(f"Repeated Words           : {result['signals']['repetition']['count']}")
        print(f"Sentiment                : {result['signals']['sentiment']['sentiment']}")
        print(f"Sentiment Score          : {result['signals']['sentiment']['score']:.2f}")
        print(f"Contradiction Detected   : {result['contradiction']['detected']}")
        print(f"Stress Indicators        : {', '.join(result['stress_indicators']) or 'None'}")
        print(f"Behavioral Confidence    : {result['behavioral_confidence_score']:.2f}/100")
        print(f"Confidence Band          : {result['band']}")

    print("\nCONFIDENCE & STRESS INDICATOR ANALYSIS COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
