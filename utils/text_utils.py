import re


def normalize_text(text):

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()