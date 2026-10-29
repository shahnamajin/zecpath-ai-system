from screening_ai.transcript_cleaner import TranscriptCleaner
from screening_ai.speech_quality import SpeechQualityAnalyzer


def test_whitespace_cleanup():
    cleaner = TranscriptCleaner()

    result = cleaner.clean_whitespace(
        "  I   have   experience   in Python.  "
    )

    assert result == "I have experience in Python."


def test_filler_word_removal():
    cleaner = TranscriptCleaner()

    result = cleaner.remove_filler_words(
        "Um, I have, uh, experience in Python."
    )

    assert "Um" not in result
    assert "uh" not in result
    assert "experience" in result


def test_punctuation_normalization():
    cleaner = TranscriptCleaner()

    result = cleaner.normalize_punctuation(
        "I have experience in Python!!!"
    )

    assert result == "I have experience in Python!"


def test_case_normalization():
    cleaner = TranscriptCleaner()

    result = cleaner.normalize_case(
        "i have experience in python."
    )

    assert result == "I have experience in python."


def test_complete_cleaning():
    cleaner = TranscriptCleaner()

    result = cleaner.clean(
        "  um, i have   experience in Python!!! uh  "
    )

    assert result == "I have experience in Python!"


def test_empty_speech():
    analyzer = SpeechQualityAnalyzer()

    assert analyzer.classify("") == "silence"


def test_partial_answer():
    analyzer = SpeechQualityAnalyzer()

    assert analyzer.classify(
        "Python and SQL."
    ) == "partial"


def test_interrupted_speech():
    analyzer = SpeechQualityAnalyzer()

    assert analyzer.classify(
        "I worked on a healthcare project..."
    ) == "interrupted"


def test_complete_answer():
    analyzer = SpeechQualityAnalyzer()

    assert analyzer.classify(
        "I worked on a healthcare project using Python and Flask."
    ) == "complete"