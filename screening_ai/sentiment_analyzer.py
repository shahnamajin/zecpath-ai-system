class SentimentAnalyzer:
    """
    Simple rule-based sentiment analyzer for screening
    communication signals.
    """

    POSITIVE_WORDS = {
        "confident",
        "confidence",
        "enjoy",
        "enjoyed",
        "excellent",
        "good",
        "great",
        "successful",
        "success",
        "strong",
        "comfortable",
        "interested",
        "passionate",
        "excited",
        "positive",
        "love",
        "achieved",
        "improved"
    }

    NEGATIVE_WORDS = {
        "bad",
        "poor",
        "difficult",
        "failure",
        "failed",
        "weak",
        "hate",
        "problem",
        "problems",
        "worried",
        "negative",
        "unable",
        "lack",
        "no experience"
    }

    def tokenize(self, text):
        """
        Convert text into normalized tokens.
        """

        if not text:
            return []

        return (
            text.lower()
            .replace(",", " ")
            .replace(".", " ")
            .replace("!", " ")
            .replace("?", " ")
            .split()
        )

    def analyze(self, text):
        """
        Calculate sentiment signals.
        """

        tokens = self.tokenize(text)

        positive_matches = [
            word
            for word in tokens
            if word in self.POSITIVE_WORDS
        ]

        negative_matches = [
            word
            for word in tokens
            if word in self.NEGATIVE_WORDS
        ]

        positive_count = len(
            positive_matches
        )

        negative_count = len(
            negative_matches
        )

        if positive_count > negative_count:
            sentiment = "positive"

        elif negative_count > positive_count:
            sentiment = "negative"

        else:
            sentiment = "neutral"

        total = (
            positive_count
            + negative_count
        )

        if total == 0:
            sentiment_score = 0.0

        else:
            sentiment_score = (
                (positive_count - negative_count)
                / total
            ) * 100

        return {
            "sentiment": sentiment,
            "sentiment_score": round(
                sentiment_score,
                2
            ),
            "positive_indicators": positive_matches,
            "negative_indicators": negative_matches
        }