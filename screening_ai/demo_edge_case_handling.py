from screening_ai.robust_screening_flow import RobustScreeningFlow


def main():
    print("=" * 70)
    print("ZECPath AI Edge Case & Failure Handling")
    print("=" * 70)

    flow = RobustScreeningFlow()

    cases = [
        {
            "name": "Normal Response",
            "transcript": "I have two years of experience with Python and Flask.",
            "audio_quality": 95,
            "noise_level": 10
        },
        {
            "name": "Poor Audio",
            "transcript": "",
            "audio_quality": 20,
            "noise_level": 20
        },
        {
            "name": "Background Noise",
            "transcript": "I have experience with Python and SQL.",
            "audio_quality": 70,
            "noise_level": 80
        },
        {
            "name": "Language Mixing",
            "transcript": "I have two years experience in Python and കുറച്ച് Java.",
            "audio_quality": 90,
            "noise_level": 10
        },
        {
            "name": "Missing Answer",
            "transcript": "",
            "audio_quality": 95,
            "noise_level": 5
        }
    ]

    print("\nEDGE CASE RESULTS")
    print("-" * 70)

    for index, case in enumerate(cases, start=1):
        result = flow.process_response(
            transcript=case["transcript"],
            audio_quality=case["audio_quality"],
            noise_level=case["noise_level"]
        )

        print(
            f"CASE_{index:03d} | "
            f"{case['name']:<20} | "
            f"Action: {result['action']:<14} | "
            f"Reason: {result['reason']}"
        )

    print("\n" + "=" * 70)
    print("Edge case and failure handling completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()