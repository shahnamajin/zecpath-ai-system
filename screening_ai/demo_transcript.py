from pathlib import Path
from pprint import pprint

from transcript_loader import TranscriptLoader
from transcript_normalizer import TranscriptNormalizer


BASE_DIR = Path(__file__).resolve().parent.parent

TRANSCRIPT_PATH = (
    BASE_DIR
    / "data"
    / "transcripts"
    / "sample_transcript.json"
)


def main():

    print("=" * 60)
    print("ZECPath Transcript Data Architecture Demo")
    print("=" * 60)

    loader = TranscriptLoader(
        str(TRANSCRIPT_PATH)
    )

    transcript = loader.load()

    print(
        f"\nTranscript ID: "
        f"{transcript['transcript_id']}"
    )

    print(
        f"Candidate ID: "
        f"{transcript['candidate_id']}"
    )

    print(
        f"Job ID: "
        f"{transcript['job_id']}"
    )

    print(
        f"Session ID: "
        f"{transcript['session_id']}"
    )

    print(
        f"Total interactions: "
        f"{len(transcript['interactions'])}"
    )

    validation = loader.validate(
        transcript
    )

    print(
        f"\nTranscript valid: "
        f"{validation['valid']}"
    )

    print("\nCandidate responses:")

    print("-" * 60)

    responses = loader.get_candidate_responses(
        transcript
    )

    for response in responses:

        print(
            f"[{response['question_id']}] "
            f"{response['text']}"
        )

        print(
            f"Confidence: "
            f"{response['confidence_level']}"
        )

    normalizer = TranscriptNormalizer()

    normalized = (
        normalizer.normalize_transcript(
            transcript
        )
    )

    print("\nNormalized candidate responses:")

    print("-" * 60)

    for interaction in normalized[
        "interactions"
    ]:

        if interaction[
            "speaker"
        ] == "candidate":

            print(
                interaction["text"]
            )

    print("\nAI-processable interaction:")

    print("-" * 60)

    pprint(
        normalized["interactions"][1],
        sort_dicts=False
    )


if __name__ == "__main__":
    main()