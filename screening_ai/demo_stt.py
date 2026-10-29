from transcript_cleaner import TranscriptCleaner
from speech_quality import SpeechQualityAnalyzer


def main():
    print("=" * 60)
    print("ZECPath Speech-to-Text & Transcript Cleaning Demo")
    print("=" * 60)

    raw_transcript = (
        "Um, I have   experience in Python and, uh, "
        "I worked on a healthcare project..."
    )

    print("\nRaw transcript:")
    print("-" * 60)
    print(raw_transcript)

    cleaner = TranscriptCleaner()
    analyzer = SpeechQualityAnalyzer()

    cleaned_text = cleaner.clean(raw_transcript)
    quality = analyzer.classify(raw_transcript)

    print("\nCleaned transcript:")
    print("-" * 60)
    print(cleaned_text)

    print("\nSpeech quality:")
    print("-" * 60)
    print(f"Classification: {quality}")

    print("\nProcessing result:")
    print("-" * 60)

    result = {
        "raw_text": raw_transcript,
        "cleaned_text": cleaned_text,
        "speech_status": quality,
    }

    print(result)

    print("\n" + "=" * 60)
    print("STT cleaning pipeline completed successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()