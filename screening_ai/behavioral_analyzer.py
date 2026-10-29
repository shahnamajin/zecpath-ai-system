class BehavioralAnalyzer:
    """
    Combines communication and sentiment signals
    into a behavioral indicators report.
    """

    def __init__(
        self,
        confidence_analyzer,
        sentiment_analyzer
    ):
        self.confidence_analyzer = (
            confidence_analyzer
        )

        self.sentiment_analyzer = (
            sentiment_analyzer
        )

    def detect_contradictions(
        self,
        current_entities,
        previous_context=None
    ):
        """
        Detect simple contradictions against
        previously stored structured information.
        """

        if not previous_context:
            return {
                "detected": False,
                "details": []
            }

        contradictions = []

        current_experience = (
            current_entities.get(
                "experience",
                {}
            )
        )

        previous_experience = (
            previous_context.get(
                "experience",
                {}
            )
        )

        current_years = (
            current_experience.get("years")
        )

        previous_years = (
            previous_experience.get("years")
        )

        if (
            current_years is not None
            and previous_years is not None
            and abs(
                current_years - previous_years
            ) > 1
        ):
            contradictions.append(
                "Experience duration differs significantly from previous information."
            )

        current_skills = set(
            current_entities.get(
                "skills",
                []
            )
        )

        previous_skills = set(
            previous_context.get(
                "skills",
                []
            )
        )

        if (
            current_skills
            and previous_skills
            and not current_skills.intersection(
                previous_skills
            )
        ):
            contradictions.append(
                "Current skills do not overlap with previously provided skills."
            )

        return {
            "detected": len(contradictions) > 0,
            "details": contradictions
        }

    def analyze(
        self,
        text,
        duration_seconds=None,
        current_entities=None,
        previous_context=None
    ):
        """
        Generate complete behavioral indicator report.
        """

        if current_entities is None:
            current_entities = {}

        communication = (
            self.confidence_analyzer.analyze(
                text,
                duration_seconds
            )
        )

        sentiment = (
            self.sentiment_analyzer.analyze(
                text
            )
        )

        contradiction = (
            self.detect_contradictions(
                current_entities,
                previous_context
            )
        )

        return {
            "communication_signals": communication,

            "sentiment": sentiment,

            "contradiction": contradiction
        }