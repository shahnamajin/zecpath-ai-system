from pathlib import Path

from screening_ai.transcript_loader import (
    TranscriptLoader
)

from screening_ai.transcript_normalizer import (
    TranscriptNormalizer
)

from screening_ai.screening_interaction import (
    ScreeningInteraction
)


TRANSCRIPT_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "transcripts"
    / "sample_transcript.json"
)


def create_loader():

    return TranscriptLoader(
        str(TRANSCRIPT_PATH)
    )


def test_transcript_loads():

    loader = create_loader()

    transcript = loader.load()

    assert transcript is not None
    assert transcript["transcript_id"] == (
        "TRX_20260915_001"
    )


def test_required_metadata_exists():

    loader = create_loader()

    transcript = loader.load()

    assert "candidate_id" in transcript
    assert "job_id" in transcript
    assert "session_id" in transcript
    assert "started_at" in transcript
    assert "ended_at" in transcript
    assert "interactions" in transcript


def test_transcript_validation():

    loader = create_loader()

    transcript = loader.load()

    result = loader.validate(
        transcript
    )

    assert result["valid"] is True
    assert result["interaction_count"] == 6
    assert result["errors"] == []


def test_interaction_schema():

    loader = create_loader()

    transcript = loader.load()

    for interaction in transcript["interactions"]:

        assert "interaction_id" in interaction
        assert "question_id" in interaction
        assert "speaker" in interaction
        assert "timestamp" in interaction
        assert "text" in interaction
        assert "confidence_level" in interaction
        assert "sequence" in interaction


def test_confidence_range():

    loader = create_loader()

    transcript = loader.load()

    for interaction in transcript["interactions"]:

        confidence = interaction[
            "confidence_level"
        ]

        assert 0 <= confidence <= 1


def test_candidate_responses():

    loader = create_loader()

    transcript = loader.load()

    responses = (
        loader.get_candidate_responses(
            transcript
        )
    )

    assert len(responses) == 3

    for response in responses:

        assert response[
            "speaker"
        ] == "candidate"


def test_ai_questions():

    loader = create_loader()

    transcript = loader.load()

    questions = (
        loader.get_ai_questions(
            transcript
        )
    )

    assert len(questions) == 3

    for question in questions:

        assert question[
            "speaker"
        ] == "ai"


def test_text_normalization():

    normalizer = TranscriptNormalizer()

    text = "   Hello    world!!!   "

    normalized = (
        normalizer.normalize_text(text)
    )

    assert normalized == "Hello world!"


def test_filler_word_removal():

    normalizer = TranscriptNormalizer()

    text = "Um I have experience in Python"

    result = (
        normalizer.remove_filler_words(
            text
        )
    )

    assert result == (
        "I have experience in Python"
    )


def test_interaction_normalization():

    normalizer = TranscriptNormalizer()

    interaction = {
        "interaction_id": "INT_001",
        "question_id": "HR_INT_001",
        "speaker": "candidate",
        "timestamp": "2026-09-15T10:00:00Z",
        "text": "  Um   I use Python!!! ",
        "confidence_level": 0.9567,
        "sequence": 1
    }

    result = (
        normalizer.normalize_interaction(
            interaction
        )
    )

    assert result["text"] == (
        "I use Python!"
    )

    assert result[
        "confidence_level"
    ] == 0.957


def test_screening_interaction():

    interaction = ScreeningInteraction(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_INT_001",
        interaction_id="INT_001",
        timestamp="2026-09-15T10:00:00Z",
        speaker="candidate",
        text="I am a software developer.",
        confidence_level=0.95,
        sequence=1
    )

    data = interaction.to_dict()

    assert data[
        "candidate_id"
    ] == "CAND_1001"

    assert data[
        "job_id"
    ] == "JOB_2001"

    assert data[
        "question_id"
    ] == "HR_INT_001"


def test_low_confidence_detection():

    interaction = ScreeningInteraction(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_INT_001",
        interaction_id="INT_001",
        timestamp="2026-09-15T10:00:00Z",
        speaker="candidate",
        text="Test response",
        confidence_level=0.55,
        sequence=1
    )

    assert interaction.is_low_confidence() is True


def test_high_confidence_detection():

    interaction = ScreeningInteraction(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        question_id="HR_INT_001",
        interaction_id="INT_001",
        timestamp="2026-09-15T10:00:00Z",
        speaker="candidate",
        text="Test response",
        confidence_level=0.95,
        sequence=1
    )

    assert interaction.is_low_confidence() is False