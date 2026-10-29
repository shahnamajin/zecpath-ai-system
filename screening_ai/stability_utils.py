
import math
import re
import unicodedata


def clean_transcript(text: str) -> str:
    """Normalize transcript text and remove unwanted characters."""
    if not isinstance(text, str):
        raise TypeError("Transcript must be a string")

    text = unicodedata.normalize("NFKC", text)

    # Remove zero-width characters and BOM
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text


def validate_score(
    score: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """Validate a numeric score and return it as a float."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError("Score must be a number")

    if not math.isfinite(score):
        raise ValueError("Score must be finite")

    if minimum > maximum:
        raise ValueError("Minimum cannot exceed maximum")

    if not minimum <= score <= maximum:
        raise ValueError(
            f"Score must be between {minimum} and {maximum}"
        )

    return float(score)


def calculate_weighted_score(
    scores: dict,
    weights: dict,
) -> float:
    """Calculate a weighted score using weights that sum to 1."""
    if not scores or set(scores) != set(weights):
        raise ValueError("Scores and weights must have matching keys")

    validated_scores = {
        key: validate_score(value)
        for key, value in scores.items()
    }

    for weight in weights.values():
        if (
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not math.isfinite(weight)
            or weight < 0
        ):
            raise ValueError("Weights must be finite, non-negative numbers")

    if not math.isclose(sum(weights.values()), 1.0, abs_tol=1e-9):
        raise ValueError("Weights must sum to 1.0")

    total = sum(
        validated_scores[key] * weights[key]
        for key in validated_scores
    )

    return round(total, 2)


def choose_follow_up(
    answer: str,
    intent: str,
    attempts: int = 0,
    max_attempts: int = 2,
) -> str:
    """Choose the next action based on answer quality and detected intent."""
    if (
        isinstance(attempts, bool)
        or not isinstance(attempts, int)
        or attempts < 0
    ):
        raise ValueError("Attempts must be a non-negative integer")

    if (
        isinstance(max_attempts, bool)
        or not isinstance(max_attempts, int)
        or max_attempts < 0
    ):
        raise ValueError("max_attempts must be a non-negative integer")

    if not isinstance(answer, str) or not isinstance(intent, str):
        raise TypeError("Answer and intent must be strings")

    if intent.strip().lower() in {"escalate", "human_help"}:
        return "escalate"

    if not answer.strip():
        return "retry" if attempts < max_attempts else "escalate"

    if intent.strip().lower() in {"unclear", "unknown"}:
        return "clarify" if attempts < max_attempts else "escalate"

    return "continue"
